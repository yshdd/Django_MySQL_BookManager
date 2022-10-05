from django.shortcuts import render
from .models import Students, LendDateStu, LendBooks, Books
from . import forms
from django.db import transaction
from django.http import Http404
# Create your views here.

def index(request):
    alldata = LendBooks.objects.all()
    allbooks = Books.objects.all()
    dict = {
        "alldata": alldata,
        "allbooks": allbooks,
    }
    return render(request, "index.html", dict)


#本を借りるための登録ページ
def callRecordFrom(request):
    alldata = LendBooks.objects.all()
    #print(Books.objects.filter(bookname="XXX").values("bookid", "returned"))
    #print(type(Books.objects.get(bookid=1001)))
    form = forms.FormForRental(request.GET or None)
    dict = {
        "form": form,
        "alldata": alldata,
    }
    return render(request, "FormForRental.html", dict)
#返却するための登録ページ
def callReturnForm(request):
    alldata = LendBooks.objects.all()
    form = forms.FormForReturn(request.GET or None)
    dict = {
        "form": form,
        "alldata": alldata,
    }
    return render(request, "FormForReturn.html", dict)
#登録内容の変更
def callUpdateForm(request):
    alldata = LendBooks.objects.all()
    form = forms.FormForUpdate(request.GET or None, initial={"book": "NoSelect"})
    dict = {
        "form": form,
        "alldata": alldata,
    }
    return render(request, "FormForUpdate.html", dict)

#本の貸出登録処理
def addRecord(request):
    if request.method=="POST":
        stuid = request.POST.get('stuid')
        stuname = request.POST.get('stuname')
        date = request.POST.get('date')
        bookid = request.POST.get('book')
        #学生が登録されているか確認
        if Students.objects.filter(stuid=stuid, stuname=stuname).exists():
            print('54')
            with transaction.atomic():
                
                student = Students.objects.get(stuid=stuid)
                print(student, type(student))
                rcrd = LendDateStu.objects.create(date=date, stuid=student)
                #rcrd.stuid = student
                #rcrd.save()
                NoID = rcrd.no
                print(f"NoID:{NoID}")
                #lendBookテーブルに追加


                book = Books.objects.get(bookid=bookid)#.values("bookid", "bookname", "returned")
                #book = Books(bookid=bookid, bookname=book["bookname"], returned=book["returned"])
                print(book, type(book))
                record_lendbook = LendBooks(
                    no = rcrd,
                    bookid = book,
                )
                record_lendbook.save()
                
                # #returnedを変更
                #res = Books.objects.get(bookid=bookid)
                #貸出中にする
                book.returned = 0
                book.save()
            
            return render(request, "complete.html")
        else:
            raise Http404("学生番号と名前が間違っています")

    #追加後のデータベース
    alldata = LendBooks.objects.all()
    dict = {
        "alldata": alldata,
    }
    return render(request, "index.html", dict)
    

#返却処理
def deleteRecord(request):
    if request.method=="POST":
        rentalid = int(request.POST.get('rentalid'))
        bookid = int(request.POST.get('bookid'))
        book = Books.objects.get(bookid=bookid)
        if LendBooks.objects.filter(id=rentalid, bookid=book).exists():
    
            with transaction.atomic():
                #
                #lend_date_stuテーブル、lendbooksテーブルを削除
                #lendbooksが外部キーなので先に削除
                #消去される列の情報を辞書に管理
                deleted_row_dict = LendBooks.objects.filter(id=rentalid).values("id", "no","bookid")[0]
                lendbook_rec = LendBooks.objects.get(id=rentalid)
                print(LendBooks.objects.filter(id=rentalid).values("id", "no","bookid")[0])
                
                
                #No = lendbook_rec.LendDateStu.no #ForeignKey->参照先のカラム名
                No = deleted_row_dict["no"]
                
                #一冊だけ返却
                lendbook_rec.delete()
                #LendBooksのNoカラムに上で削除したnoが存在しなくなったらLendDateStuも消す
                LendDateStu_rec = LendDateStu(no=deleted_row_dict["no"])
                if not LendBooks.objects.filter(no=LendDateStu_rec).exists():
                    LendDateStu.objects.filter(no=No).delete()

                #本のreturnedタグを1に変更
                book.returned = 1
                book.save()
            return render(request, "complete.html")
            
        else:
            raise Http404("No User matches the given query.")
    
    alldata = LendBooks.objects.all()
    allbooks = Books.objects.all()
    dict = {
        "alldata": alldata,
        "allbooks": allbooks,
    }
    return render(request, "index.html", dict)

def updateRecord(request):
    if request.method=="POST":
        rentalid = int(request.POST.get('rentalid'))
        #updateformに入力された内容
        stuid = int(request.POST.get('stuid'))
        stuname = request.POST.get('stuname')
        date = request.POST.get('date')
        bookid = request.POST.get('book')
        print(bookid)
        print(type(stuid), stuid, bookid, type(bookid), len(bookid))
        if Students.objects.filter(stuid=stuid, stuname=stuname).exists():
            with transaction.atomic():
            #updated_row_dict = LendBooks.objects.filter(id=rentalid).values("id", "no", "bookid")[0]
            
                update_lendbooks_row = LendBooks.objects.get(id=rentalid)
                updated_row_dict = LendBooks.objects.filter(id=rentalid).values("id", "no", "bookid")[0]

                #LendBooksのbookidの更新
                print(len(str(bookid)))
                if len(str(bookid))!=0:
                    update_lendbooks_row.bookid = bookid
                    update_lendbooks_row.save()
                
                print("150")
                #LendDateStuテーブルを更新
                student = Students.objects.get(stuid=stuid)
                update_LendDateStu_row = LendDateStu.objects.get(no=updated_row_dict["no"])
                update_LendDateStu_row.date = date
                update_LendDateStu_row.stuid = student
                update_LendDateStu_row.save()
                print("155")

                #Booksテーブルの更新:NoSelectでない場合
                #updateformのbookidと登録済のbookidが同じ場合->何もしない
                #異なる場合 -> 登録済のbookidのreturnedを1に、updateformのbookidを0に
                if len(str(bookid))!=0 and bookid != updated_row_dict["bookid"]:
                    registered_booksrow = Books.objects.get(bookid=updated_row_dict["bookid"])
                    registered_booksrow.returned = 1
                    registered_booksrow.save()
                    updateform_booksrow = Books.objects.get(bookid=bookid)
                    updateform_booksrow = 0
                    updateform_booksrow.save()
                
                # alldata = LendBooks.objects.all()
                # dict = {
                #     "alldata": alldata,
                # }
                #return render(request, "index.html", dict)
            return render(request, "complete.html")

        else:
            raise Http404("学生番号と名前が間違っています")
