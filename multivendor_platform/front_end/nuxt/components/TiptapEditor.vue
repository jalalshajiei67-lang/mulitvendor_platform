<template>
  <div class="tiptap-editor" dir="rtl">
    <div class="editor-content-wrapper">
      <div class="editor-toolbar-wrapper">
        <div class="editor-toolbar" v-if="editor">
          <div class="toolbar-groups">
            <!-- Text Formatting Group -->
            <div class="toolbar-group">
              <v-btn-toggle
                v-model="toolbarState"
                variant="outlined"
                density="compact"
                divided
                class="toolbar-buttons"
              >
                <v-btn
                  @click="editor.chain().focus().toggleBold().run(); editorState++"
                  :class="{ 'v-btn--active': isBoldActive }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-bold</v-icon>
                </v-btn>
                <v-btn
                  @click="editor.chain().focus().toggleItalic().run(); editorState++"
                  :class="{ 'v-btn--active': isItalicActive }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-italic</v-icon>
                </v-btn>
              </v-btn-toggle>
              <v-menu location="bottom">
                <template v-slot:activator="{ props }">
                  <v-btn
                    v-bind="props"
                    variant="outlined"
                    density="compact"
                    size="small"
                    class="font-size-btn"
                  >
                    <span class="font-size-label">{{ currentFontSize || 'اندازه فونت' }}</span>
                    <v-icon size="small" class="mr-1">mdi-chevron-down</v-icon>
                  </v-btn>
                </template>
                <v-card min-width="200">
                  <v-card-text class="pa-2">
                    <div class="font-size-presets">
                      <v-btn
                        v-for="size in fontSizes"
                        :key="size"
                        variant="text"
                        density="compact"
                        size="small"
                        block
                        class="justify-start"
                        :class="{ 'font-size-active': currentFontSize === size }"
                        @click="setFontSize(size)"
                      >
                        {{ size }}px
                      </v-btn>
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-text-field
                      v-model.number="customFontSize"
                      label="اندازه سفارشی (px)"
                      type="number"
                      variant="outlined"
                      density="compact"
                      :min="1"
                      :max="200"
                      @keyup.enter="setCustomFontSize"
                    ></v-text-field>
                    <v-btn
                      color="primary"
                      size="small"
                      block
                      @click="setCustomFontSize"
                    >
                      اعمال
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-menu>
            </div>

            <v-divider vertical class="toolbar-divider"></v-divider>

            <!-- Headings Group -->
            <div class="toolbar-group">
              <v-btn-toggle
                v-model="toolbarState"
                variant="outlined"
                density="compact"
                divided
                class="toolbar-buttons"
              >
                <v-btn
                  @click="editor.chain().focus().toggleHeading({ level: 1 }).run(); editorState++"
                  :class="{ 'v-btn--active': editor.isActive('heading', { level: 1 }) }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-header-1</v-icon>
                </v-btn>
                <v-btn
                  @click="editor.chain().focus().toggleHeading({ level: 2 }).run(); editorState++"
                  :class="{ 'v-btn--active': editor.isActive('heading', { level: 2 }) }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-header-2</v-icon>
                </v-btn>
                <v-btn
                  @click="editor.chain().focus().toggleHeading({ level: 3 }).run(); editorState++"
                  :class="{ 'v-btn--active': editor.isActive('heading', { level: 3 }) }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-header-3</v-icon>
                </v-btn>
              </v-btn-toggle>
            </div>

            <v-divider vertical class="toolbar-divider"></v-divider>

            <!-- Lists Group -->
            <div class="toolbar-group">
              <v-btn-toggle
                v-model="toolbarState"
                variant="outlined"
                density="compact"
                divided
                class="toolbar-buttons"
              >
                <v-btn
                  @click="editor.chain().focus().toggleBulletList().run(); editorState++"
                  :class="{ 'v-btn--active': editor.isActive('bulletList') }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-list-bulleted</v-icon>
                </v-btn>
                <v-btn
                  @click="editor.chain().focus().toggleOrderedList().run(); editorState++"
                  :class="{ 'v-btn--active': editor.isActive('orderedList') }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-format-list-numbered</v-icon>
                </v-btn>
              </v-btn-toggle>
            </div>

            <v-divider vertical class="toolbar-divider"></v-divider>

            <!-- Media Group -->
            <div class="toolbar-group">
              <v-btn-toggle
                v-model="toolbarState"
                variant="outlined"
                density="compact"
                divided
                class="toolbar-buttons"
              >
                <v-btn
                  @click="setLink"
                  :class="{ 'v-btn--active': isLinkActive }"
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
              </v-btn-toggle>
            </div>

            <v-divider vertical class="toolbar-divider"></v-divider>

            <!-- Tables Group -->
            <div class="toolbar-group">
              <v-btn-toggle
                v-model="toolbarState"
                variant="outlined"
                density="compact"
                divided
                class="toolbar-buttons"
              >
                <v-btn
                  @click="openTableDialog"
                  :class="{ 'v-btn--active': isTableActiveComputed }"
                  icon
                  size="small"
                >
                  <v-icon>mdi-table</v-icon>
                </v-btn>
              </v-btn-toggle>
            </div>
          </div>
        </div>
      </div>
      <div class="editor-content">
        <EditorContent :editor="editor" />
      
        <!-- Table Controls Menu (shown when table is active) -->
        <div v-if="isTableActive" class="table-controls-menu">
          <v-card elevation="4" class="table-controls-card">
            <v-card-text class="pa-2">
              <div class="d-flex align-center" style="gap: 4px; flex-wrap: wrap;">
                <v-btn
                  @click="addRowBefore"
                  icon
                  size="small"
                  variant="text"
                  title="افزودن سطر قبل"
                >
                  <v-icon size="small">mdi-table-row-plus-before</v-icon>
                </v-btn>
                <v-btn
                  @click="addRowAfter"
                  icon
                  size="small"
                  variant="text"
                  title="افزودن سطر بعد"
                >
                  <v-icon size="small">mdi-table-row-plus-after</v-icon>
                </v-btn>
                <v-btn
                  @click="deleteRow"
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  title="حذف سطر"
                >
                  <v-icon size="small">mdi-table-row-remove</v-icon>
                </v-btn>
                <v-divider vertical class="mx-1"></v-divider>
                <v-btn
                  @click="addColumnBefore"
                  icon
                  size="small"
                  variant="text"
                  title="افزودن ستون قبل"
                >
                  <v-icon size="small">mdi-table-column-plus-before</v-icon>
                </v-btn>
                <v-btn
                  @click="addColumnAfter"
                  icon
                  size="small"
                  variant="text"
                  title="افزودن ستون بعد"
                >
                  <v-icon size="small">mdi-table-column-plus-after</v-icon>
                </v-btn>
                <v-btn
                  @click="deleteColumn"
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  title="حذف ستون"
                >
                  <v-icon size="small">mdi-table-column-remove</v-icon>
                </v-btn>
                <v-divider vertical class="mx-1"></v-divider>
                <v-btn
                  @click="deleteTable"
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  title="حذف جدول"
                >
                  <v-icon size="small">mdi-table-remove</v-icon>
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </div>
    
    <!-- Table Dialog -->
    <v-dialog v-model="showTableDialog" max-width="400px">
      <v-card dir="rtl">
        <v-card-title>افزودن جدول</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model.number="tableRows"
                label="تعداد سطرها"
                type="number"
                variant="outlined"
                density="compact"
                :min="1"
                :max="20"
                :rules="[v => (v >= 1 && v <= 20) || 'بین 1 تا 20']"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model.number="tableCols"
                label="تعداد ستون‌ها"
                type="number"
                variant="outlined"
                density="compact"
                :min="1"
                :max="20"
                :rules="[v => (v >= 1 && v <= 20) || 'بین 1 تا 20']"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-checkbox
                v-model="tableHeaderRow"
                label="سطر هدر"
                density="compact"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeTableDialog">انصراف</v-btn>
          <v-btn color="primary" @click="insertTable">افزودن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
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

