const STATUS_AWAITING_SUPPLEMENT = 4
const STATUS_RECEIVED = 7
const notify = document.getElementById("id_notify_author")
const statusChange = document.getElementById("id_status")
const reason = document.getElementById("id_reason")

statusChange.addEventListener("change", (e) => {
  notify.checked = false
  notify.closest(".form-group").style.display = "flex"

  if (parseInt(e.target.value) === STATUS_AWAITING_SUPPLEMENT) {
    notify.checked = true
  }

  else if (parseInt(e.target.value) === STATUS_RECEIVED) {
    notify.closest(".form-group").style.display = "none"
  }

  notify.dispatchEvent(new Event("change"))
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
