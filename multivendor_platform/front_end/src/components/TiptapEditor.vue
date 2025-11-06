<template>
  <div class="tiptap-editor" dir="rtl">
    <div class="editor-toolbar" v-if="editor">
      <v-btn-toggle
        v-model="toolbarState"
        variant="outlined"
        density="compact"
        divided
        class="toolbar-buttons"
      >
        <v-btn
          @click="editor.chain().focus().toggleBold().run()"
          :class="{ 'v-btn--active': editor.isActive('bold') }"
          icon
          size="small"
        >
          <v-icon>mdi-format-bold</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleItalic().run()"
          :class="{ 'v-btn--active': editor.isActive('italic') }"
          icon
          size="small"
        >
          <v-icon>mdi-format-italic</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
          :class="{ 'v-btn--active': editor.isActive('heading', { level: 1 }) }"
          icon
          size="small"
        >
          <v-icon>mdi-format-header-1</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
          :class="{ 'v-btn--active': editor.isActive('heading', { level: 2 }) }"
          icon
          size="small"
        >
          <v-icon>mdi-format-header-2</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
          :class="{ 'v-btn--active': editor.isActive('heading', { level: 3 }) }"
          icon
          size="small"
        >
          <v-icon>mdi-format-header-3</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleBulletList().run()"
          :class="{ 'v-btn--active': editor.isActive('bulletList') }"
          icon
          size="small"
        >
          <v-icon>mdi-format-list-bulleted</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().toggleOrderedList().run()"
          :class="{ 'v-btn--active': editor.isActive('orderedList') }"
          icon
          size="small"
        >
          <v-icon>mdi-format-list-numbered</v-icon>
        </v-btn>
        <v-btn
          @click="setLink"
          :class="{ 'v-btn--active': editor.isActive('link') }"
          icon
          size="small"
        >
          <v-icon>mdi-link</v-icon>
        </v-btn>
        <v-btn
          @click="addImage"
          icon
          size="small"
        >
          <v-icon>mdi-image</v-icon>
        </v-btn>
        <v-btn
          @click="editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()"
          icon
          size="small"
        >
          <v-icon>mdi-table</v-icon>
        </v-btn>
      </v-btn-toggle>
    </div>
    <div class="editor-content">
      <editor-content :editor="editor" />
    </div>
    
    <!-- Link Dialog -->
    <v-dialog v-model="showLinkDialog" max-width="500px">
      <v-card>
        <v-card-title>افزودن لینک</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="linkUrl"
            label="آدرس لینک"
            variant="outlined"
            density="compact"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showLinkDialog = false">انصراف</v-btn>
          <v-btn color="primary" @click="insertLink">افزودن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Image Dialog -->
    <v-dialog v-model="showImageDialog" max-width="500px">
      <v-card>
        <v-card-title>افزودن تصویر</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="imageUrl"
            label="آدرس تصویر"
            variant="outlined"
            density="compact"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showImageDialog = false">انصراف</v-btn>
          <v-btn color="primary" @click="insertImage">افزودن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import { ref, watch, onBeforeUnmount } from 'vue'

export default {
  name: 'TiptapEditor',
  components: {
    EditorContent
  },
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const showLinkDialog = ref(false)
    const showImageDialog = ref(false)
    const linkUrl = ref('')
    const imageUrl = ref('')
    const toolbarState = ref(null)

    const editor = useEditor({
      content: props.modelValue,
      extensions: [
        StarterKit.configure({
          heading: {
            levels: [1, 2, 3]
          }
        }),
        Image.configure({
          inline: true,
          allowBase64: true
        }),
        Link.configure({
          openOnClick: false,
          HTMLAttributes: {
            target: '_blank',
            rel: 'noopener noreferrer'
          }
        }),
        Table.configure({
          resizable: true
        }),
        TableRow,
        TableHeader,
        TableCell
      ],
      editorProps: {
        attributes: {
          class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none',
          dir: 'rtl',
          style: 'min-height: 200px; padding: 16px;'
        }
      },
      onUpdate: ({ editor }) => {
        emit('update:modelValue', editor.getHTML())
      }
    })

    watch(() => props.modelValue, (value) => {
      const isSame = editor.value.getHTML() === value
      if (isSame) {
        return
      }
      editor.value.commands.setContent(value, false)
    })

    const setLink = () => {
      if (editor.value.isActive('link')) {
        editor.value.chain().focus().unsetLink().run()
      } else {
        showLinkDialog.value = true
      }
    }

    const insertLink = () => {
      if (linkUrl.value) {
        editor.value.chain().focus().setLink({ href: linkUrl.value }).run()
      }
      showLinkDialog.value = false
      linkUrl.value = ''
    }

    const addImage = () => {
      showImageDialog.value = true
    }

    const insertImage = () => {
      if (imageUrl.value) {
        editor.value.chain().focus().setImage({ src: imageUrl.value }).run()
      }
      showImageDialog.value = false
      imageUrl.value = ''
    }

    onBeforeUnmount(() => {
      editor.value.destroy()
    })

    return {
      editor,
      showLinkDialog,
      showImageDialog,
      linkUrl,
      imageUrl,
      toolbarState,
      setLink,
      insertLink,
      addImage,
      insertImage
    }
  }
}
</script>

<style scoped>
.tiptap-editor {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 4px;
  background-color: rgb(var(--v-theme-surface));
}

.editor-toolbar {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  padding: 8px;
  background-color: rgb(var(--v-theme-surface));
}

.toolbar-buttons {
  flex-wrap: wrap;
  gap: 4px;
}

.editor-content {
  min-height: 200px;
}

:deep(.ProseMirror) {
  outline: none;
  direction: rtl;
  text-align: right;
  font-family: 'Vazir', 'Tahoma', sans-serif;
}

:deep(.ProseMirror p) {
  margin: 0.5em 0;
}

:deep(.ProseMirror h1),
:deep(.ProseMirror h2),
:deep(.ProseMirror h3) {
  font-weight: bold;
  margin-top: 1em;
  margin-bottom: 0.5em;
}

:deep(.ProseMirror h1) {
  font-size: 2em;
}

:deep(.ProseMirror h2) {
  font-size: 1.5em;
}

:deep(.ProseMirror h3) {
  font-size: 1.25em;
}

:deep(.ProseMirror ul),
:deep(.ProseMirror ol) {
  padding-right: 1.5em;
  margin: 0.5em 0;
}

:deep(.ProseMirror li) {
  margin: 0.25em 0;
}

:deep(.ProseMirror a) {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
}

:deep(.ProseMirror img) {
  max-width: 100%;
  height: auto;
  margin: 0.5em 0;
}

:deep(.ProseMirror table) {
  border-collapse: collapse;
  margin: 0.5em 0;
  width: 100%;
}

:deep(.ProseMirror table td),
:deep(.ProseMirror table th) {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  padding: 8px;
  text-align: right;
}

:deep(.ProseMirror table th) {
  background-color: rgba(var(--v-theme-primary), 0.1);
  font-weight: bold;
}
</style>

