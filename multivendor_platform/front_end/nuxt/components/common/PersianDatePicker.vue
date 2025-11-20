<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    location="bottom"
    transition="scale-transition"
  >
    <template v-slot:activator="{ props }">
      <v-text-field
        v-bind="props"
        :model-value="displayValue"
        :label="label"
        :prepend-icon="prependIcon"
        :variant="variant"
        :rules="rules"
        readonly
        :placeholder="placeholder || 'تاریخ را انتخاب کنید'"
        clearable
        @click:clear="clearDate"
      ></v-text-field>
    </template>
    <v-card min-width="300">
      <v-card-title class="d-flex align-center justify-space-between pa-3">
        <span class="text-h6">انتخاب تاریخ</span>
        <v-btn icon="mdi-close" variant="text" size="small" @click="menu = false"></v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-0">
        <div class="persian-calendar pa-4">
          <!-- Year and Month Selector -->
          <div class="d-flex align-center justify-space-between mb-4">
            <v-btn
              icon="mdi-chevron-right"
              variant="text"
              size="small"
              @click="previousMonth"
            ></v-btn>
            <div class="text-center">
              <v-select
                v-model="selectedYear"
                :items="years"
                density="compact"
                variant="outlined"
                hide-details
                class="year-select"
                @update:model-value="updateCalendar"
              ></v-select>
              <v-select
                v-model="selectedMonth"
                :items="months"
                density="compact"
                variant="outlined"
                hide-details
                class="month-select mt-2"
                @update:model-value="updateCalendar"
              ></v-select>
            </div>
            <v-btn
              icon="mdi-chevron-left"
              variant="text"
              size="small"
              @click="nextMonth"
            ></v-btn>
          </div>

          <!-- Calendar Grid -->
          <div class="calendar-grid">
            <!-- Weekday Headers -->
            <div class="calendar-header">
              <div
                v-for="day in weekDays"
                :key="day"
                class="calendar-header-cell"
              >
                {{ day }}
              </div>
            </div>

            <!-- Calendar Days -->
            <div class="calendar-body">
              <div
                v-for="(week, weekIndex) in calendarDays"
                :key="weekIndex"
                class="calendar-week"
              >
                <div
                  v-for="day in week"
                  :key="day.key"
                  class="calendar-day"
                  :class="{
                    'other-month': day.otherMonth,
                    'today': day.isToday,
                    'selected': day.isSelected
                  }"
                  @click="selectDate(day)"
                >
                  {{ day.day }}
                </div>
              </div>
            </div>
          </div>

          <!-- Today Button -->
          <div class="text-center mt-4">
            <v-btn
              color="primary"
              variant="text"
              size="small"
              @click="selectToday"
            >
              امروز
            </v-btn>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="confirmDate">تأیید</v-btn>
        <v-btn variant="text" @click="menu = false">انصراف</v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { toJalaali, toGregorian, isValidJalaaliDate, jalaaliMonthLength } from 'jalaali-js'

interface Props {
  modelValue?: string | null
  label?: string
  prependIcon?: string
  variant?: string
  rules?: any[]
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  label: 'تاریخ',
  prependIcon: 'mdi-calendar',
  variant: 'outlined',
  rules: () => [],
  placeholder: 'تاریخ را انتخاب کنید'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | null]
}>()

const menu = ref(false)
const selectedYear = ref<number>(1403)
const selectedMonth = ref<number>(1)
const selectedDay = ref<number | null>(null)
const tempSelectedDate = ref<{ year: number; month: number; day: number } | null>(null)

const weekDays = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']

const months = [
  { title: 'فروردین', value: 1 },
  { title: 'اردیبهشت', value: 2 },
  { title: 'خرداد', value: 3 },
  { title: 'تیر', value: 4 },
  { title: 'مرداد', value: 5 },
  { title: 'شهریور', value: 6 },
  { title: 'مهر', value: 7 },
  { title: 'آبان', value: 8 },
  { title: 'آذر', value: 9 },
  { title: 'دی', value: 10 },
  { title: 'بهمن', value: 11 },
  { title: 'اسفند', value: 12 }
]

