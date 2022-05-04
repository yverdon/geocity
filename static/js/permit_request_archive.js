const form = document.getElementById('archive-form')
form.addEventListener('submit', async (e) => {
  e.preventDefault()
  const requests = document.querySelectorAll('.permit-request:checked')
  if (!requests.length) return

  document.getElementById('archive-in_progress').classList.remove('display-none')

  const data = new FormData();
  for (const id of [...requests].map((request) => { return request.value })) {
    data.append('to_archive[]', id)
  }
  data.append('csrfmiddlewaretoken', form.querySelector('input[name=csrfmiddlewaretoken]').value)
  data.append('action', 'archive-requests')
  const response = await fetch(form.action, {
    method: 'post',
    mode: 'same-origin',
    body: data,
  })

  if (response.status === 403) {
    const data = await response.json()
    let error = document.createElement("div")
    error.classList.add("alert", "alert-danger")
    error.innerText = data.message
    document.getElementById("archive-in_progress").appendChild(error)
  }
})
