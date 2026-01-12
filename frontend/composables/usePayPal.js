/**
 * PayPal-Zahlungen über Backend
 * createOrder: Erstellt PayPal-Order und gibt approval_url zurück
 *captureOrder: Schließt Zahlung nach User-Bestätigung ab
 */
import { useRuntimeConfig } from '#app'

export function usePayPal() {
  const config = useRuntimeConfig()
  const apiBase = config.public?.apiBase || ''

  async function createOrder({ amount, currency = 'EUR', returnUrl = '', cancelUrl = '' } = {}) {
    if (!amount) throw new Error('amount is required')

    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null

    const res = await $fetch(`${apiBase}/payments/create-order/`, {
      method: 'POST',
      body: { amount: String(amount), currency, return_url: returnUrl, cancel_url: cancelUrl },
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })

    return res
  }

  async function captureOrder(orderId) {
    if (!orderId) throw new Error('orderId is required')
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null

    const res = await $fetch(`${apiBase}/payments/capture-order/`, {
      method: 'POST',
      body: { order_id: orderId },
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })

    return res
  }

  return { createOrder, captureOrder }
}
