const STATUS_AWAITING_SUPPLEMENT = 4
const STATUS_RECEIVED = 7
const notify = document.getElementById("id_notify_author")
const statusChange = document.getElementById("id_status")
const reason = document.getElementById("id_reason")

statusChange.addEventListener("change", (e) => {
  if (parseInt(e.target.value) === STATUS_AWAITING_SUPPLEMENT) {
    notify.checked = true
    notify.dispatchEvent(new Event("change"))
  }
  else if (parseInt(e.target.value) === STATUS_RECEIVED) {
    notify.checked = false
    notify.dispatchEvent(new Event("change"))
    notify.closest(".form-group").style.display = "none"
  }
  else {
    notify.closest(".form-group").style.display = "flex"
  }
})

notify.addEventListener("change", (e) => {
  changeReasonDisplay(e.target.checked)
})

changeReasonDisplay()

if (parseInt(statusChange.value) === STATUS_AWAITING_SUPPLEMENT ||
  parseInt(statusChange.value) === STATUS_RECEIVED) {
  statusChange.dispatchEvent(new Event("change"))
}

function changeReasonDisplay(display = false) {
  reason.closest(".form-group").style.display = display ? "flex" : "none"
}