<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { Image } from '@tiptap/extension-image'
import { Link } from '@tiptap/extension-link'
import { Table } from '@tiptap/extension-table'
import { TableRow } from '@tiptap/extension-table-row'
import { TableCell } from '@tiptap/extension-table-cell'
import { TableHeader } from '@tiptap/extension-table-header'
import { TextStyle } from '@tiptap/extension-text-style'

// FontSize Extension
const FontSize = TextStyle.extend({
  addAttributes() {
    return {
      ...this.parent?.(),
      fontSize: {
        default: null,
        parseHTML: (element: HTMLElement) => {
          const fontSize = element.style.fontSize
          if (!fontSize) return null
          return String(fontSize)
        },
        renderHTML: (attributes: Record<string, any>) => {
          if (!attributes.fontSize) {
            return {}
          }
          return {
            style: `font-size: ${attributes.fontSize}`
          }
        }
      }
    }
  },
  
  addCommands() {
    return {
      ...this.parent?.(),
      setFontSize: (fontSize: number | string) => ({ commands }: any) => {
        if (!fontSize && fontSize !== 0) {
          return commands.unsetMark(this.name)
        }
        
        let fontSizeValue: string
        if (typeof fontSize === 'number') {
          fontSizeValue = `${fontSize}px`
        } else if (typeof fontSize === 'string') {
          fontSizeValue = fontSize.includes('px') ? fontSize : `${fontSize}px`
        } else {
          return false
        }
        
        if (!fontSizeValue || fontSizeValue === 'px') {
          return false
        }
        
        return commands.setMark(this.name, { fontSize: fontSizeValue })
      },
      unsetFontSize: () => ({ commands }: any) => {
        return commands.unsetMark(this.name)
      }
    }
  }
})

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const showLinkDialog = ref(false)
const showImageDialog = ref(false)
const showTableDialog = ref(false)
const linkUrl = ref('')
const imageUrl = ref('')
const toolbarState = ref(null)
const tableRows = ref(3)
const tableCols = ref(3)
const tableHeaderRow = ref(true)
const isTableActive = ref(false)
const fontSizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]
const customFontSize = ref<number | null>(null)
const currentFontSize = ref<number | null>(null)
const editorState = ref(0)

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3]
      },
      textStyle: false,
      link: false
    }),
    FontSize,
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
    const html = editor.getHTML()
    emit('update:modelValue', html)
  },
  onSelectionUpdate: ({ editor }) => {
    isTableActive.value = editor.isActive('table')
    updateCurrentFontSize(editor)
    editorState.value++
  },
  onFocus: ({ editor }) => {
    isTableActive.value = editor.isActive('table')
    updateCurrentFontSize(editor)
    editorState.value++
  },
  onBlur: () => {
    setTimeout(() => {
      if (editor.value) {
        isTableActive.value = editor.value.isActive('table')
        updateCurrentFontSize(editor.value)
        editorState.value++
      }
    }, 100)
  },
  onTransaction: ({ editor, transaction }) => {
    if (transaction.docChanged || transaction.selectionSet) {
      updateCurrentFontSize(editor)
      editorState.value++
    }
  }
})

