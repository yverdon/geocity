const COMPLEMENTARY_INFO = 4
const notify = document.getElementById('id_notify_author')
const statusChange = document.getElementById('id_status')
const reason = document.getElementById("id_reason")

statusChange.addEventListener('change', (e) => {
  if (parseInt(e.target.value) === COMPLEMENTARY_INFO) {
    notify.checked = true
    notify.dispatchEvent(new Event("change"))
  }
})

notify.addEventListener('change', (e) => {
  changeReasonDisplay(e.target.checked)
})

changeReasonDisplay()

if (parseInt(statusChange.value) === COMPLEMENTARY_INFO) {
  statusChange.dispatchEvent(new Event("change"))
}

function changeReasonDisplay(display = false) {
  reason.closest('.form-group').style.display = display ? 'flex' : 'none'
}
