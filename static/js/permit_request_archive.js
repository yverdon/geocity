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

  if (response.status === 403 || response.status === 500) {
    const data = await response.json()
    displayAlert(data.message, "danger")
    document.getElementById('archive-in_progress').firstElementChild.classList.add('display-none')
  }

  if (response.status === 200) {
    const data = await response.json()
    displayAlert(data.message, "success")
  }
})

function displayAlert(message, type) {
    document.getElementById('archive-in_progress').firstElementChild.classList.add('display-none')
    let container = document.createElement("div")
    container.classList.add("alert", `alert-${type}`)
    container.innerText = message
    document.getElementById("archive-in_progress").appendChild(container)
}
