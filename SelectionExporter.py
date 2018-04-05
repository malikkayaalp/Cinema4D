import c4d
from c4d import gui


#Scipting Malik Kayaalp


def main():
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    IDM_MENU1 = c4d.FIRST_POPUP_ID
    IDM_MENU2 = c4d.FIRST_POPUP_ID+1


    menu = c4d.BaseContainer()
    menu.InsData(c4d.FORMAT_OBJ2EXPORT, 'OBJ')
    menu.InsData(c4d.FORMAT_3DSEXPORT, '3DS')
    result = gui.ShowPopupDialog(cd=None, bc=menu,x=c4d.MOUSEPOS, y=c4d.MOUSEPOS)
    
    if result ==  0 :
        return
    
    if objs == [] or None:
         
         gui.MessageDialog('Bir Obje Seciniz')
         
         if objs == []:
             return
     
    

    docTemp = c4d.documents.IsolateObjects(doc, objs)
    if docTemp == None:
        return    
    
    

    unitScale = c4d.UnitScaleData()
    unitScale.SetUnitScale(1.0, c4d.DOCUMENT_UNIT_CM)

    bc = c4d.BaseContainer()
    bc[c4d.DOCUMENT_DOCUNIT] = unitScale
    docTemp.SetDocumentData(c4d. DOCUMENTSETTINGS_DOCUMENT, bc)    
    

    plug = c4d.plugins.FindPlugin(c4d.FORMAT_OBJ2EXPORT, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return

    filePath = c4d.storage.LoadDialog(title="Save File 3DS", flags=c4d.FILESELECT_SAVE, force_suffix="obj")
    if filePath is None:
        return
        
        # Finally export the document
    if c4d.documents.SaveDocument(docTemp, filePath, c4d.SAVEDOCUMENTFLAGS_EXPORTDIALOG, c4d.FORMAT_OBJ2EXPORT):
        gui.MessageDialog('Expot Islemi Tamamdir')
        
    else:
        gui.MessageDialog('Export Basarisiz!')    

    c4d.documents.KillDocument(docTemp)


if __name__=='__main__':
    main()