watch(() => props.modelValue, (value) => {
  const isSame = editor.value?.getHTML() === value
  if (isSame) {
    return
  }
  editor.value?.commands.setContent(value, false)
})

const setLink = () => {
  if (editor.value?.isActive('link')) {
    editor.value.chain().focus().unsetLink().run()
    editorState.value++
  } else {
    showLinkDialog.value = true
  }
}

const insertLink = () => {
  if (linkUrl.value && editor.value) {
    editor.value.chain().focus().setLink({ href: linkUrl.value }).run()
    editorState.value++
  }
  showLinkDialog.value = false
  linkUrl.value = ''
}

const addImage = () => {
  showImageDialog.value = true
}

const insertImage = () => {
  if (imageUrl.value && editor.value) {
    editor.value.chain().focus().setImage({ src: imageUrl.value }).run()
  }
  showImageDialog.value = false
  imageUrl.value = ''
}

const openTableDialog = () => {
  tableRows.value = 3
  tableCols.value = 3
  tableHeaderRow.value = true
  showTableDialog.value = true
}

const closeTableDialog = () => {
  showTableDialog.value = false
}

const insertTable = () => {
  if (tableRows.value >= 1 && tableRows.value <= 20 && tableCols.value >= 1 && tableCols.value <= 20 && editor.value) {
    editor.value.chain().focus().insertTable({
      rows: tableRows.value,
      cols: tableCols.value,
      withHeaderRow: tableHeaderRow.value
    }).run()
    showTableDialog.value = false
  }
}

