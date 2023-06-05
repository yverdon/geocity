(function() {
  class GlobalSearchForm {
    constructor(formElem) {
      this.searchFormElem = formElem;
      this.resultsElem = formElem.querySelector('[data-role=search-results]');
      this.searchInputElem = formElem.querySelector('[data-role=search-input]');
      this.resultsListElem = this._createResultsListElem();
      this.debounceTimer = null;
      this.highlightedResultIndex = null;
      this.results = [];

      this._addEventListeners();
    }

    hideSuggestions() {
      this.resultsElem.classList.add('d-none');
    }

    showSuggestions() {
      this.resultsElem.classList.remove('d-none');
    }

    _createResultsListElem() {
      const resultsListElem = document.createElement("ul");
      resultsListElem.setAttribute("class", "list search-results");

      return resultsListElem;
    }

    _addEventListeners() {
      this._addSearchEventListeners();
      this._addKeyUpEventListener();
      this._addClickOutsideEventListener();

      // Show suggestions after page refresh if search input is populated
      if (this.searchInputElem.value !== '') {
        this._search(this.searchInputElem.value);
        this.searchInputElem.focus();

        // Position the caret at the end of the input
        this.searchInputElem.setSelectionRange(
          this.searchInputElem.value.length,
          this.searchInputElem.value.length
        );
      }

      // Show suggestions after closing the suggestions and then clicking again
      // in the search input
      this.searchInputElem.addEventListener('focus', (e) => {
        if (this.results.length > 0) {
          this.showSuggestions();
        }
      })
    }

    _addClickOutsideEventListener() {
      // We can’t just use a blur event on the search input to hide it because
      // it would hide it when trying to click on a result
      document.addEventListener('click', (e) => {
        let parent = e.target;
        let clickInsideSearchForm = false;

        while (parent) {
          if (parent == this.searchFormElem) {
            clickInsideSearchForm = true;
            break;
          }

          parent = parent.parentElement;
        }

        if (!clickInsideSearchForm) {
          this.hideSuggestions();
        }
      });
    }

    _addHoverListener(resultElem, index) {
      resultElem.addEventListener('mouseover', (e) => {
        this.highlightedResultIndex = index;
        this._highlight(this.highlightedResultIndex);
      });
    }

    _highlight(index, scrollIntoView) {
      if (scrollIntoView === undefined) {
        scrollIntoView = false;
      }

      if (this.results.length === 0) {
        return;
      }

      // User might have closed the suggestions, show them again
      this.showSuggestions();

      this.resultsListElem.childNodes.forEach((node, i) => {
        if (i !== index && node.classList.contains('highlight')) {
          node.classList.remove('highlight');
          node.setAttribute('aria-selected', 'false');
        }
        else if (i == index && !node.classList.contains('highlight')) {
          node.classList.add('highlight');
          node.setAttribute('aria-selected', 'true');
        }
      });

      if (scrollIntoView && this.results.length > index) {
        this.resultsListElem.childNodes[index].scrollIntoView(
          {"block": "center"}
        );
      }
    }

    _addKeyUpEventListener() {
      this.searchInputElem.addEventListener('keyup', (e) => {
        if (e.key == 'Escape') {
          this.hideSuggestions();
        }

        if (e.key == 'ArrowDown') {
          this.highlightedResultIndex =
            this.highlightedResultIndex !== null
            ? this._constrainHighlight(this.highlightedResultIndex + 1)
            : 0;

          this._highlight(this.highlightedResultIndex, true);
        }

        if (e.key == 'ArrowUp') {
          this.highlightedResultIndex =
            this.highlightedResultIndex !== null
            ? this._constrainHighlight(this.highlightedResultIndex - 1)
            : this._constrainHighlight(this.results.length - 1);

          this._highlight(this.highlightedResultIndex, true);
        }

        if (e.key == 'Enter' && this.highlightedResultIndex !== null) {
          const url = this.searchFormElem.querySelector('.highlight a').getAttribute('href');
          window.location = url;
        }
      });
    }

    _addSearchEventListeners() {
      this.searchInputElem.addEventListener('input', (e) => {
        if (this.debounceTimer !== null) {
          window.clearTimeout(this.debounceTimer);
        }

        if (e.target.value.length > 1) {
          this.debounceTimer = window.setTimeout(() => this._search(e.target.value), 500);
        }
        else {
          this.debounceTimer = null;
          this.results = [];
          this.hideSuggestions();
        }
      });
    }

    _createResultGroupElement(type, label) {
      const typeIconMapping = {
        "actor": "fa-user",
        "author": "fa-user",
        "property": "fa-pencil-square",
        "sent_date": "fa-calendar-plus-o",
        "time": "fa-calendar",
      }
      const icon = document.createElement("i");
      icon.setAttribute("class", "fa fa-user mr-3 text-muted");
      if (typeIconMapping.hasOwnProperty(type)) {
        icon.classList.add(typeIconMapping[type]);
      }

      const element = document.createElement("div");
      element.setAttribute("class", "bg-light p-2");
      element.appendChild(icon);
      element.appendChild(document.createTextNode(label));

      return element;
    }

    _createResultElement(submission, match) {
      const statusElement = document.createElement("i");
      statusElement.setAttribute("class", `mr-3 fa fa-circle status${submission.status}`);

      const matchFieldValueElement = document.createElement("span");
      matchFieldValueElement.setAttribute("class", "font-weight-bold");
      matchFieldValueElement.textContent = match.fieldValue;

      const matchFieldElement = document.createElement("div");

      if (match.type == 'property') {
        matchFieldElement.appendChild(document.createTextNode(match.fieldLabel + ': '));
      }

      matchFieldElement.appendChild(matchFieldValueElement);

      const resultLinkElement = document.createElement("a");
      resultLinkElement.setAttribute("class", "d-block media-body");
      resultLinkElement.setAttribute("href", submission.url);
      resultLinkElement.appendChild(matchFieldElement);
      if (match.type != 'sent_date') {
        resultLinkElement.appendChild(document.createTextNode(`Demande du ${submission.createdAt}`));
        resultLinkElement.appendChild(document.createElement("br"));
      }
      if (match.type != 'author') {
        resultLinkElement.appendChild(document.createTextNode(`Auteur‧e: ${submission.author}`));
      }

      const resultElement = document.createElement("div");
      resultElement.setAttribute("class", "result-item media align-items-baseline p-2");
      resultElement.appendChild(statusElement);
      resultElement.appendChild(resultLinkElement);

      return resultElement;
    }

    _search(value) {
      fetch(this.searchFormElem.getAttribute('action') + "?" + (new URLSearchParams({search: value})).toString(), {
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/x-www-urlencoded',
        }
      })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.results = data.results;
        this._redraw();
        this.showSuggestions();
      });
    }

    _redraw() {
      if (this.results.length === 0) {
        const noResultsElem = document.createElement('div');
        noResultsElem.setAttribute('class', 'search-results p-2 text-muted font-italic');
        noResultsElem.textContent = 'Aucun résultat pour votre recherche.';

        this.resultsElem.childNodes.forEach(node => this.resultsElem.removeChild(node));
        this.resultsElem.appendChild(noResultsElem);
      }
      else {
        this.resultsListElem = this._createResultsListElem();
        this.highlightedResultIndex = null;

        const results = this.results.forEach((result, i) => {
          const listElement = document.createElement("li");
          const groupElement = this._createResultGroupElement(result.match.type, result.match.typeLabel);
          const resultElement = this._createResultElement(result.submission, result.match);

          listElement.appendChild(groupElement);
          listElement.appendChild(resultElement);
          this._addHoverListener(listElement, i);

          this.resultsListElem.appendChild(listElement);
        });

        this.resultsElem.childNodes.forEach(node => this.resultsElem.removeChild(node));
        this.resultsElem.appendChild(this.resultsListElem);

        // Hack: scroll doesn’t happen without setTimeout, probably because the
        // node hasn’t been rendered yet
        window.setTimeout(() => this.resultsListElem.scrollTo(0, 0), 0);
      }
    }

    _constrainHighlight(index) {
      if (index < 0) {
        return Math.max(this.results.length - 1, 0);
      }
      else if (index >= this.results.length) {
        return 0;
      }

      return index;
    }
  }

  document.addEventListener('DOMContentLoaded', (e) => {
    const searchFormElem = document.getElementById('global-search-form');
    if (searchFormElem) {
      new GlobalSearchForm(searchFormElem);
    }
  });
}());