const years = computed(() => {
  const currentYear = toJalaali(new Date()).jy
  const yearList = []
  for (let i = currentYear - 10; i <= currentYear + 10; i++) {
    yearList.push({ title: i.toString(), value: i })
  }
  return yearList
})

const displayValue = computed(() => {
  if (!props.modelValue) return ''
  
  try {
    // Parse the date (assuming it's in YYYY-MM-DD format)
    const dateParts = props.modelValue.split('-')
    if (dateParts.length === 3) {
      const gregorianDate = new Date(
        parseInt(dateParts[0]),
        parseInt(dateParts[1]) - 1,
        parseInt(dateParts[2])
      )
      const jalali = toJalaali(gregorianDate)
      return `${jalali.jy}/${String(jalali.jm).padStart(2, '0')}/${String(jalali.jd).padStart(2, '0')}`
    }
  } catch (e) {
    console.error('Error parsing date:', e)
  }
  
  return props.modelValue
})

const calendarDays = computed(() => {
  const days: any[] = []
  const monthLength = jalaaliMonthLength(selectedYear.value, selectedMonth.value)
  
  // Get first day of month
  const firstDayGregorian = toGregorian(selectedYear.value, selectedMonth.value, 1)
  const firstDayDate = new Date(firstDayGregorian.gy, firstDayGregorian.gm - 1, firstDayGregorian.gd)
  const firstDayOfWeek = firstDayDate.getDay() // 0 = Sunday, 6 = Saturday
  
  // Convert to Persian week (Saturday = 0, Friday = 6)
  let persianFirstDay = (firstDayOfWeek + 1) % 7
  
  // Add previous month days
  const prevMonth = selectedMonth.value === 1 ? 12 : selectedMonth.value - 1
  const prevYear = selectedMonth.value === 1 ? selectedYear.value - 1 : selectedYear.value
  const prevMonthLength = jalaaliMonthLength(prevYear, prevMonth)
  
  for (let i = persianFirstDay - 1; i >= 0; i--) {
    const day = prevMonthLength - i
    days.push({
      day,
      month: prevMonth,
      year: prevYear,
      otherMonth: true,
      isToday: false,
      isSelected: false,
      key: `${prevYear}-${prevMonth}-${day}`
    })
  }
  
  // Add current month days
  const today = toJalaali(new Date())
  for (let day = 1; day <= monthLength; day++) {
    const isToday =
      day === today.jd &&
      selectedMonth.value === today.jm &&
      selectedYear.value === today.jy
    
    const isSelected =
      tempSelectedDate.value &&
      day === tempSelectedDate.value.day &&
      selectedMonth.value === tempSelectedDate.value.month &&
      selectedYear.value === tempSelectedDate.value.year
    
    days.push({
      day,
      month: selectedMonth.value,
      year: selectedYear.value,
      otherMonth: false,
      isToday,
      isSelected,
      key: `${selectedYear.value}-${selectedMonth.value}-${day}`
    })
  }
  
  // Add next month days to fill the grid
  const remainingDays = 42 - days.length // 6 weeks * 7 days
  const nextMonth = selectedMonth.value === 12 ? 1 : selectedMonth.value + 1
  const nextYear = selectedMonth.value === 12 ? selectedYear.value + 1 : selectedYear.value
  
  for (let day = 1; day <= remainingDays; day++) {
    days.push({
      day,
      month: nextMonth,
      year: nextYear,
      otherMonth: true,
      isToday: false,
      isSelected: false,
      key: `${nextYear}-${nextMonth}-${day}`
    })
  }
  
  // Group into weeks
  const weeks: any[][] = []
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7))
  }
  
  return weeks
})

