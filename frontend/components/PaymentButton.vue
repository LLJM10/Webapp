<template>
  <button :class="['btn', primary ? 'primary' : 'ghost']" @click="onPay" :disabled="loading">
    <span v-if="!loading">{{ label }}</span>
    <span v-else>Bitte warten…</span>
  </button>
  <div v-if="error" class="muted" style="margin-top:8px;color:#b91c1c">{{ error }}</div>
</template>

<script setup>
import { ref } from 'vue'
import { usePayPal } from '~/composables/usePayPal'

const props = defineProps({
  amount: { type: [Number, String], required: true },
  currency: { type: String, default: 'EUR' },
  label: { type: String, default: 'Jetzt investieren' },
  primary: { type: Boolean, default: true },
})

const loading = ref(false)
const error = ref(null)
const { createOrder } = usePayPal()

async function onPay() {
  loading.value = true
  error.value = null
  try {
    const returnUrl = typeof window !== 'undefined' ? window.location.href : ''
    const cancelUrl = returnUrl

    const resp = await createOrder({ amount: props.amount, currency: props.currency, returnUrl, cancelUrl })

    const approval = resp.approval_url || resp.approvalUrl || resp.data?.approval_url
    if (approval) {
      window.location.href = approval
    } else {
      error.value = 'Keine Weiterleitungs-URL erhalten.'
      console.error('createOrder response', resp)
    }
  } catch (e) {
    console.error(e)
    error.value = e.message || 'Fehler beim Erstellen der Bestellung.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.btn { padding: 8px 12px; border-radius:6px; cursor:pointer }
.primary { background:#0ea5ff; color:white; border: none }
.ghost { background:transparent; border:1px solid #e5e7eb }
</style>
