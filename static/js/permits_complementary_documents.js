let container = document.getElementById('complementary-documents')
let documents = document.getElementsByClassName('complementary-document')
let nbDocuments = documents.length;

document.getElementById('add-document').addEventListener('click', (e) => {
  e.preventDefault()

  // display the remove button
  document.getElementById('remove-document').removeAttribute('hidden')
  // increase the number of documents
  ++nbDocuments

  // regex to find all instances of the form number
  let regex = RegExp(`form-(\\d){1}-`,'g')

  // clone the form
  let clone = documents[0].cloneNode(true)
  clone.id = `document-${nbDocuments-1}`
  clone.innerHTML = clone.innerHTML.replace(regex, `form-${nbDocuments-1}-`)

  // change the "form number"
  document.getElementById("id_form-TOTAL_FORMS").value = nbDocuments

  clone.prepend(document.createElement('hr'))
  container.appendChild(clone)
})

document.getElementById('remove-document').addEventListener('click', (e) => {
  e.preventDefault()

  // we don't want to delete the last form
  if (nbDocuments === 1) {
    return
  }

  // decrease the number of documents
  --nbDocuments

  // we don't need the remove button anymore
  if (nbDocuments === 1) {
    e.target.setAttribute('hidden', '')
  }

  // update the number of total forms
  document.getElementById("id_form-TOTAL_FORMS").value = nbDocuments

  // remove the last form
  let target = [...documents].pop()
  target.remove()
})

document.getElementById('id_form-0-document_type').addEventListener('change', (e) => {
  for (const child of document.getElementsByClassName('child-type')) {
    child.setAttribute('hidden', '')
    child.closest('.form-group').style.display = 'none'
  }

  // get the "form id" $
  // e.g. id_form-0
  const formID = e.target.id.split('document_type')[0]
  const targetChild = document.getElementById(`${formID}parent_${e.target.value}`)
  if (targetChild) {
    targetChild.removeAttribute('hidden')
    targetChild.closest('.form-group').style.display = 'flex'
  }
})

for (const child of document.getElementsByClassName('child-type')) {
  child.closest('.form-group').style.display = 'none'
}
