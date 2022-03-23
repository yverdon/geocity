let container = document.getElementById('complementary-documents')
let documents = document.getElementsByClassName('complementary-document')
let nbDocuments = documents.length;

document.getElementById('add-document').addEventListener('click', (e) => {
  e.preventDefault()
  // clone the form
  let clone = documents[0].cloneNode(true)
  // regex to find all instances of the form number
  let regex = RegExp(`form-(\\d){1}-`,'g')

  // increase the number of documents
  ++nbDocuments
  // change the "form number"
  clone.innerHTML = clone.innerHTML.replace(regex, `form-${nbDocuments-1}-`)
  container.appendChild(document.createElement('hr'))
  container.appendChild(clone)
})

