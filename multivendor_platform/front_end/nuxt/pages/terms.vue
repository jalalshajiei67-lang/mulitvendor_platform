<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <div class="text-h4 font-weight-bold mb-6">قوانین و مقررات</div>
        
        <v-card>
          <v-card-text>
            <div class="content-section">
              <h2 class="text-h5 font-weight-bold mb-4">۱. پذیرش قوانین</h2>
              <p class="text-body-1 mb-6">
                با استفاده از خدمات پلتفرم ایندکسو، شما قوانین و مقررات زیر را می‌پذیرید. در صورت عدم پذیرش، لطفاً از خدمات ما استفاده نکنید.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۲. ثبت‌نام و حساب کاربری</h2>
              <p class="text-body-1 mb-6">
                برای استفاده از برخی خدمات، باید یک حساب کاربری ایجاد کنید. شما مسئول حفظ امنیت حساب کاربری خود و تمام فعالیت‌هایی هستید که تحت حساب شما انجام می‌شود.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۳. استفاده مجاز</h2>
              <p class="text-body-1 mb-6">
                شما موافقت می‌کنید که از پلتفرم فقط برای اهداف قانونی و مطابق با این قوانین استفاده کنید. هرگونه سوءاستفاده از خدمات ممنوع است.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۴. محتوای کاربران</h2>
              <p class="text-body-1 mb-6">
                شما مسئول محتوایی هستید که در پلتفرم منتشر می‌کنید. ایندکسو حق دارد محتوای نامناسب را حذف کند.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۵. حقوق مالکیت معنوی</h2>
              <p class="text-body-1 mb-6">
                تمام محتوا، طراحی و نرم‌افزار پلتفرم متعلق به ایندکسو است و تحت حمایت قوانین مالکیت معنوی می‌باشد.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۶. خاتمه حساب</h2>
              <p class="text-body-1 mb-6">
                ایندکسو حق دارد در صورت نقض قوانین، بدون اطلاع قبلی، حساب کاربری شما را تعلیق یا حذف کند.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۷. تغییرات در قوانین</h2>
              <p class="text-body-1 mb-6">
                ایندکسو حق دارد این قوانین را در هر زمان تغییر دهد. ادامه استفاده از خدمات پس از تغییرات، به معنی پذیرش قوانین جدید است.
              </p>

              <h2 class="text-h5 font-weight-bold mb-4">۸. تماس با ما</h2>
              <p class="text-body-1 mb-6">
                در صورت داشتن سؤال درباره این قوانین، لطفاً از طریق صفحه تماس با ما با ما در ارتباط باشید.
              </p>
            </div>
          </v-card-text>
        </v-card>

        <div class="text-caption text-medium-emphasis mt-4 text-center">
          آخرین به‌روزرسانی: {{ lastUpdated }}
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
useSeoMeta({
  title: 'قوانین و مقررات',
  description: 'قوانین و مقررات استفاده از پلتفرم ایندکسو'
})

const lastUpdated = new Date().toLocaleDateString('fa-IR')
</script>

<style scoped>
.content-section {
  line-height: 1.8;
}

.content-section h2 {
  margin-top: 2rem;
}

.content-section h2:first-child {
  margin-top: 0;
}
</style>