const initializeFromModelValue = () => {
  if (props.modelValue) {
    try {
      const dateParts = props.modelValue.split('-')
      if (dateParts.length === 3) {
        const gregorianDate = new Date(
          parseInt(dateParts[0]),
          parseInt(dateParts[1]) - 1,
          parseInt(dateParts[2])
        )
        const jalali = toJalaali(gregorianDate)
        selectedYear.value = jalali.jy
        selectedMonth.value = jalali.jm
        selectedDay.value = jalali.jd
        tempSelectedDate.value = { year: jalali.jy, month: jalali.jm, day: jalali.jd }
      }
    } catch (e) {
      console.error('Error initializing date:', e)
    }
  } else {
    const today = toJalaali(new Date())
    selectedYear.value = today.jy
    selectedMonth.value = today.jm
    selectedDay.value = null
    tempSelectedDate.value = null
  }
}

const previousMonth = () => {
  if (selectedMonth.value === 1) {
    selectedMonth.value = 12
    selectedYear.value--
  } else {
    selectedMonth.value--
  }
}

const nextMonth = () => {
  if (selectedMonth.value === 12) {
    selectedMonth.value = 1
    selectedYear.value++
  } else {
    selectedMonth.value++
  }
}

const updateCalendar = () => {
  // Calendar will update automatically via computed property
}

const selectDate = (day: any) => {
  // Navigate to the month if clicking on a day from another month
  if (day.otherMonth) {
    selectedYear.value = day.year
    selectedMonth.value = day.month
    // Wait for next tick to ensure calendar updates, then select the date
    setTimeout(() => {
      tempSelectedDate.value = {
        year: day.year,
        month: day.month,
        day: day.day
      }
    }, 0)
  } else {
    tempSelectedDate.value = {
      year: day.year,
      month: day.month,
      day: day.day
    }
  }
}

const selectToday = () => {
  const today = toJalaali(new Date())
  selectedYear.value = today.jy
  selectedMonth.value = today.jm
  tempSelectedDate.value = {
    year: today.jy,
    month: today.jm,
    day: today.jd
  }
}

const confirmDate = () => {
  if (tempSelectedDate.value) {
    const gregorian = toGregorian(
      tempSelectedDate.value.year,
      tempSelectedDate.value.month,
      tempSelectedDate.value.day
    )
    const dateString = `${gregorian.gy}-${String(gregorian.gm).padStart(2, '0')}-${String(gregorian.gd).padStart(2, '0')}`
    emit('update:modelValue', dateString)
    menu.value = false
  }
}

const clearDate = () => {
  emit('update:modelValue', null)
  tempSelectedDate.value = null
  selectedDay.value = null
}

watch(() => props.modelValue, () => {
  if (menu.value) {
    initializeFromModelValue()
  }
})

watch(menu, (isOpen) => {
  if (isOpen) {
    initializeFromModelValue()
  }
})

onMounted(() => {
  initializeFromModelValue()
})
</script>

<style scoped>
.persian-calendar {
  direction: rtl;
}

.calendar-grid {
  width: 100%;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.calendar-header-cell {
  text-align: center;
  font-weight: bold;
  font-size: 0.875rem;
  padding: 8px 4px;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.calendar-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.875rem;
  transition: all 0.2s;
  user-select: none;
}

.calendar-day:hover:not(.other-month) {
  background-color: rgba(var(--v-theme-primary), 0.1);
}

.calendar-day.other-month {
  color: rgba(var(--v-theme-on-surface), 0.3);
  cursor: default;
}

.calendar-day.today {
  background-color: rgba(var(--v-theme-primary), 0.2);
  font-weight: bold;
}

.calendar-day.selected {
  background-color: rgb(var(--v-theme-primary));
  color: rgb(var(--v-theme-on-primary));
  font-weight: bold;
}

.year-select,
.month-select {
  max-width: 120px;
  margin: 0 auto;
}

.v-select :deep(.v-field__input) {
  text-align: center;
}
</style>

