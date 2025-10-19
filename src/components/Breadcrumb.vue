<!-- src/components/Breadcrumb.vue -->
<template>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li v-for="(item, index) in items" :key="index" class="breadcrumb-item">
        <router-link 
          v-if="item.to && index < items.length - 1" 
          :to="item.to" 
          class="breadcrumb-link"
        >
          {{ item.text }}
        </router-link>
        <span v-else class="breadcrumb-current">
          {{ item.text }}
        </span>
        <span v-if="index < items.length - 1" class="breadcrumb-separator">></span>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  name: 'Breadcrumb',
  props: {
    items: {
      type: Array,
      required: true,
      validator: (items) => {
        return items.every(item => 
          typeof item === 'object' && 
          typeof item.text === 'string' &&
          (item.to === undefined || typeof item.to === 'string')
        )
      }
    }
  }
}
</script>

<style scoped>
.breadcrumb {
  margin-bottom: 20px;
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.9em;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: #2196f3;
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.breadcrumb-link:hover {
  background-color: #e3f2fd;
}

.breadcrumb-current {
  color: #666;
  padding: 4px 8px;
  font-weight: 500;
}

.breadcrumb-separator {
  color: #999;
  margin: 0 4px;
}

@media (max-width: 480px) {
  .breadcrumb-list {
    font-size: 0.8em;
  }
  
  .breadcrumb-link,
  .breadcrumb-current {
    padding: 2px 4px;
  }
}
</style>
