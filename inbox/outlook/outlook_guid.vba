'Make sure to self-sign a certificate using "SelfCert.exe" in Office
'then going to Tools > Digital Signature and choosing the generated cert
'Then, add the reference to Microsoft Forms 2.0 Object Library to
'Tools > References by browsing for system32/FM20.dll

Function GetCurrentItem() As Object
    Dim objApp As Outlook.Application
           
    Set objApp = Application
    On Error Resume Next
    Select Case TypeName(objApp.ActiveWindow)
        Case "Explorer"
            Set GetCurrentItem = objApp.ActiveExplorer.Selection.Item(1)
        Case "Inspector"
            Set GetCurrentItem = objApp.ActiveInspector.CurrentItem
    End Select
       
    Set objApp = Nothing
End Function

'Adds a link to the currently selected message to the clipboard
Sub AddLinkToMessageInClipboard()
    Dim objMail As Object
    'was earlier Outlook.MailItem
    Dim doClipboard As New DataObject
    Dim message As String
      
    'One and ONLY one message muse be selected
    'If Application.ActiveExplorer.Selection.Count <> 1 Then
    '    MsgBox ("Select one and ONLY one message.")
    '    Exit Sub
    'End If
   
    'Set objMail = Application.ActiveExplorer.Selection.Item(1)
    Set objMail = GetCurrentItem()
   
    If objMail.Class = olMail Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][MESSAGE: " + objMail.Subject + " (" + objMail.SenderName + ")]]"
    ElseIf objMail.Class = olAppointment Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][MEETING: " + objMail.Subject + " (" + objMail.Organizer + ")]]"
    ElseIf objMail.Class = olTask Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][TASK: " + objMail.Subject + " (" + objMail.Owner + ")]]"
    ElseIf objMail.Class = olContact Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][CONTACT: " + objMail.Subject + " (" + objMail.FullName + ")]]"
    ElseIf objMail.Class = olJournal Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][JOURNAL: " + objMail.Subject + " (" + objMail.Type + ")]]"
    ElseIf objMail.Class = olNote Then
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][NOTE: " + objMail.Subject + " (" + " " + ")]]"
    Else
        doClipboard.SetText "[[outlook:" + objMail.EntryID + "][ITEM: " + objMail.Subject + " (" + objMail.MessageClass + ")]]"
    End If
    
    doClipboard.PutInClipboard
   
End Sub