const addRowBefore = () => {
  editor.value?.chain().focus().addRowBefore().run()
}

const addRowAfter = () => {
  editor.value?.chain().focus().addRowAfter().run()
}

const deleteRow = () => {
  editor.value?.chain().focus().deleteRow().run()
}

const addColumnBefore = () => {
  editor.value?.chain().focus().addColumnBefore().run()
}

const addColumnAfter = () => {
  editor.value?.chain().focus().addColumnAfter().run()
}

const deleteColumn = () => {
  editor.value?.chain().focus().deleteColumn().run()
}

const deleteTable = () => {
  if (confirm('آیا مطمئن هستید که می‌خواهید این جدول را حذف کنید؟')) {
    editor.value?.chain().focus().deleteTable().run()
  }
}

const updateCurrentFontSize = (editorInstance: any) => {
  const attrs = editorInstance.getAttributes('textStyle')
  if (attrs && attrs.fontSize) {
    const numericValue = attrs.fontSize.toString().replace('px', '')
    currentFontSize.value = parseInt(numericValue) || null
  } else {
    currentFontSize.value = null
  }
}

const setFontSize = (size: number | string) => {
  if (!editor.value) return
  
  const numSize = typeof size === 'string' ? parseFloat(size) : size
  
  if (isNaN(numSize) || numSize < 1 || numSize > 200) {
    console.warn('Invalid font size:', size)
    return
  }
  
  try {
    const result = editor.value.chain().focus().setFontSize(numSize).run()
    
    if (result) {
      editorState.value++
      setTimeout(() => {
        if (editor.value) {
          updateCurrentFontSize(editor.value)
          editorState.value++
        }
      }, 50)
    }
  } catch (error) {
    console.error('Error setting font size:', error)
  }
}

const setCustomFontSize = () => {
  if (customFontSize.value && customFontSize.value >= 1 && customFontSize.value <= 200) {
    setFontSize(customFontSize.value)
    customFontSize.value = null
  }
}

const isBoldActive = computed(() => {
  editorState.value
  return editor.value?.isActive('bold') ?? false
})

const isItalicActive = computed(() => {
  editorState.value
  return editor.value?.isActive('italic') ?? false
})

const isLinkActive = computed(() => {
  editorState.value
  return editor.value?.isActive('link') ?? false
})

const isTableActiveComputed = computed(() => {
  editorState.value
  return editor.value?.isActive('table') ?? false
})

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})

watch(() => editor.value, (newEditor) => {
  if (newEditor) {
    isTableActive.value = newEditor.isActive('table')
    updateCurrentFontSize(newEditor)
  }
}, { immediate: true })
</script>

<style scoped>
.tiptap-editor {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 4px;
  background-color: rgb(var(--v-theme-surface));
  position: relative;
  display: flex;
  flex-direction: column;
  max-height: 100%;
}

.editor-toolbar-wrapper {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: rgb(var(--v-theme-surface));
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
  width: 100%;
}

.editor-toolbar {
  padding: 8px;
  background-color: rgb(var(--v-theme-surface));
  overflow-x: auto;
  overflow-y: hidden;
}

.toolbar-groups {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-divider {
  height: 32px;
  margin: 0 4px;
}

.toolbar-buttons {
  flex-wrap: wrap;
  gap: 4px;
  display: flex;
  align-items: center;
}

.font-size-btn {
  min-width: 120px;
  justify-content: space-between;
}

.font-size-label {
  font-size: 0.875rem;
}

.font-size-presets {
  max-height: 200px;
  overflow-y: auto;
}

.font-size-active {
  background-color: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
}

.editor-content-wrapper {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  -webkit-overflow-scrolling: touch;
  min-height: 0;
}

.editor-content {
  min-height: 200px;
  position: relative;
}

.table-controls-menu {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 20;
  animation: slideUp 0.2s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.table-controls-card {
  background-color: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
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

