Attribute VB_Name = "Todotxt"
Dim tasksFolder As Outlook.Items
Dim priADays As Integer
Dim priBDays As Integer
Dim priCDays As Integer
Dim priDDays As Integer
Dim importantGetsPriA As Boolean
Dim waitingGetsPriE As Boolean
Dim showContexts As Boolean
Dim todoPath As String

'#################################################################################################################
'This script loops through all items of a specific tasks folder from Outlook
'(The To-do bar folder by default) and exports them in Todo.txt format
'onto the user's Dropbox folder, so it can be synchronized with the mobile application
'Todo.txt touch.
'The script also checks for new Tasks everytime it runs and creates them into the same Task folder in Outlook.
'#Todo.txt Priorities
'1. Tasks without due date take the (D) priority
'2. Tasks categorized with @waiting category take the (E) priority
'3. Tasks with a due date take the priorities A to C according to the number of days ahead of today
'4. Tasks marked as important in Outlook take the (A) priority
'5. New tasks imported from Todo.txt file do not hold their priority for now
'6. Tasks completed from todo.txt touch will be completed in outlook too
'
'To customize variables, change the User settings in the init() function
'send your comments to: nsivridis@ gmail.com
'Thanks for trying it!!!
'#################################################################################################################
Private Sub init()

'*** User settings ***

'Path to the Todo.txt files
todoPath = "d:\dropbox\todo"

'Outlook folder to be exported (By default Todo bar items)
Set tasksFolder = Outlook.GetNamespace("MAPI").GetDefaultFolder(olFolderToDo).Items

'Set priorities according to how many days ahead is each task
priADays = 3
priBDays = 5
priCDays = 9

'Do important tasks get (A) priority?
importantGetsPriA = True

'Do @waiting tasks get (E) priority?
waitingGetsPriE = True

'Do item categories show next to subject?
showContexts = True

End Sub
Sub ExportTodo()

init
For y = 1 To 100000
Next y
getNew
'Exit Sub

Dim itms As Items

Set itms = tasksFolder
 itms.Sort "[DueDate]", False
Dim ct As Integer
Dim i(100) As String
Dim w(100) As String
Dim ids(100) As String
Dim wt As Integer
wt = 0
Dim dd As String
Dim pri As String
Dim counter As Integer
counter = 2
For x = 1 To itms.Count
    If itms(x).Complete = False Then
    ct = ct + 1
    dd = ""
    'default priority D
    pri = "(D) "
    
    If itms(x).DueDate <> "1/1/4501" Then dd = " +" & itms(x).DueDate
    dayss = DateDiff("d", Now(), itms(x).DueDate, vbMonday)
    If dayss <= priADays Then pri = "(A) "
    If dayss <= priBDays And dayss > priADays Then pri = "(B) "
    If dayss < priCDays And dayss > priBDays Then pri = "(C) "
    
    If itms(x).Importance = 2 And importantGetsPriA = True Then pri = "(A) "
        
        If itms(x).Categories = "@waiting" And waitingGetsPriE Then pri = "(E) "
        
        i(ct - 1) = pri & itms(x).Subject & " " & IIf(showContexts, itms(x).Categories, "") & " " & dd
       
        ids(ct - 1) = counter & ";" & itms(x).EntryID
        counter = counter + 1
    End If
    
    
Next x


'Write Tasks
With CreateObject("ADODB.Stream")
.Open
.Charset = "UTF-8" ' sets stream encoding (UTF-8)
.lineseparator = -1
.Writetext "", 1
For x = 0 To ct - 1
.Writetext i(x), 1
Status = Status & "."
Next x

.SaveToFile todoPath & "\todo.txt", 2 ' adSaveCreateOverWrite
.Close
End With


'Write ID table file
With CreateObject("ADODB.Stream")
.Open
.Charset = "UTF-8" ' sets stream encoding (UTF-8)
.lineseparator = -1
For x = 0 To ct - 1
.Writetext ids(x), 1
Status = Status & "-"
Next x

.SaveToFile todoPath & "\ids.txt", 2 ' adSaveCreateOverWrite
.Close
End With

Status = ct & " To-dos exported"
End Sub

Private Sub getNew()
If Not todoPath <> "" Then init
'get New items
With CreateObject("ADODB.Stream")
.Open
.Charset = "UTF-8" ' sets stream encoding (UTF-8)
.lineseparator = -1
.LoadFromFile todoPath & "\todo.txt" ' Loads a File
tks = .readtext
Dim tk() As String
tkp = Split(tks, Chr(13))
lastone = UBound(tkp) - 1
.Close
End With

'get IDs
With CreateObject("ADODB.Stream")
.Open
.Charset = "UTF-8" ' sets stream encoding (UTF-8)
.lineseparator = -1
.LoadFromFile todoPath & "\ids.txt" ' Loads a File
idss = .readtext
Dim id() As String
idp = Split(idss, Chr(13))
lastid = UBound(idp)
.Close
End With

Dim newItems(100) As String
Dim newi As Integer
Dim hasPriority As String
Dim ntName As String
newi = 1
If lastid < lastone Then
'get new tasks
    For x = lastid + 1 To lastone
        newItems(newi) = tkp(x)
        newi = newi + 1
        hasPriority = ""
        ntName = tkp(x)
        'MsgBox ("New one:" & tkp(x))
        
        If Mid(tkp(x), 2, 1) = "(" Then
        hasPriority = Mid(tkp(x), 3, 1)
        ntName = Mid(tkp(x), 6, Len(tkp(x)))
        End If
        
        
        Dim it As TaskItem
        Set a = Outlook.GetNamespace("MAPI").GetDefaultFolder(olFolderTasks).Items
        Set it = a.Add()
        it.Subject = ntName
        it.Save
    Next x
End If
If (newi - 1) > 0 Then MsgBox ((newi - 1) & " New Tasks created")

'Watch for done tasks
    For x = 1 To lastone
        
        If tkp(x) <> "" Then
        If Mid(tkp(x), 2, 2) = "x " Then
            
             oid = Split(idp(x - 1), ";")
            Set it = Outlook.GetNamespace("MAPI").GetItemFromID(oid(1))
            it.Status = olTaskComplete
            it.Save

        End If
        End If
        
    Next x


End Sub
