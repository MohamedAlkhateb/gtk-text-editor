import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Editor")

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        textView = Gtk.TextView()
        toolBar = self.createToolBar(textView)
        box.pack_start(toolBar, False, False, 0)
        box.pack_start(textView, True, True, 0)

        self.add(box)

    def createToolBar(self, textView):
        toolBar = Gtk.Toolbar()

        textBuffer = textView.get_buffer()

        saveButton = Gtk.ToolButton()
        saveButton.set_icon_name("document-save-as")
        saveButton.connect("clicked", self.saveBuffer, textBuffer)
        toolBar.insert(saveButton, -1)

        toolBar.insert(Gtk.SeparatorToolItem(), -1)

        boldButton = Gtk.ToolButton()
        boldButton.set_icon_name("format-text-bold")
        boldTag = textBuffer.create_tag("bold", weight = Pango.Weight.BOLD)
        boldButton.connect("clicked", lambda widget:
            textBuffer.apply_tag(boldTag, *textBuffer.get_selection_bounds())
        )
        toolBar.insert(boldButton, -1)

        toolBar.insert(Gtk.SeparatorToolItem(), -1)
        
        toolButton = Gtk.ToolButton()
        toolButton.set_icon_name("preferences-desktop-font")
        toolButton.connect("clicked", self.setFont, textBuffer)
        toolBar.insert(toolButton, -1)

        return toolBar

    def saveBuffer(self, widget, textBuffer):
        saveDialog = Gtk.FileChooserDialog()
        saveDialog.set_action(Gtk.FileChooserAction.SAVE)
        saveDialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        saveDialog.add_button("Save As", Gtk.ResponseType.OK)

        response = saveDialog.run()
        if response != Gtk.ResponseType.OK:
            saveDialog.destroy()
            return

        path = os.path.join(saveDialog.get_current_folder(), saveDialog.get_filename())
        bounds = textBuffer.get_bounds()
        serializationFormat = textBuffer.register_serialize_tagset()
        serial = textBuffer.serialize(textBuffer, serializationFormat, *bounds)
        with open(path, 'wb') as outputFile:
            outputFile.write(serial)

        saveDialog.destroy()

    def setFont(self, widget, textBuffer):
        fontChooserDialog = Gtk.FontChooserDialog()
        fontChooserDialog.set_title("FontChooserDialog")
        response = fontChooserDialog.run()

        if response != Gtk.ResponseType.OK:
            fontChooserDialog.destroy()
            return

        fontDescriptor = fontChooserDialog.get_font_desc()
        tagTable = textBuffer.get_tag_table()
        tagName = fontDescriptor.to_string()
        tag = tagTable.lookup(tagName)
        if tag is None:
            tag = textBuffer.create_tag(tagName, font_desc=fontDescriptor)
        textBuffer.apply_tag(tag, *textBuffer.get_selection_bounds())
        fontChooserDialog.destroy()



editorWindow = EditorWindow()
editorWindow.connect("destroy", Gtk.main_quit)
editorWindow.show_all()
Gtk.main()
