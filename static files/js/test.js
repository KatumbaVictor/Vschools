var editor = CodeMirror.fromTextArea(document.getElementById('editor'),
    {
        mode: 'python',
        lineNumbers: true,
        theme: 'dracula',
        indentUnit: 2,
        smartIndent: true
    }
)

editor.save()