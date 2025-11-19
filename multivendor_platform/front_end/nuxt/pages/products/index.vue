<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

// Redirect to homepage with query params preserved
const route = useRoute()

// Preserve query parameters when redirecting
const query = { ...route.query }
navigateTo({
  path: '/',
  query
}, { replace: true })
</script>

