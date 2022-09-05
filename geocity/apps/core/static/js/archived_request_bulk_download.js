const form = document.getElementById('download-form')
form.addEventListener('submit', () => {
  const requests = document.querySelectorAll('.permit-request:checked')
  if (!requests.length) return

  for (const id of [...requests].map((request) => request.value)) {
    let input = document.createElement("input")
    input.setAttribute("type", "hidden")
    input.setAttribute("name", "to_download")
    input.setAttribute("value", id)
    form.appendChild(input)
  }
})
