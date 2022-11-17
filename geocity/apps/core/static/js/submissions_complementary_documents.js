
let setUpDocumentManagement = function(){

  let container = document.getElementById('complementary-documents')
  let documents = document.getElementsByClassName('complementary-document')
  let nbDocuments = documents.length;

  if (nbDocuments == 0) {
    return;
  }

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

    setEventOnTemplateSelect(nbDocuments-1)
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

  function setEventOnTemplateSelect(id){
    let reportInput  = document.getElementById(`id_form-${id}-generate_from_model`);
    let docInput = document.getElementById(`id_form-${id}-document`);
    let docTypeInput = document.getElementById(`id_form-${id}-document_type`);
    let childDocTypeInputs = document.querySelectorAll(`[id^="id_form-${id}-parent_"]`);
    let previewBtn = document.getElementById(`id_form-${id}-print_preview`);

    docInput.disabled=false;
    docTypeInput.disabled=false;
    previewBtn.disabled=true;

    reportInput.addEventListener('change', (e) => {
      if (e.target.value == "") {
        docInput.disabled=false;
        previewBtn.disabled=true;
        docTypeInput.disabled=false;
        for(let childDocTypeInput of childDocTypeInputs)
          childDocTypeInput.disabled=false;
      } else {
        docInput.disabled=true;
        previewBtn.disabled=false;
        docTypeInput.disabled=true;
        for(let childDocTypeInput of childDocTypeInputs)
          childDocTypeInput.disabled=true;
        previewBtn.onclick = (event) => {
          let [wot_pk, report_pk, doc_type_pk] = reportInput.value.split("/");
          let url = previewBtn.dataset.linkTpl.replace("888888888", wot_pk)
                                              .replace("999999999", report_pk);
          window.open(url, "_blank");
          return false;
        };
      }
    });

    docInput.addEventListener('change', (e) => {
      if (e.target.value == "") {
        reportInput.disabled=false;
      } else {
        reportInput.disabled=true;
      }
    });
  }

  setEventOnTemplateSelect(0)
}

setUpDocumentManagement();
