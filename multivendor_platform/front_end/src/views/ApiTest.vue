<template>
  <div class="api-test">
    <h1>API Connection Test</h1>
    
    <div class="test-section">
      <h2>Blog Posts Test</h2>
      <button @click="testBlogPosts" :disabled="loading">Test Blog Posts API</button>
      <div v-if="postsResult">
        <h3>Result:</h3>
        <pre>{{ JSON.stringify(postsResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>Blog Categories Test</h2>
      <button @click="testBlogCategories" :disabled="loading">Test Blog Categories API</button>
      <div v-if="categoriesResult">
        <h3>Result:</h3>
        <pre>{{ JSON.stringify(categoriesResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>Direct API Test</h2>
      <button @click="testDirectApi" :disabled="loading">Test Direct API Call</button>
      <div v-if="directResult">
        <h3>Result:</h3>
        <pre>{{ JSON.stringify(directResult, null, 2) }}</pre>
      </div>
    </div>

    <div v-if="error" class="error">
      <h3>Error:</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '@/services/api'

export default {
  name: 'ApiTest',
  setup() {
    const loading = ref(false)
    const postsResult = ref(null)
    const categoriesResult = ref(null)
    const directResult = ref(null)
    const error = ref(null)

    const testBlogPosts = async () => {
      loading.value = true
      error.value = null
      postsResult.value = null
      
      try {
        console.log('Testing blog posts API...')
        const response = await api.getBlogPosts()
        console.log('Blog posts response:', response)
        postsResult.value = response.data
      } catch (err) {
        console.error('Blog posts error:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const testBlogCategories = async () => {
      loading.value = true
      error.value = null
      categoriesResult.value = null
      
      try {
        console.log('Testing blog categories API...')
        const response = await api.getBlogCategories()
        console.log('Blog categories response:', response)
        categoriesResult.value = response.data
      } catch (err) {
        console.error('Blog categories error:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const testDirectApi = async () => {
      loading.value = true
      error.value = null
      directResult.value = null
      
      try {
        console.log('Testing direct API call...')
        const response = await fetch('http://127.0.0.1:8000/api/blog/posts/')
        const data = await response.json()
        console.log('Direct API response:', data)
        directResult.value = data
      } catch (err) {
        console.error('Direct API error:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      postsResult,
      categoriesResult,
      directResult,
      error,
      testBlogPosts,
      testBlogCategories,
      testDirectApi
    }
  }
}
</script>

<style scoped>
.api-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.test-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

pre {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>