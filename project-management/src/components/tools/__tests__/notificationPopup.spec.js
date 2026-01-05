import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import NotificationPopup from '../notificationPopup.vue'

const factory = (props = {}) => {
  return mount(NotificationPopup, {
    props: {
      message: 'Hello world',
      visible: true,
      ...props
    }
  })
}

describe('NotificationPopup', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.runOnlyPendingTimers()
    vi.useRealTimers()
  })

  it('auto-closes after given duration (clamped at 3000ms)', async () => {
    const wrapper = factory({ duration: 10000 }) // should clamp to 3000ms

    // Fast-forward just before clamp duration
    vi.advanceTimersByTime(2990)
    expect(wrapper.emitted('close')).toBeFalsy()

    // Finish the countdown
    vi.advanceTimersByTime(20)
    const closeEmits = wrapper.emitted('close') || []
    expect(closeEmits.length).toBe(1)
  })

  it('emits close when overlay is clicked', async () => {
    const wrapper = factory({ duration: 500 })
    await wrapper.find('.notification-overlay').trigger('click')
    const closeEmits = wrapper.emitted('close') || []
    expect(closeEmits.length).toBe(1)
  })

  it('does not close when clicking inside popup (event stop)', async () => {
    const wrapper = factory({ duration: 500 })
    await wrapper.find('.notification-popup').trigger('click')
    expect(wrapper.emitted('close')).toBeFalsy()
  })

  it('emits close when clicking the close button', async () => {
    const wrapper = factory({ duration: 500 })
    await wrapper.find('.notification-close').trigger('click')
    const closeEmits = wrapper.emitted('close') || []
    expect(closeEmits.length).toBe(1)
  })

  it('restarts progress when visible toggles back to true', async () => {
    const wrapper = factory({ duration: 500 })

    // let some time pass
    vi.advanceTimersByTime(200)
    const progressAfter = wrapper.vm.progress
    expect(progressAfter).toBeLessThan(100)

    // hide then show again
    await wrapper.setProps({ visible: false })
    await wrapper.setProps({ visible: true })

    // progress should reset to 100 on restart
    expect(wrapper.vm.progress).toBe(100)
  })
})
