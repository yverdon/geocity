let container = document.getElementById('complementary-documents')
let documents = document.getElementsByClassName('complementary-document')
let nbDocuments = documents.length;

hideChildrenDocumentTypes(document)
displayChildSelect(documents[0])

document.getElementById('add-document').addEventListener('click', (e) => {
  e.preventDefault()

  // display the remove button
  document.getElementById('remove-document').removeAttribute('hidden')
  // increase the number of documents
  ++nbDocuments

  // regex to find all instances of the form number
  const regex = RegExp(`form-(\\d){1}`,'g')

  // clone the form
  let clone = documents[0].cloneNode(true)
  clone.id = `document-${nbDocuments-1}`
  clone.innerHTML = clone.innerHTML.replace(regex, `form-${nbDocuments-1}`)

  // change the "form number"
  document.getElementById("id_form-TOTAL_FORMS").value = nbDocuments

  hideChildrenDocumentTypes(clone)

  clone.prepend(document.createElement('hr'))
  container.appendChild(clone)

  displayChildSelect(clone)
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

function displayChildSelect(parent) {
  const regex = RegExp(`form-(\\d){1}`,'g')
  const prefix = parent.innerHTML.match(regex)[0]

  const documentType = document.getElementById(`id_${prefix}-document_type`)
  documentType.addEventListener('change', (e) => {
    for (const child of parent.getElementsByClassName('child-type')) {
      child.setAttribute('hidden', '')
      child.closest('.form-group').style.display = 'none'
    }

    const targetChild = document.getElementById(`id_${prefix}-parent_${e.target.value}`)
    if (targetChild) {
      targetChild.removeAttribute('hidden')
      targetChild.closest('.form-group').style.display = 'flex'
    }
  })

  if (documentType.value) {
    documentType.dispatchEvent(new Event('change'))
  }
}

function hideChildrenDocumentTypes(parent) {
  for (const child of parent.getElementsByClassName('child-type')) {
    child.closest('.form-group').style.display = 'none'
  }
}
