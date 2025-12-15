import { toJalaali } from 'jalaali-js'

export const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    // Use jalaali-js for proper Jalali calendar conversion
    const jalali = toJalaali(date)
    
    const months = [
      'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
      'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    
    const monthName = months[jalali.jm - 1]
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${jalali.jd} ${monthName} ${jalali.jy}، ${hours}:${minutes}`
  } catch (error) {
    return dateString
  }
}

export const formatDateShort = (dateString: string | null | undefined): string => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    const jalali = toJalaali(date)
    
    const months = [
      'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
      'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    
    const monthName = months[jalali.jm - 1]
    return `${jalali.jd} ${monthName} ${jalali.jy}`
  } catch (error) {
    return dateString
  }
}

