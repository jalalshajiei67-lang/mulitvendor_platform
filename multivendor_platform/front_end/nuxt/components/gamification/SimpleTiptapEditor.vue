<template>
  <div class="simple-tiptap-editor" dir="rtl">
    <!-- Toolbar -->
    <v-card
      v-if="editor"
      elevation="0"
      rounded="lg"
      class="editor-toolbar mb-2"
      color="surface-variant"
    >
      <div class="d-flex flex-wrap align-center gap-1 pa-2">
        <!-- Text Formatting -->
        <v-btn-toggle
          variant="text"
          density="compact"
          divided
          class="toolbar-group"
        >
          <v-btn
            @click="editor.chain().focus().toggleBold().run()"
            :class="{ 'v-btn--active': editor.isActive('bold') }"
            icon
            size="small"
            title="پررنگ (Ctrl+B)"
          >
            <v-icon size="20">mdi-format-bold</v-icon>
          </v-btn>
          <v-btn
            @click="editor.chain().focus().toggleItalic().run()"
            :class="{ 'v-btn--active': editor.isActive('italic') }"
            icon
            size="small"
            title="ایتالیک (Ctrl+I)"
          >
            <v-icon size="20">mdi-format-italic</v-icon>
          </v-btn>
        </v-btn-toggle>

        <v-divider vertical class="mx-1" style="height: 24px;"></v-divider>

        <!-- Lists -->
        <v-btn-toggle
          variant="text"
          density="compact"
          divided
          class="toolbar-group"
        >
          <v-btn
            @click="editor.chain().focus().toggleBulletList().run()"
            :class="{ 'v-btn--active': editor.isActive('bulletList') }"
            icon
            size="small"
            title="لیست نقطه‌ای"
          >
            <v-icon size="20">mdi-format-list-bulleted</v-icon>
          </v-btn>
          <v-btn
            @click="editor.chain().focus().toggleOrderedList().run()"
            :class="{ 'v-btn--active': editor.isActive('orderedList') }"
            icon
            size="small"
            title="لیست شماره‌دار"
          >
            <v-icon size="20">mdi-format-list-numbered</v-icon>
          </v-btn>
        </v-btn-toggle>

        <v-divider vertical class="mx-1" style="height: 24px;"></v-divider>

        <!-- Blockquote -->
        <v-btn
          @click="editor.chain().focus().toggleBlockquote().run()"
          :class="{ 'v-btn--active': editor.isActive('blockquote') }"
          variant="text"
          icon
          size="small"
          title="نقل قول"
        >
          <v-icon size="20">mdi-format-quote-close</v-icon>
        </v-btn>

        <v-divider vertical class="mx-1" style="height: 24px;"></v-divider>

        <!-- Clear Formatting -->
        <v-btn
          @click="editor.chain().focus().clearNodes().unsetAllMarks().run()"
          variant="text"
          icon
          size="small"
          title="پاک کردن فرمت"
        >
          <v-icon size="20">mdi-format-clear</v-icon>
        </v-btn>
      </div>
    </v-card>

    <!-- Editor Content -->
    <div
      class="editor-content"
      :class="{ 'editor-disabled': disabled, 'editor-focused': isFocused }"
    >
      <EditorContent :editor="editor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
  modelValue: string
  disabled?: boolean
  placeholder?: string
  minHeight?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const isFocused = ref(false)

const editor = useEditor({
  content: props.modelValue || '',
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [2, 3]
      }
    })
  ],
  editorProps: {
    attributes: {
      class: 'prose prose-sm max-w-none focus:outline-none',
      dir: 'rtl',
      style: `min-height: ${props.minHeight || '150px'}; padding: 16px;`,
      'data-placeholder': props.placeholder || 'متن خود را بنویسید...'
    },
    handleDOMEvents: {
      focus: () => {
        isFocused.value = true
        return false
      },
      blur: () => {
        isFocused.value = false
        return false
      }
    }
  },
  onUpdate: ({ editor }) => {
    const html = editor.getHTML()
    emit('update:modelValue', html)
  },
  editable: !props.disabled
})

watch(() => props.modelValue, (value) => {
  if (editor.value && editor.value.getHTML() !== value) {
    editor.value.commands.setContent(value || '', false)
  }
})

watch(() => props.disabled, (disabled) => {
  if (editor.value) {
    editor.value.setEditable(!disabled)
  }
})

onMounted(() => {
  if (props.modelValue && editor.value) {
    editor.value.commands.setContent(props.modelValue, false)
  }
})

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})
</script>

<style scoped>
.simple-tiptap-editor {
  width: 100%;
}

.editor-toolbar {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.toolbar-group {
  border: none;
}

.toolbar-group :deep(.v-btn) {
  min-width: 36px;
  padding: 4px;
}

.toolbar-group :deep(.v-btn--active) {
  background-color: rgba(var(--v-theme-primary), 0.1);
  color: rgb(var(--v-theme-primary));
}

.editor-content {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 8px;
  background-color: rgb(var(--v-theme-surface));
  transition: all 0.2s ease;
}

.editor-content:hover {
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.editor-focused {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 2px rgba(var(--v-theme-primary), 0.1);
}

.editor-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: rgba(var(--v-theme-surface-variant), 0.5);
}

.editor-content :deep(.ProseMirror) {
  outline: none;
  font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.editor-content :deep(.ProseMirror p) {
  margin: 0.5em 0;
}

.editor-content :deep(.ProseMirror p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: right;
  color: rgba(var(--v-theme-on-surface), 0.4);
  pointer-events: none;
  height: 0;
}

.editor-content :deep(.ProseMirror ul),
.editor-content :deep(.ProseMirror ol) {
  padding-right: 1.5em;
  margin: 0.5em 0;
}

.editor-content :deep(.ProseMirror li) {
  margin: 0.25em 0;
}

.editor-content :deep(.ProseMirror blockquote) {
  border-right: 3px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1em;
  margin: 1em 0;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.editor-content :deep(.ProseMirror h2) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 1em 0 0.5em 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror h3) {
  font-size: 1.25em;
  font-weight: bold;
  margin: 0.75em 0 0.5em 0;
  line-height: 1.3;
}

.editor-content :deep(.ProseMirror strong) {
  font-weight: bold;
}

.editor-content :deep(.ProseMirror em) {
  font-style: italic;
}

/* RTL Specific */
[dir="rtl"] .editor-content :deep(.ProseMirror ul),
[dir="rtl"] .editor-content :deep(.ProseMirror ol) {
  padding-right: 1.5em;
  padding-left: 0;
}

[dir="rtl"] .editor-content :deep(.ProseMirror blockquote) {
  border-right: 3px solid rgba(var(--v-theme-primary), 0.5);
  border-left: none;
  padding-right: 1em;
  padding-left: 0;
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .editor-toolbar {
    padding: 0.5rem !important;
  }
  
  .toolbar-group :deep(.v-btn) {
    min-width: 32px;
    padding: 2px;
  }
  
  .editor-content :deep(.ProseMirror) {
    padding: 12px !important;
    font-size: 13px;
  }
}
</style>
