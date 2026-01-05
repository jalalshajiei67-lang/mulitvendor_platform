<template>
  <v-card>
    <v-card-title>ثبت پیشنهاد</v-card-title>
    <v-card-text>
      <v-form ref="formRef" v-model="valid">
        <v-text-field
          v-model="amount"
          label="مبلغ پیشنهاد (تومان)"
          type="number"
          :rules="amountRules"
          :disabled="loading || !canBid"
          :hint="hintText"
          persistent-hint
          variant="outlined"
          prepend-inner-icon="mdi-currency-usd"
        ></v-text-field>

        <div v-if="previousBid" class="mb-4">
          <v-alert type="info" variant="tonal" density="compact">
            پیشنهاد قبلی شما: {{ formatPrice(previousBid) }} تومان
          </v-alert>
        </div>

        <div v-if="minimumDecrement" class="mb-4">
          <v-alert type="warning" variant="tonal" density="compact">
            باید حداقل {{ formatPrice(minimumDecrement) }} تومان از پیشنهاد قبلی کمتر باشد
          </v-alert>
        </div>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        :loading="loading"
        :disabled="!canBid || !valid"
        @click="submitBid"
      >
        ثبت پیشنهاد
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useToast } from '~/composables/useToast'

interface Props {
  startingPrice: number | string
  previousBid?: number | string | null
  minimumDecrement?: number | string
  canBid?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  canBid: true
})

const emit = defineEmits<{
  submit: [amount: number]
}>()

const { showToast } = useToast()
const formRef = ref()
const valid = ref(false)
const loading = ref(false)
const amount = ref('')

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(num)
}

const hintText = computed(() => {
  if (props.previousBid) {
    return `مبلغ باید کمتر از ${formatPrice(props.previousBid)} تومان باشد`
  }
  return `مبلغ باید کمتر از ${formatPrice(props.startingPrice)} تومان باشد`
})

const amountRules = computed(() => {
  const rules: Array<(v: string) => boolean | string> = [
    (v: string) => !!v || 'لطفا مبلغ را وارد کنید',
    (v: string) => {
      const num = parseFloat(v)
      if (isNaN(num) || num <= 0) {
        return 'مبلغ باید بیشتر از صفر باشد'
      }
      
      const startingPriceNum = typeof props.startingPrice === 'string' 
        ? parseFloat(props.startingPrice) 
        : props.startingPrice
      
      if (num >= startingPriceNum) {
        return `مبلغ باید کمتر از ${formatPrice(startingPriceNum)} تومان باشد`
      }
      
      if (props.previousBid) {
        const previousBidNum = typeof props.previousBid === 'string'
          ? parseFloat(props.previousBid)
          : props.previousBid
        if (num >= previousBidNum) {
          return `مبلغ باید کمتر از ${formatPrice(previousBidNum)} تومان باشد`
        }
        
        if (props.minimumDecrement) {
          const minDec = typeof props.minimumDecrement === 'string'
            ? parseFloat(props.minimumDecrement)
            : props.minimumDecrement
          const decrement = previousBidNum - num
          if (decrement < minDec) {
            return `باید حداقل ${formatPrice(minDec)} تومان از پیشنهاد قبلی کمتر باشد`
          }
        }
      } else if (props.minimumDecrement) {
        const minDec = typeof props.minimumDecrement === 'string'
          ? parseFloat(props.minimumDecrement)
          : props.minimumDecrement
        const startingPriceNum = typeof props.startingPrice === 'string'
          ? parseFloat(props.startingPrice)
          : props.startingPrice
        const decrement = startingPriceNum - num
        if (decrement < minDec) {
          return `باید حداقل ${formatPrice(minDec)} تومان از قیمت شروع کمتر باشد`
        }
      }
      
      return true
    }
  ]
  return rules
})

const submitBid = async () => {
  const { valid: isValid } = await formRef.value.validate()
  if (!isValid) {
    return
  }
  
  const amountNum = parseFloat(amount.value)
  if (isNaN(amountNum) || amountNum <= 0) {
    showToast('لطفا مبلغ معتبری وارد کنید', 'error')
    return
  }
  
  loading.value = true
  try {
    emit('submit', amountNum)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Add any custom styles if needed */
</style>




