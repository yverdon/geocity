/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Tr = window, Wa = Tr.ShadowRoot && (Tr.ShadyCSS === void 0 || Tr.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, su = Symbol(), th = /* @__PURE__ */ new WeakMap();
class Xf {
  constructor(t, e, n) {
    if (this._$cssResult$ = !0, n !== su)
      throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Wa && t === void 0) {
      const n = e !== void 0 && e.length === 1;
      n && (t = th.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), n && th.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
}
const yt = (i) => new Xf(typeof i == "string" ? i : i + "", void 0, su), Yf = (i, t) => {
  Wa ? i.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet) : t.forEach((e) => {
    const n = document.createElement("style"), s = Tr.litNonce;
    s !== void 0 && n.setAttribute("nonce", s), n.textContent = e.cssText, i.appendChild(n);
  });
}, eh = Wa ? (i) => i : (i) => i instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const n of t.cssRules)
    e += n.cssText;
  return yt(e);
})(i) : i;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var Do;
const Nr = window, ih = Nr.trustedTypes, jf = ih ? ih.emptyScript : "", nh = Nr.reactiveElementPolyfillSupport, oa = { toAttribute(i, t) {
  switch (t) {
    case Boolean:
      i = i ? jf : null;
      break;
    case Object:
    case Array:
      i = i == null ? i : JSON.stringify(i);
  }
  return i;
}, fromAttribute(i, t) {
  let e = i;
  switch (t) {
    case Boolean:
      e = i !== null;
      break;
    case Number:
      e = i === null ? null : Number(i);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(i);
      } catch {
        e = null;
      }
  }
  return e;
} }, ru = (i, t) => t !== i && (t == t || i == i), ko = { attribute: !0, type: String, converter: oa, reflect: !1, hasChanged: ru };
class vn extends HTMLElement {
  constructor() {
    super(), this._$Ei = /* @__PURE__ */ new Map(), this.isUpdatePending = !1, this.hasUpdated = !1, this._$El = null, this.u();
  }
  static addInitializer(t) {
    var e;
    this.finalize(), ((e = this.h) !== null && e !== void 0 ? e : this.h = []).push(t);
  }
  static get observedAttributes() {
    this.finalize();
    const t = [];
    return this.elementProperties.forEach((e, n) => {
      const s = this._$Ep(n, e);
      s !== void 0 && (this._$Ev.set(s, n), t.push(s));
    }), t;
  }
  static createProperty(t, e = ko) {
    if (e.state && (e.attribute = !1), this.finalize(), this.elementProperties.set(t, e), !e.noAccessor && !this.prototype.hasOwnProperty(t)) {
      const n = typeof t == "symbol" ? Symbol() : "__" + t, s = this.getPropertyDescriptor(t, n, e);
      s !== void 0 && Object.defineProperty(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, n) {
    return { get() {
      return this[e];
    }, set(s) {
      const r = this[t];
      this[e] = s, this.requestUpdate(t, r, n);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) || ko;
  }
  static finalize() {
    if (this.hasOwnProperty("finalized"))
      return !1;
    this.finalized = !0;
    const t = Object.getPrototypeOf(this);
    if (t.finalize(), t.h !== void 0 && (this.h = [...t.h]), this.elementProperties = new Map(t.elementProperties), this._$Ev = /* @__PURE__ */ new Map(), this.hasOwnProperty("properties")) {
      const e = this.properties, n = [...Object.getOwnPropertyNames(e), ...Object.getOwnPropertySymbols(e)];
      for (const s of n)
        this.createProperty(s, e[s]);
    }
    return this.elementStyles = this.finalizeStyles(this.styles), !0;
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const n = new Set(t.flat(1 / 0).reverse());
      for (const s of n)
        e.unshift(eh(s));
    } else
      t !== void 0 && e.push(eh(t));
    return e;
  }
  static _$Ep(t, e) {
    const n = e.attribute;
    return n === !1 ? void 0 : typeof n == "string" ? n : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  u() {
    var t;
    this._$E_ = new Promise((e) => this.enableUpdating = e), this._$AL = /* @__PURE__ */ new Map(), this._$Eg(), this.requestUpdate(), (t = this.constructor.h) === null || t === void 0 || t.forEach((e) => e(this));
  }
  addController(t) {
    var e, n;
    ((e = this._$ES) !== null && e !== void 0 ? e : this._$ES = []).push(t), this.renderRoot !== void 0 && this.isConnected && ((n = t.hostConnected) === null || n === void 0 || n.call(t));
  }
  removeController(t) {
    var e;
    (e = this._$ES) === null || e === void 0 || e.splice(this._$ES.indexOf(t) >>> 0, 1);
  }
  _$Eg() {
    this.constructor.elementProperties.forEach((t, e) => {
      this.hasOwnProperty(e) && (this._$Ei.set(e, this[e]), delete this[e]);
    });
  }
  createRenderRoot() {
    var t;
    const e = (t = this.shadowRoot) !== null && t !== void 0 ? t : this.attachShadow(this.constructor.shadowRootOptions);
    return Yf(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    var t;
    this.renderRoot === void 0 && (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$ES) === null || t === void 0 || t.forEach((e) => {
      var n;
      return (n = e.hostConnected) === null || n === void 0 ? void 0 : n.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$ES) === null || t === void 0 || t.forEach((e) => {
      var n;
      return (n = e.hostDisconnected) === null || n === void 0 ? void 0 : n.call(e);
    });
  }
  attributeChangedCallback(t, e, n) {
    this._$AK(t, n);
  }
  _$EO(t, e, n = ko) {
    var s;
    const r = this.constructor._$Ep(t, n);
    if (r !== void 0 && n.reflect === !0) {
      const o = (((s = n.converter) === null || s === void 0 ? void 0 : s.toAttribute) !== void 0 ? n.converter : oa).toAttribute(e, n.type);
      this._$El = t, o == null ? this.removeAttribute(r) : this.setAttribute(r, o), this._$El = null;
    }
  }
  _$AK(t, e) {
    var n;
    const s = this.constructor, r = s._$Ev.get(t);
    if (r !== void 0 && this._$El !== r) {
      const o = s.getPropertyOptions(r), a = typeof o.converter == "function" ? { fromAttribute: o.converter } : ((n = o.converter) === null || n === void 0 ? void 0 : n.fromAttribute) !== void 0 ? o.converter : oa;
      this._$El = r, this[r] = a.fromAttribute(e, o.type), this._$El = null;
    }
  }
  requestUpdate(t, e, n) {
    let s = !0;
    t !== void 0 && (((n = n || this.constructor.getPropertyOptions(t)).hasChanged || ru)(this[t], e) ? (this._$AL.has(t) || this._$AL.set(t, e), n.reflect === !0 && this._$El !== t && (this._$EC === void 0 && (this._$EC = /* @__PURE__ */ new Map()), this._$EC.set(t, n))) : s = !1), !this.isUpdatePending && s && (this._$E_ = this._$Ej());
  }
  async _$Ej() {
    this.isUpdatePending = !0;
    try {
      await this._$E_;
    } catch (e) {
      Promise.reject(e);
    }
    const t = this.scheduleUpdate();
    return t != null && await t, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    var t;
    if (!this.isUpdatePending)
      return;
    this.hasUpdated, this._$Ei && (this._$Ei.forEach((s, r) => this[r] = s), this._$Ei = void 0);
    let e = !1;
    const n = this._$AL;
    try {
      e = this.shouldUpdate(n), e ? (this.willUpdate(n), (t = this._$ES) === null || t === void 0 || t.forEach((s) => {
        var r;
        return (r = s.hostUpdate) === null || r === void 0 ? void 0 : r.call(s);
      }), this.update(n)) : this._$Ek();
    } catch (s) {
      throw e = !1, this._$Ek(), s;
    }
    e && this._$AE(n);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$ES) === null || e === void 0 || e.forEach((n) => {
      var s;
      return (s = n.hostUpdated) === null || s === void 0 ? void 0 : s.call(n);
    }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
  }
  _$Ek() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$E_;
  }
  shouldUpdate(t) {
    return !0;
  }
  update(t) {
    this._$EC !== void 0 && (this._$EC.forEach((e, n) => this._$EO(n, this[n], e)), this._$EC = void 0), this._$Ek();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
}
vn.finalized = !0, vn.elementProperties = /* @__PURE__ */ new Map(), vn.elementStyles = [], vn.shadowRootOptions = { mode: "open" }, nh == null || nh({ ReactiveElement: vn }), ((Do = Nr.reactiveElementVersions) !== null && Do !== void 0 ? Do : Nr.reactiveElementVersions = []).push("1.5.0");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var Go;
const Fr = window, Fn = Fr.trustedTypes, sh = Fn ? Fn.createPolicy("lit-html", { createHTML: (i) => i }) : void 0, Qe = `lit$${(Math.random() + "").slice(9)}$`, Ha = "?" + Qe, Kf = `<${Ha}>`, Dn = document, vs = (i = "") => Dn.createComment(i), xs = (i) => i === null || typeof i != "object" && typeof i != "function", ou = Array.isArray, au = (i) => ou(i) || typeof (i == null ? void 0 : i[Symbol.iterator]) == "function", ss = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, rh = /-->/g, oh = />/g, Oi = RegExp(`>|[ 	
\f\r](?:([^\\s"'>=/]+)([ 	
\f\r]*=[ 	
\f\r]*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), ah = /'/g, lh = /"/g, lu = /^(?:script|style|textarea|title)$/i, qf = (i) => (t, ...e) => ({ _$litType$: i, strings: t, values: e }), Lt = qf(1), Ei = Symbol.for("lit-noChange"), bt = Symbol.for("lit-nothing"), hh = /* @__PURE__ */ new WeakMap(), Pn = Dn.createTreeWalker(Dn, 129, null, !1), hu = (i, t) => {
  const e = i.length - 1, n = [];
  let s, r = t === 2 ? "<svg>" : "", o = ss;
  for (let l = 0; l < e; l++) {
    const h = i[l];
    let c, u, d = -1, f = 0;
    for (; f < h.length && (o.lastIndex = f, u = o.exec(h), u !== null); )
      f = o.lastIndex, o === ss ? u[1] === "!--" ? o = rh : u[1] !== void 0 ? o = oh : u[2] !== void 0 ? (lu.test(u[2]) && (s = RegExp("</" + u[2], "g")), o = Oi) : u[3] !== void 0 && (o = Oi) : o === Oi ? u[0] === ">" ? (o = s != null ? s : ss, d = -1) : u[1] === void 0 ? d = -2 : (d = o.lastIndex - u[2].length, c = u[1], o = u[3] === void 0 ? Oi : u[3] === '"' ? lh : ah) : o === lh || o === ah ? o = Oi : o === rh || o === oh ? o = ss : (o = Oi, s = void 0);
    const g = o === Oi && i[l + 1].startsWith("/>") ? " " : "";
    r += o === ss ? h + Kf : d >= 0 ? (n.push(c), h.slice(0, d) + "$lit$" + h.slice(d) + Qe + g) : h + Qe + (d === -2 ? (n.push(void 0), l) : g);
  }
  const a = r + (i[e] || "<?>") + (t === 2 ? "</svg>" : "");
  if (!Array.isArray(i) || !i.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return [sh !== void 0 ? sh.createHTML(a) : a, n];
};
class Cs {
  constructor({ strings: t, _$litType$: e }, n) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, l = this.parts, [h, c] = hu(t, e);
    if (this.el = Cs.createElement(h, n), Pn.currentNode = this.el.content, e === 2) {
      const u = this.el.content, d = u.firstChild;
      d.remove(), u.append(...d.childNodes);
    }
    for (; (s = Pn.nextNode()) !== null && l.length < a; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) {
          const u = [];
          for (const d of s.getAttributeNames())
            if (d.endsWith("$lit$") || d.startsWith(Qe)) {
              const f = c[o++];
              if (u.push(d), f !== void 0) {
                const g = s.getAttribute(f.toLowerCase() + "$lit$").split(Qe), m = /([.?@])?(.*)/.exec(f);
                l.push({ type: 1, index: r, name: m[2], strings: g, ctor: m[1] === "." ? uu : m[1] === "?" ? du : m[1] === "@" ? fu : Bs });
              } else
                l.push({ type: 6, index: r });
            }
          for (const d of u)
            s.removeAttribute(d);
        }
        if (lu.test(s.tagName)) {
          const u = s.textContent.split(Qe), d = u.length - 1;
          if (d > 0) {
            s.textContent = Fn ? Fn.emptyScript : "";
            for (let f = 0; f < d; f++)
              s.append(u[f], vs()), Pn.nextNode(), l.push({ type: 2, index: ++r });
            s.append(u[d], vs());
          }
        }
      } else if (s.nodeType === 8)
        if (s.data === Ha)
          l.push({ type: 2, index: r });
        else {
          let u = -1;
          for (; (u = s.data.indexOf(Qe, u + 1)) !== -1; )
            l.push({ type: 7, index: r }), u += Qe.length - 1;
        }
      r++;
    }
  }
  static createElement(t, e) {
    const n = Dn.createElement("template");
    return n.innerHTML = t, n;
  }
}
function Xi(i, t, e = i, n) {
  var s, r, o, a;
  if (t === Ei)
    return t;
  let l = n !== void 0 ? (s = e._$Co) === null || s === void 0 ? void 0 : s[n] : e._$Cl;
  const h = xs(t) ? void 0 : t._$litDirective$;
  return (l == null ? void 0 : l.constructor) !== h && ((r = l == null ? void 0 : l._$AO) === null || r === void 0 || r.call(l, !1), h === void 0 ? l = void 0 : (l = new h(i), l._$AT(i, e, n)), n !== void 0 ? ((o = (a = e)._$Co) !== null && o !== void 0 ? o : a._$Co = [])[n] = l : e._$Cl = l), l !== void 0 && (t = Xi(i, l._$AS(i, t.values), l, n)), t;
}
class cu {
  constructor(t, e) {
    this.u = [], this._$AN = void 0, this._$AD = t, this._$AM = e;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  v(t) {
    var e;
    const { el: { content: n }, parts: s } = this._$AD, r = ((e = t == null ? void 0 : t.creationScope) !== null && e !== void 0 ? e : Dn).importNode(n, !0);
    Pn.currentNode = r;
    let o = Pn.nextNode(), a = 0, l = 0, h = s[0];
    for (; h !== void 0; ) {
      if (a === h.index) {
        let c;
        h.type === 2 ? c = new Xn(o, o.nextSibling, this, t) : h.type === 1 ? c = new h.ctor(o, h.name, h.strings, this, t) : h.type === 6 && (c = new gu(o, this, t)), this.u.push(c), h = s[++l];
      }
      a !== (h == null ? void 0 : h.index) && (o = Pn.nextNode(), a++);
    }
    return r;
  }
  p(t) {
    let e = 0;
    for (const n of this.u)
      n !== void 0 && (n.strings !== void 0 ? (n._$AI(t, n, e), e += n.strings.length - 2) : n._$AI(t[e])), e++;
  }
}
class Xn {
  constructor(t, e, n, s) {
    var r;
    this.type = 2, this._$AH = bt, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = n, this.options = s, this._$Cm = (r = s == null ? void 0 : s.isConnected) === null || r === void 0 || r;
  }
  get _$AU() {
    var t, e;
    return (e = (t = this._$AM) === null || t === void 0 ? void 0 : t._$AU) !== null && e !== void 0 ? e : this._$Cm;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const e = this._$AM;
    return e !== void 0 && t.nodeType === 11 && (t = e.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, e = this) {
    t = Xi(this, t, e), xs(t) ? t === bt || t == null || t === "" ? (this._$AH !== bt && this._$AR(), this._$AH = bt) : t !== this._$AH && t !== Ei && this.g(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : au(t) ? this.k(t) : this.g(t);
  }
  O(t, e = this._$AB) {
    return this._$AA.parentNode.insertBefore(t, e);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  g(t) {
    this._$AH !== bt && xs(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Dn.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var e;
    const { values: n, _$litType$: s } = t, r = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = Cs.createElement(s.h, this.options)), s);
    if (((e = this._$AH) === null || e === void 0 ? void 0 : e._$AD) === r)
      this._$AH.p(n);
    else {
      const o = new cu(r, this), a = o.v(this.options);
      o.p(n), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = hh.get(t.strings);
    return e === void 0 && hh.set(t.strings, e = new Cs(t)), e;
  }
  k(t) {
    ou(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let n, s = 0;
    for (const r of t)
      s === e.length ? e.push(n = new Xn(this.O(vs()), this.O(vs()), this, this.options)) : n = e[s], n._$AI(r), s++;
    s < e.length && (this._$AR(n && n._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var n;
    for ((n = this._$AP) === null || n === void 0 || n.call(this, !1, !0, e); t && t !== this._$AB; ) {
      const s = t.nextSibling;
      t.remove(), t = s;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cm = t, (e = this._$AP) === null || e === void 0 || e.call(this, t));
  }
}
class Bs {
  constructor(t, e, n, s, r) {
    this.type = 1, this._$AH = bt, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, n.length > 2 || n[0] !== "" || n[1] !== "" ? (this._$AH = Array(n.length - 1).fill(new String()), this.strings = n) : this._$AH = bt;
  }
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t, e = this, n, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0)
      t = Xi(this, t, e, 0), o = !xs(t) || t !== this._$AH && t !== Ei, o && (this._$AH = t);
    else {
      const a = t;
      let l, h;
      for (t = r[0], l = 0; l < r.length - 1; l++)
        h = Xi(this, a[n + l], e, l), h === Ei && (h = this._$AH[l]), o || (o = !xs(h) || h !== this._$AH[l]), h === bt ? t = bt : t !== bt && (t += (h != null ? h : "") + r[l + 1]), this._$AH[l] = h;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === bt ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t != null ? t : "");
  }
}
class uu extends Bs {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === bt ? void 0 : t;
  }
}
const Jf = Fn ? Fn.emptyScript : "";
class du extends Bs {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    t && t !== bt ? this.element.setAttribute(this.name, Jf) : this.element.removeAttribute(this.name);
  }
}
class fu extends Bs {
  constructor(t, e, n, s, r) {
    super(t, e, n, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    var n;
    if ((t = (n = Xi(this, t, e, 0)) !== null && n !== void 0 ? n : bt) === Ei)
      return;
    const s = this._$AH, r = t === bt && s !== bt || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, o = t !== bt && (s === bt || r);
    r && this.element.removeEventListener(this.name, this, s), o && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e, n;
    typeof this._$AH == "function" ? this._$AH.call((n = (e = this.options) === null || e === void 0 ? void 0 : e.host) !== null && n !== void 0 ? n : this.element, t) : this._$AH.handleEvent(t);
  }
}
class gu {
  constructor(t, e, n) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = n;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    Xi(this, t);
  }
}
const Qf = { P: "$lit$", A: Qe, M: Ha, C: 1, L: hu, R: cu, D: au, V: Xi, I: Xn, H: Bs, N: du, U: fu, B: uu, F: gu }, ch = Fr.litHtmlPolyfillSupport;
ch == null || ch(Cs, Xn), ((Go = Fr.litHtmlVersions) !== null && Go !== void 0 ? Go : Fr.litHtmlVersions = []).push("2.5.0");
const mu = (i, t, e) => {
  var n, s;
  const r = (n = e == null ? void 0 : e.renderBefore) !== null && n !== void 0 ? n : t;
  let o = r._$litPart$;
  if (o === void 0) {
    const a = (s = e == null ? void 0 : e.renderBefore) !== null && s !== void 0 ? s : null;
    r._$litPart$ = o = new Xn(t.insertBefore(vs(), a), a, void 0, e != null ? e : {});
  }
  return o._$AI(i), o;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var $o, Bo;
class Pt extends vn {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var t, e;
    const n = super.createRenderRoot();
    return (t = (e = this.renderOptions).renderBefore) !== null && t !== void 0 || (e.renderBefore = n.firstChild), n;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = mu(e, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    var t;
    super.connectedCallback(), (t = this._$Do) === null || t === void 0 || t.setConnected(!0);
  }
  disconnectedCallback() {
    var t;
    super.disconnectedCallback(), (t = this._$Do) === null || t === void 0 || t.setConnected(!1);
  }
  render() {
    return Ei;
  }
}
Pt.finalized = !0, Pt._$litElement$ = !0, ($o = globalThis.litElementHydrateSupport) === null || $o === void 0 || $o.call(globalThis, { LitElement: Pt });
const uh = globalThis.litElementPolyfillSupport;
uh == null || uh({ LitElement: Pt });
((Bo = globalThis.litElementVersions) !== null && Bo !== void 0 ? Bo : globalThis.litElementVersions = []).push("3.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const qt = (i) => (t) => typeof t == "function" ? ((e, n) => (customElements.define(e, n), n))(i, t) : ((e, n) => {
  const { kind: s, elements: r } = n;
  return { kind: s, elements: r, finisher(o) {
    customElements.define(e, o);
  } };
})(i, t);
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t0 = (i, t) => t.kind === "method" && t.descriptor && !("value" in t.descriptor) ? { ...t, finisher(e) {
  e.createProperty(t.key, i);
} } : { kind: "field", key: Symbol(), placement: "own", descriptor: {}, originalKey: t.key, initializer() {
  typeof t.initializer == "function" && (this[t.key] = t.initializer.call(this));
}, finisher(e) {
  e.createProperty(t.key, i);
} };
function Ti(i) {
  return (t, e) => e !== void 0 ? ((n, s, r) => {
    s.constructor.createProperty(r, n);
  })(i, t, e) : t0(i, t);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function Dt(i) {
  return Ti({ ...i, state: !0 });
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const e0 = ({ finisher: i, descriptor: t }) => (e, n) => {
  var s;
  if (n === void 0) {
    const r = (s = e.originalKey) !== null && s !== void 0 ? s : e.key, o = t != null ? { kind: "method", placement: "prototype", key: r, descriptor: t(e.key) } : { ...e, key: r };
    return i != null && (o.finisher = function(a) {
      i(a, r);
    }), o;
  }
  {
    const r = e.constructor;
    t !== void 0 && Object.defineProperty(e, n, t(n)), i == null || i(r, n);
  }
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function pu(i, t) {
  return e0({ descriptor: (e) => {
    const n = { get() {
      var s, r;
      return (r = (s = this.renderRoot) === null || s === void 0 ? void 0 : s.querySelector(i)) !== null && r !== void 0 ? r : null;
    }, enumerable: !0, configurable: !0 };
    if (t) {
      const s = typeof e == "symbol" ? Symbol() : "__" + e;
      n.get = function() {
        var r, o;
        return this[s] === void 0 && (this[s] = (o = (r = this.renderRoot) === null || r === void 0 ? void 0 : r.querySelector(i)) !== null && o !== void 0 ? o : null), this[s];
      };
    }
    return n;
  } });
}
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var zo;
((zo = window.HTMLSlotElement) === null || zo === void 0 ? void 0 : zo.prototype.assignedElements) != null;
class i0 {
  constructor(t) {
    this.propagationStopped, this.defaultPrevented, this.type = t, this.target = null;
  }
  preventDefault() {
    this.defaultPrevented = !0;
  }
  stopPropagation() {
    this.propagationStopped = !0;
  }
}
const Be = i0, kn = {
  PROPERTYCHANGE: "propertychange"
};
class n0 {
  constructor() {
    this.disposed = !1;
  }
  dispose() {
    this.disposed || (this.disposed = !0, this.disposeInternal());
  }
  disposeInternal() {
  }
}
const Xa = n0;
function s0(i, t, e) {
  let n, s;
  e = e || Yi;
  let r = 0, o = i.length, a = !1;
  for (; r < o; )
    n = r + (o - r >> 1), s = +e(i[n], t), s < 0 ? r = n + 1 : (o = n, a = !s);
  return a ? r : ~r;
}
function Yi(i, t) {
  return i > t ? 1 : i < t ? -1 : 0;
}
function Ya(i, t, e) {
  const n = i.length;
  if (i[0] <= t)
    return 0;
  if (t <= i[n - 1])
    return n - 1;
  {
    let s;
    if (e > 0) {
      for (s = 1; s < n; ++s)
        if (i[s] < t)
          return s - 1;
    } else if (e < 0) {
      for (s = 1; s < n; ++s)
        if (i[s] <= t)
          return s;
    } else
      for (s = 1; s < n; ++s) {
        if (i[s] == t)
          return s;
        if (i[s] < t)
          return typeof e == "function" ? e(t, i[s - 1], i[s]) > 0 ? s - 1 : s : i[s - 1] - t < t - i[s] ? s - 1 : s;
      }
    return n - 1;
  }
}
function r0(i, t, e) {
  for (; t < e; ) {
    const n = i[t];
    i[t] = i[e], i[e] = n, ++t, --e;
  }
}
function Kt(i, t) {
  const e = Array.isArray(t) ? t : [t], n = e.length;
  for (let s = 0; s < n; s++)
    i[i.length] = e[s];
}
function nn(i, t) {
  const e = i.length;
  if (e !== t.length)
    return !1;
  for (let n = 0; n < e; n++)
    if (i[n] !== t[n])
      return !1;
  return !0;
}
function o0(i, t, e) {
  const n = t || Yi;
  return i.every(function(s, r) {
    if (r === 0)
      return !0;
    const o = n(i[r - 1], s);
    return !(o > 0 || e && o === 0);
  });
}
function Ms() {
  return !0;
}
function ao() {
  return !1;
}
function ji() {
}
function a0(i) {
  let t = !1, e, n, s;
  return function() {
    const r = Array.prototype.slice.call(arguments);
    return (!t || this !== s || !nn(r, n)) && (t = !0, s = this, n = r, e = i.apply(this, arguments)), e;
  };
}
function zs(i) {
  for (const t in i)
    delete i[t];
}
function Gn(i) {
  let t;
  for (t in i)
    return !1;
  return !t;
}
class l0 extends Xa {
  constructor(t) {
    super(), this.eventTarget_ = t, this.pendingRemovals_ = null, this.dispatching_ = null, this.listeners_ = null;
  }
  addEventListener(t, e) {
    if (!t || !e)
      return;
    const n = this.listeners_ || (this.listeners_ = {}), s = n[t] || (n[t] = []);
    s.includes(e) || s.push(e);
  }
  dispatchEvent(t) {
    const e = typeof t == "string", n = e ? t : t.type, s = this.listeners_ && this.listeners_[n];
    if (!s)
      return;
    const r = e ? new Be(t) : t;
    r.target || (r.target = this.eventTarget_ || this);
    const o = this.dispatching_ || (this.dispatching_ = {}), a = this.pendingRemovals_ || (this.pendingRemovals_ = {});
    n in o || (o[n] = 0, a[n] = 0), ++o[n];
    let l;
    for (let h = 0, c = s.length; h < c; ++h)
      if ("handleEvent" in s[h] ? l = s[h].handleEvent(r) : l = s[h].call(this, r), l === !1 || r.propagationStopped) {
        l = !1;
        break;
      }
    if (--o[n] === 0) {
      let h = a[n];
      for (delete a[n]; h--; )
        this.removeEventListener(n, ji);
      delete o[n];
    }
    return l;
  }
  disposeInternal() {
    this.listeners_ && zs(this.listeners_);
  }
  getListeners(t) {
    return this.listeners_ && this.listeners_[t] || void 0;
  }
  hasListener(t) {
    return this.listeners_ ? t ? t in this.listeners_ : Object.keys(this.listeners_).length > 0 : !1;
  }
  removeEventListener(t, e) {
    const n = this.listeners_ && this.listeners_[t];
    if (n) {
      const s = n.indexOf(e);
      s !== -1 && (this.pendingRemovals_ && t in this.pendingRemovals_ ? (n[s] = ji, ++this.pendingRemovals_[t]) : (n.splice(s, 1), n.length === 0 && delete this.listeners_[t]));
    }
  }
}
const lo = l0, X = {
  CHANGE: "change",
  ERROR: "error",
  BLUR: "blur",
  CLEAR: "clear",
  CONTEXTMENU: "contextmenu",
  CLICK: "click",
  DBLCLICK: "dblclick",
  DRAGENTER: "dragenter",
  DRAGOVER: "dragover",
  DROP: "drop",
  FOCUS: "focus",
  KEYDOWN: "keydown",
  KEYPRESS: "keypress",
  LOAD: "load",
  RESIZE: "resize",
  TOUCHMOVE: "touchmove",
  WHEEL: "wheel"
};
function et(i, t, e, n, s) {
  if (n && n !== i && (e = e.bind(n)), s) {
    const o = e;
    e = function() {
      i.removeEventListener(t, e), o.apply(this, arguments);
    };
  }
  const r = {
    target: i,
    type: t,
    listener: e
  };
  return i.addEventListener(t, e), r;
}
function Dr(i, t, e, n) {
  return et(i, t, e, n, !0);
}
function pt(i) {
  i && i.target && (i.target.removeEventListener(i.type, i.listener), zs(i));
}
class ho extends lo {
  constructor() {
    super(), this.on = this.onInternal, this.once = this.onceInternal, this.un = this.unInternal, this.revision_ = 0;
  }
  changed() {
    ++this.revision_, this.dispatchEvent(X.CHANGE);
  }
  getRevision() {
    return this.revision_;
  }
  onInternal(t, e) {
    if (Array.isArray(t)) {
      const n = t.length, s = new Array(n);
      for (let r = 0; r < n; ++r)
        s[r] = et(this, t[r], e);
      return s;
    } else
      return et(this, t, e);
  }
  onceInternal(t, e) {
    let n;
    if (Array.isArray(t)) {
      const s = t.length;
      n = new Array(s);
      for (let r = 0; r < s; ++r)
        n[r] = Dr(this, t[r], e);
    } else
      n = Dr(this, t, e);
    return e.ol_key = n, n;
  }
  unInternal(t, e) {
    const n = e.ol_key;
    if (n)
      h0(n);
    else if (Array.isArray(t))
      for (let s = 0, r = t.length; s < r; ++s)
        this.removeEventListener(t[s], e);
    else
      this.removeEventListener(t, e);
  }
}
ho.prototype.on;
ho.prototype.once;
ho.prototype.un;
function h0(i) {
  if (Array.isArray(i))
    for (let t = 0, e = i.length; t < e; ++t)
      pt(i[t]);
  else
    pt(i);
}
const _u = ho;
function W() {
  throw new Error("Unimplemented abstract method.");
}
let c0 = 0;
function ot(i) {
  return i.ol_uid || (i.ol_uid = String(++c0));
}
class dh extends Be {
  constructor(t, e, n) {
    super(t), this.key = e, this.oldValue = n;
  }
}
class u0 extends _u {
  constructor(t) {
    super(), this.on, this.once, this.un, ot(this), this.values_ = null, t !== void 0 && this.setProperties(t);
  }
  get(t) {
    let e;
    return this.values_ && this.values_.hasOwnProperty(t) && (e = this.values_[t]), e;
  }
  getKeys() {
    return this.values_ && Object.keys(this.values_) || [];
  }
  getProperties() {
    return this.values_ && Object.assign({}, this.values_) || {};
  }
  hasProperties() {
    return !!this.values_;
  }
  notify(t, e) {
    let n;
    n = `change:${t}`, this.hasListener(n) && this.dispatchEvent(new dh(n, t, e)), n = kn.PROPERTYCHANGE, this.hasListener(n) && this.dispatchEvent(new dh(n, t, e));
  }
  addChangeListener(t, e) {
    this.addEventListener(`change:${t}`, e);
  }
  removeChangeListener(t, e) {
    this.removeEventListener(`change:${t}`, e);
  }
  set(t, e, n) {
    const s = this.values_ || (this.values_ = {});
    if (n)
      s[t] = e;
    else {
      const r = s[t];
      s[t] = e, r !== e && this.notify(t, r);
    }
  }
  setProperties(t, e) {
    for (const n in t)
      this.set(n, t[n], e);
  }
  applyProperties(t) {
    !t.values_ || Object.assign(this.values_ || (this.values_ = {}), t.values_);
  }
  unset(t, e) {
    if (this.values_ && t in this.values_) {
      const n = this.values_[t];
      delete this.values_[t], Gn(this.values_) && (this.values_ = null), e || this.notify(t, n);
    }
  }
}
const Ce = u0, d0 = {
  1: "The view center is not defined",
  2: "The view resolution is not defined",
  3: "The view rotation is not defined",
  4: "`image` and `src` cannot be provided at the same time",
  5: "`imgSize` must be set when `image` is provided",
  7: "`format` must be set when `url` is set",
  8: "Unknown `serverType` configured",
  9: "`url` must be configured or set using `#setUrl()`",
  10: "The default `geometryFunction` can only handle `Point` geometries",
  11: "`options.featureTypes` must be an Array",
  12: "`options.geometryName` must also be provided when `options.bbox` is set",
  13: "Invalid corner",
  14: "Invalid color",
  15: "Tried to get a value for a key that does not exist in the cache",
  16: "Tried to set a value for a key that is used already",
  17: "`resolutions` must be sorted in descending order",
  18: "Either `origin` or `origins` must be configured, never both",
  19: "Number of `tileSizes` and `resolutions` must be equal",
  20: "Number of `origins` and `resolutions` must be equal",
  22: "Either `tileSize` or `tileSizes` must be configured, never both",
  24: "Invalid extent or geometry provided as `geometry`",
  25: "Cannot fit empty extent provided as `geometry`",
  26: "Features must have an id set",
  27: "Features must have an id set",
  28: '`renderMode` must be `"hybrid"` or `"vector"`',
  30: "The passed `feature` was already added to the source",
  31: "Tried to enqueue an `element` that was already added to the queue",
  32: "Transformation matrix cannot be inverted",
  33: "Invalid units",
  34: "Invalid geometry layout",
  36: "Unknown SRS type",
  37: "Unknown geometry type found",
  38: "`styleMapValue` has an unknown type",
  39: "Unknown geometry type",
  40: "Expected `feature` to have a geometry",
  41: "Expected an `ol/style/Style` or an array of `ol/style/Style.js`",
  42: "Question unknown, the answer is 42",
  43: "Expected `layers` to be an array or a `Collection`",
  47: "Expected `controls` to be an array or an `ol/Collection`",
  48: "Expected `interactions` to be an array or an `ol/Collection`",
  49: "Expected `overlays` to be an array or an `ol/Collection`",
  50: "`options.featureTypes` should be an Array",
  51: "Either `url` or `tileJSON` options must be provided",
  52: "Unknown `serverType` configured",
  53: "Unknown `tierSizeCalculation` configured",
  55: "The {-y} placeholder requires a tile grid with extent",
  56: "mapBrowserEvent must originate from a pointer event",
  57: "At least 2 conditions are required",
  59: "Invalid command found in the PBF",
  60: "Missing or invalid `size`",
  61: "Cannot determine IIIF Image API version from provided image information JSON",
  62: "A `WebGLArrayBuffer` must either be of type `ELEMENT_ARRAY_BUFFER` or `ARRAY_BUFFER`",
  64: "Layer opacity must be a number",
  66: "`forEachFeatureAtCoordinate` cannot be used on a WebGL layer if the hit detection logic has not been enabled. This is done by providing adequate shaders using the `hitVertexShader` and `hitFragmentShader` properties of `WebGLPointsLayerRenderer`",
  67: "A layer can only be added to the map once. Use either `layer.setMap()` or `map.addLayer()`, not both",
  68: "A VectorTile source can only be rendered if it has a projection compatible with the view projection"
};
class f0 extends Error {
  constructor(t) {
    const e = d0[t];
    super(e), this.code = t, this.name = "AssertionError", this.message = e;
  }
}
const yu = f0, ee = {
  ADD: "add",
  REMOVE: "remove"
}, fh = {
  LENGTH: "length"
};
class dr extends Be {
  constructor(t, e, n) {
    super(t), this.element = e, this.index = n;
  }
}
class g0 extends Ce {
  constructor(t, e) {
    if (super(), this.on, this.once, this.un, e = e || {}, this.unique_ = !!e.unique, this.array_ = t || [], this.unique_)
      for (let n = 0, s = this.array_.length; n < s; ++n)
        this.assertUnique_(this.array_[n], n);
    this.updateLength_();
  }
  clear() {
    for (; this.getLength() > 0; )
      this.pop();
  }
  extend(t) {
    for (let e = 0, n = t.length; e < n; ++e)
      this.push(t[e]);
    return this;
  }
  forEach(t) {
    const e = this.array_;
    for (let n = 0, s = e.length; n < s; ++n)
      t(e[n], n, e);
  }
  getArray() {
    return this.array_;
  }
  item(t) {
    return this.array_[t];
  }
  getLength() {
    return this.get(fh.LENGTH);
  }
  insertAt(t, e) {
    if (t < 0 || t > this.getLength())
      throw new Error("Index out of bounds: " + t);
    this.unique_ && this.assertUnique_(e), this.array_.splice(t, 0, e), this.updateLength_(), this.dispatchEvent(
      new dr(ee.ADD, e, t)
    );
  }
  pop() {
    return this.removeAt(this.getLength() - 1);
  }
  push(t) {
    this.unique_ && this.assertUnique_(t);
    const e = this.getLength();
    return this.insertAt(e, t), this.getLength();
  }
  remove(t) {
    const e = this.array_;
    for (let n = 0, s = e.length; n < s; ++n)
      if (e[n] === t)
        return this.removeAt(n);
  }
  removeAt(t) {
    if (t < 0 || t >= this.getLength())
      return;
    const e = this.array_[t];
    return this.array_.splice(t, 1), this.updateLength_(), this.dispatchEvent(
      new dr(ee.REMOVE, e, t)
    ), e;
  }
  setAt(t, e) {
    const n = this.getLength();
    if (t >= n) {
      this.insertAt(t, e);
      return;
    }
    if (t < 0)
      throw new Error("Index out of bounds: " + t);
    this.unique_ && this.assertUnique_(e, t);
    const s = this.array_[t];
    this.array_[t] = e, this.dispatchEvent(
      new dr(ee.REMOVE, s, t)
    ), this.dispatchEvent(
      new dr(ee.ADD, e, t)
    );
  }
  updateLength_() {
    this.set(fh.LENGTH, this.array_.length);
  }
  assertUnique_(t, e) {
    for (let n = 0, s = this.array_.length; n < s; ++n)
      if (this.array_[n] === t && n !== e)
        throw new yu(58);
  }
}
const Ae = g0, wi = typeof navigator < "u" && typeof navigator.userAgent < "u" ? navigator.userAgent.toLowerCase() : "", m0 = wi.includes("firefox"), p0 = wi.includes("safari") && !wi.includes("chrom");
p0 && (wi.includes("version/15.4") || /cpu (os|iphone os) 15_4 like mac os x/.test(wi));
const _0 = wi.includes("webkit") && !wi.includes("edge"), y0 = wi.includes("macintosh"), vu = typeof devicePixelRatio < "u" ? devicePixelRatio : 1, ja = typeof WorkerGlobalScope < "u" && typeof OffscreenCanvas < "u" && self instanceof WorkerGlobalScope, v0 = typeof Image < "u" && Image.prototype.decode, xu = function() {
  let i = !1;
  try {
    const t = Object.defineProperty({}, "passive", {
      get: function() {
        i = !0;
      }
    });
    window.addEventListener("_", null, t), window.removeEventListener("_", null, t);
  } catch {
  }
  return i;
}();
function Y(i, t) {
  if (!i)
    throw new yu(t);
}
new Array(6);
function Fe() {
  return [1, 0, 0, 1, 0, 0];
}
function x0(i, t) {
  const e = i[0], n = i[1], s = i[2], r = i[3], o = i[4], a = i[5], l = t[0], h = t[1], c = t[2], u = t[3], d = t[4], f = t[5];
  return i[0] = e * l + s * h, i[1] = n * l + r * h, i[2] = e * c + s * u, i[3] = n * c + r * u, i[4] = e * d + s * f + o, i[5] = n * d + r * f + a, i;
}
function C0(i, t, e, n, s, r, o) {
  return i[0] = t, i[1] = e, i[2] = n, i[3] = s, i[4] = r, i[5] = o, i;
}
function M0(i, t) {
  return i[0] = t[0], i[1] = t[1], i[2] = t[2], i[3] = t[3], i[4] = t[4], i[5] = t[5], i;
}
function Ft(i, t) {
  const e = t[0], n = t[1];
  return t[0] = i[0] * e + i[2] * n + i[4], t[1] = i[1] * e + i[3] * n + i[5], t;
}
function E0(i, t, e) {
  return C0(i, t, 0, 0, e, 0, 0);
}
function Si(i, t, e, n, s, r, o, a) {
  const l = Math.sin(r), h = Math.cos(r);
  return i[0] = n * h, i[1] = s * l, i[2] = -n * l, i[3] = s * h, i[4] = o * n * h - a * n * l + t, i[5] = o * s * l + a * s * h + e, i;
}
function Ka(i, t) {
  const e = w0(t);
  Y(e !== 0, 32);
  const n = t[0], s = t[1], r = t[2], o = t[3], a = t[4], l = t[5];
  return i[0] = o / e, i[1] = -s / e, i[2] = -r / e, i[3] = n / e, i[4] = (r * l - o * a) / e, i[5] = -(n * l - s * a) / e, i;
}
function w0(i) {
  return i[0] * i[3] - i[1] * i[2];
}
let gh;
function Cu(i) {
  const t = "matrix(" + i.join(", ") + ")";
  if (ja)
    return t;
  const e = gh || (gh = document.createElement("div"));
  return e.style.transform = t, e.style.transform;
}
const Nt = {
  UNKNOWN: 0,
  INTERSECTING: 1,
  ABOVE: 2,
  RIGHT: 4,
  BELOW: 8,
  LEFT: 16
};
function aa(i) {
  const t = fe();
  for (let e = 0, n = i.length; e < n; ++e)
    gs(t, i[e]);
  return t;
}
function S0(i, t, e) {
  const n = Math.min.apply(null, i), s = Math.min.apply(null, t), r = Math.max.apply(null, i), o = Math.max.apply(null, t);
  return xe(n, s, r, o, e);
}
function co(i, t, e) {
  return e ? (e[0] = i[0] - t, e[1] = i[1] - t, e[2] = i[2] + t, e[3] = i[3] + t, e) : [
    i[0] - t,
    i[1] - t,
    i[2] + t,
    i[3] + t
  ];
}
function Mu(i, t) {
  return t ? (t[0] = i[0], t[1] = i[1], t[2] = i[2], t[3] = i[3], t) : i.slice();
}
function sn(i, t, e) {
  let n, s;
  return t < i[0] ? n = i[0] - t : i[2] < t ? n = t - i[2] : n = 0, e < i[1] ? s = i[1] - e : i[3] < e ? s = e - i[3] : s = 0, n * n + s * s;
}
function uo(i, t) {
  return qa(i, t[0], t[1]);
}
function yi(i, t) {
  return i[0] <= t[0] && t[2] <= i[2] && i[1] <= t[1] && t[3] <= i[3];
}
function qa(i, t, e) {
  return i[0] <= t && t <= i[2] && i[1] <= e && e <= i[3];
}
function la(i, t) {
  const e = i[0], n = i[1], s = i[2], r = i[3], o = t[0], a = t[1];
  let l = Nt.UNKNOWN;
  return o < e ? l = l | Nt.LEFT : o > s && (l = l | Nt.RIGHT), a < n ? l = l | Nt.BELOW : a > r && (l = l | Nt.ABOVE), l === Nt.UNKNOWN && (l = Nt.INTERSECTING), l;
}
function fe() {
  return [1 / 0, 1 / 0, -1 / 0, -1 / 0];
}
function xe(i, t, e, n, s) {
  return s ? (s[0] = i, s[1] = t, s[2] = e, s[3] = n, s) : [i, t, e, n];
}
function Zs(i) {
  return xe(1 / 0, 1 / 0, -1 / 0, -1 / 0, i);
}
function Eu(i, t) {
  const e = i[0], n = i[1];
  return xe(e, n, e, n, t);
}
function wu(i, t, e, n, s) {
  const r = Zs(s);
  return Ru(r, i, t, e, n);
}
function Es(i, t) {
  return i[0] == t[0] && i[2] == t[2] && i[1] == t[1] && i[3] == t[3];
}
function Su(i, t) {
  return t[0] < i[0] && (i[0] = t[0]), t[2] > i[2] && (i[2] = t[2]), t[1] < i[1] && (i[1] = t[1]), t[3] > i[3] && (i[3] = t[3]), i;
}
function gs(i, t) {
  t[0] < i[0] && (i[0] = t[0]), t[0] > i[2] && (i[2] = t[0]), t[1] < i[1] && (i[1] = t[1]), t[1] > i[3] && (i[3] = t[1]);
}
function Ru(i, t, e, n, s) {
  for (; e < n; e += s)
    R0(i, t[e], t[e + 1]);
  return i;
}
function R0(i, t, e) {
  i[0] = Math.min(i[0], t), i[1] = Math.min(i[1], e), i[2] = Math.max(i[2], t), i[3] = Math.max(i[3], e);
}
function bu(i, t) {
  let e;
  return e = t(fo(i)), e || (e = t(go(i)), e) || (e = t(mo(i)), e) || (e = t(Ii(i)), e) ? e : !1;
}
function ha(i) {
  let t = 0;
  return Ja(i) || (t = mt(i) * ke(i)), t;
}
function fo(i) {
  return [i[0], i[1]];
}
function go(i) {
  return [i[2], i[1]];
}
function Ri(i) {
  return [(i[0] + i[2]) / 2, (i[1] + i[3]) / 2];
}
function b0(i, t) {
  let e;
  return t === "bottom-left" ? e = fo(i) : t === "bottom-right" ? e = go(i) : t === "top-left" ? e = Ii(i) : t === "top-right" ? e = mo(i) : Y(!1, 13), e;
}
function ca(i, t, e, n, s) {
  const [r, o, a, l, h, c, u, d] = ua(
    i,
    t,
    e,
    n
  );
  return xe(
    Math.min(r, a, h, u),
    Math.min(o, l, c, d),
    Math.max(r, a, h, u),
    Math.max(o, l, c, d),
    s
  );
}
function ua(i, t, e, n) {
  const s = t * n[0] / 2, r = t * n[1] / 2, o = Math.cos(e), a = Math.sin(e), l = s * o, h = s * a, c = r * o, u = r * a, d = i[0], f = i[1];
  return [
    d - l + u,
    f - h - c,
    d - l - u,
    f - h + c,
    d + l - u,
    f + h + c,
    d + l + u,
    f + h - c,
    d - l + u,
    f - h - c
  ];
}
function ke(i) {
  return i[3] - i[1];
}
function ms(i, t, e) {
  const n = e || fe();
  return ie(i, t) ? (i[0] > t[0] ? n[0] = i[0] : n[0] = t[0], i[1] > t[1] ? n[1] = i[1] : n[1] = t[1], i[2] < t[2] ? n[2] = i[2] : n[2] = t[2], i[3] < t[3] ? n[3] = i[3] : n[3] = t[3]) : Zs(n), n;
}
function Ii(i) {
  return [i[0], i[3]];
}
function mo(i) {
  return [i[2], i[3]];
}
function mt(i) {
  return i[2] - i[0];
}
function ie(i, t) {
  return i[0] <= t[2] && i[2] >= t[0] && i[1] <= t[3] && i[3] >= t[1];
}
function Ja(i) {
  return i[2] < i[0] || i[3] < i[1];
}
function L0(i, t) {
  return t ? (t[0] = i[0], t[1] = i[1], t[2] = i[2], t[3] = i[3], t) : i;
}
function T0(i, t, e) {
  let n = !1;
  const s = la(i, t), r = la(i, e);
  if (s === Nt.INTERSECTING || r === Nt.INTERSECTING)
    n = !0;
  else {
    const o = i[0], a = i[1], l = i[2], h = i[3], c = t[0], u = t[1], d = e[0], f = e[1], g = (f - u) / (d - c);
    let m, p;
    !!(r & Nt.ABOVE) && !(s & Nt.ABOVE) && (m = d - (f - h) / g, n = m >= o && m <= l), !n && !!(r & Nt.RIGHT) && !(s & Nt.RIGHT) && (p = f - (d - l) * g, n = p >= a && p <= h), !n && !!(r & Nt.BELOW) && !(s & Nt.BELOW) && (m = d - (f - a) / g, n = m >= o && m <= l), !n && !!(r & Nt.LEFT) && !(s & Nt.LEFT) && (p = f - (d - o) * g, n = p >= a && p <= h);
  }
  return n;
}
function I0(i, t, e, n) {
  let s = [];
  if (n > 1) {
    const a = i[2] - i[0], l = i[3] - i[1];
    for (let h = 0; h < n; ++h)
      s.push(
        i[0] + a * h / n,
        i[1],
        i[2],
        i[1] + l * h / n,
        i[2] - a * h / n,
        i[3],
        i[0],
        i[3] - l * h / n
      );
  } else
    s = [
      i[0],
      i[1],
      i[2],
      i[1],
      i[2],
      i[3],
      i[0],
      i[3]
    ];
  t(s, s, 2);
  const r = [], o = [];
  for (let a = 0, l = s.length; a < l; a += 2)
    r.push(s[a]), o.push(s[a + 1]);
  return S0(r, o, e);
}
function Lu(i, t) {
  const e = t.getExtent(), n = Ri(i);
  if (t.canWrapX() && (n[0] < e[0] || n[0] >= e[2])) {
    const s = mt(e), o = Math.floor(
      (n[0] - e[0]) / s
    ) * s;
    i[0] -= o, i[2] -= o;
  }
  return i;
}
function P0(i, t) {
  if (t.canWrapX()) {
    const e = t.getExtent();
    if (!isFinite(i[0]) || !isFinite(i[2]))
      return [[e[0], i[1], e[2], i[3]]];
    Lu(i, t);
    const n = mt(e);
    if (mt(i) > n)
      return [[e[0], i[1], e[2], i[3]]];
    if (i[0] < e[0])
      return [
        [i[0] + n, i[1], e[2], i[3]],
        [e[0], i[1], i[2], i[3]]
      ];
    if (i[2] > e[2])
      return [
        [i[0], i[1], e[2], i[3]],
        [e[0], i[1], i[2] - n, i[3]]
      ];
  }
  return [i];
}
function wt(i, t, e) {
  return Math.min(Math.max(i, t), e);
}
function A0(i, t, e, n, s, r) {
  const o = s - e, a = r - n;
  if (o !== 0 || a !== 0) {
    const l = ((i - e) * o + (t - n) * a) / (o * o + a * a);
    l > 1 ? (e = s, n = r) : l > 0 && (e += o * l, n += a * l);
  }
  return Vi(i, t, e, n);
}
function Vi(i, t, e, n) {
  const s = e - i, r = n - t;
  return s * s + r * r;
}
function O0(i) {
  const t = i.length;
  for (let n = 0; n < t; n++) {
    let s = n, r = Math.abs(i[n][n]);
    for (let a = n + 1; a < t; a++) {
      const l = Math.abs(i[a][n]);
      l > r && (r = l, s = a);
    }
    if (r === 0)
      return null;
    const o = i[s];
    i[s] = i[n], i[n] = o;
    for (let a = n + 1; a < t; a++) {
      const l = -i[a][n] / i[n][n];
      for (let h = n; h < t + 1; h++)
        n == h ? i[a][h] = 0 : i[a][h] += l * i[n][h];
    }
  }
  const e = new Array(t);
  for (let n = t - 1; n >= 0; n--) {
    e[n] = i[n][t] / i[n][n];
    for (let s = n - 1; s >= 0; s--)
      i[s][t] -= i[s][n] * e[n];
  }
  return e;
}
function mh(i) {
  return i * 180 / Math.PI;
}
function Ui(i) {
  return i * Math.PI / 180;
}
function An(i, t) {
  const e = i % t;
  return e * t < 0 ? e + t : e;
}
function Je(i, t, e) {
  return i + e * (t - i);
}
function Tu(i, t) {
  const e = Math.pow(10, t);
  return Math.round(i * e) / e;
}
function fr(i, t) {
  return Math.floor(Tu(i, t));
}
function gr(i, t) {
  return Math.ceil(Tu(i, t));
}
const N0 = /^#([a-f0-9]{3}|[a-f0-9]{4}(?:[a-f0-9]{2}){0,2})$/i, F0 = /^([a-z]*)$|^hsla?\(.*\)$/i;
function Iu(i) {
  return typeof i == "string" ? i : Pu(i);
}
function D0(i) {
  const t = document.createElement("div");
  if (t.style.color = i, t.style.color !== "") {
    document.body.appendChild(t);
    const e = getComputedStyle(t).color;
    return document.body.removeChild(t), e;
  } else
    return "";
}
const k0 = function() {
  const t = {};
  let e = 0;
  return function(n) {
    let s;
    if (t.hasOwnProperty(n))
      s = t[n];
    else {
      if (e >= 1024) {
        let r = 0;
        for (const o in t)
          (r++ & 3) === 0 && (delete t[o], --e);
      }
      s = G0(n), t[n] = s, ++e;
    }
    return s;
  };
}();
function kr(i) {
  return Array.isArray(i) ? i : k0(i);
}
function G0(i) {
  let t, e, n, s, r;
  if (F0.exec(i) && (i = D0(i)), N0.exec(i)) {
    const o = i.length - 1;
    let a;
    o <= 4 ? a = 1 : a = 2;
    const l = o === 4 || o === 8;
    t = parseInt(i.substr(1 + 0 * a, a), 16), e = parseInt(i.substr(1 + 1 * a, a), 16), n = parseInt(i.substr(1 + 2 * a, a), 16), l ? s = parseInt(i.substr(1 + 3 * a, a), 16) : s = 255, a == 1 && (t = (t << 4) + t, e = (e << 4) + e, n = (n << 4) + n, l && (s = (s << 4) + s)), r = [t, e, n, s / 255];
  } else
    i.startsWith("rgba(") ? (r = i.slice(5, -1).split(",").map(Number), ph(r)) : i.startsWith("rgb(") ? (r = i.slice(4, -1).split(",").map(Number), r.push(1), ph(r)) : Y(!1, 14);
  return r;
}
function ph(i) {
  return i[0] = wt(i[0] + 0.5 | 0, 0, 255), i[1] = wt(i[1] + 0.5 | 0, 0, 255), i[2] = wt(i[2] + 0.5 | 0, 0, 255), i[3] = wt(i[3], 0, 1), i;
}
function Pu(i) {
  let t = i[0];
  t != (t | 0) && (t = t + 0.5 | 0);
  let e = i[1];
  e != (e | 0) && (e = e + 0.5 | 0);
  let n = i[2];
  n != (n | 0) && (n = n + 0.5 | 0);
  const s = i[3] === void 0 ? 1 : Math.round(i[3] * 100) / 100;
  return "rgba(" + t + "," + e + "," + n + "," + s + ")";
}
class $0 {
  constructor() {
    this.cache_ = {}, this.cacheSize_ = 0, this.maxCacheSize_ = 32;
  }
  clear() {
    this.cache_ = {}, this.cacheSize_ = 0;
  }
  canExpireCache() {
    return this.cacheSize_ > this.maxCacheSize_;
  }
  expire() {
    if (this.canExpireCache()) {
      let t = 0;
      for (const e in this.cache_) {
        const n = this.cache_[e];
        (t++ & 3) === 0 && !n.hasListener() && (delete this.cache_[e], --this.cacheSize_);
      }
    }
  }
  get(t, e, n) {
    const s = _h(t, e, n);
    return s in this.cache_ ? this.cache_[s] : null;
  }
  set(t, e, n, s) {
    const r = _h(t, e, n);
    this.cache_[r] = s, ++this.cacheSize_;
  }
  setSize(t) {
    this.maxCacheSize_ = t, this.expire();
  }
}
function _h(i, t, e) {
  const n = e ? Iu(e) : "null";
  return t + ":" + i + ":" + n;
}
const Gr = new $0(), dt = {
  OPACITY: "opacity",
  VISIBLE: "visible",
  EXTENT: "extent",
  Z_INDEX: "zIndex",
  MAX_RESOLUTION: "maxResolution",
  MIN_RESOLUTION: "minResolution",
  MAX_ZOOM: "maxZoom",
  MIN_ZOOM: "minZoom",
  SOURCE: "source",
  MAP: "map"
};
class B0 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, this.background_ = t.background;
    const e = Object.assign({}, t);
    typeof t.properties == "object" && (delete e.properties, Object.assign(e, t.properties)), e[dt.OPACITY] = t.opacity !== void 0 ? t.opacity : 1, Y(typeof e[dt.OPACITY] == "number", 64), e[dt.VISIBLE] = t.visible !== void 0 ? t.visible : !0, e[dt.Z_INDEX] = t.zIndex, e[dt.MAX_RESOLUTION] = t.maxResolution !== void 0 ? t.maxResolution : 1 / 0, e[dt.MIN_RESOLUTION] = t.minResolution !== void 0 ? t.minResolution : 0, e[dt.MIN_ZOOM] = t.minZoom !== void 0 ? t.minZoom : -1 / 0, e[dt.MAX_ZOOM] = t.maxZoom !== void 0 ? t.maxZoom : 1 / 0, this.className_ = e.className !== void 0 ? e.className : "ol-layer", delete e.className, this.setProperties(e), this.state_ = null;
  }
  getBackground() {
    return this.background_;
  }
  getClassName() {
    return this.className_;
  }
  getLayerState(t) {
    const e = this.state_ || {
      layer: this,
      managed: t === void 0 ? !0 : t
    }, n = this.getZIndex();
    return e.opacity = wt(Math.round(this.getOpacity() * 100) / 100, 0, 1), e.visible = this.getVisible(), e.extent = this.getExtent(), e.zIndex = n === void 0 && !e.managed ? 1 / 0 : n, e.maxResolution = this.getMaxResolution(), e.minResolution = Math.max(this.getMinResolution(), 0), e.minZoom = this.getMinZoom(), e.maxZoom = this.getMaxZoom(), this.state_ = e, e;
  }
  getLayersArray(t) {
    return W();
  }
  getLayerStatesArray(t) {
    return W();
  }
  getExtent() {
    return this.get(dt.EXTENT);
  }
  getMaxResolution() {
    return this.get(dt.MAX_RESOLUTION);
  }
  getMinResolution() {
    return this.get(dt.MIN_RESOLUTION);
  }
  getMinZoom() {
    return this.get(dt.MIN_ZOOM);
  }
  getMaxZoom() {
    return this.get(dt.MAX_ZOOM);
  }
  getOpacity() {
    return this.get(dt.OPACITY);
  }
  getSourceState() {
    return W();
  }
  getVisible() {
    return this.get(dt.VISIBLE);
  }
  getZIndex() {
    return this.get(dt.Z_INDEX);
  }
  setBackground(t) {
    this.background_ = t, this.changed();
  }
  setExtent(t) {
    this.set(dt.EXTENT, t);
  }
  setMaxResolution(t) {
    this.set(dt.MAX_RESOLUTION, t);
  }
  setMinResolution(t) {
    this.set(dt.MIN_RESOLUTION, t);
  }
  setMaxZoom(t) {
    this.set(dt.MAX_ZOOM, t);
  }
  setMinZoom(t) {
    this.set(dt.MIN_ZOOM, t);
  }
  setOpacity(t) {
    Y(typeof t == "number", 64), this.set(dt.OPACITY, t);
  }
  setVisible(t) {
    this.set(dt.VISIBLE, t);
  }
  setZIndex(t) {
    this.set(dt.Z_INDEX, t);
  }
  disposeInternal() {
    this.state_ && (this.state_.layer = null, this.state_ = null), super.disposeInternal();
  }
}
const Au = B0, Ci = {
  PRERENDER: "prerender",
  POSTRENDER: "postrender",
  PRECOMPOSE: "precompose",
  POSTCOMPOSE: "postcompose",
  RENDERCOMPLETE: "rendercomplete"
};
class z0 extends Au {
  constructor(t) {
    const e = Object.assign({}, t);
    delete e.source, super(e), this.on, this.once, this.un, this.mapPrecomposeKey_ = null, this.mapRenderKey_ = null, this.sourceChangeKey_ = null, this.renderer_ = null, this.rendered = !1, t.render && (this.render = t.render), t.map && this.setMap(t.map), this.addChangeListener(
      dt.SOURCE,
      this.handleSourcePropertyChange_
    );
    const n = t.source ? t.source : null;
    this.setSource(n);
  }
  getLayersArray(t) {
    return t = t || [], t.push(this), t;
  }
  getLayerStatesArray(t) {
    return t = t || [], t.push(this.getLayerState()), t;
  }
  getSource() {
    return this.get(dt.SOURCE) || null;
  }
  getRenderSource() {
    return this.getSource();
  }
  getSourceState() {
    const t = this.getSource();
    return t ? t.getState() : "undefined";
  }
  handleSourceChange_() {
    this.changed();
  }
  handleSourcePropertyChange_() {
    this.sourceChangeKey_ && (pt(this.sourceChangeKey_), this.sourceChangeKey_ = null);
    const t = this.getSource();
    t && (this.sourceChangeKey_ = et(
      t,
      X.CHANGE,
      this.handleSourceChange_,
      this
    )), this.changed();
  }
  getFeatures(t) {
    return this.renderer_ ? this.renderer_.getFeatures(t) : new Promise((e) => e([]));
  }
  getData(t) {
    return !this.renderer_ || !this.rendered ? null : this.renderer_.getData(t);
  }
  render(t, e) {
    const n = this.getRenderer();
    if (n.prepareFrame(t))
      return this.rendered = !0, n.renderFrame(t, e);
  }
  unrender() {
    this.rendered = !1;
  }
  setMapInternal(t) {
    t || this.unrender(), this.set(dt.MAP, t);
  }
  getMapInternal() {
    return this.get(dt.MAP);
  }
  setMap(t) {
    this.mapPrecomposeKey_ && (pt(this.mapPrecomposeKey_), this.mapPrecomposeKey_ = null), t || this.changed(), this.mapRenderKey_ && (pt(this.mapRenderKey_), this.mapRenderKey_ = null), t && (this.mapPrecomposeKey_ = et(
      t,
      Ci.PRECOMPOSE,
      function(e) {
        const s = e.frameState.layerStatesArray, r = this.getLayerState(!1);
        Y(
          !s.some(function(o) {
            return o.layer === r.layer;
          }),
          67
        ), s.push(r);
      },
      this
    ), this.mapRenderKey_ = et(this, X.CHANGE, t.render, t), this.changed());
  }
  setSource(t) {
    this.set(dt.SOURCE, t);
  }
  getRenderer() {
    return this.renderer_ || (this.renderer_ = this.createRenderer()), this.renderer_;
  }
  hasRenderer() {
    return !!this.renderer_;
  }
  createRenderer() {
    return null;
  }
  disposeInternal() {
    this.renderer_ && (this.renderer_.dispose(), delete this.renderer_), this.setSource(null), super.disposeInternal();
  }
}
function Qa(i, t) {
  if (!i.visible)
    return !1;
  const e = t.resolution;
  if (e < i.minResolution || e >= i.maxResolution)
    return !1;
  const n = t.zoom;
  return n > i.minZoom && n <= i.maxZoom;
}
const po = z0;
function Ou(i, t) {
  return i[0] += +t[0], i[1] += +t[1], i;
}
function $r(i, t) {
  let e = !0;
  for (let n = i.length - 1; n >= 0; --n)
    if (i[n] != t[n]) {
      e = !1;
      break;
    }
  return e;
}
function tl(i, t) {
  const e = Math.cos(t), n = Math.sin(t), s = i[0] * e - i[1] * n, r = i[1] * e + i[0] * n;
  return i[0] = s, i[1] = r, i;
}
function Nu(i, t) {
  return i[0] *= t, i[1] *= t, i;
}
function Fu(i, t) {
  if (t.canWrapX()) {
    const e = mt(t.getExtent()), n = Du(i, t, e);
    n && (i[0] -= n * e);
  }
  return i;
}
function Du(i, t, e) {
  const n = t.getExtent();
  let s = 0;
  return t.canWrapX() && (i[0] < n[0] || i[0] > n[2]) && (e = e || mt(n), s = Math.floor(
    (i[0] - n[0]) / e
  )), s;
}
class Z0 extends Xa {
  constructor(t) {
    super(), this.map_ = t;
  }
  dispatchRenderEvent(t, e) {
    W();
  }
  calculateMatrices2D(t) {
    const e = t.viewState, n = t.coordinateToPixelTransform, s = t.pixelToCoordinateTransform;
    Si(
      n,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / e.resolution,
      -1 / e.resolution,
      -e.rotation,
      -e.center[0],
      -e.center[1]
    ), Ka(s, n);
  }
  forEachFeatureAtCoordinate(t, e, n, s, r, o, a, l) {
    let h;
    const c = e.viewState;
    function u(x, C, w, S) {
      return r.call(o, C, x ? w : null, S);
    }
    const d = c.projection, f = Fu(t.slice(), d), g = [[0, 0]];
    if (d.canWrapX() && s) {
      const x = d.getExtent(), C = mt(x);
      g.push([-C, 0], [C, 0]);
    }
    const m = e.layerStatesArray, p = m.length, _ = [], y = [];
    for (let x = 0; x < g.length; x++)
      for (let C = p - 1; C >= 0; --C) {
        const w = m[C], S = w.layer;
        if (S.hasRenderer() && Qa(w, c) && a.call(l, S)) {
          const b = S.getRenderer(), A = S.getSource();
          if (b && A) {
            const G = A.getWrapX() ? f : t, V = u.bind(
              null,
              w.managed
            );
            y[0] = G[0] + g[x][0], y[1] = G[1] + g[x][1], h = b.forEachFeatureAtCoordinate(
              y,
              e,
              n,
              V,
              _
            );
          }
          if (h)
            return h;
        }
      }
    if (_.length === 0)
      return;
    const v = 1 / _.length;
    return _.forEach((x, C) => x.distanceSq += C * v), _.sort((x, C) => x.distanceSq - C.distanceSq), _.some((x) => h = x.callback(x.feature, x.layer, x.geometry)), h;
  }
  hasFeatureAtCoordinate(t, e, n, s, r, o) {
    return this.forEachFeatureAtCoordinate(
      t,
      e,
      n,
      s,
      Ms,
      this,
      r,
      o
    ) !== void 0;
  }
  getMap() {
    return this.map_;
  }
  renderFrame(t) {
    W();
  }
  scheduleExpireIconCache(t) {
    Gr.canExpireCache() && t.postRenderFunctions.push(V0);
  }
}
function V0(i, t) {
  Gr.expire();
}
const U0 = Z0;
class W0 extends Be {
  constructor(t, e, n, s) {
    super(t), this.inversePixelTransform = e, this.frameState = n, this.context = s;
  }
}
const ku = W0, mr = "ol-hidden", H0 = "ol-selectable", Yn = "ol-unselectable", yh = "ol-unsupported", _o = "ol-control", vh = "ol-collapsed", X0 = new RegExp(
  [
    "^\\s*(?=(?:(?:[-a-z]+\\s*){0,2}(italic|oblique))?)",
    "(?=(?:(?:[-a-z]+\\s*){0,2}(small-caps))?)",
    "(?=(?:(?:[-a-z]+\\s*){0,2}(bold(?:er)?|lighter|[1-9]00 ))?)",
    "(?:(?:normal|\\1|\\2|\\3)\\s*){0,3}((?:xx?-)?",
    "(?:small|large)|medium|smaller|larger|[\\.\\d]+(?:\\%|in|[cem]m|ex|p[ctx]))",
    "(?:\\s*\\/\\s*(normal|[\\.\\d]+(?:\\%|in|[cem]m|ex|p[ctx])?))",
    `?\\s*([-,\\"\\'\\sa-z]+?)\\s*$`
  ].join(""),
  "i"
), xh = [
  "style",
  "variant",
  "weight",
  "size",
  "lineHeight",
  "family"
], Gu = function(i) {
  const t = i.match(X0);
  if (!t)
    return null;
  const e = {
    lineHeight: "normal",
    size: "1.2em",
    style: "normal",
    weight: "normal",
    variant: "normal"
  };
  for (let n = 0, s = xh.length; n < s; ++n) {
    const r = t[n + 1];
    r !== void 0 && (e[xh[n]] = r);
  }
  return e.families = e.family.split(/,\s?/), e;
};
function ge(i, t, e, n) {
  let s;
  return e && e.length ? s = e.shift() : ja ? s = new OffscreenCanvas(i || 300, t || 300) : s = document.createElement("canvas"), i && (s.width = i), t && (s.height = t), s.getContext("2d", n);
}
function $u(i) {
  const t = i.canvas;
  t.width = 1, t.height = 1, i.clearRect(0, 0, 1, 1);
}
function Y0(i) {
  let t = i.offsetWidth;
  const e = getComputedStyle(i);
  return t += parseInt(e.marginLeft, 10) + parseInt(e.marginRight, 10), t;
}
function j0(i) {
  let t = i.offsetHeight;
  const e = getComputedStyle(i);
  return t += parseInt(e.marginTop, 10) + parseInt(e.marginBottom, 10), t;
}
function Br(i, t) {
  const e = t.parentNode;
  e && e.replaceChild(i, t);
}
function zr(i) {
  return i && i.parentNode ? i.parentNode.removeChild(i) : null;
}
function Bu(i) {
  for (; i.lastChild; )
    i.removeChild(i.lastChild);
}
function K0(i, t) {
  const e = i.childNodes;
  for (let n = 0; ; ++n) {
    const s = e[n], r = t[n];
    if (!s && !r)
      break;
    if (s !== r) {
      if (!s) {
        i.appendChild(r);
        continue;
      }
      if (!r) {
        i.removeChild(s), --n;
        continue;
      }
      i.insertBefore(r, s);
    }
  }
}
const zu = "10px sans-serif", ii = "#000", Zr = "round", ws = [], Ss = 0, $n = "round", Rs = 10, bs = "#000", Ls = "center", Vr = "middle", ki = [0, 0, 0, 0], Ts = 1, je = new Ce();
let xn = null, da;
const fa = {}, q0 = function() {
  const t = "32px ", e = ["monospace", "serif"], n = e.length, s = "wmytzilWMYTZIL@#/&?$%10\uF013";
  let r, o;
  function a(h, c, u) {
    let d = !0;
    for (let f = 0; f < n; ++f) {
      const g = e[f];
      if (o = Ur(
        h + " " + c + " " + t + g,
        s
      ), u != g) {
        const m = Ur(
          h + " " + c + " " + t + u + "," + g,
          s
        );
        d = d && m != o;
      }
    }
    return !!d;
  }
  function l() {
    let h = !0;
    const c = je.getKeys();
    for (let u = 0, d = c.length; u < d; ++u) {
      const f = c[u];
      je.get(f) < 100 && (a.apply(this, f.split(`
`)) ? (zs(fa), xn = null, da = void 0, je.set(f, 100)) : (je.set(f, je.get(f) + 1, !0), h = !1));
    }
    h && (clearInterval(r), r = void 0);
  }
  return function(h) {
    const c = Gu(h);
    if (!c)
      return;
    const u = c.families;
    for (let d = 0, f = u.length; d < f; ++d) {
      const g = u[d], m = c.style + `
` + c.weight + `
` + g;
      je.get(m) === void 0 && (je.set(m, 100, !0), a(c.style, c.weight, g) || (je.set(m, 0, !0), r === void 0 && (r = setInterval(l, 32))));
    }
  };
}(), J0 = function() {
  let i;
  return function(t) {
    let e = fa[t];
    if (e == null) {
      if (ja) {
        const n = Gu(t), s = Zu(t, "\u017Dg");
        e = (isNaN(Number(n.lineHeight)) ? 1.2 : Number(n.lineHeight)) * (s.actualBoundingBoxAscent + s.actualBoundingBoxDescent);
      } else
        i || (i = document.createElement("div"), i.innerHTML = "M", i.style.minHeight = "0", i.style.maxHeight = "none", i.style.height = "auto", i.style.padding = "0", i.style.border = "none", i.style.position = "absolute", i.style.display = "block", i.style.left = "-99999px"), i.style.font = t, document.body.appendChild(i), e = i.offsetHeight, document.body.removeChild(i);
      fa[t] = e;
    }
    return e;
  };
}();
function Zu(i, t) {
  return xn || (xn = ge(1, 1)), i != da && (xn.font = i, da = xn.font), xn.measureText(t);
}
function Ur(i, t) {
  return Zu(i, t).width;
}
function Ch(i, t, e) {
  if (t in e)
    return e[t];
  const n = t.split(`
`).reduce((s, r) => Math.max(s, Ur(i, r)), 0);
  return e[t] = n, n;
}
function Q0(i, t) {
  const e = [], n = [], s = [];
  let r = 0, o = 0, a = 0, l = 0;
  for (let h = 0, c = t.length; h <= c; h += 2) {
    const u = t[h];
    if (u === `
` || h === c) {
      r = Math.max(r, o), s.push(o), o = 0, a += l;
      continue;
    }
    const d = t[h + 1] || i.font, f = Ur(d, u);
    e.push(f), o += f;
    const g = J0(d);
    n.push(g), l = Math.max(l, g);
  }
  return { width: r, height: a, widths: e, heights: n, lineWidths: s };
}
function tg(i, t, e, n, s, r, o, a, l, h, c) {
  i.save(), e !== 1 && (i.globalAlpha *= e), t && i.setTransform.apply(i, t), n.contextInstructions ? (i.translate(l, h), i.scale(c[0], c[1]), eg(n, i)) : c[0] < 0 || c[1] < 0 ? (i.translate(l, h), i.scale(c[0], c[1]), i.drawImage(
    n,
    s,
    r,
    o,
    a,
    0,
    0,
    o,
    a
  )) : i.drawImage(
    n,
    s,
    r,
    o,
    a,
    l,
    h,
    o * c[0],
    a * c[1]
  ), i.restore();
}
function eg(i, t) {
  const e = i.contextInstructions;
  for (let n = 0, s = e.length; n < s; n += 2)
    Array.isArray(e[n + 1]) ? t[e[n]].apply(
      t,
      e[n + 1]
    ) : t[e[n]] = e[n + 1];
}
class ig extends U0 {
  constructor(t) {
    super(t), this.fontChangeListenerKey_ = et(
      je,
      kn.PROPERTYCHANGE,
      t.redrawText.bind(t)
    ), this.element_ = document.createElement("div");
    const e = this.element_.style;
    e.position = "absolute", e.width = "100%", e.height = "100%", e.zIndex = "0", this.element_.className = Yn + " ol-layers";
    const n = t.getViewport();
    n.insertBefore(this.element_, n.firstChild || null), this.children_ = [], this.renderedVisible_ = !0;
  }
  dispatchRenderEvent(t, e) {
    const n = this.getMap();
    if (n.hasListener(t)) {
      const s = new ku(t, void 0, e);
      n.dispatchEvent(s);
    }
  }
  disposeInternal() {
    pt(this.fontChangeListenerKey_), this.element_.parentNode.removeChild(this.element_), super.disposeInternal();
  }
  renderFrame(t) {
    if (!t) {
      this.renderedVisible_ && (this.element_.style.display = "none", this.renderedVisible_ = !1);
      return;
    }
    this.calculateMatrices2D(t), this.dispatchRenderEvent(Ci.PRECOMPOSE, t);
    const e = t.layerStatesArray.sort(function(o, a) {
      return o.zIndex - a.zIndex;
    }), n = t.viewState;
    this.children_.length = 0;
    const s = [];
    let r = null;
    for (let o = 0, a = e.length; o < a; ++o) {
      const l = e[o];
      t.layerIndex = o;
      const h = l.layer, c = h.getSourceState();
      if (!Qa(l, n) || c != "ready" && c != "undefined") {
        h.unrender();
        continue;
      }
      const u = h.render(t, r);
      !u || (u !== r && (this.children_.push(u), r = u), "getDeclutter" in h && s.push(
        h
      ));
    }
    for (let o = s.length - 1; o >= 0; --o)
      s[o].renderDeclutter(t);
    K0(this.element_, this.children_), this.dispatchRenderEvent(Ci.POSTCOMPOSE, t), this.renderedVisible_ || (this.element_.style.display = "", this.renderedVisible_ = !0), this.scheduleExpireIconCache(t);
  }
}
const ng = ig;
class _i extends Be {
  constructor(t, e) {
    super(t), this.layer = e;
  }
}
const Zo = {
  LAYERS: "layers"
};
class el extends Au {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.layers;
    let n = t.layers;
    super(e), this.on, this.once, this.un, this.layersListenerKeys_ = [], this.listenerKeys_ = {}, this.addChangeListener(Zo.LAYERS, this.handleLayersChanged_), n ? Array.isArray(n) ? n = new Ae(n.slice(), { unique: !0 }) : Y(typeof n.getArray == "function", 43) : n = new Ae(void 0, { unique: !0 }), this.setLayers(n);
  }
  handleLayerChange_() {
    this.changed();
  }
  handleLayersChanged_() {
    this.layersListenerKeys_.forEach(pt), this.layersListenerKeys_.length = 0;
    const t = this.getLayers();
    this.layersListenerKeys_.push(
      et(t, ee.ADD, this.handleLayersAdd_, this),
      et(t, ee.REMOVE, this.handleLayersRemove_, this)
    );
    for (const n in this.listenerKeys_)
      this.listenerKeys_[n].forEach(pt);
    zs(this.listenerKeys_);
    const e = t.getArray();
    for (let n = 0, s = e.length; n < s; n++) {
      const r = e[n];
      this.registerLayerListeners_(r), this.dispatchEvent(new _i("addlayer", r));
    }
    this.changed();
  }
  registerLayerListeners_(t) {
    const e = [
      et(
        t,
        kn.PROPERTYCHANGE,
        this.handleLayerChange_,
        this
      ),
      et(t, X.CHANGE, this.handleLayerChange_, this)
    ];
    t instanceof el && e.push(
      et(t, "addlayer", this.handleLayerGroupAdd_, this),
      et(t, "removelayer", this.handleLayerGroupRemove_, this)
    ), this.listenerKeys_[ot(t)] = e;
  }
  handleLayerGroupAdd_(t) {
    this.dispatchEvent(new _i("addlayer", t.layer));
  }
  handleLayerGroupRemove_(t) {
    this.dispatchEvent(new _i("removelayer", t.layer));
  }
  handleLayersAdd_(t) {
    const e = t.element;
    this.registerLayerListeners_(e), this.dispatchEvent(new _i("addlayer", e)), this.changed();
  }
  handleLayersRemove_(t) {
    const e = t.element, n = ot(e);
    this.listenerKeys_[n].forEach(pt), delete this.listenerKeys_[n], this.dispatchEvent(new _i("removelayer", e)), this.changed();
  }
  getLayers() {
    return this.get(Zo.LAYERS);
  }
  setLayers(t) {
    const e = this.getLayers();
    if (e) {
      const n = e.getArray();
      for (let s = 0, r = n.length; s < r; ++s)
        this.dispatchEvent(new _i("removelayer", n[s]));
    }
    this.set(Zo.LAYERS, t);
  }
  getLayersArray(t) {
    return t = t !== void 0 ? t : [], this.getLayers().forEach(function(e) {
      e.getLayersArray(t);
    }), t;
  }
  getLayerStatesArray(t) {
    const e = t !== void 0 ? t : [], n = e.length;
    this.getLayers().forEach(function(o) {
      o.getLayerStatesArray(e);
    });
    const s = this.getLayerState();
    let r = s.zIndex;
    !t && s.zIndex === void 0 && (r = 0);
    for (let o = n, a = e.length; o < a; o++) {
      const l = e[o];
      l.opacity *= s.opacity, l.visible = l.visible && s.visible, l.maxResolution = Math.min(
        l.maxResolution,
        s.maxResolution
      ), l.minResolution = Math.max(
        l.minResolution,
        s.minResolution
      ), l.minZoom = Math.max(l.minZoom, s.minZoom), l.maxZoom = Math.min(l.maxZoom, s.maxZoom), s.extent !== void 0 && (l.extent !== void 0 ? l.extent = ms(
        l.extent,
        s.extent
      ) : l.extent = s.extent), l.zIndex === void 0 && (l.zIndex = r);
    }
    return e;
  }
  getSourceState() {
    return "ready";
  }
}
const yo = el;
class sg extends Be {
  constructor(t, e, n) {
    super(t), this.map = e, this.frameState = n !== void 0 ? n : null;
  }
}
const Cn = sg;
class rg extends Cn {
  constructor(t, e, n, s, r, o) {
    super(t, e, r), this.originalEvent = n, this.pixel_ = null, this.coordinate_ = null, this.dragging = s !== void 0 ? s : !1, this.activePointers = o;
  }
  get pixel() {
    return this.pixel_ || (this.pixel_ = this.map.getEventPixel(this.originalEvent)), this.pixel_;
  }
  set pixel(t) {
    this.pixel_ = t;
  }
  get coordinate() {
    return this.coordinate_ || (this.coordinate_ = this.map.getCoordinateFromPixel(this.pixel)), this.coordinate_;
  }
  set coordinate(t) {
    this.coordinate_ = t;
  }
  preventDefault() {
    super.preventDefault(), "preventDefault" in this.originalEvent && this.originalEvent.preventDefault();
  }
  stopPropagation() {
    super.stopPropagation(), "stopPropagation" in this.originalEvent && this.originalEvent.stopPropagation();
  }
}
const mi = rg, Mt = {
  SINGLECLICK: "singleclick",
  CLICK: X.CLICK,
  DBLCLICK: X.DBLCLICK,
  POINTERDRAG: "pointerdrag",
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
}, ga = {
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
};
class og extends lo {
  constructor(t, e) {
    super(t), this.map_ = t, this.clickTimeoutId_, this.emulateClicks_ = !1, this.dragging_ = !1, this.dragListenerKeys_ = [], this.moveTolerance_ = e === void 0 ? 1 : e, this.down_ = null;
    const n = this.map_.getViewport();
    this.activePointers_ = [], this.trackedTouches_ = {}, this.element_ = n, this.pointerdownListenerKey_ = et(
      n,
      ga.POINTERDOWN,
      this.handlePointerDown_,
      this
    ), this.originalPointerMoveEvent_, this.relayedListenerKey_ = et(
      n,
      ga.POINTERMOVE,
      this.relayMoveEvent_,
      this
    ), this.boundHandleTouchMove_ = this.handleTouchMove_.bind(this), this.element_.addEventListener(
      X.TOUCHMOVE,
      this.boundHandleTouchMove_,
      xu ? { passive: !1 } : !1
    );
  }
  emulateClick_(t) {
    let e = new mi(
      Mt.CLICK,
      this.map_,
      t
    );
    this.dispatchEvent(e), this.clickTimeoutId_ !== void 0 ? (clearTimeout(this.clickTimeoutId_), this.clickTimeoutId_ = void 0, e = new mi(
      Mt.DBLCLICK,
      this.map_,
      t
    ), this.dispatchEvent(e)) : this.clickTimeoutId_ = setTimeout(
      function() {
        this.clickTimeoutId_ = void 0;
        const n = new mi(
          Mt.SINGLECLICK,
          this.map_,
          t
        );
        this.dispatchEvent(n);
      }.bind(this),
      250
    );
  }
  updateActivePointers_(t) {
    const e = t, n = e.pointerId;
    if (e.type == Mt.POINTERUP || e.type == Mt.POINTERCANCEL) {
      delete this.trackedTouches_[n];
      for (const s in this.trackedTouches_)
        if (this.trackedTouches_[s].target !== e.target) {
          delete this.trackedTouches_[s];
          break;
        }
    } else
      (e.type == Mt.POINTERDOWN || e.type == Mt.POINTERMOVE) && (this.trackedTouches_[n] = e);
    this.activePointers_ = Object.values(this.trackedTouches_);
  }
  handlePointerUp_(t) {
    this.updateActivePointers_(t);
    const e = new mi(
      Mt.POINTERUP,
      this.map_,
      t,
      void 0,
      void 0,
      this.activePointers_
    );
    this.dispatchEvent(e), this.emulateClicks_ && !e.defaultPrevented && !this.dragging_ && this.isMouseActionButton_(t) && this.emulateClick_(this.down_), this.activePointers_.length === 0 && (this.dragListenerKeys_.forEach(pt), this.dragListenerKeys_.length = 0, this.dragging_ = !1, this.down_ = null);
  }
  isMouseActionButton_(t) {
    return t.button === 0;
  }
  handlePointerDown_(t) {
    this.emulateClicks_ = this.activePointers_.length === 0, this.updateActivePointers_(t);
    const e = new mi(
      Mt.POINTERDOWN,
      this.map_,
      t,
      void 0,
      void 0,
      this.activePointers_
    );
    this.dispatchEvent(e), this.down_ = {};
    for (const n in t) {
      const s = t[n];
      this.down_[n] = typeof s == "function" ? ji : s;
    }
    if (this.dragListenerKeys_.length === 0) {
      const n = this.map_.getOwnerDocument();
      this.dragListenerKeys_.push(
        et(
          n,
          Mt.POINTERMOVE,
          this.handlePointerMove_,
          this
        ),
        et(n, Mt.POINTERUP, this.handlePointerUp_, this),
        et(
          this.element_,
          Mt.POINTERCANCEL,
          this.handlePointerUp_,
          this
        )
      ), this.element_.getRootNode && this.element_.getRootNode() !== n && this.dragListenerKeys_.push(
        et(
          this.element_.getRootNode(),
          Mt.POINTERUP,
          this.handlePointerUp_,
          this
        )
      );
    }
  }
  handlePointerMove_(t) {
    if (this.isMoving_(t)) {
      this.updateActivePointers_(t), this.dragging_ = !0;
      const e = new mi(
        Mt.POINTERDRAG,
        this.map_,
        t,
        this.dragging_,
        void 0,
        this.activePointers_
      );
      this.dispatchEvent(e);
    }
  }
  relayMoveEvent_(t) {
    this.originalPointerMoveEvent_ = t;
    const e = !!(this.down_ && this.isMoving_(t));
    this.dispatchEvent(
      new mi(
        Mt.POINTERMOVE,
        this.map_,
        t,
        e
      )
    );
  }
  handleTouchMove_(t) {
    const e = this.originalPointerMoveEvent_;
    (!e || e.defaultPrevented) && (typeof t.cancelable != "boolean" || t.cancelable === !0) && t.preventDefault();
  }
  isMoving_(t) {
    return this.dragging_ || Math.abs(t.clientX - this.down_.clientX) > this.moveTolerance_ || Math.abs(t.clientY - this.down_.clientY) > this.moveTolerance_;
  }
  disposeInternal() {
    this.relayedListenerKey_ && (pt(this.relayedListenerKey_), this.relayedListenerKey_ = null), this.element_.removeEventListener(
      X.TOUCHMOVE,
      this.boundHandleTouchMove_
    ), this.pointerdownListenerKey_ && (pt(this.pointerdownListenerKey_), this.pointerdownListenerKey_ = null), this.dragListenerKeys_.forEach(pt), this.dragListenerKeys_.length = 0, this.element_ = null, super.disposeInternal();
  }
}
const ag = og, qe = {
  POSTRENDER: "postrender",
  MOVESTART: "movestart",
  MOVEEND: "moveend",
  LOADSTART: "loadstart",
  LOADEND: "loadend"
}, Ot = {
  LAYERGROUP: "layergroup",
  SIZE: "size",
  TARGET: "target",
  VIEW: "view"
}, Wr = 1 / 0;
class lg {
  constructor(t, e) {
    this.priorityFunction_ = t, this.keyFunction_ = e, this.elements_ = [], this.priorities_ = [], this.queuedElements_ = {};
  }
  clear() {
    this.elements_.length = 0, this.priorities_.length = 0, zs(this.queuedElements_);
  }
  dequeue() {
    const t = this.elements_, e = this.priorities_, n = t[0];
    t.length == 1 ? (t.length = 0, e.length = 0) : (t[0] = t.pop(), e[0] = e.pop(), this.siftUp_(0));
    const s = this.keyFunction_(n);
    return delete this.queuedElements_[s], n;
  }
  enqueue(t) {
    Y(!(this.keyFunction_(t) in this.queuedElements_), 31);
    const e = this.priorityFunction_(t);
    return e != Wr ? (this.elements_.push(t), this.priorities_.push(e), this.queuedElements_[this.keyFunction_(t)] = !0, this.siftDown_(0, this.elements_.length - 1), !0) : !1;
  }
  getCount() {
    return this.elements_.length;
  }
  getLeftChildIndex_(t) {
    return t * 2 + 1;
  }
  getRightChildIndex_(t) {
    return t * 2 + 2;
  }
  getParentIndex_(t) {
    return t - 1 >> 1;
  }
  heapify_() {
    let t;
    for (t = (this.elements_.length >> 1) - 1; t >= 0; t--)
      this.siftUp_(t);
  }
  isEmpty() {
    return this.elements_.length === 0;
  }
  isKeyQueued(t) {
    return t in this.queuedElements_;
  }
  isQueued(t) {
    return this.isKeyQueued(this.keyFunction_(t));
  }
  siftUp_(t) {
    const e = this.elements_, n = this.priorities_, s = e.length, r = e[t], o = n[t], a = t;
    for (; t < s >> 1; ) {
      const l = this.getLeftChildIndex_(t), h = this.getRightChildIndex_(t), c = h < s && n[h] < n[l] ? h : l;
      e[t] = e[c], n[t] = n[c], t = c;
    }
    e[t] = r, n[t] = o, this.siftDown_(a, t);
  }
  siftDown_(t, e) {
    const n = this.elements_, s = this.priorities_, r = n[e], o = s[e];
    for (; e > t; ) {
      const a = this.getParentIndex_(e);
      if (s[a] > o)
        n[e] = n[a], s[e] = s[a], e = a;
      else
        break;
    }
    n[e] = r, s[e] = o;
  }
  reprioritize() {
    const t = this.priorityFunction_, e = this.elements_, n = this.priorities_;
    let s = 0;
    const r = e.length;
    let o, a, l;
    for (a = 0; a < r; ++a)
      o = e[a], l = t(o), l == Wr ? delete this.queuedElements_[this.keyFunction_(o)] : (n[s] = l, e[s++] = o);
    e.length = s, n.length = s, this.heapify_();
  }
}
const hg = lg, z = {
  IDLE: 0,
  LOADING: 1,
  LOADED: 2,
  ERROR: 3,
  EMPTY: 4
};
class cg extends hg {
  constructor(t, e) {
    super(
      function(n) {
        return t.apply(null, n);
      },
      function(n) {
        return n[0].getKey();
      }
    ), this.boundHandleTileChange_ = this.handleTileChange.bind(this), this.tileChangeCallback_ = e, this.tilesLoading_ = 0, this.tilesLoadingKeys_ = {};
  }
  enqueue(t) {
    const e = super.enqueue(t);
    return e && t[0].addEventListener(X.CHANGE, this.boundHandleTileChange_), e;
  }
  getTilesLoading() {
    return this.tilesLoading_;
  }
  handleTileChange(t) {
    const e = t.target, n = e.getState();
    if (n === z.LOADED || n === z.ERROR || n === z.EMPTY) {
      n !== z.ERROR && e.removeEventListener(X.CHANGE, this.boundHandleTileChange_);
      const s = e.getKey();
      s in this.tilesLoadingKeys_ && (delete this.tilesLoadingKeys_[s], --this.tilesLoading_), this.tileChangeCallback_();
    }
  }
  loadMoreTiles(t, e) {
    let n = 0, s, r, o;
    for (; this.tilesLoading_ < t && n < e && this.getCount() > 0; )
      r = this.dequeue()[0], o = r.getKey(), s = r.getState(), s === z.IDLE && !(o in this.tilesLoadingKeys_) && (this.tilesLoadingKeys_[o] = !0, ++this.tilesLoading_, ++n, r.load());
  }
}
const ug = cg;
function dg(i, t, e, n, s) {
  if (!i || !(e in i.wantedTiles) || !i.wantedTiles[e][t.getKey()])
    return Wr;
  const r = i.viewState.center, o = n[0] - r[0], a = n[1] - r[1];
  return 65536 * Math.log(s) + Math.sqrt(o * o + a * a) / s;
}
const Zt = {
  ANIMATING: 0,
  INTERACTING: 1
}, Ee = {
  CENTER: "center",
  RESOLUTION: "resolution",
  ROTATION: "rotation"
}, fg = 42, il = 256, Bn = {
  radians: 6370997 / (2 * Math.PI),
  degrees: 2 * Math.PI * 6370997 / 360,
  ft: 0.3048,
  m: 1,
  "us-ft": 1200 / 3937
};
class gg {
  constructor(t) {
    this.code_ = t.code, this.units_ = t.units, this.extent_ = t.extent !== void 0 ? t.extent : null, this.worldExtent_ = t.worldExtent !== void 0 ? t.worldExtent : null, this.axisOrientation_ = t.axisOrientation !== void 0 ? t.axisOrientation : "enu", this.global_ = t.global !== void 0 ? t.global : !1, this.canWrapX_ = !!(this.global_ && this.extent_), this.getPointResolutionFunc_ = t.getPointResolution, this.defaultTileGrid_ = null, this.metersPerUnit_ = t.metersPerUnit;
  }
  canWrapX() {
    return this.canWrapX_;
  }
  getCode() {
    return this.code_;
  }
  getExtent() {
    return this.extent_;
  }
  getUnits() {
    return this.units_;
  }
  getMetersPerUnit() {
    return this.metersPerUnit_ || Bn[this.units_];
  }
  getWorldExtent() {
    return this.worldExtent_;
  }
  getAxisOrientation() {
    return this.axisOrientation_;
  }
  isGlobal() {
    return this.global_;
  }
  setGlobal(t) {
    this.global_ = t, this.canWrapX_ = !!(t && this.extent_);
  }
  getDefaultTileGrid() {
    return this.defaultTileGrid_;
  }
  setDefaultTileGrid(t) {
    this.defaultTileGrid_ = t;
  }
  setExtent(t) {
    this.extent_ = t, this.canWrapX_ = !!(this.global_ && t);
  }
  setWorldExtent(t) {
    this.worldExtent_ = t;
  }
  setGetPointResolution(t) {
    this.getPointResolutionFunc_ = t;
  }
  getPointResolutionFunc() {
    return this.getPointResolutionFunc_;
  }
}
const nl = gg, Vs = 6378137, Sn = Math.PI * Vs, mg = [-Sn, -Sn, Sn, Sn], pg = [-180, -85, 180, 85], pr = Vs * Math.log(Math.tan(Math.PI / 2));
class gn extends nl {
  constructor(t) {
    super({
      code: t,
      units: "m",
      extent: mg,
      global: !0,
      worldExtent: pg,
      getPointResolution: function(e, n) {
        return e / Math.cosh(n[1] / Vs);
      }
    });
  }
}
const Mh = [
  new gn("EPSG:3857"),
  new gn("EPSG:102100"),
  new gn("EPSG:102113"),
  new gn("EPSG:900913"),
  new gn("http://www.opengis.net/def/crs/EPSG/0/3857"),
  new gn("http://www.opengis.net/gml/srs/epsg.xml#3857")
];
function _g(i, t, e) {
  const n = i.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = i.slice() : t = new Array(n));
  for (let s = 0; s < n; s += e) {
    t[s] = Sn * i[s] / 180;
    let r = Vs * Math.log(Math.tan(Math.PI * (+i[s + 1] + 90) / 360));
    r > pr ? r = pr : r < -pr && (r = -pr), t[s + 1] = r;
  }
  return t;
}
function yg(i, t, e) {
  const n = i.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = i.slice() : t = new Array(n));
  for (let s = 0; s < n; s += e)
    t[s] = 180 * i[s] / Sn, t[s + 1] = 360 * Math.atan(Math.exp(i[s + 1] / Vs)) / Math.PI - 90;
  return t;
}
const vg = 6378137, Eh = [-180, -90, 180, 90], xg = Math.PI * vg / 180;
class Ni extends nl {
  constructor(t, e) {
    super({
      code: t,
      units: "degrees",
      extent: Eh,
      axisOrientation: e,
      global: !0,
      metersPerUnit: xg,
      worldExtent: Eh
    });
  }
}
const wh = [
  new Ni("CRS:84"),
  new Ni("EPSG:4326", "neu"),
  new Ni("urn:ogc:def:crs:OGC:1.3:CRS84"),
  new Ni("urn:ogc:def:crs:OGC:2:84"),
  new Ni("http://www.opengis.net/def/crs/OGC/1.3/CRS84"),
  new Ni("http://www.opengis.net/gml/srs/epsg.xml#4326", "neu"),
  new Ni("http://www.opengis.net/def/crs/EPSG/0/4326", "neu")
];
let ma = {};
function Cg(i) {
  return ma[i] || ma[i.replace(/urn:(x-)?ogc:def:crs:EPSG:(.*:)?(\w+)$/, "EPSG:$3")] || null;
}
function Mg(i, t) {
  ma[i] = t;
}
let On = {};
function zn(i, t, e) {
  const n = i.getCode(), s = t.getCode();
  n in On || (On[n] = {}), On[n][s] = e;
}
function Vu(i, t) {
  let e;
  return i in On && t in On[i] && (e = On[i][t]), e;
}
const Uu = 63710088e-1;
function Sh(i, t, e) {
  e = e || Uu;
  const n = Ui(i[1]), s = Ui(t[1]), r = (s - n) / 2, o = Ui(t[0] - i[0]) / 2, a = Math.sin(r) * Math.sin(r) + Math.sin(o) * Math.sin(o) * Math.cos(n) * Math.cos(s);
  return 2 * e * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
function Eg(i, t, e, n) {
  n = n || Uu;
  const s = Ui(i[1]), r = Ui(i[0]), o = t / n, a = Math.asin(
    Math.sin(s) * Math.cos(o) + Math.cos(s) * Math.sin(o) * Math.cos(e)
  ), l = r + Math.atan2(
    Math.sin(e) * Math.sin(o) * Math.cos(s),
    Math.cos(o) - Math.sin(s) * Math.sin(a)
  );
  return [mh(l), mh(a)];
}
let pa = !0;
function Wu(i) {
  pa = !(i === void 0 ? !0 : i);
}
function sl(i, t, e) {
  if (t !== void 0) {
    for (let n = 0, s = i.length; n < s; ++n)
      t[n] = i[n];
    t = t;
  } else
    t = i.slice();
  return t;
}
function rl(i, t, e) {
  if (t !== void 0 && i !== t) {
    for (let n = 0, s = i.length; n < s; ++n)
      t[n] = i[n];
    i = t;
  }
  return i;
}
function Hu(i) {
  Mg(i.getCode(), i), zn(i, i, sl);
}
function wg(i) {
  i.forEach(Hu);
}
function J(i) {
  return typeof i == "string" ? Cg(i) : i || null;
}
function Hr(i, t, e, n) {
  i = J(i);
  let s;
  const r = i.getPointResolutionFunc();
  if (r) {
    if (s = r(t, e), n && n !== i.getUnits()) {
      const o = i.getMetersPerUnit();
      o && (s = s * o / Bn[n]);
    }
  } else {
    const o = i.getUnits();
    if (o == "degrees" && !n || n == "degrees")
      s = t;
    else {
      const a = vo(
        i,
        J("EPSG:4326")
      );
      if (a === rl && o !== "degrees")
        s = t * i.getMetersPerUnit();
      else {
        let h = [
          e[0] - t / 2,
          e[1],
          e[0] + t / 2,
          e[1],
          e[0],
          e[1] - t / 2,
          e[0],
          e[1] + t / 2
        ];
        h = a(h, h, 2);
        const c = Sh(h.slice(0, 2), h.slice(2, 4)), u = Sh(h.slice(4, 6), h.slice(6, 8));
        s = (c + u) / 2;
      }
      const l = n ? Bn[n] : i.getMetersPerUnit();
      l !== void 0 && (s /= l);
    }
  }
  return s;
}
function _a(i) {
  wg(i), i.forEach(function(t) {
    i.forEach(function(e) {
      t !== e && zn(t, e, sl);
    });
  });
}
function Sg(i, t, e, n) {
  i.forEach(function(s) {
    t.forEach(function(r) {
      zn(s, r, e), zn(r, s, n);
    });
  });
}
function ol(i, t) {
  return i ? typeof i == "string" ? J(i) : i : J(t);
}
function Rh(i) {
  return function(t, e, n) {
    const s = t.length;
    n = n !== void 0 ? n : 2, e = e !== void 0 ? e : new Array(s);
    for (let r = 0; r < s; r += n) {
      const o = i(t.slice(r, r + n)), a = o.length;
      for (let l = 0, h = n; l < h; ++l)
        e[r + l] = l >= a ? t[r + l] : o[l];
    }
    return e;
  };
}
function Rg(i, t, e, n) {
  const s = J(i), r = J(t);
  zn(
    s,
    r,
    Rh(e)
  ), zn(
    r,
    s,
    Rh(n)
  );
}
function bg(i, t) {
  return Wu(), Xu(
    i,
    "EPSG:4326",
    t !== void 0 ? t : "EPSG:3857"
  );
}
function Ie(i, t) {
  if (i === t)
    return !0;
  const e = i.getUnits() === t.getUnits();
  return (i.getCode() === t.getCode() || vo(i, t) === sl) && e;
}
function vo(i, t) {
  const e = i.getCode(), n = t.getCode();
  let s = Vu(e, n);
  return s || (s = rl), s;
}
function Is(i, t) {
  const e = J(i), n = J(t);
  return vo(e, n);
}
function Xu(i, t, e) {
  return Is(t, e)(i, void 0, i.length);
}
function Yu(i, t, e, n) {
  const s = Is(t, e);
  return I0(i, s, void 0, n);
}
function ya(i, t) {
  return i;
}
function Ke(i, t) {
  return pa && !$r(i, [0, 0]) && i[0] >= -180 && i[0] <= 180 && i[1] >= -90 && i[1] <= 90 && (pa = !1, console.warn(
    "Call useGeographic() from ol/proj once to work with [longitude, latitude] coordinates."
  )), i;
}
function ju(i, t) {
  return i;
}
function Gi(i, t) {
  return i;
}
function bh(i, t, e) {
  return function(n) {
    let s, r;
    if (i.canWrapX()) {
      const o = i.getExtent(), a = mt(o);
      n = n.slice(0), r = Du(n, i, a), r && (n[0] = n[0] - r * a), n[0] = wt(n[0], o[0], o[2]), n[1] = wt(n[1], o[1], o[3]), s = e(n);
    } else
      s = e(n);
    return r && t.canWrapX() && (s[0] += r * mt(t.getExtent())), s;
  };
}
function Lg() {
  _a(Mh), _a(wh), Sg(
    wh,
    Mh,
    _g,
    yg
  );
}
Lg();
function Lh(i, t, e) {
  return function(n, s, r, o, a) {
    if (!n)
      return;
    if (!s && !t)
      return n;
    const l = t ? 0 : r[0] * s, h = t ? 0 : r[1] * s, c = a ? a[0] : 0, u = a ? a[1] : 0;
    let d = i[0] + l / 2 + c, f = i[2] - l / 2 + c, g = i[1] + h / 2 + u, m = i[3] - h / 2 + u;
    d > f && (d = (f + d) / 2, f = d), g > m && (g = (m + g) / 2, m = g);
    let p = wt(n[0], d, f), _ = wt(n[1], g, m);
    if (o && e && s) {
      const y = 30 * s;
      p += -y * Math.log(1 + Math.max(0, d - n[0]) / y) + y * Math.log(1 + Math.max(0, n[0] - f) / y), _ += -y * Math.log(1 + Math.max(0, g - n[1]) / y) + y * Math.log(1 + Math.max(0, n[1] - m) / y);
    }
    return [p, _];
  };
}
function Tg(i) {
  return i;
}
function al(i, t, e, n) {
  const s = mt(t) / e[0], r = ke(t) / e[1];
  return n ? Math.min(i, Math.max(s, r)) : Math.min(i, Math.min(s, r));
}
function ll(i, t, e) {
  let n = Math.min(i, t);
  const s = 50;
  return n *= Math.log(1 + s * Math.max(0, i / t - 1)) / s + 1, e && (n = Math.max(n, e), n /= Math.log(1 + s * Math.max(0, e / i - 1)) / s + 1), wt(n, e / 2, t * 2);
}
function Ig(i, t, e, n) {
  return t = t !== void 0 ? t : !0, function(s, r, o, a) {
    if (s !== void 0) {
      const l = i[0], h = i[i.length - 1], c = e ? al(
        l,
        e,
        o,
        n
      ) : l;
      if (a)
        return t ? ll(
          s,
          c,
          h
        ) : wt(s, h, c);
      const u = Math.min(c, s), d = Math.floor(Ya(i, u, r));
      return i[d] > c && d < i.length - 1 ? i[d + 1] : i[d];
    } else
      return;
  };
}
function Pg(i, t, e, n, s, r) {
  return n = n !== void 0 ? n : !0, e = e !== void 0 ? e : 0, function(o, a, l, h) {
    if (o !== void 0) {
      const c = s ? al(
        t,
        s,
        l,
        r
      ) : t;
      if (h)
        return n ? ll(
          o,
          c,
          e
        ) : wt(o, e, c);
      const u = 1e-9, d = Math.ceil(
        Math.log(t / c) / Math.log(i) - u
      ), f = -a * (0.5 - u) + 0.5, g = Math.min(c, o), m = Math.floor(
        Math.log(t / g) / Math.log(i) + f
      ), p = Math.max(d, m), _ = t / Math.pow(i, p);
      return wt(_, e, c);
    } else
      return;
  };
}
function Th(i, t, e, n, s) {
  return e = e !== void 0 ? e : !0, function(r, o, a, l) {
    if (r !== void 0) {
      const h = n ? al(
        i,
        n,
        a,
        s
      ) : i;
      return !e || !l ? wt(r, t, h) : ll(
        r,
        h,
        t
      );
    } else
      return;
  };
}
function hl(i) {
  if (i !== void 0)
    return 0;
}
function Ih(i) {
  if (i !== void 0)
    return i;
}
function Ag(i) {
  const t = 2 * Math.PI / i;
  return function(e, n) {
    if (n)
      return e;
    if (e !== void 0)
      return e = Math.floor(e / t + 0.5) * t, e;
  };
}
function Og(i) {
  return i = i || Ui(5), function(t, e) {
    if (e)
      return t;
    if (t !== void 0)
      return Math.abs(t) <= i ? 0 : t;
  };
}
function Ku(i) {
  return Math.pow(i, 3);
}
function jn(i) {
  return 1 - Ku(1 - i);
}
function Ng(i) {
  return 3 * i * i - 2 * i * i * i;
}
function Fg(i) {
  return i;
}
function Wi(i, t, e, n, s, r) {
  r = r || [];
  let o = 0;
  for (let a = t; a < e; a += n) {
    const l = i[a], h = i[a + 1];
    r[o++] = s[0] * l + s[2] * h + s[4], r[o++] = s[1] * l + s[3] * h + s[5];
  }
  return r && r.length != o && (r.length = o), r;
}
function qu(i, t, e, n, s, r, o) {
  o = o || [];
  const a = Math.cos(s), l = Math.sin(s), h = r[0], c = r[1];
  let u = 0;
  for (let d = t; d < e; d += n) {
    const f = i[d] - h, g = i[d + 1] - c;
    o[u++] = h + f * a - g * l, o[u++] = c + f * l + g * a;
    for (let m = d + 2; m < d + n; ++m)
      o[u++] = i[m];
  }
  return o && o.length != u && (o.length = u), o;
}
function Dg(i, t, e, n, s, r, o, a) {
  a = a || [];
  const l = o[0], h = o[1];
  let c = 0;
  for (let u = t; u < e; u += n) {
    const d = i[u] - l, f = i[u + 1] - h;
    a[c++] = l + s * d, a[c++] = h + r * f;
    for (let g = u + 2; g < u + n; ++g)
      a[c++] = i[g];
  }
  return a && a.length != c && (a.length = c), a;
}
function kg(i, t, e, n, s, r, o) {
  o = o || [];
  let a = 0;
  for (let l = t; l < e; l += n) {
    o[a++] = i[l] + s, o[a++] = i[l + 1] + r;
    for (let h = l + 2; h < l + n; ++h)
      o[a++] = i[h];
  }
  return o && o.length != a && (o.length = a), o;
}
const Ph = Fe();
class Gg extends Ce {
  constructor() {
    super(), this.extent_ = fe(), this.extentRevision_ = -1, this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = 0, this.simplifyTransformedInternal = a0(function(t, e, n) {
      if (!n)
        return this.getSimplifiedGeometry(e);
      const s = this.clone();
      return s.applyTransform(n), s.getSimplifiedGeometry(e);
    });
  }
  simplifyTransformed(t, e) {
    return this.simplifyTransformedInternal(
      this.getRevision(),
      t,
      e
    );
  }
  clone() {
    return W();
  }
  closestPointXY(t, e, n, s) {
    return W();
  }
  containsXY(t, e) {
    const n = this.getClosestPoint([t, e]);
    return n[0] === t && n[1] === e;
  }
  getClosestPoint(t, e) {
    return e = e || [NaN, NaN], this.closestPointXY(t[0], t[1], e, 1 / 0), e;
  }
  intersectsCoordinate(t) {
    return this.containsXY(t[0], t[1]);
  }
  computeExtent(t) {
    return W();
  }
  getExtent(t) {
    if (this.extentRevision_ != this.getRevision()) {
      const e = this.computeExtent(this.extent_);
      (isNaN(e[0]) || isNaN(e[1])) && Zs(e), this.extentRevision_ = this.getRevision();
    }
    return L0(this.extent_, t);
  }
  rotate(t, e) {
    W();
  }
  scale(t, e, n) {
    W();
  }
  simplify(t) {
    return this.getSimplifiedGeometry(t * t);
  }
  getSimplifiedGeometry(t) {
    return W();
  }
  getType() {
    return W();
  }
  applyTransform(t) {
    W();
  }
  intersectsExtent(t) {
    return W();
  }
  translate(t, e) {
    W();
  }
  transform(t, e) {
    const n = J(t), s = n.getUnits() == "tile-pixels" ? function(r, o, a) {
      const l = n.getExtent(), h = n.getWorldExtent(), c = ke(h) / ke(l);
      return Si(
        Ph,
        h[0],
        h[3],
        c,
        -c,
        0,
        0,
        0
      ), Wi(
        r,
        0,
        r.length,
        a,
        Ph,
        o
      ), Is(n, e)(
        r,
        o,
        a
      );
    } : Is(n, e);
    return this.applyTransform(s), this;
  }
}
const Ju = Gg;
class $g extends Ju {
  constructor() {
    super(), this.layout = "XY", this.stride = 2, this.flatCoordinates = null;
  }
  computeExtent(t) {
    return wu(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinates() {
    return W();
  }
  getFirstCoordinate() {
    return this.flatCoordinates.slice(0, this.stride);
  }
  getFlatCoordinates() {
    return this.flatCoordinates;
  }
  getLastCoordinate() {
    return this.flatCoordinates.slice(
      this.flatCoordinates.length - this.stride
    );
  }
  getLayout() {
    return this.layout;
  }
  getSimplifiedGeometry(t) {
    if (this.simplifiedGeometryRevision !== this.getRevision() && (this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = this.getRevision()), t < 0 || this.simplifiedGeometryMaxMinSquaredTolerance !== 0 && t <= this.simplifiedGeometryMaxMinSquaredTolerance)
      return this;
    const e = this.getSimplifiedGeometryInternal(t);
    return e.getFlatCoordinates().length < this.flatCoordinates.length ? e : (this.simplifiedGeometryMaxMinSquaredTolerance = t, this);
  }
  getSimplifiedGeometryInternal(t) {
    return this;
  }
  getStride() {
    return this.stride;
  }
  setFlatCoordinates(t, e) {
    this.stride = Ah(t), this.layout = t, this.flatCoordinates = e;
  }
  setCoordinates(t, e) {
    W();
  }
  setLayout(t, e, n) {
    let s;
    if (t)
      s = Ah(t);
    else {
      for (let r = 0; r < n; ++r)
        if (e.length === 0) {
          this.layout = "XY", this.stride = 2;
          return;
        } else
          e = e[0];
      s = e.length, t = Bg(s);
    }
    this.layout = t, this.stride = s;
  }
  applyTransform(t) {
    this.flatCoordinates && (t(this.flatCoordinates, this.flatCoordinates, this.stride), this.changed());
  }
  rotate(t, e) {
    const n = this.getFlatCoordinates();
    if (n) {
      const s = this.getStride();
      qu(
        n,
        0,
        n.length,
        s,
        t,
        e,
        n
      ), this.changed();
    }
  }
  scale(t, e, n) {
    e === void 0 && (e = t), n || (n = Ri(this.getExtent()));
    const s = this.getFlatCoordinates();
    if (s) {
      const r = this.getStride();
      Dg(
        s,
        0,
        s.length,
        r,
        t,
        e,
        n,
        s
      ), this.changed();
    }
  }
  translate(t, e) {
    const n = this.getFlatCoordinates();
    if (n) {
      const s = this.getStride();
      kg(
        n,
        0,
        n.length,
        s,
        t,
        e,
        n
      ), this.changed();
    }
  }
}
function Bg(i) {
  let t;
  return i == 2 ? t = "XY" : i == 3 ? t = "XYZ" : i == 4 && (t = "XYZM"), t;
}
function Ah(i) {
  let t;
  return i == "XY" ? t = 2 : i == "XYZ" || i == "XYM" ? t = 3 : i == "XYZM" && (t = 4), t;
}
function zg(i, t, e) {
  const n = i.getFlatCoordinates();
  if (n) {
    const s = i.getStride();
    return Wi(
      n,
      0,
      n.length,
      s,
      t,
      e
    );
  } else
    return null;
}
const rn = $g;
function Oh(i, t, e, n, s, r, o) {
  const a = i[t], l = i[t + 1], h = i[e] - a, c = i[e + 1] - l;
  let u;
  if (h === 0 && c === 0)
    u = t;
  else {
    const d = ((s - a) * h + (r - l) * c) / (h * h + c * c);
    if (d > 1)
      u = e;
    else if (d > 0) {
      for (let f = 0; f < n; ++f)
        o[f] = Je(
          i[t + f],
          i[e + f],
          d
        );
      o.length = n;
      return;
    } else
      u = t;
  }
  for (let d = 0; d < n; ++d)
    o[d] = i[u + d];
  o.length = n;
}
function cl(i, t, e, n, s) {
  let r = i[t], o = i[t + 1];
  for (t += n; t < e; t += n) {
    const a = i[t], l = i[t + 1], h = Vi(r, o, a, l);
    h > s && (s = h), r = a, o = l;
  }
  return s;
}
function ul(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s = cl(i, t, a, n, s), t = a;
  }
  return s;
}
function Zg(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s = ul(i, t, a, n, s), t = a[a.length - 1];
  }
  return s;
}
function dl(i, t, e, n, s, r, o, a, l, h, c) {
  if (t == e)
    return h;
  let u, d;
  if (s === 0)
    if (d = Vi(
      o,
      a,
      i[t],
      i[t + 1]
    ), d < h) {
      for (u = 0; u < n; ++u)
        l[u] = i[t + u];
      return l.length = n, d;
    } else
      return h;
  c = c || [NaN, NaN];
  let f = t + n;
  for (; f < e; )
    if (Oh(
      i,
      f - n,
      f,
      n,
      o,
      a,
      c
    ), d = Vi(o, a, c[0], c[1]), d < h) {
      for (h = d, u = 0; u < n; ++u)
        l[u] = c[u];
      l.length = n, f += n;
    } else
      f += n * Math.max(
        (Math.sqrt(d) - Math.sqrt(h)) / s | 0,
        1
      );
  if (r && (Oh(
    i,
    e - n,
    t,
    n,
    o,
    a,
    c
  ), d = Vi(o, a, c[0], c[1]), d < h)) {
    for (h = d, u = 0; u < n; ++u)
      l[u] = c[u];
    l.length = n;
  }
  return h;
}
function fl(i, t, e, n, s, r, o, a, l, h, c) {
  c = c || [NaN, NaN];
  for (let u = 0, d = e.length; u < d; ++u) {
    const f = e[u];
    h = dl(
      i,
      t,
      f,
      n,
      s,
      r,
      o,
      a,
      l,
      h,
      c
    ), t = f;
  }
  return h;
}
function Vg(i, t, e, n, s, r, o, a, l, h, c) {
  c = c || [NaN, NaN];
  for (let u = 0, d = e.length; u < d; ++u) {
    const f = e[u];
    h = fl(
      i,
      t,
      f,
      n,
      s,
      r,
      o,
      a,
      l,
      h,
      c
    ), t = f[f.length - 1];
  }
  return h;
}
function Ug(i, t, e, n) {
  for (let s = 0, r = e.length; s < r; ++s)
    i[t++] = e[s];
  return t;
}
function xo(i, t, e, n) {
  for (let s = 0, r = e.length; s < r; ++s) {
    const o = e[s];
    for (let a = 0; a < n; ++a)
      i[t++] = o[a];
  }
  return t;
}
function gl(i, t, e, n, s) {
  s = s || [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = xo(
      i,
      t,
      e[o],
      n
    );
    s[r++] = l, t = l;
  }
  return s.length = r, s;
}
function Wg(i, t, e, n, s) {
  s = s || [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = gl(
      i,
      t,
      e[o],
      n,
      s[r]
    );
    l.length === 0 && (l[0] = t), s[r++] = l, t = l[l.length - 1];
  }
  return s.length = r, s;
}
function ml(i, t, e, n, s, r, o) {
  const a = (e - t) / n;
  if (a < 3) {
    for (; t < e; t += n)
      r[o++] = i[t], r[o++] = i[t + 1];
    return o;
  }
  const l = new Array(a);
  l[0] = 1, l[a - 1] = 1;
  const h = [t, e - n];
  let c = 0;
  for (; h.length > 0; ) {
    const u = h.pop(), d = h.pop();
    let f = 0;
    const g = i[d], m = i[d + 1], p = i[u], _ = i[u + 1];
    for (let y = d + n; y < u; y += n) {
      const v = i[y], x = i[y + 1], C = A0(v, x, g, m, p, _);
      C > f && (c = y, f = C);
    }
    f > s && (l[(c - t) / n] = 1, d + n < c && h.push(d, c), c + n < u && h.push(c, u));
  }
  for (let u = 0; u < a; ++u)
    l[u] && (r[o++] = i[t + u * n], r[o++] = i[t + u * n + 1]);
  return o;
}
function Hg(i, t, e, n, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    o = ml(
      i,
      t,
      c,
      n,
      s,
      r,
      o
    ), a.push(o), t = c;
  }
  return o;
}
function Di(i, t) {
  return t * Math.round(i / t);
}
function Xg(i, t, e, n, s, r, o) {
  if (t == e)
    return o;
  let a = Di(i[t], s), l = Di(i[t + 1], s);
  t += n, r[o++] = a, r[o++] = l;
  let h, c;
  do
    if (h = Di(i[t], s), c = Di(i[t + 1], s), t += n, t == e)
      return r[o++] = h, r[o++] = c, o;
  while (h == a && c == l);
  for (; t < e; ) {
    const u = Di(i[t], s), d = Di(i[t + 1], s);
    if (t += n, u == h && d == c)
      continue;
    const f = h - a, g = c - l, m = u - a, p = d - l;
    if (f * p == g * m && (f < 0 && m < f || f == m || f > 0 && m > f) && (g < 0 && p < g || g == p || g > 0 && p > g)) {
      h = u, c = d;
      continue;
    }
    r[o++] = h, r[o++] = c, a = h, l = c, h = u, c = d;
  }
  return r[o++] = h, r[o++] = c, o;
}
function Qu(i, t, e, n, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    o = Xg(
      i,
      t,
      c,
      n,
      s,
      r,
      o
    ), a.push(o), t = c;
  }
  return o;
}
function Yg(i, t, e, n, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l], u = [];
    o = Qu(
      i,
      t,
      c,
      n,
      s,
      r,
      o,
      u
    ), a.push(u), t = c[c.length - 1];
  }
  return o;
}
function vi(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = t; o < e; o += n)
    s[r++] = i.slice(o, o + n);
  return s.length = r, s;
}
function Ps(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = vi(
      i,
      t,
      l,
      n,
      s[r]
    ), t = l;
  }
  return s.length = r, s;
}
function va(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = l.length === 1 && l[0] === t ? [] : Ps(
      i,
      t,
      l,
      n,
      s[r]
    ), t = l[l.length - 1];
  }
  return s.length = r, s;
}
function td(i, t, e, n) {
  let s = 0, r = i[e - n], o = i[e - n + 1];
  for (; t < e; t += n) {
    const a = i[t], l = i[t + 1];
    s += o * a - r * l, r = a, o = l;
  }
  return s / 2;
}
function ed(i, t, e, n) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += td(i, t, a, n), t = a;
  }
  return s;
}
function jg(i, t, e, n) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += ed(i, t, a, n), t = a[a.length - 1];
  }
  return s;
}
class Xr extends rn {
  constructor(t, e) {
    super(), this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, e !== void 0 && !Array.isArray(t[0]) ? this.setFlatCoordinates(
      e,
      t
    ) : this.setCoordinates(
      t,
      e
    );
  }
  clone() {
    return new Xr(this.flatCoordinates.slice(), this.layout);
  }
  closestPointXY(t, e, n, s) {
    return s < sn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      cl(
        this.flatCoordinates,
        0,
        this.flatCoordinates.length,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), dl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      n,
      s
    ));
  }
  getArea() {
    return td(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinates() {
    return vi(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getSimplifiedGeometryInternal(t) {
    const e = [];
    return e.length = ml(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e,
      0
    ), new Xr(e, "XY");
  }
  getType() {
    return "LinearRing";
  }
  intersectsExtent(t) {
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = xo(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const xa = Xr;
class pl extends rn {
  constructor(t, e) {
    super(), this.setCoordinates(t, e);
  }
  clone() {
    const t = new pl(this.flatCoordinates.slice(), this.layout);
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    const r = this.flatCoordinates, o = Vi(
      t,
      e,
      r[0],
      r[1]
    );
    if (o < s) {
      const a = this.stride;
      for (let l = 0; l < a; ++l)
        n[l] = r[l];
      return n.length = a, o;
    } else
      return s;
  }
  getCoordinates() {
    return this.flatCoordinates ? this.flatCoordinates.slice() : [];
  }
  computeExtent(t) {
    return Eu(this.flatCoordinates, t);
  }
  getType() {
    return "Point";
  }
  intersectsExtent(t) {
    return qa(t, this.flatCoordinates[0], this.flatCoordinates[1]);
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 0), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Ug(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const si = pl;
function Kg(i, t, e, n, s) {
  return !bu(
    s,
    function(o) {
      return !$i(
        i,
        t,
        e,
        n,
        o[0],
        o[1]
      );
    }
  );
}
function $i(i, t, e, n, s, r) {
  let o = 0, a = i[e - n], l = i[e - n + 1];
  for (; t < e; t += n) {
    const h = i[t], c = i[t + 1];
    l <= r ? c > r && (h - a) * (r - l) - (s - a) * (c - l) > 0 && o++ : c <= r && (h - a) * (r - l) - (s - a) * (c - l) < 0 && o--, a = h, l = c;
  }
  return o !== 0;
}
function _l(i, t, e, n, s, r) {
  if (e.length === 0 || !$i(i, t, e[0], n, s, r))
    return !1;
  for (let o = 1, a = e.length; o < a; ++o)
    if ($i(i, e[o - 1], e[o], n, s, r))
      return !1;
  return !0;
}
function qg(i, t, e, n, s, r) {
  if (e.length === 0)
    return !1;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    if (_l(i, t, l, n, s, r))
      return !0;
    t = l[l.length - 1];
  }
  return !1;
}
function id(i, t, e, n, s, r, o) {
  let a, l, h, c, u, d, f;
  const g = s[r + 1], m = [];
  for (let y = 0, v = e.length; y < v; ++y) {
    const x = e[y];
    for (c = i[x - n], d = i[x - n + 1], a = t; a < x; a += n)
      u = i[a], f = i[a + 1], (g <= d && f <= g || d <= g && g <= f) && (h = (g - d) / (f - d) * (u - c) + c, m.push(h)), c = u, d = f;
  }
  let p = NaN, _ = -1 / 0;
  for (m.sort(Yi), c = m[0], a = 1, l = m.length; a < l; ++a) {
    u = m[a];
    const y = Math.abs(u - c);
    y > _ && (h = (c + u) / 2, _l(i, t, e, n, h, g) && (p = h, _ = y)), c = u;
  }
  return isNaN(p) && (p = s[r]), o ? (o.push(p, g, _), o) : [p, g, _];
}
function Jg(i, t, e, n, s) {
  let r = [];
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = id(
      i,
      t,
      l,
      n,
      s,
      2 * o,
      r
    ), t = l[l.length - 1];
  }
  return r;
}
function nd(i, t, e, n, s) {
  let r;
  for (t += n; t < e; t += n)
    if (r = s(
      i.slice(t - n, t),
      i.slice(t, t + n)
    ), r)
      return r;
  return !1;
}
function Co(i, t, e, n, s) {
  const r = Ru(
    fe(),
    i,
    t,
    e,
    n
  );
  return ie(s, r) ? yi(s, r) || r[0] >= s[0] && r[2] <= s[2] || r[1] >= s[1] && r[3] <= s[3] ? !0 : nd(
    i,
    t,
    e,
    n,
    function(o, a) {
      return T0(s, o, a);
    }
  ) : !1;
}
function Qg(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    if (Co(i, t, e[r], n, s))
      return !0;
    t = e[r];
  }
  return !1;
}
function sd(i, t, e, n, s) {
  return !!(Co(i, t, e, n, s) || $i(
    i,
    t,
    e,
    n,
    s[0],
    s[1]
  ) || $i(
    i,
    t,
    e,
    n,
    s[0],
    s[3]
  ) || $i(
    i,
    t,
    e,
    n,
    s[2],
    s[1]
  ) || $i(
    i,
    t,
    e,
    n,
    s[2],
    s[3]
  ));
}
function rd(i, t, e, n, s) {
  if (!sd(i, t, e[0], n, s))
    return !1;
  if (e.length === 1)
    return !0;
  for (let r = 1, o = e.length; r < o; ++r)
    if (Kg(
      i,
      e[r - 1],
      e[r],
      n,
      s
    ) && !Co(
      i,
      e[r - 1],
      e[r],
      n,
      s
    ))
      return !1;
  return !0;
}
function t1(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (rd(i, t, a, n, s))
      return !0;
    t = a[a.length - 1];
  }
  return !1;
}
function e1(i, t, e, n) {
  for (; t < e - n; ) {
    for (let s = 0; s < n; ++s) {
      const r = i[t + s];
      i[t + s] = i[e - n + s], i[e - n + s] = r;
    }
    t += n, e -= n;
  }
}
function od(i, t, e, n) {
  let s = 0, r = i[e - n], o = i[e - n + 1];
  for (; t < e; t += n) {
    const a = i[t], l = i[t + 1];
    s += (a - r) * (l + o), r = a, o = l;
  }
  return s === 0 ? void 0 : s > 0;
}
function ad(i, t, e, n, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = od(
      i,
      t,
      a,
      n
    );
    if (r === 0) {
      if (s && l || !s && !l)
        return !1;
    } else if (s && !l || !s && l)
      return !1;
    t = a;
  }
  return !0;
}
function i1(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (!ad(i, t, a, n, s))
      return !1;
    a.length && (t = a[a.length - 1]);
  }
  return !0;
}
function Ca(i, t, e, n, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = od(
      i,
      t,
      a,
      n
    );
    (r === 0 ? s && l || !s && !l : s && !l || !s && l) && e1(i, t, a, n), t = a;
  }
  return t;
}
function Nh(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r)
    t = Ca(
      i,
      t,
      e[r],
      n,
      s
    );
  return t;
}
class Zn extends rn {
  constructor(t, e, n) {
    super(), this.ends_ = [], this.flatInteriorPointRevision_ = -1, this.flatInteriorPoint_ = null, this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, this.orientedRevision_ = -1, this.orientedFlatCoordinates_ = null, e !== void 0 && n ? (this.setFlatCoordinates(
      e,
      t
    ), this.ends_ = n) : this.setCoordinates(
      t,
      e
    );
  }
  appendLinearRing(t) {
    this.flatCoordinates ? Kt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new Zn(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < sn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      ul(
        this.flatCoordinates,
        0,
        this.ends_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), fl(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      n,
      s
    ));
  }
  containsXY(t, e) {
    return _l(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return ed(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), Ca(e, 0, this.ends_, this.stride, t)) : e = this.flatCoordinates, Ps(e, 0, this.ends_, this.stride);
  }
  getEnds() {
    return this.ends_;
  }
  getFlatInteriorPoint() {
    if (this.flatInteriorPointRevision_ != this.getRevision()) {
      const t = Ri(this.getExtent());
      this.flatInteriorPoint_ = id(
        this.getOrientedFlatCoordinates(),
        0,
        this.ends_,
        this.stride,
        t,
        0
      ), this.flatInteriorPointRevision_ = this.getRevision();
    }
    return this.flatInteriorPoint_;
  }
  getInteriorPoint() {
    return new si(this.getFlatInteriorPoint(), "XYM");
  }
  getLinearRingCount() {
    return this.ends_.length;
  }
  getLinearRing(t) {
    return t < 0 || this.ends_.length <= t ? null : new xa(
      this.flatCoordinates.slice(
        t === 0 ? 0 : this.ends_[t - 1],
        this.ends_[t]
      ),
      this.layout
    );
  }
  getLinearRings() {
    const t = this.layout, e = this.flatCoordinates, n = this.ends_, s = [];
    let r = 0;
    for (let o = 0, a = n.length; o < a; ++o) {
      const l = n[o], h = new xa(
        e.slice(r, l),
        t
      );
      s.push(h), r = l;
    }
    return s;
  }
  getOrientedFlatCoordinates() {
    if (this.orientedRevision_ != this.getRevision()) {
      const t = this.flatCoordinates;
      ad(t, 0, this.ends_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = Ca(
        this.orientedFlatCoordinates_,
        0,
        this.ends_,
        this.stride
      )), this.orientedRevision_ = this.getRevision();
    }
    return this.orientedFlatCoordinates_;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], n = [];
    return e.length = Qu(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      Math.sqrt(t),
      e,
      0,
      n
    ), new Zn(e, "XY", n);
  }
  getType() {
    return "Polygon";
  }
  intersectsExtent(t) {
    return rd(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 2), this.flatCoordinates || (this.flatCoordinates = []);
    const n = gl(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.ends_
    );
    this.flatCoordinates.length = n.length === 0 ? 0 : n[n.length - 1], this.changed();
  }
}
const Vn = Zn;
function n1(i, t, e, n) {
  e = e || 32;
  const s = [];
  for (let r = 0; r < e; ++r)
    Kt(
      s,
      Eg(i, t, 2 * Math.PI * r / e, n)
    );
  return s.push(s[0], s[1]), new Zn(s, "XY", [s.length]);
}
function Fh(i) {
  const t = i[0], e = i[1], n = i[2], s = i[3], r = [
    t,
    e,
    t,
    s,
    n,
    s,
    n,
    e,
    t,
    e
  ];
  return new Zn(r, "XY", [r.length]);
}
const Vo = 0;
class s1 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, t = Object.assign({}, t), this.hints_ = [0, 0], this.animations_ = [], this.updateAnimationKey_, this.projection_ = ol(t.projection, "EPSG:3857"), this.viewportSize_ = [100, 100], this.targetCenter_ = null, this.targetResolution_, this.targetRotation_, this.nextCenter_ = null, this.nextResolution_, this.nextRotation_, this.cancelAnchor_ = void 0, t.projection && Wu(), t.center && (t.center = Ke(t.center, this.projection_)), t.extent && (t.extent = Gi(t.extent, this.projection_)), this.applyOptions_(t);
  }
  applyOptions_(t) {
    const e = Object.assign({}, t);
    for (const a in Ee)
      delete e[a];
    this.setProperties(e, !0);
    const n = o1(t);
    this.maxResolution_ = n.maxResolution, this.minResolution_ = n.minResolution, this.zoomFactor_ = n.zoomFactor, this.resolutions_ = t.resolutions, this.padding_ = t.padding, this.minZoom_ = n.minZoom;
    const s = r1(t), r = n.constraint, o = a1(t);
    this.constraints_ = {
      center: s,
      resolution: r,
      rotation: o
    }, this.setRotation(t.rotation !== void 0 ? t.rotation : 0), this.setCenterInternal(
      t.center !== void 0 ? t.center : null
    ), t.resolution !== void 0 ? this.setResolution(t.resolution) : t.zoom !== void 0 && this.setZoom(t.zoom);
  }
  get padding() {
    return this.padding_;
  }
  set padding(t) {
    let e = this.padding_;
    this.padding_ = t;
    const n = this.getCenter();
    if (n) {
      const s = t || [0, 0, 0, 0];
      e = e || [0, 0, 0, 0];
      const r = this.getResolution(), o = r / 2 * (s[3] - e[3] + e[1] - s[1]), a = r / 2 * (s[0] - e[0] + e[2] - s[2]);
      this.setCenterInternal([n[0] + o, n[1] - a]);
    }
  }
  getUpdatedOptions_(t) {
    const e = this.getProperties();
    return e.resolution !== void 0 ? e.resolution = this.getResolution() : e.zoom = this.getZoom(), e.center = this.getCenterInternal(), e.rotation = this.getRotation(), Object.assign({}, e, t);
  }
  animate(t) {
    this.isDef() && !this.getAnimating() && this.resolveConstraints(0);
    const e = new Array(arguments.length);
    for (let n = 0; n < e.length; ++n) {
      let s = arguments[n];
      s.center && (s = Object.assign({}, s), s.center = Ke(
        s.center,
        this.getProjection()
      )), s.anchor && (s = Object.assign({}, s), s.anchor = Ke(
        s.anchor,
        this.getProjection()
      )), e[n] = s;
    }
    this.animateInternal.apply(this, e);
  }
  animateInternal(t) {
    let e = arguments.length, n;
    e > 1 && typeof arguments[e - 1] == "function" && (n = arguments[e - 1], --e);
    let s = 0;
    for (; s < e && !this.isDef(); ++s) {
      const c = arguments[s];
      c.center && this.setCenterInternal(c.center), c.zoom !== void 0 ? this.setZoom(c.zoom) : c.resolution && this.setResolution(c.resolution), c.rotation !== void 0 && this.setRotation(c.rotation);
    }
    if (s === e) {
      n && _r(n, !0);
      return;
    }
    let r = Date.now(), o = this.targetCenter_.slice(), a = this.targetResolution_, l = this.targetRotation_;
    const h = [];
    for (; s < e; ++s) {
      const c = arguments[s], u = {
        start: r,
        complete: !1,
        anchor: c.anchor,
        duration: c.duration !== void 0 ? c.duration : 1e3,
        easing: c.easing || Ng,
        callback: n
      };
      if (c.center && (u.sourceCenter = o, u.targetCenter = c.center.slice(), o = u.targetCenter), c.zoom !== void 0 ? (u.sourceResolution = a, u.targetResolution = this.getResolutionForZoom(c.zoom), a = u.targetResolution) : c.resolution && (u.sourceResolution = a, u.targetResolution = c.resolution, a = u.targetResolution), c.rotation !== void 0) {
        u.sourceRotation = l;
        const d = An(c.rotation - l + Math.PI, 2 * Math.PI) - Math.PI;
        u.targetRotation = l + d, l = u.targetRotation;
      }
      l1(u) ? u.complete = !0 : r += u.duration, h.push(u);
    }
    this.animations_.push(h), this.setHint(Zt.ANIMATING, 1), this.updateAnimations_();
  }
  getAnimating() {
    return this.hints_[Zt.ANIMATING] > 0;
  }
  getInteracting() {
    return this.hints_[Zt.INTERACTING] > 0;
  }
  cancelAnimations() {
    this.setHint(Zt.ANIMATING, -this.hints_[Zt.ANIMATING]);
    let t;
    for (let e = 0, n = this.animations_.length; e < n; ++e) {
      const s = this.animations_[e];
      if (s[0].callback && _r(s[0].callback, !1), !t)
        for (let r = 0, o = s.length; r < o; ++r) {
          const a = s[r];
          if (!a.complete) {
            t = a.anchor;
            break;
          }
        }
    }
    this.animations_.length = 0, this.cancelAnchor_ = t, this.nextCenter_ = null, this.nextResolution_ = NaN, this.nextRotation_ = NaN;
  }
  updateAnimations_() {
    if (this.updateAnimationKey_ !== void 0 && (cancelAnimationFrame(this.updateAnimationKey_), this.updateAnimationKey_ = void 0), !this.getAnimating())
      return;
    const t = Date.now();
    let e = !1;
    for (let n = this.animations_.length - 1; n >= 0; --n) {
      const s = this.animations_[n];
      let r = !0;
      for (let o = 0, a = s.length; o < a; ++o) {
        const l = s[o];
        if (l.complete)
          continue;
        const h = t - l.start;
        let c = l.duration > 0 ? h / l.duration : 1;
        c >= 1 ? (l.complete = !0, c = 1) : r = !1;
        const u = l.easing(c);
        if (l.sourceCenter) {
          const d = l.sourceCenter[0], f = l.sourceCenter[1], g = l.targetCenter[0], m = l.targetCenter[1];
          this.nextCenter_ = l.targetCenter;
          const p = d + u * (g - d), _ = f + u * (m - f);
          this.targetCenter_ = [p, _];
        }
        if (l.sourceResolution && l.targetResolution) {
          const d = u === 1 ? l.targetResolution : l.sourceResolution + u * (l.targetResolution - l.sourceResolution);
          if (l.anchor) {
            const f = this.getViewportSize_(this.getRotation()), g = this.constraints_.resolution(
              d,
              0,
              f,
              !0
            );
            this.targetCenter_ = this.calculateCenterZoom(
              g,
              l.anchor
            );
          }
          this.nextResolution_ = l.targetResolution, this.targetResolution_ = d, this.applyTargetState_(!0);
        }
        if (l.sourceRotation !== void 0 && l.targetRotation !== void 0) {
          const d = u === 1 ? An(l.targetRotation + Math.PI, 2 * Math.PI) - Math.PI : l.sourceRotation + u * (l.targetRotation - l.sourceRotation);
          if (l.anchor) {
            const f = this.constraints_.rotation(
              d,
              !0
            );
            this.targetCenter_ = this.calculateCenterRotate(
              f,
              l.anchor
            );
          }
          this.nextRotation_ = l.targetRotation, this.targetRotation_ = d;
        }
        if (this.applyTargetState_(!0), e = !0, !l.complete)
          break;
      }
      if (r) {
        this.animations_[n] = null, this.setHint(Zt.ANIMATING, -1), this.nextCenter_ = null, this.nextResolution_ = NaN, this.nextRotation_ = NaN;
        const o = s[0].callback;
        o && _r(o, !0);
      }
    }
    this.animations_ = this.animations_.filter(Boolean), e && this.updateAnimationKey_ === void 0 && (this.updateAnimationKey_ = requestAnimationFrame(
      this.updateAnimations_.bind(this)
    ));
  }
  calculateCenterRotate(t, e) {
    let n;
    const s = this.getCenterInternal();
    return s !== void 0 && (n = [s[0] - e[0], s[1] - e[1]], tl(n, t - this.getRotation()), Ou(n, e)), n;
  }
  calculateCenterZoom(t, e) {
    let n;
    const s = this.getCenterInternal(), r = this.getResolution();
    if (s !== void 0 && r !== void 0) {
      const o = e[0] - t * (e[0] - s[0]) / r, a = e[1] - t * (e[1] - s[1]) / r;
      n = [o, a];
    }
    return n;
  }
  getViewportSize_(t) {
    const e = this.viewportSize_;
    if (t) {
      const n = e[0], s = e[1];
      return [
        Math.abs(n * Math.cos(t)) + Math.abs(s * Math.sin(t)),
        Math.abs(n * Math.sin(t)) + Math.abs(s * Math.cos(t))
      ];
    } else
      return e;
  }
  setViewportSize(t) {
    this.viewportSize_ = Array.isArray(t) ? t.slice() : [100, 100], this.getAnimating() || this.resolveConstraints(0);
  }
  getCenter() {
    const t = this.getCenterInternal();
    return t && ya(t, this.getProjection());
  }
  getCenterInternal() {
    return this.get(Ee.CENTER);
  }
  getConstraints() {
    return this.constraints_;
  }
  getConstrainResolution() {
    return this.get("constrainResolution");
  }
  getHints(t) {
    return t !== void 0 ? (t[0] = this.hints_[0], t[1] = this.hints_[1], t) : this.hints_.slice();
  }
  calculateExtent(t) {
    const e = this.calculateExtentInternal(t);
    return ju(e, this.getProjection());
  }
  calculateExtentInternal(t) {
    t = t || this.getViewportSizeMinusPadding_();
    const e = this.getCenterInternal();
    Y(e, 1);
    const n = this.getResolution();
    Y(n !== void 0, 2);
    const s = this.getRotation();
    return Y(s !== void 0, 3), ca(e, n, s, t);
  }
  getMaxResolution() {
    return this.maxResolution_;
  }
  getMinResolution() {
    return this.minResolution_;
  }
  getMaxZoom() {
    return this.getZoomForResolution(this.minResolution_);
  }
  setMaxZoom(t) {
    this.applyOptions_(this.getUpdatedOptions_({ maxZoom: t }));
  }
  getMinZoom() {
    return this.getZoomForResolution(this.maxResolution_);
  }
  setMinZoom(t) {
    this.applyOptions_(this.getUpdatedOptions_({ minZoom: t }));
  }
  setConstrainResolution(t) {
    this.applyOptions_(this.getUpdatedOptions_({ constrainResolution: t }));
  }
  getProjection() {
    return this.projection_;
  }
  getResolution() {
    return this.get(Ee.RESOLUTION);
  }
  getResolutions() {
    return this.resolutions_;
  }
  getResolutionForExtent(t, e) {
    return this.getResolutionForExtentInternal(
      Gi(t, this.getProjection()),
      e
    );
  }
  getResolutionForExtentInternal(t, e) {
    e = e || this.getViewportSizeMinusPadding_();
    const n = mt(t) / e[0], s = ke(t) / e[1];
    return Math.max(n, s);
  }
  getResolutionForValueFunction(t) {
    t = t || 2;
    const e = this.getConstrainedResolution(this.maxResolution_), n = this.minResolution_, s = Math.log(e / n) / Math.log(t);
    return function(r) {
      return e / Math.pow(t, r * s);
    };
  }
  getRotation() {
    return this.get(Ee.ROTATION);
  }
  getValueForResolutionFunction(t) {
    const e = Math.log(t || 2), n = this.getConstrainedResolution(this.maxResolution_), s = this.minResolution_, r = Math.log(n / s) / e;
    return function(o) {
      return Math.log(n / o) / e / r;
    };
  }
  getViewportSizeMinusPadding_(t) {
    let e = this.getViewportSize_(t);
    const n = this.padding_;
    return n && (e = [
      e[0] - n[1] - n[3],
      e[1] - n[0] - n[2]
    ]), e;
  }
  getState() {
    const t = this.getProjection(), e = this.getResolution(), n = this.getRotation();
    let s = this.getCenterInternal();
    const r = this.padding_;
    if (r) {
      const o = this.getViewportSizeMinusPadding_();
      s = Uo(
        s,
        this.getViewportSize_(),
        [o[0] / 2 + r[3], o[1] / 2 + r[0]],
        e,
        n
      );
    }
    return {
      center: s.slice(0),
      projection: t !== void 0 ? t : null,
      resolution: e,
      nextCenter: this.nextCenter_,
      nextResolution: this.nextResolution_,
      nextRotation: this.nextRotation_,
      rotation: n,
      zoom: this.getZoom()
    };
  }
  getZoom() {
    let t;
    const e = this.getResolution();
    return e !== void 0 && (t = this.getZoomForResolution(e)), t;
  }
  getZoomForResolution(t) {
    let e = this.minZoom_ || 0, n, s;
    if (this.resolutions_) {
      const r = Ya(this.resolutions_, t, 1);
      e = r, n = this.resolutions_[r], r == this.resolutions_.length - 1 ? s = 2 : s = n / this.resolutions_[r + 1];
    } else
      n = this.maxResolution_, s = this.zoomFactor_;
    return e + Math.log(n / t) / Math.log(s);
  }
  getResolutionForZoom(t) {
    if (this.resolutions_) {
      if (this.resolutions_.length <= 1)
        return 0;
      const e = wt(
        Math.floor(t),
        0,
        this.resolutions_.length - 2
      ), n = this.resolutions_[e] / this.resolutions_[e + 1];
      return this.resolutions_[e] / Math.pow(n, wt(t - e, 0, 1));
    } else
      return this.maxResolution_ / Math.pow(this.zoomFactor_, t - this.minZoom_);
  }
  fit(t, e) {
    let n;
    if (Y(
      Array.isArray(t) || typeof t.getSimplifiedGeometry == "function",
      24
    ), Array.isArray(t)) {
      Y(!Ja(t), 25);
      const s = Gi(t, this.getProjection());
      n = Fh(s);
    } else if (t.getType() === "Circle") {
      const s = Gi(
        t.getExtent(),
        this.getProjection()
      );
      n = Fh(s), n.rotate(this.getRotation(), Ri(s));
    } else
      n = t;
    this.fitInternal(n, e);
  }
  rotatedExtentForGeometry(t) {
    const e = this.getRotation(), n = Math.cos(e), s = Math.sin(-e), r = t.getFlatCoordinates(), o = t.getStride();
    let a = 1 / 0, l = 1 / 0, h = -1 / 0, c = -1 / 0;
    for (let u = 0, d = r.length; u < d; u += o) {
      const f = r[u] * n - r[u + 1] * s, g = r[u] * s + r[u + 1] * n;
      a = Math.min(a, f), l = Math.min(l, g), h = Math.max(h, f), c = Math.max(c, g);
    }
    return [a, l, h, c];
  }
  fitInternal(t, e) {
    e = e || {};
    let n = e.size;
    n || (n = this.getViewportSizeMinusPadding_());
    const s = e.padding !== void 0 ? e.padding : [0, 0, 0, 0], r = e.nearest !== void 0 ? e.nearest : !1;
    let o;
    e.minResolution !== void 0 ? o = e.minResolution : e.maxZoom !== void 0 ? o = this.getResolutionForZoom(e.maxZoom) : o = 0;
    const a = this.rotatedExtentForGeometry(t);
    let l = this.getResolutionForExtentInternal(a, [
      n[0] - s[1] - s[3],
      n[1] - s[0] - s[2]
    ]);
    l = isNaN(l) ? o : Math.max(l, o), l = this.getConstrainedResolution(l, r ? 0 : 1);
    const h = this.getRotation(), c = Math.sin(h), u = Math.cos(h), d = Ri(a);
    d[0] += (s[1] - s[3]) / 2 * l, d[1] += (s[0] - s[2]) / 2 * l;
    const f = d[0] * u - d[1] * c, g = d[1] * u + d[0] * c, m = this.getConstrainedCenter([f, g], l), p = e.callback ? e.callback : ji;
    e.duration !== void 0 ? this.animateInternal(
      {
        resolution: l,
        center: m,
        duration: e.duration,
        easing: e.easing
      },
      p
    ) : (this.targetResolution_ = l, this.targetCenter_ = m, this.applyTargetState_(!1, !0), _r(p, !0));
  }
  centerOn(t, e, n) {
    this.centerOnInternal(
      Ke(t, this.getProjection()),
      e,
      n
    );
  }
  centerOnInternal(t, e, n) {
    this.setCenterInternal(
      Uo(
        t,
        e,
        n,
        this.getResolution(),
        this.getRotation()
      )
    );
  }
  calculateCenterShift(t, e, n, s) {
    let r;
    const o = this.padding_;
    if (o && t) {
      const a = this.getViewportSizeMinusPadding_(-n), l = Uo(
        t,
        s,
        [a[0] / 2 + o[3], a[1] / 2 + o[0]],
        e,
        n
      );
      r = [
        t[0] - l[0],
        t[1] - l[1]
      ];
    }
    return r;
  }
  isDef() {
    return !!this.getCenterInternal() && this.getResolution() !== void 0;
  }
  adjustCenter(t) {
    const e = ya(this.targetCenter_, this.getProjection());
    this.setCenter([
      e[0] + t[0],
      e[1] + t[1]
    ]);
  }
  adjustCenterInternal(t) {
    const e = this.targetCenter_;
    this.setCenterInternal([
      e[0] + t[0],
      e[1] + t[1]
    ]);
  }
  adjustResolution(t, e) {
    e = e && Ke(e, this.getProjection()), this.adjustResolutionInternal(t, e);
  }
  adjustResolutionInternal(t, e) {
    const n = this.getAnimating() || this.getInteracting(), s = this.getViewportSize_(this.getRotation()), r = this.constraints_.resolution(
      this.targetResolution_ * t,
      0,
      s,
      n
    );
    e && (this.targetCenter_ = this.calculateCenterZoom(r, e)), this.targetResolution_ *= t, this.applyTargetState_();
  }
  adjustZoom(t, e) {
    this.adjustResolution(Math.pow(this.zoomFactor_, -t), e);
  }
  adjustRotation(t, e) {
    e && (e = Ke(e, this.getProjection())), this.adjustRotationInternal(t, e);
  }
  adjustRotationInternal(t, e) {
    const n = this.getAnimating() || this.getInteracting(), s = this.constraints_.rotation(
      this.targetRotation_ + t,
      n
    );
    e && (this.targetCenter_ = this.calculateCenterRotate(s, e)), this.targetRotation_ += t, this.applyTargetState_();
  }
  setCenter(t) {
    this.setCenterInternal(
      t && Ke(t, this.getProjection())
    );
  }
  setCenterInternal(t) {
    this.targetCenter_ = t, this.applyTargetState_();
  }
  setHint(t, e) {
    return this.hints_[t] += e, this.changed(), this.hints_[t];
  }
  setResolution(t) {
    this.targetResolution_ = t, this.applyTargetState_();
  }
  setRotation(t) {
    this.targetRotation_ = t, this.applyTargetState_();
  }
  setZoom(t) {
    this.setResolution(this.getResolutionForZoom(t));
  }
  applyTargetState_(t, e) {
    const n = this.getAnimating() || this.getInteracting() || e, s = this.constraints_.rotation(
      this.targetRotation_,
      n
    ), r = this.getViewportSize_(s), o = this.constraints_.resolution(
      this.targetResolution_,
      0,
      r,
      n
    ), a = this.constraints_.center(
      this.targetCenter_,
      o,
      r,
      n,
      this.calculateCenterShift(
        this.targetCenter_,
        o,
        s,
        r
      )
    );
    this.get(Ee.ROTATION) !== s && this.set(Ee.ROTATION, s), this.get(Ee.RESOLUTION) !== o && (this.set(Ee.RESOLUTION, o), this.set("zoom", this.getZoom(), !0)), (!a || !this.get(Ee.CENTER) || !$r(this.get(Ee.CENTER), a)) && this.set(Ee.CENTER, a), this.getAnimating() && !t && this.cancelAnimations(), this.cancelAnchor_ = void 0;
  }
  resolveConstraints(t, e, n) {
    t = t !== void 0 ? t : 200;
    const s = e || 0, r = this.constraints_.rotation(this.targetRotation_), o = this.getViewportSize_(r), a = this.constraints_.resolution(
      this.targetResolution_,
      s,
      o
    ), l = this.constraints_.center(
      this.targetCenter_,
      a,
      o,
      !1,
      this.calculateCenterShift(
        this.targetCenter_,
        a,
        r,
        o
      )
    );
    if (t === 0 && !this.cancelAnchor_) {
      this.targetResolution_ = a, this.targetRotation_ = r, this.targetCenter_ = l, this.applyTargetState_();
      return;
    }
    n = n || (t === 0 ? this.cancelAnchor_ : void 0), this.cancelAnchor_ = void 0, (this.getResolution() !== a || this.getRotation() !== r || !this.getCenterInternal() || !$r(this.getCenterInternal(), l)) && (this.getAnimating() && this.cancelAnimations(), this.animateInternal({
      rotation: r,
      center: l,
      resolution: a,
      duration: t,
      easing: jn,
      anchor: n
    }));
  }
  beginInteraction() {
    this.resolveConstraints(0), this.setHint(Zt.INTERACTING, 1);
  }
  endInteraction(t, e, n) {
    n = n && Ke(n, this.getProjection()), this.endInteractionInternal(t, e, n);
  }
  endInteractionInternal(t, e, n) {
    this.setHint(Zt.INTERACTING, -1), this.resolveConstraints(t, e, n);
  }
  getConstrainedCenter(t, e) {
    const n = this.getViewportSize_(this.getRotation());
    return this.constraints_.center(
      t,
      e || this.getResolution(),
      n
    );
  }
  getConstrainedZoom(t, e) {
    const n = this.getResolutionForZoom(t);
    return this.getZoomForResolution(
      this.getConstrainedResolution(n, e)
    );
  }
  getConstrainedResolution(t, e) {
    e = e || 0;
    const n = this.getViewportSize_(this.getRotation());
    return this.constraints_.resolution(t, e, n);
  }
}
function _r(i, t) {
  setTimeout(function() {
    i(t);
  }, 0);
}
function r1(i) {
  if (i.extent !== void 0) {
    const e = i.smoothExtentConstraint !== void 0 ? i.smoothExtentConstraint : !0;
    return Lh(i.extent, i.constrainOnlyCenter, e);
  }
  const t = ol(i.projection, "EPSG:3857");
  if (i.multiWorld !== !0 && t.isGlobal()) {
    const e = t.getExtent().slice();
    return e[0] = -1 / 0, e[2] = 1 / 0, Lh(e, !1, !1);
  }
  return Tg;
}
function o1(i) {
  let t, e, n, o = i.minZoom !== void 0 ? i.minZoom : Vo, a = i.maxZoom !== void 0 ? i.maxZoom : 28;
  const l = i.zoomFactor !== void 0 ? i.zoomFactor : 2, h = i.multiWorld !== void 0 ? i.multiWorld : !1, c = i.smoothResolutionConstraint !== void 0 ? i.smoothResolutionConstraint : !0, u = i.showFullExtent !== void 0 ? i.showFullExtent : !1, d = ol(i.projection, "EPSG:3857"), f = d.getExtent();
  let g = i.constrainOnlyCenter, m = i.extent;
  if (!h && !m && d.isGlobal() && (g = !1, m = f), i.resolutions !== void 0) {
    const p = i.resolutions;
    e = p[o], n = p[a] !== void 0 ? p[a] : p[p.length - 1], i.constrainResolution ? t = Ig(
      p,
      c,
      !g && m,
      u
    ) : t = Th(
      e,
      n,
      c,
      !g && m,
      u
    );
  } else {
    const _ = (f ? Math.max(mt(f), ke(f)) : 360 * Bn.degrees / d.getMetersPerUnit()) / il / Math.pow(2, Vo), y = _ / Math.pow(2, 28 - Vo);
    e = i.maxResolution, e !== void 0 ? o = 0 : e = _ / Math.pow(l, o), n = i.minResolution, n === void 0 && (i.maxZoom !== void 0 ? i.maxResolution !== void 0 ? n = e / Math.pow(l, a) : n = _ / Math.pow(l, a) : n = y), a = o + Math.floor(
      Math.log(e / n) / Math.log(l)
    ), n = e / Math.pow(l, a - o), i.constrainResolution ? t = Pg(
      l,
      e,
      n,
      c,
      !g && m,
      u
    ) : t = Th(
      e,
      n,
      c,
      !g && m,
      u
    );
  }
  return {
    constraint: t,
    maxResolution: e,
    minResolution: n,
    minZoom: o,
    zoomFactor: l
  };
}
function a1(i) {
  if (i.enableRotation !== void 0 ? i.enableRotation : !0) {
    const e = i.constrainRotation;
    return e === void 0 || e === !0 ? Og() : e === !1 ? Ih : typeof e == "number" ? Ag(e) : Ih;
  } else
    return hl;
}
function l1(i) {
  return !(i.sourceCenter && i.targetCenter && !$r(i.sourceCenter, i.targetCenter) || i.sourceResolution !== i.targetResolution || i.sourceRotation !== i.targetRotation);
}
function Uo(i, t, e, n, s) {
  const r = Math.cos(-s);
  let o = Math.sin(-s), a = i[0] * r - i[1] * o, l = i[1] * r + i[0] * o;
  a += (t[0] / 2 - e[0]) * n, l += (e[1] - t[1] / 2) * n, o = -o;
  const h = a * r - l * o, c = l * r + a * o;
  return [h, c];
}
const ti = s1;
class h1 extends Ce {
  constructor(t) {
    super();
    const e = t.element;
    e && !t.target && !e.style.pointerEvents && (e.style.pointerEvents = "auto"), this.element = e || null, this.target_ = null, this.map_ = null, this.listenerKeys = [], t.render && (this.render = t.render), t.target && this.setTarget(t.target);
  }
  disposeInternal() {
    zr(this.element), super.disposeInternal();
  }
  getMap() {
    return this.map_;
  }
  setMap(t) {
    this.map_ && zr(this.element);
    for (let e = 0, n = this.listenerKeys.length; e < n; ++e)
      pt(this.listenerKeys[e]);
    this.listenerKeys.length = 0, this.map_ = t, t && ((this.target_ ? this.target_ : t.getOverlayContainerStopEvent()).appendChild(this.element), this.render !== ji && this.listenerKeys.push(
      et(t, qe.POSTRENDER, this.render, this)
    ), t.render());
  }
  render(t) {
  }
  setTarget(t) {
    this.target_ = typeof t == "string" ? document.getElementById(t) : t;
  }
}
const kt = h1;
class c1 extends kt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      render: t.render,
      target: t.target
    }), this.ulElement_ = document.createElement("ul"), this.collapsed_ = t.collapsed !== void 0 ? t.collapsed : !0, this.userCollapsed_ = this.collapsed_, this.overrideCollapsible_ = t.collapsible !== void 0, this.collapsible_ = t.collapsible !== void 0 ? t.collapsible : !0, this.collapsible_ || (this.collapsed_ = !1);
    const e = t.className !== void 0 ? t.className : "ol-attribution", n = t.tipLabel !== void 0 ? t.tipLabel : "Attributions", s = t.expandClassName !== void 0 ? t.expandClassName : e + "-expand", r = t.collapseLabel !== void 0 ? t.collapseLabel : "\u203A", o = t.collapseClassName !== void 0 ? t.collapseClassName : e + "-collapse";
    typeof r == "string" ? (this.collapseLabel_ = document.createElement("span"), this.collapseLabel_.textContent = r, this.collapseLabel_.className = o) : this.collapseLabel_ = r;
    const a = t.label !== void 0 ? t.label : "i";
    typeof a == "string" ? (this.label_ = document.createElement("span"), this.label_.textContent = a, this.label_.className = s) : this.label_ = a;
    const l = this.collapsible_ && !this.collapsed_ ? this.collapseLabel_ : this.label_;
    this.toggleButton_ = document.createElement("button"), this.toggleButton_.setAttribute("type", "button"), this.toggleButton_.setAttribute("aria-expanded", String(!this.collapsed_)), this.toggleButton_.title = n, this.toggleButton_.appendChild(l), this.toggleButton_.addEventListener(
      X.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const h = e + " " + Yn + " " + _o + (this.collapsed_ && this.collapsible_ ? " " + vh : "") + (this.collapsible_ ? "" : " ol-uncollapsible"), c = this.element;
    c.className = h, c.appendChild(this.toggleButton_), c.appendChild(this.ulElement_), this.renderedAttributions_ = [], this.renderedVisible_ = !0;
  }
  collectSourceAttributions_(t) {
    const e = {}, n = [];
    let s = !0;
    const r = t.layerStatesArray;
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      if (!Qa(l, t.viewState))
        continue;
      const h = l.layer.getSource();
      if (!h)
        continue;
      const c = h.getAttributions();
      if (!c)
        continue;
      const u = c(t);
      if (!!u)
        if (s = s && h.getAttributionsCollapsible() !== !1, Array.isArray(u))
          for (let d = 0, f = u.length; d < f; ++d)
            u[d] in e || (n.push(u[d]), e[u[d]] = !0);
        else
          u in e || (n.push(u), e[u] = !0);
    }
    return this.overrideCollapsible_ || this.setCollapsible(s), n;
  }
  updateElement_(t) {
    if (!t) {
      this.renderedVisible_ && (this.element.style.display = "none", this.renderedVisible_ = !1);
      return;
    }
    const e = this.collectSourceAttributions_(t), n = e.length > 0;
    if (this.renderedVisible_ != n && (this.element.style.display = n ? "" : "none", this.renderedVisible_ = n), !nn(e, this.renderedAttributions_)) {
      Bu(this.ulElement_);
      for (let s = 0, r = e.length; s < r; ++s) {
        const o = document.createElement("li");
        o.innerHTML = e[s], this.ulElement_.appendChild(o);
      }
      this.renderedAttributions_ = e;
    }
  }
  handleClick_(t) {
    t.preventDefault(), this.handleToggle_(), this.userCollapsed_ = this.collapsed_;
  }
  handleToggle_() {
    this.element.classList.toggle(vh), this.collapsed_ ? Br(this.collapseLabel_, this.label_) : Br(this.label_, this.collapseLabel_), this.collapsed_ = !this.collapsed_, this.toggleButton_.setAttribute("aria-expanded", String(!this.collapsed_));
  }
  getCollapsible() {
    return this.collapsible_;
  }
  setCollapsible(t) {
    this.collapsible_ !== t && (this.collapsible_ = t, this.element.classList.toggle("ol-uncollapsible"), this.userCollapsed_ && this.handleToggle_());
  }
  setCollapsed(t) {
    this.userCollapsed_ = t, !(!this.collapsible_ || this.collapsed_ === t) && this.handleToggle_();
  }
  getCollapsed() {
    return this.collapsed_;
  }
  render(t) {
    this.updateElement_(t.frameState);
  }
}
const u1 = c1;
class d1 extends kt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      render: t.render,
      target: t.target
    });
    const e = t.className !== void 0 ? t.className : "ol-rotate", n = t.label !== void 0 ? t.label : "\u21E7", s = t.compassClassName !== void 0 ? t.compassClassName : "ol-compass";
    this.label_ = null, typeof n == "string" ? (this.label_ = document.createElement("span"), this.label_.className = s, this.label_.textContent = n) : (this.label_ = n, this.label_.classList.add(s));
    const r = t.tipLabel ? t.tipLabel : "Reset rotation", o = document.createElement("button");
    o.className = e + "-reset", o.setAttribute("type", "button"), o.title = r, o.appendChild(this.label_), o.addEventListener(
      X.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const a = e + " " + Yn + " " + _o, l = this.element;
    l.className = a, l.appendChild(o), this.callResetNorth_ = t.resetNorth ? t.resetNorth : void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.autoHide_ = t.autoHide !== void 0 ? t.autoHide : !0, this.rotation_ = void 0, this.autoHide_ && this.element.classList.add(mr);
  }
  handleClick_(t) {
    t.preventDefault(), this.callResetNorth_ !== void 0 ? this.callResetNorth_() : this.resetNorth_();
  }
  resetNorth_() {
    const e = this.getMap().getView();
    if (!e)
      return;
    const n = e.getRotation();
    n !== void 0 && (this.duration_ > 0 && n % (2 * Math.PI) !== 0 ? e.animate({
      rotation: 0,
      duration: this.duration_,
      easing: jn
    }) : e.setRotation(0));
  }
  render(t) {
    const e = t.frameState;
    if (!e)
      return;
    const n = e.viewState.rotation;
    if (n != this.rotation_) {
      const s = "rotate(" + n + "rad)";
      if (this.autoHide_) {
        const r = this.element.classList.contains(mr);
        !r && n === 0 ? this.element.classList.add(mr) : r && n !== 0 && this.element.classList.remove(mr);
      }
      this.label_.style.transform = s;
    }
    this.rotation_ = n;
  }
}
const f1 = d1;
class g1 extends kt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      target: t.target
    });
    const e = t.className !== void 0 ? t.className : "ol-zoom", n = t.delta !== void 0 ? t.delta : 1, s = t.zoomInClassName !== void 0 ? t.zoomInClassName : e + "-in", r = t.zoomOutClassName !== void 0 ? t.zoomOutClassName : e + "-out", o = t.zoomInLabel !== void 0 ? t.zoomInLabel : "+", a = t.zoomOutLabel !== void 0 ? t.zoomOutLabel : "\u2013", l = t.zoomInTipLabel !== void 0 ? t.zoomInTipLabel : "Zoom in", h = t.zoomOutTipLabel !== void 0 ? t.zoomOutTipLabel : "Zoom out", c = document.createElement("button");
    c.className = s, c.setAttribute("type", "button"), c.title = l, c.appendChild(
      typeof o == "string" ? document.createTextNode(o) : o
    ), c.addEventListener(
      X.CLICK,
      this.handleClick_.bind(this, n),
      !1
    );
    const u = document.createElement("button");
    u.className = r, u.setAttribute("type", "button"), u.title = h, u.appendChild(
      typeof a == "string" ? document.createTextNode(a) : a
    ), u.addEventListener(
      X.CLICK,
      this.handleClick_.bind(this, -n),
      !1
    );
    const d = e + " " + Yn + " " + _o, f = this.element;
    f.className = d, f.appendChild(c), f.appendChild(u), this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleClick_(t, e) {
    e.preventDefault(), this.zoomByDelta_(t);
  }
  zoomByDelta_(t) {
    const n = this.getMap().getView();
    if (!n)
      return;
    const s = n.getZoom();
    if (s !== void 0) {
      const r = n.getConstrainedZoom(s + t);
      this.duration_ > 0 ? (n.getAnimating() && n.cancelAnimations(), n.animate({
        zoom: r,
        duration: this.duration_,
        easing: jn
      })) : n.setZoom(r);
    }
  }
}
const ld = g1;
function m1(i) {
  i = i || {};
  const t = new Ae();
  return (i.zoom !== void 0 ? i.zoom : !0) && t.push(new ld(i.zoomOptions)), (i.rotate !== void 0 ? i.rotate : !0) && t.push(new f1(i.rotateOptions)), (i.attribution !== void 0 ? i.attribution : !0) && t.push(new u1(i.attributionOptions)), t;
}
const Dh = {
  ACTIVE: "active"
};
class p1 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, t && t.handleEvent && (this.handleEvent = t.handleEvent), this.map_ = null, this.setActive(!0);
  }
  getActive() {
    return this.get(Dh.ACTIVE);
  }
  getMap() {
    return this.map_;
  }
  handleEvent(t) {
    return !0;
  }
  setActive(t) {
    this.set(Dh.ACTIVE, t);
  }
  setMap(t) {
    this.map_ = t;
  }
}
function _1(i, t, e) {
  const n = i.getCenterInternal();
  if (n) {
    const s = [n[0] + t[0], n[1] + t[1]];
    i.animateInternal({
      duration: e !== void 0 ? e : 250,
      easing: Fg,
      center: i.getConstrainedCenter(s)
    });
  }
}
function yl(i, t, e, n) {
  const s = i.getZoom();
  if (s === void 0)
    return;
  const r = i.getConstrainedZoom(s + t), o = i.getResolutionForZoom(r);
  i.getAnimating() && i.cancelAnimations(), i.animate({
    resolution: o,
    anchor: e,
    duration: n !== void 0 ? n : 250,
    easing: jn
  });
}
const Us = p1;
class y1 extends Us {
  constructor(t) {
    super(), t = t || {}, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == Mt.DBLCLICK) {
      const n = t.originalEvent, s = t.map, r = t.coordinate, o = n.shiftKey ? -this.delta_ : this.delta_, a = s.getView();
      yl(a, o, r, this.duration_), n.preventDefault(), e = !0;
    }
    return !e;
  }
}
const v1 = y1;
class x1 extends Us {
  constructor(t) {
    t = t || {}, super(
      t
    ), t.handleDownEvent && (this.handleDownEvent = t.handleDownEvent), t.handleDragEvent && (this.handleDragEvent = t.handleDragEvent), t.handleMoveEvent && (this.handleMoveEvent = t.handleMoveEvent), t.handleUpEvent && (this.handleUpEvent = t.handleUpEvent), t.stopDown && (this.stopDown = t.stopDown), this.handlingDownUpSequence = !1, this.targetPointers = [];
  }
  getPointerCount() {
    return this.targetPointers.length;
  }
  handleDownEvent(t) {
    return !1;
  }
  handleDragEvent(t) {
  }
  handleEvent(t) {
    if (!t.originalEvent)
      return !0;
    let e = !1;
    if (this.updateTrackedPointers_(t), this.handlingDownUpSequence) {
      if (t.type == Mt.POINTERDRAG)
        this.handleDragEvent(t), t.originalEvent.preventDefault();
      else if (t.type == Mt.POINTERUP) {
        const n = this.handleUpEvent(t);
        this.handlingDownUpSequence = n && this.targetPointers.length > 0;
      }
    } else if (t.type == Mt.POINTERDOWN) {
      const n = this.handleDownEvent(t);
      this.handlingDownUpSequence = n, e = this.stopDown(n);
    } else
      t.type == Mt.POINTERMOVE && this.handleMoveEvent(t);
    return !e;
  }
  handleMoveEvent(t) {
  }
  handleUpEvent(t) {
    return !1;
  }
  stopDown(t) {
    return t;
  }
  updateTrackedPointers_(t) {
    t.activePointers && (this.targetPointers = t.activePointers);
  }
}
function vl(i) {
  const t = i.length;
  let e = 0, n = 0;
  for (let s = 0; s < t; s++)
    e += i[s].clientX, n += i[s].clientY;
  return [e / t, n / t];
}
const Ws = x1;
function Ma(i) {
  const t = arguments;
  return function(e) {
    let n = !0;
    for (let s = 0, r = t.length; s < r && (n = n && t[s](e), !!n); ++s)
      ;
    return n;
  };
}
const C1 = function(i) {
  const t = i.originalEvent;
  return t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, M1 = function(i) {
  const t = i.map.getTargetElement(), e = i.map.getOwnerDocument().activeElement;
  return t.contains(e);
}, hd = function(i) {
  return i.map.getTargetElement().hasAttribute("tabindex") ? M1(i) : !0;
}, E1 = Ms, cd = function(i) {
  const t = i.originalEvent;
  return t.button == 0 && !(_0 && y0 && t.ctrlKey);
}, ud = function(i) {
  const t = i.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && !t.shiftKey;
}, w1 = function(i) {
  const t = i.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, dd = function(i) {
  const t = i.originalEvent, e = t.target.tagName;
  return e !== "INPUT" && e !== "SELECT" && e !== "TEXTAREA" && !t.target.isContentEditable;
}, Wo = function(i) {
  const t = i.originalEvent;
  return Y(t !== void 0, 56), t.pointerType == "mouse";
}, S1 = function(i) {
  const t = i.originalEvent;
  return Y(t !== void 0, 56), t.isPrimary && t.button === 0;
};
class R1 extends Ws {
  constructor(t) {
    super({
      stopDown: ao
    }), t = t || {}, this.kinetic_ = t.kinetic, this.lastCentroid = null, this.lastPointersCount_, this.panning_ = !1;
    const e = t.condition ? t.condition : Ma(ud, S1);
    this.condition_ = t.onFocusOnly ? Ma(hd, e) : e, this.noKinetic_ = !1;
  }
  handleDragEvent(t) {
    this.panning_ || (this.panning_ = !0, this.getMap().getView().beginInteraction());
    const e = this.targetPointers, n = vl(e);
    if (e.length == this.lastPointersCount_) {
      if (this.kinetic_ && this.kinetic_.update(n[0], n[1]), this.lastCentroid) {
        const s = [
          this.lastCentroid[0] - n[0],
          n[1] - this.lastCentroid[1]
        ], o = t.map.getView();
        Nu(s, o.getResolution()), tl(s, o.getRotation()), o.adjustCenterInternal(s);
      }
    } else
      this.kinetic_ && this.kinetic_.begin();
    this.lastCentroid = n, this.lastPointersCount_ = e.length, t.originalEvent.preventDefault();
  }
  handleUpEvent(t) {
    const e = t.map, n = e.getView();
    if (this.targetPointers.length === 0) {
      if (!this.noKinetic_ && this.kinetic_ && this.kinetic_.end()) {
        const s = this.kinetic_.getDistance(), r = this.kinetic_.getAngle(), o = n.getCenterInternal(), a = e.getPixelFromCoordinateInternal(o), l = e.getCoordinateFromPixelInternal([
          a[0] - s * Math.cos(r),
          a[1] - s * Math.sin(r)
        ]);
        n.animateInternal({
          center: n.getConstrainedCenter(l),
          duration: 500,
          easing: jn
        });
      }
      return this.panning_ && (this.panning_ = !1, n.endInteraction()), !1;
    } else
      return this.kinetic_ && this.kinetic_.begin(), this.lastCentroid = null, !0;
  }
  handleDownEvent(t) {
    if (this.targetPointers.length > 0 && this.condition_(t)) {
      const n = t.map.getView();
      return this.lastCentroid = null, n.getAnimating() && n.cancelAnimations(), this.kinetic_ && this.kinetic_.begin(), this.noKinetic_ = this.targetPointers.length > 1, !0;
    } else
      return !1;
  }
}
const b1 = R1;
class L1 extends Ws {
  constructor(t) {
    t = t || {}, super({
      stopDown: ao
    }), this.condition_ = t.condition ? t.condition : C1, this.lastAngle_ = void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleDragEvent(t) {
    if (!Wo(t))
      return;
    const e = t.map, n = e.getView();
    if (n.getConstraints().rotation === hl)
      return;
    const s = e.getSize(), r = t.pixel, o = Math.atan2(s[1] / 2 - r[1], r[0] - s[0] / 2);
    if (this.lastAngle_ !== void 0) {
      const a = o - this.lastAngle_;
      n.adjustRotationInternal(-a);
    }
    this.lastAngle_ = o;
  }
  handleUpEvent(t) {
    return Wo(t) ? (t.map.getView().endInteraction(this.duration_), !1) : !0;
  }
  handleDownEvent(t) {
    return Wo(t) && cd(t) && this.condition_(t) ? (t.map.getView().beginInteraction(), this.lastAngle_ = void 0, !0) : !1;
  }
}
const T1 = L1;
class I1 extends Xa {
  constructor(t) {
    super(), this.geometry_ = null, this.element_ = document.createElement("div"), this.element_.style.position = "absolute", this.element_.style.pointerEvents = "auto", this.element_.className = "ol-box " + t, this.map_ = null, this.startPixel_ = null, this.endPixel_ = null;
  }
  disposeInternal() {
    this.setMap(null);
  }
  render_() {
    const t = this.startPixel_, e = this.endPixel_, n = "px", s = this.element_.style;
    s.left = Math.min(t[0], e[0]) + n, s.top = Math.min(t[1], e[1]) + n, s.width = Math.abs(e[0] - t[0]) + n, s.height = Math.abs(e[1] - t[1]) + n;
  }
  setMap(t) {
    if (this.map_) {
      this.map_.getOverlayContainer().removeChild(this.element_);
      const e = this.element_.style;
      e.left = "inherit", e.top = "inherit", e.width = "inherit", e.height = "inherit";
    }
    this.map_ = t, this.map_ && this.map_.getOverlayContainer().appendChild(this.element_);
  }
  setPixels(t, e) {
    this.startPixel_ = t, this.endPixel_ = e, this.createOrUpdateGeometry(), this.render_();
  }
  createOrUpdateGeometry() {
    const t = this.startPixel_, e = this.endPixel_, s = [
      t,
      [t[0], e[1]],
      e,
      [e[0], t[1]]
    ].map(
      this.map_.getCoordinateFromPixelInternal,
      this.map_
    );
    s[4] = s[0].slice(), this.geometry_ ? this.geometry_.setCoordinates([s]) : this.geometry_ = new Vn([s]);
  }
  getGeometry() {
    return this.geometry_;
  }
}
const P1 = I1, yr = {
  BOXSTART: "boxstart",
  BOXDRAG: "boxdrag",
  BOXEND: "boxend",
  BOXCANCEL: "boxcancel"
};
class Ho extends Be {
  constructor(t, e, n) {
    super(t), this.coordinate = e, this.mapBrowserEvent = n;
  }
}
class A1 extends Ws {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.box_ = new P1(t.className || "ol-dragbox"), this.minArea_ = t.minArea !== void 0 ? t.minArea : 64, t.onBoxEnd && (this.onBoxEnd = t.onBoxEnd), this.startPixel_ = null, this.condition_ = t.condition ? t.condition : cd, this.boxEndCondition_ = t.boxEndCondition ? t.boxEndCondition : this.defaultBoxEndCondition;
  }
  defaultBoxEndCondition(t, e, n) {
    const s = n[0] - e[0], r = n[1] - e[1];
    return s * s + r * r >= this.minArea_;
  }
  getGeometry() {
    return this.box_.getGeometry();
  }
  handleDragEvent(t) {
    this.box_.setPixels(this.startPixel_, t.pixel), this.dispatchEvent(
      new Ho(
        yr.BOXDRAG,
        t.coordinate,
        t
      )
    );
  }
  handleUpEvent(t) {
    this.box_.setMap(null);
    const e = this.boxEndCondition_(
      t,
      this.startPixel_,
      t.pixel
    );
    return e && this.onBoxEnd(t), this.dispatchEvent(
      new Ho(
        e ? yr.BOXEND : yr.BOXCANCEL,
        t.coordinate,
        t
      )
    ), !1;
  }
  handleDownEvent(t) {
    return this.condition_(t) ? (this.startPixel_ = t.pixel, this.box_.setMap(t.map), this.box_.setPixels(this.startPixel_, this.startPixel_), this.dispatchEvent(
      new Ho(
        yr.BOXSTART,
        t.coordinate,
        t
      )
    ), !0) : !1;
  }
  onBoxEnd(t) {
  }
}
const O1 = A1;
class N1 extends O1 {
  constructor(t) {
    t = t || {};
    const e = t.condition ? t.condition : w1;
    super({
      condition: e,
      className: t.className || "ol-dragzoom",
      minArea: t.minArea
    }), this.duration_ = t.duration !== void 0 ? t.duration : 200, this.out_ = t.out !== void 0 ? t.out : !1;
  }
  onBoxEnd(t) {
    const n = this.getMap().getView();
    let s = this.getGeometry();
    if (this.out_) {
      const r = n.rotatedExtentForGeometry(s), o = n.getResolutionForExtentInternal(r), a = n.getResolution() / o;
      s = s.clone(), s.scale(a * a);
    }
    n.fitInternal(s, {
      duration: this.duration_,
      easing: jn
    });
  }
}
const F1 = N1, Fi = {
  LEFT: 37,
  UP: 38,
  RIGHT: 39,
  DOWN: 40
};
class D1 extends Us {
  constructor(t) {
    super(), t = t || {}, this.defaultCondition_ = function(e) {
      return ud(e) && dd(e);
    }, this.condition_ = t.condition !== void 0 ? t.condition : this.defaultCondition_, this.duration_ = t.duration !== void 0 ? t.duration : 100, this.pixelDelta_ = t.pixelDelta !== void 0 ? t.pixelDelta : 128;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == X.KEYDOWN) {
      const n = t.originalEvent, s = n.keyCode;
      if (this.condition_(t) && (s == Fi.DOWN || s == Fi.LEFT || s == Fi.RIGHT || s == Fi.UP)) {
        const o = t.map.getView(), a = o.getResolution() * this.pixelDelta_;
        let l = 0, h = 0;
        s == Fi.DOWN ? h = -a : s == Fi.LEFT ? l = -a : s == Fi.RIGHT ? l = a : h = a;
        const c = [l, h];
        tl(c, o.getRotation()), _1(o, c, this.duration_), n.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const k1 = D1;
class G1 extends Us {
  constructor(t) {
    super(), t = t || {}, this.condition_ = t.condition ? t.condition : dd, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 100;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == X.KEYDOWN || t.type == X.KEYPRESS) {
      const n = t.originalEvent, s = n.charCode;
      if (this.condition_(t) && (s == "+".charCodeAt(0) || s == "-".charCodeAt(0))) {
        const r = t.map, o = s == "+".charCodeAt(0) ? this.delta_ : -this.delta_, a = r.getView();
        yl(a, o, void 0, this.duration_), n.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const $1 = G1;
class B1 {
  constructor(t, e, n) {
    this.decay_ = t, this.minVelocity_ = e, this.delay_ = n, this.points_ = [], this.angle_ = 0, this.initialVelocity_ = 0;
  }
  begin() {
    this.points_.length = 0, this.angle_ = 0, this.initialVelocity_ = 0;
  }
  update(t, e) {
    this.points_.push(t, e, Date.now());
  }
  end() {
    if (this.points_.length < 6)
      return !1;
    const t = Date.now() - this.delay_, e = this.points_.length - 3;
    if (this.points_[e + 2] < t)
      return !1;
    let n = e - 3;
    for (; n > 0 && this.points_[n + 2] > t; )
      n -= 3;
    const s = this.points_[e + 2] - this.points_[n + 2];
    if (s < 1e3 / 60)
      return !1;
    const r = this.points_[e] - this.points_[n], o = this.points_[e + 1] - this.points_[n + 1];
    return this.angle_ = Math.atan2(o, r), this.initialVelocity_ = Math.sqrt(r * r + o * o) / s, this.initialVelocity_ > this.minVelocity_;
  }
  getDistance() {
    return (this.minVelocity_ - this.initialVelocity_) / this.decay_;
  }
  getAngle() {
    return this.angle_;
  }
}
const z1 = B1;
class Z1 extends Us {
  constructor(t) {
    t = t || {}, super(
      t
    ), this.totalDelta_ = 0, this.lastDelta_ = 0, this.maxDelta_ = t.maxDelta !== void 0 ? t.maxDelta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.timeout_ = t.timeout !== void 0 ? t.timeout : 80, this.useAnchor_ = t.useAnchor !== void 0 ? t.useAnchor : !0, this.constrainResolution_ = t.constrainResolution !== void 0 ? t.constrainResolution : !1;
    const e = t.condition ? t.condition : E1;
    this.condition_ = t.onFocusOnly ? Ma(hd, e) : e, this.lastAnchor_ = null, this.startTime_ = void 0, this.timeoutId_, this.mode_ = void 0, this.trackpadEventGap_ = 400, this.trackpadTimeoutId_, this.deltaPerZoom_ = 300;
  }
  endInteraction_() {
    this.trackpadTimeoutId_ = void 0;
    const t = this.getMap();
    if (!t)
      return;
    t.getView().endInteraction(
      void 0,
      this.lastDelta_ ? this.lastDelta_ > 0 ? 1 : -1 : 0,
      this.lastAnchor_
    );
  }
  handleEvent(t) {
    if (!this.condition_(t) || t.type !== X.WHEEL)
      return !0;
    const n = t.map, s = t.originalEvent;
    s.preventDefault(), this.useAnchor_ && (this.lastAnchor_ = t.coordinate);
    let r;
    if (t.type == X.WHEEL && (r = s.deltaY, m0 && s.deltaMode === WheelEvent.DOM_DELTA_PIXEL && (r /= vu), s.deltaMode === WheelEvent.DOM_DELTA_LINE && (r *= 40)), r === 0)
      return !1;
    this.lastDelta_ = r;
    const o = Date.now();
    this.startTime_ === void 0 && (this.startTime_ = o), (!this.mode_ || o - this.startTime_ > this.trackpadEventGap_) && (this.mode_ = Math.abs(r) < 4 ? "trackpad" : "wheel");
    const a = n.getView();
    if (this.mode_ === "trackpad" && !(a.getConstrainResolution() || this.constrainResolution_))
      return this.trackpadTimeoutId_ ? clearTimeout(this.trackpadTimeoutId_) : (a.getAnimating() && a.cancelAnimations(), a.beginInteraction()), this.trackpadTimeoutId_ = setTimeout(
        this.endInteraction_.bind(this),
        this.timeout_
      ), a.adjustZoom(-r / this.deltaPerZoom_, this.lastAnchor_), this.startTime_ = o, !1;
    this.totalDelta_ += r;
    const l = Math.max(this.timeout_ - (o - this.startTime_), 0);
    return clearTimeout(this.timeoutId_), this.timeoutId_ = setTimeout(
      this.handleWheelZoom_.bind(this, n),
      l
    ), !1;
  }
  handleWheelZoom_(t) {
    const e = t.getView();
    e.getAnimating() && e.cancelAnimations();
    let n = -wt(
      this.totalDelta_,
      -this.maxDelta_ * this.deltaPerZoom_,
      this.maxDelta_ * this.deltaPerZoom_
    ) / this.deltaPerZoom_;
    (e.getConstrainResolution() || this.constrainResolution_) && (n = n ? n > 0 ? 1 : -1 : 0), yl(e, n, this.lastAnchor_, this.duration_), this.mode_ = void 0, this.totalDelta_ = 0, this.lastAnchor_ = null, this.startTime_ = void 0, this.timeoutId_ = void 0;
  }
  setMouseAnchor(t) {
    this.useAnchor_ = t, t || (this.lastAnchor_ = null);
  }
}
const V1 = Z1;
class U1 extends Ws {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = ao), super(e), this.anchor_ = null, this.lastAngle_ = void 0, this.rotating_ = !1, this.rotationDelta_ = 0, this.threshold_ = t.threshold !== void 0 ? t.threshold : 0.3, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleDragEvent(t) {
    let e = 0;
    const n = this.targetPointers[0], s = this.targetPointers[1], r = Math.atan2(
      s.clientY - n.clientY,
      s.clientX - n.clientX
    );
    if (this.lastAngle_ !== void 0) {
      const c = r - this.lastAngle_;
      this.rotationDelta_ += c, !this.rotating_ && Math.abs(this.rotationDelta_) > this.threshold_ && (this.rotating_ = !0), e = c;
    }
    this.lastAngle_ = r;
    const o = t.map, a = o.getView();
    if (a.getConstraints().rotation === hl)
      return;
    const l = o.getViewport().getBoundingClientRect(), h = vl(this.targetPointers);
    h[0] -= l.left, h[1] -= l.top, this.anchor_ = o.getCoordinateFromPixelInternal(h), this.rotating_ && (o.render(), a.adjustRotationInternal(e, this.anchor_));
  }
  handleUpEvent(t) {
    return this.targetPointers.length < 2 ? (t.map.getView().endInteraction(this.duration_), !1) : !0;
  }
  handleDownEvent(t) {
    if (this.targetPointers.length >= 2) {
      const e = t.map;
      return this.anchor_ = null, this.lastAngle_ = void 0, this.rotating_ = !1, this.rotationDelta_ = 0, this.handlingDownUpSequence || e.getView().beginInteraction(), !0;
    } else
      return !1;
  }
}
const W1 = U1;
class H1 extends Ws {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = ao), super(e), this.anchor_ = null, this.duration_ = t.duration !== void 0 ? t.duration : 400, this.lastDistance_ = void 0, this.lastScaleDelta_ = 1;
  }
  handleDragEvent(t) {
    let e = 1;
    const n = this.targetPointers[0], s = this.targetPointers[1], r = n.clientX - s.clientX, o = n.clientY - s.clientY, a = Math.sqrt(r * r + o * o);
    this.lastDistance_ !== void 0 && (e = this.lastDistance_ / a), this.lastDistance_ = a;
    const l = t.map, h = l.getView();
    e != 1 && (this.lastScaleDelta_ = e);
    const c = l.getViewport().getBoundingClientRect(), u = vl(this.targetPointers);
    u[0] -= c.left, u[1] -= c.top, this.anchor_ = l.getCoordinateFromPixelInternal(u), l.render(), h.adjustResolutionInternal(e, this.anchor_);
  }
  handleUpEvent(t) {
    if (this.targetPointers.length < 2) {
      const n = t.map.getView(), s = this.lastScaleDelta_ > 1 ? 1 : -1;
      return n.endInteraction(this.duration_, s), !1;
    } else
      return !0;
  }
  handleDownEvent(t) {
    if (this.targetPointers.length >= 2) {
      const e = t.map;
      return this.anchor_ = null, this.lastDistance_ = void 0, this.lastScaleDelta_ = 1, this.handlingDownUpSequence || e.getView().beginInteraction(), !0;
    } else
      return !1;
  }
}
const X1 = H1;
function Y1(i) {
  i = i || {};
  const t = new Ae(), e = new z1(-5e-3, 0.05, 100);
  return (i.altShiftDragRotate !== void 0 ? i.altShiftDragRotate : !0) && t.push(new T1()), (i.doubleClickZoom !== void 0 ? i.doubleClickZoom : !0) && t.push(
    new v1({
      delta: i.zoomDelta,
      duration: i.zoomDuration
    })
  ), (i.dragPan !== void 0 ? i.dragPan : !0) && t.push(
    new b1({
      onFocusOnly: i.onFocusOnly,
      kinetic: e
    })
  ), (i.pinchRotate !== void 0 ? i.pinchRotate : !0) && t.push(new W1()), (i.pinchZoom !== void 0 ? i.pinchZoom : !0) && t.push(
    new X1({
      duration: i.zoomDuration
    })
  ), (i.keyboard !== void 0 ? i.keyboard : !0) && (t.push(new k1()), t.push(
    new $1({
      delta: i.zoomDelta,
      duration: i.zoomDuration
    })
  )), (i.mouseWheelZoom !== void 0 ? i.mouseWheelZoom : !0) && t.push(
    new V1({
      onFocusOnly: i.onFocusOnly,
      duration: i.zoomDuration
    })
  ), (i.shiftDragZoom !== void 0 ? i.shiftDragZoom : !0) && t.push(
    new F1({
      duration: i.zoomDuration
    })
  ), t;
}
function kh(i) {
  return i[0] > 0 && i[1] > 0;
}
function j1(i, t, e) {
  return e === void 0 && (e = [0, 0]), e[0] = i[0] * t + 0.5 | 0, e[1] = i[1] * t + 0.5 | 0, e;
}
function ce(i, t) {
  return Array.isArray(i) ? i : (t === void 0 ? t = [i, i] : (t[0] = i, t[1] = i), t);
}
function fd(i) {
  if (i instanceof po) {
    i.setMapInternal(null);
    return;
  }
  i instanceof yo && i.getLayers().forEach(fd);
}
function gd(i, t) {
  if (i instanceof po) {
    i.setMapInternal(t);
    return;
  }
  if (i instanceof yo) {
    const e = i.getLayers().getArray();
    for (let n = 0, s = e.length; n < s; ++n)
      gd(e[n], t);
  }
}
class K1 extends Ce {
  constructor(t) {
    super(), t = t || {}, this.on, this.once, this.un;
    const e = q1(t);
    this.renderComplete_, this.loaded_ = !0, this.boundHandleBrowserEvent_ = this.handleBrowserEvent.bind(this), this.maxTilesLoading_ = t.maxTilesLoading !== void 0 ? t.maxTilesLoading : 16, this.pixelRatio_ = t.pixelRatio !== void 0 ? t.pixelRatio : vu, this.postRenderTimeoutHandle_, this.animationDelayKey_, this.animationDelay_ = this.animationDelay_.bind(this), this.coordinateToPixelTransform_ = Fe(), this.pixelToCoordinateTransform_ = Fe(), this.frameIndex_ = 0, this.frameState_ = null, this.previousExtent_ = null, this.viewPropertyListenerKey_ = null, this.viewChangeListenerKey_ = null, this.layerGroupPropertyListenerKeys_ = null, this.viewport_ = document.createElement("div"), this.viewport_.className = "ol-viewport" + ("ontouchstart" in window ? " ol-touch" : ""), this.viewport_.style.position = "relative", this.viewport_.style.overflow = "hidden", this.viewport_.style.width = "100%", this.viewport_.style.height = "100%", this.overlayContainer_ = document.createElement("div"), this.overlayContainer_.style.position = "absolute", this.overlayContainer_.style.zIndex = "0", this.overlayContainer_.style.width = "100%", this.overlayContainer_.style.height = "100%", this.overlayContainer_.style.pointerEvents = "none", this.overlayContainer_.className = "ol-overlaycontainer", this.viewport_.appendChild(this.overlayContainer_), this.overlayContainerStopEvent_ = document.createElement("div"), this.overlayContainerStopEvent_.style.position = "absolute", this.overlayContainerStopEvent_.style.zIndex = "0", this.overlayContainerStopEvent_.style.width = "100%", this.overlayContainerStopEvent_.style.height = "100%", this.overlayContainerStopEvent_.style.pointerEvents = "none", this.overlayContainerStopEvent_.className = "ol-overlaycontainer-stopevent", this.viewport_.appendChild(this.overlayContainerStopEvent_), this.mapBrowserEventHandler_ = null, this.moveTolerance_ = t.moveTolerance, this.keyboardEventTarget_ = e.keyboardEventTarget, this.targetChangeHandlerKeys_ = null, this.controls = e.controls || m1(), this.interactions = e.interactions || Y1({
      onFocusOnly: !0
    }), this.overlays_ = e.overlays, this.overlayIdIndex_ = {}, this.renderer_ = null, this.postRenderFunctions_ = [], this.tileQueue_ = new ug(
      this.getTilePriority.bind(this),
      this.handleTileChange_.bind(this)
    ), this.addChangeListener(
      Ot.LAYERGROUP,
      this.handleLayerGroupChanged_
    ), this.addChangeListener(Ot.VIEW, this.handleViewChanged_), this.addChangeListener(Ot.SIZE, this.handleSizeChanged_), this.addChangeListener(Ot.TARGET, this.handleTargetChanged_), this.setProperties(e.values);
    const n = this;
    t.view && !(t.view instanceof ti) && t.view.then(function(s) {
      n.setView(new ti(s));
    }), this.controls.addEventListener(
      ee.ADD,
      function(s) {
        s.element.setMap(this);
      }.bind(this)
    ), this.controls.addEventListener(
      ee.REMOVE,
      function(s) {
        s.element.setMap(null);
      }.bind(this)
    ), this.interactions.addEventListener(
      ee.ADD,
      function(s) {
        s.element.setMap(this);
      }.bind(this)
    ), this.interactions.addEventListener(
      ee.REMOVE,
      function(s) {
        s.element.setMap(null);
      }.bind(this)
    ), this.overlays_.addEventListener(
      ee.ADD,
      function(s) {
        this.addOverlayInternal_(s.element);
      }.bind(this)
    ), this.overlays_.addEventListener(
      ee.REMOVE,
      function(s) {
        const r = s.element.getId();
        r !== void 0 && delete this.overlayIdIndex_[r.toString()], s.element.setMap(null);
      }.bind(this)
    ), this.controls.forEach(
      function(s) {
        s.setMap(this);
      }.bind(this)
    ), this.interactions.forEach(
      function(s) {
        s.setMap(this);
      }.bind(this)
    ), this.overlays_.forEach(this.addOverlayInternal_.bind(this));
  }
  addControl(t) {
    this.getControls().push(t);
  }
  addInteraction(t) {
    this.getInteractions().push(t);
  }
  addLayer(t) {
    this.getLayerGroup().getLayers().push(t);
  }
  handleLayerAdd_(t) {
    gd(t.layer, this);
  }
  addOverlay(t) {
    this.getOverlays().push(t);
  }
  addOverlayInternal_(t) {
    const e = t.getId();
    e !== void 0 && (this.overlayIdIndex_[e.toString()] = t), t.setMap(this);
  }
  disposeInternal() {
    this.controls.clear(), this.interactions.clear(), this.overlays_.clear(), this.setTarget(null), super.disposeInternal();
  }
  forEachFeatureAtPixel(t, e, n) {
    if (!this.frameState_ || !this.renderer_)
      return;
    const s = this.getCoordinateFromPixelInternal(t);
    n = n !== void 0 ? n : {};
    const r = n.hitTolerance !== void 0 ? n.hitTolerance : 0, o = n.layerFilter !== void 0 ? n.layerFilter : Ms, a = n.checkWrapped !== !1;
    return this.renderer_.forEachFeatureAtCoordinate(
      s,
      this.frameState_,
      r,
      a,
      e,
      null,
      o,
      null
    );
  }
  getFeaturesAtPixel(t, e) {
    const n = [];
    return this.forEachFeatureAtPixel(
      t,
      function(s) {
        n.push(s);
      },
      e
    ), n;
  }
  getAllLayers() {
    const t = [];
    function e(n) {
      n.forEach(function(s) {
        s instanceof yo ? e(s.getLayers()) : t.push(s);
      });
    }
    return e(this.getLayers()), t;
  }
  hasFeatureAtPixel(t, e) {
    if (!this.frameState_ || !this.renderer_)
      return !1;
    const n = this.getCoordinateFromPixelInternal(t);
    e = e !== void 0 ? e : {};
    const s = e.layerFilter !== void 0 ? e.layerFilter : Ms, r = e.hitTolerance !== void 0 ? e.hitTolerance : 0, o = e.checkWrapped !== !1;
    return this.renderer_.hasFeatureAtCoordinate(
      n,
      this.frameState_,
      r,
      o,
      s,
      null
    );
  }
  getEventCoordinate(t) {
    return this.getCoordinateFromPixel(this.getEventPixel(t));
  }
  getEventCoordinateInternal(t) {
    return this.getCoordinateFromPixelInternal(this.getEventPixel(t));
  }
  getEventPixel(t) {
    const e = this.viewport_.getBoundingClientRect(), n = "changedTouches" in t ? t.changedTouches[0] : t;
    return [
      n.clientX - e.left,
      n.clientY - e.top
    ];
  }
  getTarget() {
    return this.get(Ot.TARGET);
  }
  getTargetElement() {
    const t = this.getTarget();
    return t !== void 0 ? typeof t == "string" ? document.getElementById(t) : t : null;
  }
  getCoordinateFromPixel(t) {
    return ya(
      this.getCoordinateFromPixelInternal(t),
      this.getView().getProjection()
    );
  }
  getCoordinateFromPixelInternal(t) {
    const e = this.frameState_;
    return e ? Ft(
      e.pixelToCoordinateTransform,
      t.slice()
    ) : null;
  }
  getControls() {
    return this.controls;
  }
  getOverlays() {
    return this.overlays_;
  }
  getOverlayById(t) {
    const e = this.overlayIdIndex_[t.toString()];
    return e !== void 0 ? e : null;
  }
  getInteractions() {
    return this.interactions;
  }
  getLayerGroup() {
    return this.get(Ot.LAYERGROUP);
  }
  setLayers(t) {
    const e = this.getLayerGroup();
    if (t instanceof Ae) {
      e.setLayers(t);
      return;
    }
    const n = e.getLayers();
    n.clear(), n.extend(t);
  }
  getLayers() {
    return this.getLayerGroup().getLayers();
  }
  getLoadingOrNotReady() {
    const t = this.getLayerGroup().getLayerStatesArray();
    for (let e = 0, n = t.length; e < n; ++e) {
      const s = t[e];
      if (!s.visible)
        continue;
      const r = s.layer.getRenderer();
      if (r && !r.ready)
        return !0;
      const o = s.layer.getSource();
      if (o && o.loading)
        return !0;
    }
    return !1;
  }
  getPixelFromCoordinate(t) {
    const e = Ke(
      t,
      this.getView().getProjection()
    );
    return this.getPixelFromCoordinateInternal(e);
  }
  getPixelFromCoordinateInternal(t) {
    const e = this.frameState_;
    return e ? Ft(
      e.coordinateToPixelTransform,
      t.slice(0, 2)
    ) : null;
  }
  getRenderer() {
    return this.renderer_;
  }
  getSize() {
    return this.get(Ot.SIZE);
  }
  getView() {
    return this.get(Ot.VIEW);
  }
  getViewport() {
    return this.viewport_;
  }
  getOverlayContainer() {
    return this.overlayContainer_;
  }
  getOverlayContainerStopEvent() {
    return this.overlayContainerStopEvent_;
  }
  getOwnerDocument() {
    const t = this.getTargetElement();
    return t ? t.ownerDocument : document;
  }
  getTilePriority(t, e, n, s) {
    return dg(
      this.frameState_,
      t,
      e,
      n,
      s
    );
  }
  handleBrowserEvent(t, e) {
    e = e || t.type;
    const n = new mi(e, this, t);
    this.handleMapBrowserEvent(n);
  }
  handleMapBrowserEvent(t) {
    if (!this.frameState_)
      return;
    const e = t.originalEvent, n = e.type;
    if (n === ga.POINTERDOWN || n === X.WHEEL || n === X.KEYDOWN) {
      const s = this.getOwnerDocument(), r = this.viewport_.getRootNode ? this.viewport_.getRootNode() : s, o = e.target;
      if (this.overlayContainerStopEvent_.contains(o) || !(r === s ? s.documentElement : r).contains(o))
        return;
    }
    if (t.frameState = this.frameState_, this.dispatchEvent(t) !== !1) {
      const s = this.getInteractions().getArray().slice();
      for (let r = s.length - 1; r >= 0; r--) {
        const o = s[r];
        if (o.getMap() !== this || !o.getActive() || !this.getTargetElement())
          continue;
        if (!o.handleEvent(t) || t.propagationStopped)
          break;
      }
    }
  }
  handlePostRender() {
    const t = this.frameState_, e = this.tileQueue_;
    if (!e.isEmpty()) {
      let s = this.maxTilesLoading_, r = s;
      if (t) {
        const o = t.viewHints;
        if (o[Zt.ANIMATING] || o[Zt.INTERACTING]) {
          const a = Date.now() - t.time > 8;
          s = a ? 0 : 8, r = a ? 0 : 2;
        }
      }
      e.getTilesLoading() < s && (e.reprioritize(), e.loadMoreTiles(s, r));
    }
    t && this.renderer_ && !t.animate && (this.renderComplete_ === !0 ? (this.hasListener(Ci.RENDERCOMPLETE) && this.renderer_.dispatchRenderEvent(
      Ci.RENDERCOMPLETE,
      t
    ), this.loaded_ === !1 && (this.loaded_ = !0, this.dispatchEvent(
      new Cn(qe.LOADEND, this, t)
    ))) : this.loaded_ === !0 && (this.loaded_ = !1, this.dispatchEvent(
      new Cn(qe.LOADSTART, this, t)
    )));
    const n = this.postRenderFunctions_;
    for (let s = 0, r = n.length; s < r; ++s)
      n[s](this, t);
    n.length = 0;
  }
  handleSizeChanged_() {
    this.getView() && !this.getView().getAnimating() && this.getView().resolveConstraints(0), this.render();
  }
  handleTargetChanged_() {
    if (this.mapBrowserEventHandler_) {
      for (let e = 0, n = this.targetChangeHandlerKeys_.length; e < n; ++e)
        pt(this.targetChangeHandlerKeys_[e]);
      this.targetChangeHandlerKeys_ = null, this.viewport_.removeEventListener(
        X.CONTEXTMENU,
        this.boundHandleBrowserEvent_
      ), this.viewport_.removeEventListener(
        X.WHEEL,
        this.boundHandleBrowserEvent_
      ), this.mapBrowserEventHandler_.dispose(), this.mapBrowserEventHandler_ = null, zr(this.viewport_);
    }
    const t = this.getTargetElement();
    if (!t)
      this.renderer_ && (clearTimeout(this.postRenderTimeoutHandle_), this.postRenderTimeoutHandle_ = void 0, this.postRenderFunctions_.length = 0, this.renderer_.dispose(), this.renderer_ = null), this.animationDelayKey_ && (cancelAnimationFrame(this.animationDelayKey_), this.animationDelayKey_ = void 0);
    else {
      t.appendChild(this.viewport_), this.renderer_ || (this.renderer_ = new ng(this)), this.mapBrowserEventHandler_ = new ag(
        this,
        this.moveTolerance_
      );
      for (const s in Mt)
        this.mapBrowserEventHandler_.addEventListener(
          Mt[s],
          this.handleMapBrowserEvent.bind(this)
        );
      this.viewport_.addEventListener(
        X.CONTEXTMENU,
        this.boundHandleBrowserEvent_,
        !1
      ), this.viewport_.addEventListener(
        X.WHEEL,
        this.boundHandleBrowserEvent_,
        xu ? { passive: !1 } : !1
      );
      const e = this.getOwnerDocument().defaultView, n = this.keyboardEventTarget_ ? this.keyboardEventTarget_ : t;
      this.targetChangeHandlerKeys_ = [
        et(
          n,
          X.KEYDOWN,
          this.handleBrowserEvent,
          this
        ),
        et(
          n,
          X.KEYPRESS,
          this.handleBrowserEvent,
          this
        ),
        et(e, X.RESIZE, this.updateSize, this)
      ];
    }
    this.updateSize();
  }
  handleTileChange_() {
    this.render();
  }
  handleViewPropertyChanged_() {
    this.render();
  }
  handleViewChanged_() {
    this.viewPropertyListenerKey_ && (pt(this.viewPropertyListenerKey_), this.viewPropertyListenerKey_ = null), this.viewChangeListenerKey_ && (pt(this.viewChangeListenerKey_), this.viewChangeListenerKey_ = null);
    const t = this.getView();
    t && (this.updateViewportSize_(), this.viewPropertyListenerKey_ = et(
      t,
      kn.PROPERTYCHANGE,
      this.handleViewPropertyChanged_,
      this
    ), this.viewChangeListenerKey_ = et(
      t,
      X.CHANGE,
      this.handleViewPropertyChanged_,
      this
    ), t.resolveConstraints(0)), this.render();
  }
  handleLayerGroupChanged_() {
    this.layerGroupPropertyListenerKeys_ && (this.layerGroupPropertyListenerKeys_.forEach(pt), this.layerGroupPropertyListenerKeys_ = null);
    const t = this.getLayerGroup();
    t && (this.handleLayerAdd_(new _i("addlayer", t)), this.layerGroupPropertyListenerKeys_ = [
      et(t, kn.PROPERTYCHANGE, this.render, this),
      et(t, X.CHANGE, this.render, this),
      et(t, "addlayer", this.handleLayerAdd_, this),
      et(t, "removelayer", this.handleLayerRemove_, this)
    ]), this.render();
  }
  isRendered() {
    return !!this.frameState_;
  }
  animationDelay_() {
    this.animationDelayKey_ = void 0, this.renderFrame_(Date.now());
  }
  renderSync() {
    this.animationDelayKey_ && cancelAnimationFrame(this.animationDelayKey_), this.animationDelay_();
  }
  redrawText() {
    const t = this.getLayerGroup().getLayerStatesArray();
    for (let e = 0, n = t.length; e < n; ++e) {
      const s = t[e].layer;
      s.hasRenderer() && s.getRenderer().handleFontsChanged();
    }
  }
  render() {
    this.renderer_ && this.animationDelayKey_ === void 0 && (this.animationDelayKey_ = requestAnimationFrame(this.animationDelay_));
  }
  removeControl(t) {
    return this.getControls().remove(t);
  }
  removeInteraction(t) {
    return this.getInteractions().remove(t);
  }
  removeLayer(t) {
    return this.getLayerGroup().getLayers().remove(t);
  }
  handleLayerRemove_(t) {
    fd(t.layer);
  }
  removeOverlay(t) {
    return this.getOverlays().remove(t);
  }
  renderFrame_(t) {
    const e = this.getSize(), n = this.getView(), s = this.frameState_;
    let r = null;
    if (e !== void 0 && kh(e) && n && n.isDef()) {
      const o = n.getHints(
        this.frameState_ ? this.frameState_.viewHints : void 0
      ), a = n.getState();
      if (r = {
        animate: !1,
        coordinateToPixelTransform: this.coordinateToPixelTransform_,
        declutterTree: null,
        extent: ca(
          a.center,
          a.resolution,
          a.rotation,
          e
        ),
        index: this.frameIndex_++,
        layerIndex: 0,
        layerStatesArray: this.getLayerGroup().getLayerStatesArray(),
        pixelRatio: this.pixelRatio_,
        pixelToCoordinateTransform: this.pixelToCoordinateTransform_,
        postRenderFunctions: [],
        size: e,
        tileQueue: this.tileQueue_,
        time: t,
        usedTiles: {},
        viewState: a,
        viewHints: o,
        wantedTiles: {},
        mapId: ot(this),
        renderTargets: {}
      }, a.nextCenter && a.nextResolution) {
        const l = isNaN(a.nextRotation) ? a.rotation : a.nextRotation;
        r.nextExtent = ca(
          a.nextCenter,
          a.nextResolution,
          l,
          e
        );
      }
    }
    this.frameState_ = r, this.renderer_.renderFrame(r), r && (r.animate && this.render(), Array.prototype.push.apply(
      this.postRenderFunctions_,
      r.postRenderFunctions
    ), s && (!this.previousExtent_ || !Ja(this.previousExtent_) && !Es(r.extent, this.previousExtent_)) && (this.dispatchEvent(
      new Cn(qe.MOVESTART, this, s)
    ), this.previousExtent_ = Zs(this.previousExtent_)), this.previousExtent_ && !r.viewHints[Zt.ANIMATING] && !r.viewHints[Zt.INTERACTING] && !Es(r.extent, this.previousExtent_) && (this.dispatchEvent(
      new Cn(qe.MOVEEND, this, r)
    ), Mu(r.extent, this.previousExtent_))), this.dispatchEvent(new Cn(qe.POSTRENDER, this, r)), this.renderComplete_ = this.hasListener(qe.LOADSTART) || this.hasListener(qe.LOADEND) || this.hasListener(Ci.RENDERCOMPLETE) ? !this.tileQueue_.getTilesLoading() && !this.tileQueue_.getCount() && !this.getLoadingOrNotReady() : void 0, this.postRenderTimeoutHandle_ || (this.postRenderTimeoutHandle_ = setTimeout(() => {
      this.postRenderTimeoutHandle_ = void 0, this.handlePostRender();
    }, 0));
  }
  setLayerGroup(t) {
    const e = this.getLayerGroup();
    e && this.handleLayerRemove_(new _i("removelayer", e)), this.set(Ot.LAYERGROUP, t);
  }
  setSize(t) {
    this.set(Ot.SIZE, t);
  }
  setTarget(t) {
    this.set(Ot.TARGET, t);
  }
  setView(t) {
    if (!t || t instanceof ti) {
      this.set(Ot.VIEW, t);
      return;
    }
    this.set(Ot.VIEW, new ti());
    const e = this;
    t.then(function(n) {
      e.setView(new ti(n));
    });
  }
  updateSize() {
    const t = this.getTargetElement();
    let e;
    if (t) {
      const n = getComputedStyle(t), s = t.offsetWidth - parseFloat(n.borderLeftWidth) - parseFloat(n.paddingLeft) - parseFloat(n.paddingRight) - parseFloat(n.borderRightWidth), r = t.offsetHeight - parseFloat(n.borderTopWidth) - parseFloat(n.paddingTop) - parseFloat(n.paddingBottom) - parseFloat(n.borderBottomWidth);
      !isNaN(s) && !isNaN(r) && (e = [s, r], !kh(e) && !!(t.offsetWidth || t.offsetHeight || t.getClientRects().length) && console.warn(
        "No map visible because the map container's width or height are 0."
      ));
    }
    this.setSize(e), this.updateViewportSize_();
  }
  updateViewportSize_() {
    const t = this.getView();
    if (t) {
      let e;
      const n = getComputedStyle(this.viewport_);
      n.width && n.height && (e = [
        parseInt(n.width, 10),
        parseInt(n.height, 10)
      ]), t.setViewportSize(e);
    }
  }
}
function q1(i) {
  let t = null;
  i.keyboardEventTarget !== void 0 && (t = typeof i.keyboardEventTarget == "string" ? document.getElementById(i.keyboardEventTarget) : i.keyboardEventTarget);
  const e = {}, n = i.layers && typeof i.layers.getLayers == "function" ? i.layers : new yo({
    layers: i.layers
  });
  e[Ot.LAYERGROUP] = n, e[Ot.TARGET] = i.target, e[Ot.VIEW] = i.view instanceof ti ? i.view : new ti();
  let s;
  i.controls !== void 0 && (Array.isArray(i.controls) ? s = new Ae(i.controls.slice()) : (Y(
    typeof i.controls.getArray == "function",
    47
  ), s = i.controls));
  let r;
  i.interactions !== void 0 && (Array.isArray(i.interactions) ? r = new Ae(i.interactions.slice()) : (Y(
    typeof i.interactions.getArray == "function",
    48
  ), r = i.interactions));
  let o;
  return i.overlays !== void 0 ? Array.isArray(i.overlays) ? o = new Ae(i.overlays.slice()) : (Y(
    typeof i.overlays.getArray == "function",
    49
  ), o = i.overlays) : o = new Ae(), {
    controls: s,
    interactions: r,
    keyboardEventTarget: t,
    overlays: o,
    values: e
  };
}
const J1 = K1;
class xl extends Ce {
  constructor(t) {
    if (super(), this.on, this.once, this.un, this.id_ = void 0, this.geometryName_ = "geometry", this.style_ = null, this.styleFunction_ = void 0, this.geometryChangeKey_ = null, this.addChangeListener(this.geometryName_, this.handleGeometryChanged_), t)
      if (typeof t.getSimplifiedGeometry == "function") {
        const e = t;
        this.setGeometry(e);
      } else {
        const e = t;
        this.setProperties(e);
      }
  }
  clone() {
    const t = new xl(this.hasProperties() ? this.getProperties() : null);
    t.setGeometryName(this.getGeometryName());
    const e = this.getGeometry();
    e && t.setGeometry(e.clone());
    const n = this.getStyle();
    return n && t.setStyle(n), t;
  }
  getGeometry() {
    return this.get(this.geometryName_);
  }
  getId() {
    return this.id_;
  }
  getGeometryName() {
    return this.geometryName_;
  }
  getStyle() {
    return this.style_;
  }
  getStyleFunction() {
    return this.styleFunction_;
  }
  handleGeometryChange_() {
    this.changed();
  }
  handleGeometryChanged_() {
    this.geometryChangeKey_ && (pt(this.geometryChangeKey_), this.geometryChangeKey_ = null);
    const t = this.getGeometry();
    t && (this.geometryChangeKey_ = et(
      t,
      X.CHANGE,
      this.handleGeometryChange_,
      this
    )), this.changed();
  }
  setGeometry(t) {
    this.set(this.geometryName_, t);
  }
  setStyle(t) {
    this.style_ = t, this.styleFunction_ = t ? Q1(t) : void 0, this.changed();
  }
  setId(t) {
    this.id_ = t, this.changed();
  }
  setGeometryName(t) {
    this.removeChangeListener(this.geometryName_, this.handleGeometryChanged_), this.geometryName_ = t, this.addChangeListener(this.geometryName_, this.handleGeometryChanged_), this.handleGeometryChanged_();
  }
}
function Q1(i) {
  if (typeof i == "function")
    return i;
  {
    let t;
    return Array.isArray(i) ? t = i : (Y(typeof i.getZIndex == "function", 41), t = [i]), function() {
      return t;
    };
  }
}
const on = xl, vt = {
  ACCURACY: "accuracy",
  ACCURACY_GEOMETRY: "accuracyGeometry",
  ALTITUDE: "altitude",
  ALTITUDE_ACCURACY: "altitudeAccuracy",
  HEADING: "heading",
  POSITION: "position",
  PROJECTION: "projection",
  SPEED: "speed",
  TRACKING: "tracking",
  TRACKING_OPTIONS: "trackingOptions"
};
class tm extends Be {
  constructor(t) {
    super(X.ERROR), this.code = t.code, this.message = t.message;
  }
}
class em extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.position_ = null, this.transform_ = rl, this.watchId_ = void 0, this.addChangeListener(vt.PROJECTION, this.handleProjectionChanged_), this.addChangeListener(vt.TRACKING, this.handleTrackingChanged_), t.projection !== void 0 && this.setProjection(t.projection), t.trackingOptions !== void 0 && this.setTrackingOptions(t.trackingOptions), this.setTracking(t.tracking !== void 0 ? t.tracking : !1);
  }
  disposeInternal() {
    this.setTracking(!1), super.disposeInternal();
  }
  handleProjectionChanged_() {
    const t = this.getProjection();
    t && (this.transform_ = vo(
      J("EPSG:4326"),
      t
    ), this.position_ && this.set(vt.POSITION, this.transform_(this.position_)));
  }
  handleTrackingChanged_() {
    if ("geolocation" in navigator) {
      const t = this.getTracking();
      t && this.watchId_ === void 0 ? this.watchId_ = navigator.geolocation.watchPosition(
        this.positionChange_.bind(this),
        this.positionError_.bind(this),
        this.getTrackingOptions()
      ) : !t && this.watchId_ !== void 0 && (navigator.geolocation.clearWatch(this.watchId_), this.watchId_ = void 0);
    }
  }
  positionChange_(t) {
    const e = t.coords;
    this.set(vt.ACCURACY, e.accuracy), this.set(
      vt.ALTITUDE,
      e.altitude === null ? void 0 : e.altitude
    ), this.set(
      vt.ALTITUDE_ACCURACY,
      e.altitudeAccuracy === null ? void 0 : e.altitudeAccuracy
    ), this.set(
      vt.HEADING,
      e.heading === null ? void 0 : Ui(e.heading)
    ), this.position_ ? (this.position_[0] = e.longitude, this.position_[1] = e.latitude) : this.position_ = [e.longitude, e.latitude];
    const n = this.transform_(this.position_);
    this.set(vt.POSITION, n), this.set(vt.SPEED, e.speed === null ? void 0 : e.speed);
    const s = n1(this.position_, e.accuracy);
    s.applyTransform(this.transform_), this.set(vt.ACCURACY_GEOMETRY, s), this.changed();
  }
  positionError_(t) {
    this.dispatchEvent(new tm(t));
  }
  getAccuracy() {
    return this.get(vt.ACCURACY);
  }
  getAccuracyGeometry() {
    return this.get(vt.ACCURACY_GEOMETRY) || null;
  }
  getAltitude() {
    return this.get(vt.ALTITUDE);
  }
  getAltitudeAccuracy() {
    return this.get(vt.ALTITUDE_ACCURACY);
  }
  getHeading() {
    return this.get(vt.HEADING);
  }
  getPosition() {
    return this.get(vt.POSITION);
  }
  getProjection() {
    return this.get(vt.PROJECTION);
  }
  getSpeed() {
    return this.get(vt.SPEED);
  }
  getTracking() {
    return this.get(vt.TRACKING);
  }
  getTrackingOptions() {
    return this.get(vt.TRACKING_OPTIONS);
  }
  setProjection(t) {
    this.set(vt.PROJECTION, J(t));
  }
  setTracking(t) {
    this.set(vt.TRACKING, t);
  }
  setTrackingOptions(t) {
    this.set(vt.TRACKING_OPTIONS, t);
  }
}
const im = em;
class Cl {
  constructor(t) {
    t = t || {}, this.color_ = t.color !== void 0 ? t.color : null;
  }
  clone() {
    const t = this.getColor();
    return new Cl({
      color: Array.isArray(t) ? t.slice() : t || void 0
    });
  }
  getColor() {
    return this.color_;
  }
  setColor(t) {
    this.color_ = t;
  }
}
const Yt = Cl;
function md(i, t, e, n, s, r, o) {
  let a, l;
  const h = (e - t) / n;
  if (h === 1)
    a = t;
  else if (h === 2)
    a = t, l = s;
  else if (h !== 0) {
    let c = i[t], u = i[t + 1], d = 0;
    const f = [0];
    for (let p = t + n; p < e; p += n) {
      const _ = i[p], y = i[p + 1];
      d += Math.sqrt((_ - c) * (_ - c) + (y - u) * (y - u)), f.push(d), c = _, u = y;
    }
    const g = s * d, m = s0(f, g);
    m < 0 ? (l = (g - f[-m - 2]) / (f[-m - 1] - f[-m - 2]), a = t + (-m - 2) * n) : a = t + m * n;
  }
  o = o > 1 ? o : 2, r = r || new Array(o);
  for (let c = 0; c < o; ++c)
    r[c] = a === void 0 ? NaN : l === void 0 ? i[a + c] : Je(i[a + c], i[a + n + c], l);
  return r;
}
function Ea(i, t, e, n, s, r) {
  if (e == t)
    return null;
  let o;
  if (s < i[t + n - 1])
    return r ? (o = i.slice(t, t + n), o[n - 1] = s, o) : null;
  if (i[e - 1] < s)
    return r ? (o = i.slice(e - n, e), o[n - 1] = s, o) : null;
  if (s == i[t + n - 1])
    return i.slice(t, t + n);
  let a = t / n, l = e / n;
  for (; a < l; ) {
    const d = a + l >> 1;
    s < i[(d + 1) * n - 1] ? l = d : a = d + 1;
  }
  const h = i[a * n - 1];
  if (s == h)
    return i.slice((a - 1) * n, (a - 1) * n + n);
  const c = i[(a + 1) * n - 1], u = (s - h) / (c - h);
  o = [];
  for (let d = 0; d < n - 1; ++d)
    o.push(
      Je(
        i[(a - 1) * n + d],
        i[a * n + d],
        u
      )
    );
  return o.push(s), o;
}
function nm(i, t, e, n, s, r, o) {
  if (o)
    return Ea(
      i,
      t,
      e[e.length - 1],
      n,
      s,
      r
    );
  let a;
  if (s < i[n - 1])
    return r ? (a = i.slice(0, n), a[n - 1] = s, a) : null;
  if (i[i.length - 1] < s)
    return r ? (a = i.slice(i.length - n), a[n - 1] = s, a) : null;
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    if (t != c) {
      if (s < i[t + n - 1])
        return null;
      if (s <= i[c - 1])
        return Ea(
          i,
          t,
          c,
          n,
          s,
          !1
        );
      t = c;
    }
  }
  return null;
}
function pd(i, t, e, n) {
  let s = i[t], r = i[t + 1], o = 0;
  for (let a = t + n; a < e; a += n) {
    const l = i[a], h = i[a + 1];
    o += Math.sqrt((l - s) * (l - s) + (h - r) * (h - r)), s = l, r = h;
  }
  return o;
}
class Yr extends rn {
  constructor(t, e) {
    super(), this.flatMidpoint_ = null, this.flatMidpointRevision_ = -1, this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, e !== void 0 && !Array.isArray(t[0]) ? this.setFlatCoordinates(
      e,
      t
    ) : this.setCoordinates(
      t,
      e
    );
  }
  appendCoordinate(t) {
    this.flatCoordinates ? Kt(this.flatCoordinates, t) : this.flatCoordinates = t.slice(), this.changed();
  }
  clone() {
    const t = new Yr(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < sn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      cl(
        this.flatCoordinates,
        0,
        this.flatCoordinates.length,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), dl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      this.maxDelta_,
      !1,
      t,
      e,
      n,
      s
    ));
  }
  forEachSegment(t) {
    return nd(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinateAtM(t, e) {
    return this.layout != "XYM" && this.layout != "XYZM" ? null : (e = e !== void 0 ? e : !1, Ea(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e
    ));
  }
  getCoordinates() {
    return vi(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinateAt(t, e) {
    return md(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e,
      this.stride
    );
  }
  getLength() {
    return pd(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getFlatMidpoint() {
    return this.flatMidpointRevision_ != this.getRevision() && (this.flatMidpoint_ = this.getCoordinateAt(0.5, this.flatMidpoint_), this.flatMidpointRevision_ = this.getRevision()), this.flatMidpoint_;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [];
    return e.length = ml(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e,
      0
    ), new Yr(e, "XY");
  }
  getType() {
    return "LineString";
  }
  intersectsExtent(t) {
    return Co(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = xo(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const As = Yr;
class Ml {
  constructor(t) {
    t = t || {}, this.color_ = t.color !== void 0 ? t.color : null, this.lineCap_ = t.lineCap, this.lineDash_ = t.lineDash !== void 0 ? t.lineDash : null, this.lineDashOffset_ = t.lineDashOffset, this.lineJoin_ = t.lineJoin, this.miterLimit_ = t.miterLimit, this.width_ = t.width;
  }
  clone() {
    const t = this.getColor();
    return new Ml({
      color: Array.isArray(t) ? t.slice() : t || void 0,
      lineCap: this.getLineCap(),
      lineDash: this.getLineDash() ? this.getLineDash().slice() : void 0,
      lineDashOffset: this.getLineDashOffset(),
      lineJoin: this.getLineJoin(),
      miterLimit: this.getMiterLimit(),
      width: this.getWidth()
    });
  }
  getColor() {
    return this.color_;
  }
  getLineCap() {
    return this.lineCap_;
  }
  getLineDash() {
    return this.lineDash_;
  }
  getLineDashOffset() {
    return this.lineDashOffset_;
  }
  getLineJoin() {
    return this.lineJoin_;
  }
  getMiterLimit() {
    return this.miterLimit_;
  }
  getWidth() {
    return this.width_;
  }
  setColor(t) {
    this.color_ = t;
  }
  setLineCap(t) {
    this.lineCap_ = t;
  }
  setLineDash(t) {
    this.lineDash_ = t;
  }
  setLineDashOffset(t) {
    this.lineDashOffset_ = t;
  }
  setLineJoin(t) {
    this.lineJoin_ = t;
  }
  setMiterLimit(t) {
    this.miterLimit_ = t;
  }
  setWidth(t) {
    this.width_ = t;
  }
}
const Re = Ml, It = {
  IDLE: 0,
  LOADING: 1,
  LOADED: 2,
  ERROR: 3,
  EMPTY: 4
};
class El {
  constructor(t) {
    this.opacity_ = t.opacity, this.rotateWithView_ = t.rotateWithView, this.rotation_ = t.rotation, this.scale_ = t.scale, this.scaleArray_ = ce(t.scale), this.displacement_ = t.displacement, this.declutterMode_ = t.declutterMode;
  }
  clone() {
    const t = this.getScale();
    return new El({
      opacity: this.getOpacity(),
      scale: Array.isArray(t) ? t.slice() : t,
      rotation: this.getRotation(),
      rotateWithView: this.getRotateWithView(),
      displacement: this.getDisplacement().slice(),
      declutterMode: this.getDeclutterMode()
    });
  }
  getOpacity() {
    return this.opacity_;
  }
  getRotateWithView() {
    return this.rotateWithView_;
  }
  getRotation() {
    return this.rotation_;
  }
  getScale() {
    return this.scale_;
  }
  getScaleArray() {
    return this.scaleArray_;
  }
  getDisplacement() {
    return this.displacement_;
  }
  getDeclutterMode() {
    return this.declutterMode_;
  }
  getAnchor() {
    return W();
  }
  getImage(t) {
    return W();
  }
  getHitDetectionImage() {
    return W();
  }
  getPixelRatio(t) {
    return 1;
  }
  getImageState() {
    return W();
  }
  getImageSize() {
    return W();
  }
  getOrigin() {
    return W();
  }
  getSize() {
    return W();
  }
  setDisplacement(t) {
    this.displacement_ = t;
  }
  setOpacity(t) {
    this.opacity_ = t;
  }
  setRotateWithView(t) {
    this.rotateWithView_ = t;
  }
  setRotation(t) {
    this.rotation_ = t;
  }
  setScale(t) {
    this.scale_ = t, this.scaleArray_ = ce(t);
  }
  listenImageChange(t) {
    W();
  }
  load() {
    W();
  }
  unlistenImageChange(t) {
    W();
  }
}
const _d = El;
function Oe(i) {
  return Array.isArray(i) ? Pu(i) : i;
}
class wl extends _d {
  constructor(t) {
    const e = t.rotateWithView !== void 0 ? t.rotateWithView : !1;
    super({
      opacity: 1,
      rotateWithView: e,
      rotation: t.rotation !== void 0 ? t.rotation : 0,
      scale: t.scale !== void 0 ? t.scale : 1,
      displacement: t.displacement !== void 0 ? t.displacement : [0, 0],
      declutterMode: t.declutterMode
    }), this.canvas_ = void 0, this.hitDetectionCanvas_ = null, this.fill_ = t.fill !== void 0 ? t.fill : null, this.origin_ = [0, 0], this.points_ = t.points, this.radius_ = t.radius !== void 0 ? t.radius : t.radius1, this.radius2_ = t.radius2, this.angle_ = t.angle !== void 0 ? t.angle : 0, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.size_ = null, this.renderOptions_ = null, this.render();
  }
  clone() {
    const t = this.getScale(), e = new wl({
      fill: this.getFill() ? this.getFill().clone() : void 0,
      points: this.getPoints(),
      radius: this.getRadius(),
      radius2: this.getRadius2(),
      angle: this.getAngle(),
      stroke: this.getStroke() ? this.getStroke().clone() : void 0,
      rotation: this.getRotation(),
      rotateWithView: this.getRotateWithView(),
      scale: Array.isArray(t) ? t.slice() : t,
      displacement: this.getDisplacement().slice(),
      declutterMode: this.getDeclutterMode()
    });
    return e.setOpacity(this.getOpacity()), e;
  }
  getAnchor() {
    const t = this.size_;
    if (!t)
      return null;
    const e = this.getDisplacement(), n = this.getScaleArray();
    return [
      t[0] / 2 - e[0] / n[0],
      t[1] / 2 + e[1] / n[1]
    ];
  }
  getAngle() {
    return this.angle_;
  }
  getFill() {
    return this.fill_;
  }
  setFill(t) {
    this.fill_ = t, this.render();
  }
  getHitDetectionImage() {
    return this.hitDetectionCanvas_ || this.createHitDetectionCanvas_(this.renderOptions_), this.hitDetectionCanvas_;
  }
  getImage(t) {
    let e = this.canvas_[t];
    if (!e) {
      const n = this.renderOptions_, s = ge(
        n.size * t,
        n.size * t
      );
      this.draw_(n, s, t), e = s.canvas, this.canvas_[t] = e;
    }
    return e;
  }
  getPixelRatio(t) {
    return t;
  }
  getImageSize() {
    return this.size_;
  }
  getImageState() {
    return It.LOADED;
  }
  getOrigin() {
    return this.origin_;
  }
  getPoints() {
    return this.points_;
  }
  getRadius() {
    return this.radius_;
  }
  getRadius2() {
    return this.radius2_;
  }
  getSize() {
    return this.size_;
  }
  getStroke() {
    return this.stroke_;
  }
  setStroke(t) {
    this.stroke_ = t, this.render();
  }
  listenImageChange(t) {
  }
  load() {
  }
  unlistenImageChange(t) {
  }
  calculateLineJoinSize_(t, e, n) {
    if (e === 0 || this.points_ === 1 / 0 || t !== "bevel" && t !== "miter")
      return e;
    let s = this.radius_, r = this.radius2_ === void 0 ? s : this.radius2_;
    if (s < r) {
      const w = s;
      s = r, r = w;
    }
    const o = this.radius2_ === void 0 ? this.points_ : this.points_ * 2, a = 2 * Math.PI / o, l = r * Math.sin(a), h = Math.sqrt(r * r - l * l), c = s - h, u = Math.sqrt(l * l + c * c), d = u / l;
    if (t === "miter" && d <= n)
      return d * e;
    const f = e / 2 / d, g = e / 2 * (c / u), p = Math.sqrt((s + f) * (s + f) + g * g) - s;
    if (this.radius2_ === void 0 || t === "bevel")
      return p * 2;
    const _ = s * Math.sin(a), y = Math.sqrt(s * s - _ * _), v = r - y, C = Math.sqrt(_ * _ + v * v) / _;
    if (C <= n) {
      const w = C * e / 2 - r - s;
      return 2 * Math.max(p, w);
    }
    return p * 2;
  }
  createRenderOptions() {
    let t = $n, e = 0, n = null, s = 0, r, o = 0;
    this.stroke_ && (r = this.stroke_.getColor(), r === null && (r = bs), r = Oe(r), o = this.stroke_.getWidth(), o === void 0 && (o = Ts), n = this.stroke_.getLineDash(), s = this.stroke_.getLineDashOffset(), t = this.stroke_.getLineJoin(), t === void 0 && (t = $n), e = this.stroke_.getMiterLimit(), e === void 0 && (e = Rs));
    const a = this.calculateLineJoinSize_(t, o, e), l = Math.max(this.radius_, this.radius2_ || 0), h = Math.ceil(2 * l + a);
    return {
      strokeStyle: r,
      strokeWidth: o,
      size: h,
      lineDash: n,
      lineDashOffset: s,
      lineJoin: t,
      miterLimit: e
    };
  }
  render() {
    this.renderOptions_ = this.createRenderOptions();
    const t = this.renderOptions_.size;
    this.canvas_ = {}, this.size_ = [t, t];
  }
  draw_(t, e, n) {
    if (e.scale(n, n), e.translate(t.size / 2, t.size / 2), this.createPath_(e), this.fill_) {
      let s = this.fill_.getColor();
      s === null && (s = ii), e.fillStyle = Oe(s), e.fill();
    }
    this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
  createHitDetectionCanvas_(t) {
    if (this.fill_) {
      let e = this.fill_.getColor(), n = 0;
      if (typeof e == "string" && (e = kr(e)), e === null ? n = 1 : Array.isArray(e) && (n = e.length === 4 ? e[3] : 1), n === 0) {
        const s = ge(
          t.size,
          t.size
        );
        this.hitDetectionCanvas_ = s.canvas, this.drawHitDetectionCanvas_(t, s);
      }
    }
    this.hitDetectionCanvas_ || (this.hitDetectionCanvas_ = this.getImage(1));
  }
  createPath_(t) {
    let e = this.points_;
    const n = this.radius_;
    if (e === 1 / 0)
      t.arc(0, 0, n, 0, 2 * Math.PI);
    else {
      const s = this.radius2_ === void 0 ? n : this.radius2_;
      this.radius2_ !== void 0 && (e *= 2);
      const r = this.angle_ - Math.PI / 2, o = 2 * Math.PI / e;
      for (let a = 0; a < e; a++) {
        const l = r + a * o, h = a % 2 === 0 ? n : s;
        t.lineTo(h * Math.cos(l), h * Math.sin(l));
      }
      t.closePath();
    }
  }
  drawHitDetectionCanvas_(t, e) {
    e.translate(t.size / 2, t.size / 2), this.createPath_(e), e.fillStyle = ii, e.fill(), this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
}
const yd = wl;
class Sl extends yd {
  constructor(t) {
    t = t || { radius: 5 }, super({
      points: 1 / 0,
      fill: t.fill,
      radius: t.radius,
      stroke: t.stroke,
      scale: t.scale !== void 0 ? t.scale : 1,
      rotation: t.rotation !== void 0 ? t.rotation : 0,
      rotateWithView: t.rotateWithView !== void 0 ? t.rotateWithView : !1,
      displacement: t.displacement !== void 0 ? t.displacement : [0, 0],
      declutterMode: t.declutterMode
    });
  }
  clone() {
    const t = this.getScale(), e = new Sl({
      fill: this.getFill() ? this.getFill().clone() : void 0,
      stroke: this.getStroke() ? this.getStroke().clone() : void 0,
      radius: this.getRadius(),
      scale: Array.isArray(t) ? t.slice() : t,
      rotation: this.getRotation(),
      rotateWithView: this.getRotateWithView(),
      displacement: this.getDisplacement().slice(),
      declutterMode: this.getDeclutterMode()
    });
    return e.setOpacity(this.getOpacity()), e;
  }
  setRadius(t) {
    this.radius_ = t, this.render();
  }
}
const ei = Sl;
class Mo {
  constructor(t) {
    t = t || {}, this.geometry_ = null, this.geometryFunction_ = Gh, t.geometry !== void 0 && this.setGeometry(t.geometry), this.fill_ = t.fill !== void 0 ? t.fill : null, this.image_ = t.image !== void 0 ? t.image : null, this.renderer_ = t.renderer !== void 0 ? t.renderer : null, this.hitDetectionRenderer_ = t.hitDetectionRenderer !== void 0 ? t.hitDetectionRenderer : null, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.text_ = t.text !== void 0 ? t.text : null, this.zIndex_ = t.zIndex;
  }
  clone() {
    let t = this.getGeometry();
    return t && typeof t == "object" && (t = t.clone()), new Mo({
      geometry: t,
      fill: this.getFill() ? this.getFill().clone() : void 0,
      image: this.getImage() ? this.getImage().clone() : void 0,
      renderer: this.getRenderer(),
      stroke: this.getStroke() ? this.getStroke().clone() : void 0,
      text: this.getText() ? this.getText().clone() : void 0,
      zIndex: this.getZIndex()
    });
  }
  getRenderer() {
    return this.renderer_;
  }
  setRenderer(t) {
    this.renderer_ = t;
  }
  setHitDetectionRenderer(t) {
    this.hitDetectionRenderer_ = t;
  }
  getHitDetectionRenderer() {
    return this.hitDetectionRenderer_;
  }
  getGeometry() {
    return this.geometry_;
  }
  getGeometryFunction() {
    return this.geometryFunction_;
  }
  getFill() {
    return this.fill_;
  }
  setFill(t) {
    this.fill_ = t;
  }
  getImage() {
    return this.image_;
  }
  setImage(t) {
    this.image_ = t;
  }
  getStroke() {
    return this.stroke_;
  }
  setStroke(t) {
    this.stroke_ = t;
  }
  getText() {
    return this.text_;
  }
  setText(t) {
    this.text_ = t;
  }
  getZIndex() {
    return this.zIndex_;
  }
  setGeometry(t) {
    typeof t == "function" ? this.geometryFunction_ = t : typeof t == "string" ? this.geometryFunction_ = function(e) {
      return e.get(t);
    } : t ? t !== void 0 && (this.geometryFunction_ = function() {
      return t;
    }) : this.geometryFunction_ = Gh, this.geometry_ = t;
  }
  setZIndex(t) {
    this.zIndex_ = t;
  }
}
function sm(i) {
  let t;
  if (typeof i == "function")
    t = i;
  else {
    let e;
    Array.isArray(i) ? e = i : (Y(typeof i.getZIndex == "function", 41), e = [i]), t = function() {
      return e;
    };
  }
  return t;
}
let Xo = null;
function rm(i, t) {
  if (!Xo) {
    const e = new Yt({
      color: "rgba(255,255,255,0.4)"
    }), n = new Re({
      color: "#3399CC",
      width: 1.25
    });
    Xo = [
      new Mo({
        image: new ei({
          fill: e,
          stroke: n,
          radius: 5
        }),
        fill: e,
        stroke: n
      })
    ];
  }
  return Xo;
}
function Gh(i) {
  return i.getGeometry();
}
const Ut = Mo, om = "#333";
class Rl {
  constructor(t) {
    t = t || {}, this.font_ = t.font, this.rotation_ = t.rotation, this.rotateWithView_ = t.rotateWithView, this.scale_ = t.scale, this.scaleArray_ = ce(t.scale !== void 0 ? t.scale : 1), this.text_ = t.text, this.textAlign_ = t.textAlign, this.justify_ = t.justify, this.textBaseline_ = t.textBaseline, this.fill_ = t.fill !== void 0 ? t.fill : new Yt({ color: om }), this.maxAngle_ = t.maxAngle !== void 0 ? t.maxAngle : Math.PI / 4, this.placement_ = t.placement !== void 0 ? t.placement : "point", this.overflow_ = !!t.overflow, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.offsetX_ = t.offsetX !== void 0 ? t.offsetX : 0, this.offsetY_ = t.offsetY !== void 0 ? t.offsetY : 0, this.backgroundFill_ = t.backgroundFill ? t.backgroundFill : null, this.backgroundStroke_ = t.backgroundStroke ? t.backgroundStroke : null, this.padding_ = t.padding === void 0 ? null : t.padding;
  }
  clone() {
    const t = this.getScale();
    return new Rl({
      font: this.getFont(),
      placement: this.getPlacement(),
      maxAngle: this.getMaxAngle(),
      overflow: this.getOverflow(),
      rotation: this.getRotation(),
      rotateWithView: this.getRotateWithView(),
      scale: Array.isArray(t) ? t.slice() : t,
      text: this.getText(),
      textAlign: this.getTextAlign(),
      justify: this.getJustify(),
      textBaseline: this.getTextBaseline(),
      fill: this.getFill() ? this.getFill().clone() : void 0,
      stroke: this.getStroke() ? this.getStroke().clone() : void 0,
      offsetX: this.getOffsetX(),
      offsetY: this.getOffsetY(),
      backgroundFill: this.getBackgroundFill() ? this.getBackgroundFill().clone() : void 0,
      backgroundStroke: this.getBackgroundStroke() ? this.getBackgroundStroke().clone() : void 0,
      padding: this.getPadding() || void 0
    });
  }
  getOverflow() {
    return this.overflow_;
  }
  getFont() {
    return this.font_;
  }
  getMaxAngle() {
    return this.maxAngle_;
  }
  getPlacement() {
    return this.placement_;
  }
  getOffsetX() {
    return this.offsetX_;
  }
  getOffsetY() {
    return this.offsetY_;
  }
  getFill() {
    return this.fill_;
  }
  getRotateWithView() {
    return this.rotateWithView_;
  }
  getRotation() {
    return this.rotation_;
  }
  getScale() {
    return this.scale_;
  }
  getScaleArray() {
    return this.scaleArray_;
  }
  getStroke() {
    return this.stroke_;
  }
  getText() {
    return this.text_;
  }
  getTextAlign() {
    return this.textAlign_;
  }
  getJustify() {
    return this.justify_;
  }
  getTextBaseline() {
    return this.textBaseline_;
  }
  getBackgroundFill() {
    return this.backgroundFill_;
  }
  getBackgroundStroke() {
    return this.backgroundStroke_;
  }
  getPadding() {
    return this.padding_;
  }
  setOverflow(t) {
    this.overflow_ = t;
  }
  setFont(t) {
    this.font_ = t;
  }
  setMaxAngle(t) {
    this.maxAngle_ = t;
  }
  setOffsetX(t) {
    this.offsetX_ = t;
  }
  setOffsetY(t) {
    this.offsetY_ = t;
  }
  setPlacement(t) {
    this.placement_ = t;
  }
  setRotateWithView(t) {
    this.rotateWithView_ = t;
  }
  setFill(t) {
    this.fill_ = t;
  }
  setRotation(t) {
    this.rotation_ = t;
  }
  setScale(t) {
    this.scale_ = t, this.scaleArray_ = ce(t !== void 0 ? t : 1);
  }
  setStroke(t) {
    this.stroke_ = t;
  }
  setText(t) {
    this.text_ = t;
  }
  setTextAlign(t) {
    this.textAlign_ = t;
  }
  setJustify(t) {
    this.justify_ = t;
  }
  setTextBaseline(t) {
    this.textBaseline_ = t;
  }
  setBackgroundFill(t) {
    this.backgroundFill_ = t;
  }
  setBackgroundStroke(t) {
    this.backgroundStroke_ = t;
  }
  setPadding(t) {
    this.padding_ = t;
  }
}
const wa = Rl;
function am(i, t, e, n, s) {
  vd(i, t, e || 0, n || i.length - 1, s || lm);
}
function vd(i, t, e, n, s) {
  for (; n > e; ) {
    if (n - e > 600) {
      var r = n - e + 1, o = t - e + 1, a = Math.log(r), l = 0.5 * Math.exp(2 * a / 3), h = 0.5 * Math.sqrt(a * l * (r - l) / r) * (o - r / 2 < 0 ? -1 : 1), c = Math.max(e, Math.floor(t - o * l / r + h)), u = Math.min(n, Math.floor(t + (r - o) * l / r + h));
      vd(i, t, c, u, s);
    }
    var d = i[t], f = e, g = n;
    for (rs(i, e, t), s(i[n], d) > 0 && rs(i, e, n); f < g; ) {
      for (rs(i, f, g), f++, g--; s(i[f], d) < 0; )
        f++;
      for (; s(i[g], d) > 0; )
        g--;
    }
    s(i[e], d) === 0 ? rs(i, e, g) : (g++, rs(i, g, n)), g <= t && (e = g + 1), t <= g && (n = g - 1);
  }
}
function rs(i, t, e) {
  var n = i[t];
  i[t] = i[e], i[e] = n;
}
function lm(i, t) {
  return i < t ? -1 : i > t ? 1 : 0;
}
class xd {
  constructor(t = 9) {
    this._maxEntries = Math.max(4, t), this._minEntries = Math.max(2, Math.ceil(this._maxEntries * 0.4)), this.clear();
  }
  all() {
    return this._all(this.data, []);
  }
  search(t) {
    let e = this.data;
    const n = [];
    if (!xr(t, e))
      return n;
    const s = this.toBBox, r = [];
    for (; e; ) {
      for (let o = 0; o < e.children.length; o++) {
        const a = e.children[o], l = e.leaf ? s(a) : a;
        xr(t, l) && (e.leaf ? n.push(a) : jo(t, l) ? this._all(a, n) : r.push(a));
      }
      e = r.pop();
    }
    return n;
  }
  collides(t) {
    let e = this.data;
    if (!xr(t, e))
      return !1;
    const n = [];
    for (; e; ) {
      for (let s = 0; s < e.children.length; s++) {
        const r = e.children[s], o = e.leaf ? this.toBBox(r) : r;
        if (xr(t, o)) {
          if (e.leaf || jo(t, o))
            return !0;
          n.push(r);
        }
      }
      e = n.pop();
    }
    return !1;
  }
  load(t) {
    if (!(t && t.length))
      return this;
    if (t.length < this._minEntries) {
      for (let n = 0; n < t.length; n++)
        this.insert(t[n]);
      return this;
    }
    let e = this._build(t.slice(), 0, t.length - 1, 0);
    if (!this.data.children.length)
      this.data = e;
    else if (this.data.height === e.height)
      this._splitRoot(this.data, e);
    else {
      if (this.data.height < e.height) {
        const n = this.data;
        this.data = e, e = n;
      }
      this._insert(e, this.data.height - e.height - 1, !0);
    }
    return this;
  }
  insert(t) {
    return t && this._insert(t, this.data.height - 1), this;
  }
  clear() {
    return this.data = Mn([]), this;
  }
  remove(t, e) {
    if (!t)
      return this;
    let n = this.data;
    const s = this.toBBox(t), r = [], o = [];
    let a, l, h;
    for (; n || r.length; ) {
      if (n || (n = r.pop(), l = r[r.length - 1], a = o.pop(), h = !0), n.leaf) {
        const c = hm(t, n.children, e);
        if (c !== -1)
          return n.children.splice(c, 1), r.push(n), this._condense(r), this;
      }
      !h && !n.leaf && jo(n, s) ? (r.push(n), o.push(a), a = 0, l = n, n = n.children[0]) : l ? (a++, n = l.children[a], h = !1) : n = null;
    }
    return this;
  }
  toBBox(t) {
    return t;
  }
  compareMinX(t, e) {
    return t.minX - e.minX;
  }
  compareMinY(t, e) {
    return t.minY - e.minY;
  }
  toJSON() {
    return this.data;
  }
  fromJSON(t) {
    return this.data = t, this;
  }
  _all(t, e) {
    const n = [];
    for (; t; )
      t.leaf ? e.push(...t.children) : n.push(...t.children), t = n.pop();
    return e;
  }
  _build(t, e, n, s) {
    const r = n - e + 1;
    let o = this._maxEntries, a;
    if (r <= o)
      return a = Mn(t.slice(e, n + 1)), mn(a, this.toBBox), a;
    s || (s = Math.ceil(Math.log(r) / Math.log(o)), o = Math.ceil(r / Math.pow(o, s - 1))), a = Mn([]), a.leaf = !1, a.height = s;
    const l = Math.ceil(r / o), h = l * Math.ceil(Math.sqrt(o));
    $h(t, e, n, h, this.compareMinX);
    for (let c = e; c <= n; c += h) {
      const u = Math.min(c + h - 1, n);
      $h(t, c, u, l, this.compareMinY);
      for (let d = c; d <= u; d += l) {
        const f = Math.min(d + l - 1, u);
        a.children.push(this._build(t, d, f, s - 1));
      }
    }
    return mn(a, this.toBBox), a;
  }
  _chooseSubtree(t, e, n, s) {
    for (; s.push(e), !(e.leaf || s.length - 1 === n); ) {
      let r = 1 / 0, o = 1 / 0, a;
      for (let l = 0; l < e.children.length; l++) {
        const h = e.children[l], c = Yo(h), u = dm(t, h) - c;
        u < o ? (o = u, r = c < r ? c : r, a = h) : u === o && c < r && (r = c, a = h);
      }
      e = a || e.children[0];
    }
    return e;
  }
  _insert(t, e, n) {
    const s = n ? t : this.toBBox(t), r = [], o = this._chooseSubtree(s, this.data, e, r);
    for (o.children.push(t), cs(o, s); e >= 0 && r[e].children.length > this._maxEntries; )
      this._split(r, e), e--;
    this._adjustParentBBoxes(s, r, e);
  }
  _split(t, e) {
    const n = t[e], s = n.children.length, r = this._minEntries;
    this._chooseSplitAxis(n, r, s);
    const o = this._chooseSplitIndex(n, r, s), a = Mn(n.children.splice(o, n.children.length - o));
    a.height = n.height, a.leaf = n.leaf, mn(n, this.toBBox), mn(a, this.toBBox), e ? t[e - 1].children.push(a) : this._splitRoot(n, a);
  }
  _splitRoot(t, e) {
    this.data = Mn([t, e]), this.data.height = t.height + 1, this.data.leaf = !1, mn(this.data, this.toBBox);
  }
  _chooseSplitIndex(t, e, n) {
    let s, r = 1 / 0, o = 1 / 0;
    for (let a = e; a <= n - e; a++) {
      const l = hs(t, 0, a, this.toBBox), h = hs(t, a, n, this.toBBox), c = fm(l, h), u = Yo(l) + Yo(h);
      c < r ? (r = c, s = a, o = u < o ? u : o) : c === r && u < o && (o = u, s = a);
    }
    return s || n - e;
  }
  _chooseSplitAxis(t, e, n) {
    const s = t.leaf ? this.compareMinX : cm, r = t.leaf ? this.compareMinY : um, o = this._allDistMargin(t, e, n, s), a = this._allDistMargin(t, e, n, r);
    o < a && t.children.sort(s);
  }
  _allDistMargin(t, e, n, s) {
    t.children.sort(s);
    const r = this.toBBox, o = hs(t, 0, e, r), a = hs(t, n - e, n, r);
    let l = vr(o) + vr(a);
    for (let h = e; h < n - e; h++) {
      const c = t.children[h];
      cs(o, t.leaf ? r(c) : c), l += vr(o);
    }
    for (let h = n - e - 1; h >= e; h--) {
      const c = t.children[h];
      cs(a, t.leaf ? r(c) : c), l += vr(a);
    }
    return l;
  }
  _adjustParentBBoxes(t, e, n) {
    for (let s = n; s >= 0; s--)
      cs(e[s], t);
  }
  _condense(t) {
    for (let e = t.length - 1, n; e >= 0; e--)
      t[e].children.length === 0 ? e > 0 ? (n = t[e - 1].children, n.splice(n.indexOf(t[e]), 1)) : this.clear() : mn(t[e], this.toBBox);
  }
}
function hm(i, t, e) {
  if (!e)
    return t.indexOf(i);
  for (let n = 0; n < t.length; n++)
    if (e(i, t[n]))
      return n;
  return -1;
}
function mn(i, t) {
  hs(i, 0, i.children.length, t, i);
}
function hs(i, t, e, n, s) {
  s || (s = Mn(null)), s.minX = 1 / 0, s.minY = 1 / 0, s.maxX = -1 / 0, s.maxY = -1 / 0;
  for (let r = t; r < e; r++) {
    const o = i.children[r];
    cs(s, i.leaf ? n(o) : o);
  }
  return s;
}
function cs(i, t) {
  return i.minX = Math.min(i.minX, t.minX), i.minY = Math.min(i.minY, t.minY), i.maxX = Math.max(i.maxX, t.maxX), i.maxY = Math.max(i.maxY, t.maxY), i;
}
function cm(i, t) {
  return i.minX - t.minX;
}
function um(i, t) {
  return i.minY - t.minY;
}
function Yo(i) {
  return (i.maxX - i.minX) * (i.maxY - i.minY);
}
function vr(i) {
  return i.maxX - i.minX + (i.maxY - i.minY);
}
function dm(i, t) {
  return (Math.max(t.maxX, i.maxX) - Math.min(t.minX, i.minX)) * (Math.max(t.maxY, i.maxY) - Math.min(t.minY, i.minY));
}
function fm(i, t) {
  const e = Math.max(i.minX, t.minX), n = Math.max(i.minY, t.minY), s = Math.min(i.maxX, t.maxX), r = Math.min(i.maxY, t.maxY);
  return Math.max(0, s - e) * Math.max(0, r - n);
}
function jo(i, t) {
  return i.minX <= t.minX && i.minY <= t.minY && t.maxX <= i.maxX && t.maxY <= i.maxY;
}
function xr(i, t) {
  return t.minX <= i.maxX && t.minY <= i.maxY && t.maxX >= i.minX && t.maxY >= i.minY;
}
function Mn(i) {
  return {
    children: i,
    height: 1,
    leaf: !0,
    minX: 1 / 0,
    minY: 1 / 0,
    maxX: -1 / 0,
    maxY: -1 / 0
  };
}
function $h(i, t, e, n, s) {
  const r = [t, e];
  for (; r.length; ) {
    if (e = r.pop(), t = r.pop(), e - t <= n)
      continue;
    const o = t + Math.ceil((e - t) / n / 2) * n;
    am(i, o, t, e, s), r.push(t, o, o, e);
  }
}
function Cd(i, t, e) {
  const n = i;
  let s = !0, r = !1, o = !1;
  const a = [
    Dr(n, X.LOAD, function() {
      o = !0, r || t();
    })
  ];
  return n.src && v0 ? (r = !0, n.decode().then(function() {
    s && t();
  }).catch(function(l) {
    s && (o ? t() : e());
  })) : a.push(Dr(n, X.ERROR, e)), function() {
    s = !1, a.forEach(pt);
  };
}
let os = null;
class gm extends lo {
  constructor(t, e, n, s, r, o) {
    super(), this.hitDetectionImage_ = null, this.image_ = t, this.crossOrigin_ = s, this.canvas_ = {}, this.color_ = o, this.unlisten_ = null, this.imageState_ = r, this.size_ = n, this.src_ = e, this.tainted_;
  }
  initializeImage_() {
    this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_);
  }
  isTainted_() {
    if (this.tainted_ === void 0 && this.imageState_ === It.LOADED) {
      os || (os = ge(1, 1)), os.drawImage(this.image_, 0, 0);
      try {
        os.getImageData(0, 0, 1, 1), this.tainted_ = !1;
      } catch {
        os = null, this.tainted_ = !0;
      }
    }
    return this.tainted_ === !0;
  }
  dispatchChangeEvent_() {
    this.dispatchEvent(X.CHANGE);
  }
  handleImageError_() {
    this.imageState_ = It.ERROR, this.unlistenImage_(), this.dispatchChangeEvent_();
  }
  handleImageLoad_() {
    this.imageState_ = It.LOADED, this.size_ ? (this.image_.width = this.size_[0], this.image_.height = this.size_[1]) : this.size_ = [this.image_.width, this.image_.height], this.unlistenImage_(), this.dispatchChangeEvent_();
  }
  getImage(t) {
    return this.image_ || this.initializeImage_(), this.replaceColor_(t), this.canvas_[t] ? this.canvas_[t] : this.image_;
  }
  getPixelRatio(t) {
    return this.replaceColor_(t), this.canvas_[t] ? t : 1;
  }
  getImageState() {
    return this.imageState_;
  }
  getHitDetectionImage() {
    if (this.image_ || this.initializeImage_(), !this.hitDetectionImage_)
      if (this.isTainted_()) {
        const t = this.size_[0], e = this.size_[1], n = ge(t, e);
        n.fillRect(0, 0, t, e), this.hitDetectionImage_ = n.canvas;
      } else
        this.hitDetectionImage_ = this.image_;
    return this.hitDetectionImage_;
  }
  getSize() {
    return this.size_;
  }
  getSrc() {
    return this.src_;
  }
  load() {
    if (this.imageState_ === It.IDLE) {
      this.image_ || this.initializeImage_(), this.imageState_ = It.LOADING;
      try {
        this.image_.src = this.src_;
      } catch {
        this.handleImageError_();
      }
      this.unlisten_ = Cd(
        this.image_,
        this.handleImageLoad_.bind(this),
        this.handleImageError_.bind(this)
      );
    }
  }
  replaceColor_(t) {
    if (!this.color_ || this.canvas_[t] || this.imageState_ !== It.LOADED)
      return;
    const e = this.image_, n = document.createElement("canvas");
    n.width = Math.ceil(e.width * t), n.height = Math.ceil(e.height * t);
    const s = n.getContext("2d");
    s.scale(t, t), s.drawImage(e, 0, 0), s.globalCompositeOperation = "multiply", s.fillStyle = Iu(this.color_), s.fillRect(0, 0, n.width / t, n.height / t), s.globalCompositeOperation = "destination-in", s.drawImage(e, 0, 0), this.canvas_[t] = n;
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function mm(i, t, e, n, s, r) {
  let o = Gr.get(t, n, r);
  return o || (o = new gm(i, t, e, n, s, r), Gr.set(t, n, r, o)), o;
}
class bl extends _d {
  constructor(t) {
    t = t || {};
    const e = t.opacity !== void 0 ? t.opacity : 1, n = t.rotation !== void 0 ? t.rotation : 0, s = t.scale !== void 0 ? t.scale : 1, r = t.rotateWithView !== void 0 ? t.rotateWithView : !1;
    super({
      opacity: e,
      rotation: n,
      scale: s,
      displacement: t.displacement !== void 0 ? t.displacement : [0, 0],
      rotateWithView: r,
      declutterMode: t.declutterMode
    }), this.anchor_ = t.anchor !== void 0 ? t.anchor : [0.5, 0.5], this.normalizedAnchor_ = null, this.anchorOrigin_ = t.anchorOrigin !== void 0 ? t.anchorOrigin : "top-left", this.anchorXUnits_ = t.anchorXUnits !== void 0 ? t.anchorXUnits : "fraction", this.anchorYUnits_ = t.anchorYUnits !== void 0 ? t.anchorYUnits : "fraction", this.crossOrigin_ = t.crossOrigin !== void 0 ? t.crossOrigin : null;
    const o = t.img !== void 0 ? t.img : null;
    this.imgSize_ = t.imgSize;
    let a = t.src;
    Y(!(a !== void 0 && o), 4), Y(!o || o && this.imgSize_, 5), (a === void 0 || a.length === 0) && o && (a = o.src || ot(o)), Y(a !== void 0 && a.length > 0, 6);
    const l = t.src !== void 0 ? It.IDLE : It.LOADED;
    this.color_ = t.color !== void 0 ? kr(t.color) : null, this.iconImage_ = mm(
      o,
      a,
      this.imgSize_ !== void 0 ? this.imgSize_ : null,
      this.crossOrigin_,
      l,
      this.color_
    ), this.offset_ = t.offset !== void 0 ? t.offset : [0, 0], this.offsetOrigin_ = t.offsetOrigin !== void 0 ? t.offsetOrigin : "top-left", this.origin_ = null, this.size_ = t.size !== void 0 ? t.size : null;
  }
  clone() {
    const t = this.getScale();
    return new bl({
      anchor: this.anchor_.slice(),
      anchorOrigin: this.anchorOrigin_,
      anchorXUnits: this.anchorXUnits_,
      anchorYUnits: this.anchorYUnits_,
      color: this.color_ && this.color_.slice ? this.color_.slice() : this.color_ || void 0,
      crossOrigin: this.crossOrigin_,
      imgSize: this.imgSize_,
      offset: this.offset_.slice(),
      offsetOrigin: this.offsetOrigin_,
      opacity: this.getOpacity(),
      rotateWithView: this.getRotateWithView(),
      rotation: this.getRotation(),
      scale: Array.isArray(t) ? t.slice() : t,
      size: this.size_ !== null ? this.size_.slice() : void 0,
      src: this.getSrc(),
      displacement: this.getDisplacement().slice(),
      declutterMode: this.getDeclutterMode()
    });
  }
  getAnchor() {
    let t = this.normalizedAnchor_;
    if (!t) {
      t = this.anchor_;
      const s = this.getSize();
      if (this.anchorXUnits_ == "fraction" || this.anchorYUnits_ == "fraction") {
        if (!s)
          return null;
        t = this.anchor_.slice(), this.anchorXUnits_ == "fraction" && (t[0] *= s[0]), this.anchorYUnits_ == "fraction" && (t[1] *= s[1]);
      }
      if (this.anchorOrigin_ != "top-left") {
        if (!s)
          return null;
        t === this.anchor_ && (t = this.anchor_.slice()), (this.anchorOrigin_ == "top-right" || this.anchorOrigin_ == "bottom-right") && (t[0] = -t[0] + s[0]), (this.anchorOrigin_ == "bottom-left" || this.anchorOrigin_ == "bottom-right") && (t[1] = -t[1] + s[1]);
      }
      this.normalizedAnchor_ = t;
    }
    const e = this.getDisplacement(), n = this.getScaleArray();
    return [
      t[0] - e[0] / n[0],
      t[1] + e[1] / n[1]
    ];
  }
  setAnchor(t) {
    this.anchor_ = t, this.normalizedAnchor_ = null;
  }
  getColor() {
    return this.color_;
  }
  getImage(t) {
    return this.iconImage_.getImage(t);
  }
  getPixelRatio(t) {
    return this.iconImage_.getPixelRatio(t);
  }
  getImageSize() {
    return this.iconImage_.getSize();
  }
  getImageState() {
    return this.iconImage_.getImageState();
  }
  getHitDetectionImage() {
    return this.iconImage_.getHitDetectionImage();
  }
  getOrigin() {
    if (this.origin_)
      return this.origin_;
    let t = this.offset_;
    if (this.offsetOrigin_ != "top-left") {
      const e = this.getSize(), n = this.iconImage_.getSize();
      if (!e || !n)
        return null;
      t = t.slice(), (this.offsetOrigin_ == "top-right" || this.offsetOrigin_ == "bottom-right") && (t[0] = n[0] - e[0] - t[0]), (this.offsetOrigin_ == "bottom-left" || this.offsetOrigin_ == "bottom-right") && (t[1] = n[1] - e[1] - t[1]);
    }
    return this.origin_ = t, this.origin_;
  }
  getSrc() {
    return this.iconImage_.getSrc();
  }
  getSize() {
    return this.size_ ? this.size_ : this.iconImage_.getSize();
  }
  listenImageChange(t) {
    this.iconImage_.addEventListener(X.CHANGE, t);
  }
  load() {
    this.iconImage_.load();
  }
  unlistenImageChange(t) {
    this.iconImage_.removeEventListener(X.CHANGE, t);
  }
}
const ps = bl;
function Bh(i) {
  return new Ut({
    fill: Os(i, ""),
    stroke: Ns(i, ""),
    text: pm(i),
    image: _m(i)
  });
}
function Os(i, t) {
  const e = i[t + "fill-color"];
  if (!!e)
    return new Yt({ color: e });
}
function Ns(i, t) {
  const e = i[t + "stroke-width"], n = i[t + "stroke-color"];
  if (!(!e && !n))
    return new Re({
      width: e,
      color: n,
      lineCap: i[t + "stroke-line-cap"],
      lineJoin: i[t + "stroke-line-join"],
      lineDash: i[t + "stroke-line-dash"],
      lineDashOffset: i[t + "stroke-line-dash-offset"],
      miterLimit: i[t + "stroke-miter-limit"]
    });
}
function pm(i) {
  const t = i["text-value"];
  return t ? new wa({
    text: t,
    font: i["text-font"],
    maxAngle: i["text-max-angle"],
    offsetX: i["text-offset-x"],
    offsetY: i["text-offset-y"],
    overflow: i["text-overflow"],
    placement: i["text-placement"],
    scale: i["text-scale"],
    rotateWithView: i["text-rotate-with-view"],
    rotation: i["text-rotation"],
    textAlign: i["text-align"],
    justify: i["text-justify"],
    textBaseline: i["text-baseline"],
    padding: i["text-padding"],
    fill: Os(i, "text-"),
    backgroundFill: Os(i, "text-background-"),
    stroke: Ns(i, "text-"),
    backgroundStroke: Ns(i, "text-background-")
  }) : void 0;
}
function _m(i) {
  const t = i["icon-src"], e = i["icon-img"];
  if (t || e)
    return new ps({
      src: t,
      img: e,
      imgSize: i["icon-img-size"],
      anchor: i["icon-anchor"],
      anchorOrigin: i["icon-anchor-origin"],
      anchorXUnits: i["icon-anchor-x-units"],
      anchorYUnits: i["icon-anchor-y-units"],
      color: i["icon-color"],
      crossOrigin: i["icon-cross-origin"],
      offset: i["icon-offset"],
      displacement: i["icon-displacement"],
      opacity: i["icon-opacity"],
      scale: i["icon-scale"],
      rotation: i["icon-rotation"],
      rotateWithView: i["icon-rotate-with-view"],
      size: i["icon-size"],
      declutterMode: i["icon-declutter-mode"]
    });
  const n = i["shape-points"];
  if (n) {
    const r = "shape-";
    return new yd({
      points: n,
      fill: Os(i, r),
      stroke: Ns(i, r),
      radius: i["shape-radius"],
      radius1: i["shape-radius1"],
      radius2: i["shape-radius2"],
      angle: i["shape-angle"],
      displacement: i["shape-displacement"],
      rotation: i["shape-rotation"],
      rotateWithView: i["shape-rotate-with-view"],
      scale: i["shape-scale"],
      declutterMode: i["shape-declutter-mode"]
    });
  }
  const s = i["circle-radius"];
  if (s) {
    const r = "circle-";
    return new ei({
      radius: s,
      fill: Os(i, r),
      stroke: Ns(i, r),
      displacement: i["circle-displacement"],
      scale: i["circle-scale"],
      rotation: i["circle-rotation"],
      rotateWithView: i["circle-rotate-with-view"],
      declutterMode: i["circle-declutter-mode"]
    });
  }
}
const zh = {
  RENDER_ORDER: "renderOrder"
};
class ym extends po {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.style, delete e.renderBuffer, delete e.updateWhileAnimating, delete e.updateWhileInteracting, super(e), this.declutter_ = t.declutter !== void 0 ? t.declutter : !1, this.renderBuffer_ = t.renderBuffer !== void 0 ? t.renderBuffer : 100, this.style_ = null, this.styleFunction_ = void 0, this.setStyle(t.style), this.updateWhileAnimating_ = t.updateWhileAnimating !== void 0 ? t.updateWhileAnimating : !1, this.updateWhileInteracting_ = t.updateWhileInteracting !== void 0 ? t.updateWhileInteracting : !1;
  }
  getDeclutter() {
    return this.declutter_;
  }
  getFeatures(t) {
    return super.getFeatures(t);
  }
  getRenderBuffer() {
    return this.renderBuffer_;
  }
  getRenderOrder() {
    return this.get(zh.RENDER_ORDER);
  }
  getStyle() {
    return this.style_;
  }
  getStyleFunction() {
    return this.styleFunction_;
  }
  getUpdateWhileAnimating() {
    return this.updateWhileAnimating_;
  }
  getUpdateWhileInteracting() {
    return this.updateWhileInteracting_;
  }
  renderDeclutter(t) {
    t.declutterTree || (t.declutterTree = new xd(9)), this.getRenderer().renderDeclutter(t);
  }
  setRenderOrder(t) {
    this.set(zh.RENDER_ORDER, t);
  }
  setStyle(t) {
    let e;
    if (t === void 0)
      e = rm;
    else if (t === null)
      e = null;
    else if (typeof t == "function")
      e = t;
    else if (t instanceof Ut)
      e = t;
    else if (Array.isArray(t)) {
      const n = t.length, s = new Array(n);
      for (let r = 0; r < n; ++r) {
        const o = t[r];
        o instanceof Ut ? s[r] = o : s[r] = Bh(o);
      }
      e = s;
    } else
      e = Bh(t);
    this.style_ = e, this.styleFunction_ = t === null ? void 0 : sm(this.style_), this.changed();
  }
}
const vm = ym, Hs = {
  BEGIN_GEOMETRY: 0,
  BEGIN_PATH: 1,
  CIRCLE: 2,
  CLOSE_PATH: 3,
  CUSTOM: 4,
  DRAW_CHARS: 5,
  DRAW_IMAGE: 6,
  END_GEOMETRY: 7,
  FILL: 8,
  MOVE_TO_LINE_TO: 9,
  SET_FILL_STYLE: 10,
  SET_STROKE_STYLE: 11,
  STROKE: 12
}, Cr = [Hs.FILL], xi = [Hs.STROKE], Bi = [Hs.BEGIN_PATH], Zh = [Hs.CLOSE_PATH], U = Hs;
class xm {
  drawCustom(t, e, n, s) {
  }
  drawGeometry(t) {
  }
  setStyle(t) {
  }
  drawCircle(t, e) {
  }
  drawFeature(t, e) {
  }
  drawGeometryCollection(t, e) {
  }
  drawLineString(t, e) {
  }
  drawMultiLineString(t, e) {
  }
  drawMultiPoint(t, e) {
  }
  drawMultiPolygon(t, e) {
  }
  drawPoint(t, e) {
  }
  drawPolygon(t, e) {
  }
  drawText(t, e) {
  }
  setFillStrokeStyle(t, e) {
  }
  setImageStyle(t, e) {
  }
  setTextStyle(t, e) {
  }
}
const Md = xm;
class Cm extends Md {
  constructor(t, e, n, s) {
    super(), this.tolerance = t, this.maxExtent = e, this.pixelRatio = s, this.maxLineWidth = 0, this.resolution = n, this.beginGeometryInstruction1_ = null, this.beginGeometryInstruction2_ = null, this.bufferedMaxExtent_ = null, this.instructions = [], this.coordinates = [], this.tmpCoordinate_ = [], this.hitDetectionInstructions = [], this.state = {};
  }
  applyPixelRatio(t) {
    const e = this.pixelRatio;
    return e == 1 ? t : t.map(function(n) {
      return n * e;
    });
  }
  appendFlatPointCoordinates(t, e) {
    const n = this.getBufferedMaxExtent(), s = this.tmpCoordinate_, r = this.coordinates;
    let o = r.length;
    for (let a = 0, l = t.length; a < l; a += e)
      s[0] = t[a], s[1] = t[a + 1], uo(n, s) && (r[o++] = s[0], r[o++] = s[1]);
    return o;
  }
  appendFlatLineCoordinates(t, e, n, s, r, o) {
    const a = this.coordinates;
    let l = a.length;
    const h = this.getBufferedMaxExtent();
    o && (e += s);
    let c = t[e], u = t[e + 1];
    const d = this.tmpCoordinate_;
    let f = !0, g, m, p;
    for (g = e + s; g < n; g += s)
      d[0] = t[g], d[1] = t[g + 1], p = la(h, d), p !== m ? (f && (a[l++] = c, a[l++] = u, f = !1), a[l++] = d[0], a[l++] = d[1]) : p === Nt.INTERSECTING ? (a[l++] = d[0], a[l++] = d[1], f = !1) : f = !0, c = d[0], u = d[1], m = p;
    return (r && f || g === e + s) && (a[l++] = c, a[l++] = u), l;
  }
  drawCustomCoordinates_(t, e, n, s, r) {
    for (let o = 0, a = n.length; o < a; ++o) {
      const l = n[o], h = this.appendFlatLineCoordinates(
        t,
        e,
        l,
        s,
        !1,
        !1
      );
      r.push(h), e = l;
    }
    return e;
  }
  drawCustom(t, e, n, s) {
    this.beginGeometry(t, e);
    const r = t.getType(), o = t.getStride(), a = this.coordinates.length;
    let l, h, c, u, d;
    switch (r) {
      case "MultiPolygon":
        l = t.getOrientedFlatCoordinates(), u = [];
        const f = t.getEndss();
        d = 0;
        for (let g = 0, m = f.length; g < m; ++g) {
          const p = [];
          d = this.drawCustomCoordinates_(
            l,
            d,
            f[g],
            o,
            p
          ), u.push(p);
        }
        this.instructions.push([
          U.CUSTOM,
          a,
          u,
          t,
          n,
          va
        ]), this.hitDetectionInstructions.push([
          U.CUSTOM,
          a,
          u,
          t,
          s || n,
          va
        ]);
        break;
      case "Polygon":
      case "MultiLineString":
        c = [], l = r == "Polygon" ? t.getOrientedFlatCoordinates() : t.getFlatCoordinates(), d = this.drawCustomCoordinates_(
          l,
          0,
          t.getEnds(),
          o,
          c
        ), this.instructions.push([
          U.CUSTOM,
          a,
          c,
          t,
          n,
          Ps
        ]), this.hitDetectionInstructions.push([
          U.CUSTOM,
          a,
          c,
          t,
          s || n,
          Ps
        ]);
        break;
      case "LineString":
      case "Circle":
        l = t.getFlatCoordinates(), h = this.appendFlatLineCoordinates(
          l,
          0,
          l.length,
          o,
          !1,
          !1
        ), this.instructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          n,
          vi
        ]), this.hitDetectionInstructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          s || n,
          vi
        ]);
        break;
      case "MultiPoint":
        l = t.getFlatCoordinates(), h = this.appendFlatPointCoordinates(l, o), h > a && (this.instructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          n,
          vi
        ]), this.hitDetectionInstructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          s || n,
          vi
        ]));
        break;
      case "Point":
        l = t.getFlatCoordinates(), this.coordinates.push(l[0], l[1]), h = this.coordinates.length, this.instructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          n
        ]), this.hitDetectionInstructions.push([
          U.CUSTOM,
          a,
          h,
          t,
          s || n
        ]);
        break;
    }
    this.endGeometry(e);
  }
  beginGeometry(t, e) {
    this.beginGeometryInstruction1_ = [
      U.BEGIN_GEOMETRY,
      e,
      0,
      t
    ], this.instructions.push(this.beginGeometryInstruction1_), this.beginGeometryInstruction2_ = [
      U.BEGIN_GEOMETRY,
      e,
      0,
      t
    ], this.hitDetectionInstructions.push(this.beginGeometryInstruction2_);
  }
  finish() {
    return {
      instructions: this.instructions,
      hitDetectionInstructions: this.hitDetectionInstructions,
      coordinates: this.coordinates
    };
  }
  reverseHitDetectionInstructions() {
    const t = this.hitDetectionInstructions;
    t.reverse();
    let e;
    const n = t.length;
    let s, r, o = -1;
    for (e = 0; e < n; ++e)
      s = t[e], r = s[0], r == U.END_GEOMETRY ? o = e : r == U.BEGIN_GEOMETRY && (s[2] = e, r0(this.hitDetectionInstructions, o, e), o = -1);
  }
  setFillStrokeStyle(t, e) {
    const n = this.state;
    if (t) {
      const s = t.getColor();
      n.fillStyle = Oe(
        s || ii
      );
    } else
      n.fillStyle = void 0;
    if (e) {
      const s = e.getColor();
      n.strokeStyle = Oe(
        s || bs
      );
      const r = e.getLineCap();
      n.lineCap = r !== void 0 ? r : Zr;
      const o = e.getLineDash();
      n.lineDash = o ? o.slice() : ws;
      const a = e.getLineDashOffset();
      n.lineDashOffset = a || Ss;
      const l = e.getLineJoin();
      n.lineJoin = l !== void 0 ? l : $n;
      const h = e.getWidth();
      n.lineWidth = h !== void 0 ? h : Ts;
      const c = e.getMiterLimit();
      n.miterLimit = c !== void 0 ? c : Rs, n.lineWidth > this.maxLineWidth && (this.maxLineWidth = n.lineWidth, this.bufferedMaxExtent_ = null);
    } else
      n.strokeStyle = void 0, n.lineCap = void 0, n.lineDash = null, n.lineDashOffset = void 0, n.lineJoin = void 0, n.lineWidth = void 0, n.miterLimit = void 0;
  }
  createFill(t) {
    const e = t.fillStyle, n = [U.SET_FILL_STYLE, e];
    return typeof e != "string" && n.push(!0), n;
  }
  applyStroke(t) {
    this.instructions.push(this.createStroke(t));
  }
  createStroke(t) {
    return [
      U.SET_STROKE_STYLE,
      t.strokeStyle,
      t.lineWidth * this.pixelRatio,
      t.lineCap,
      t.lineJoin,
      t.miterLimit,
      this.applyPixelRatio(t.lineDash),
      t.lineDashOffset * this.pixelRatio
    ];
  }
  updateFillStyle(t, e) {
    const n = t.fillStyle;
    (typeof n != "string" || t.currentFillStyle != n) && (n !== void 0 && this.instructions.push(e.call(this, t)), t.currentFillStyle = n);
  }
  updateStrokeStyle(t, e) {
    const n = t.strokeStyle, s = t.lineCap, r = t.lineDash, o = t.lineDashOffset, a = t.lineJoin, l = t.lineWidth, h = t.miterLimit;
    (t.currentStrokeStyle != n || t.currentLineCap != s || r != t.currentLineDash && !nn(t.currentLineDash, r) || t.currentLineDashOffset != o || t.currentLineJoin != a || t.currentLineWidth != l || t.currentMiterLimit != h) && (n !== void 0 && e.call(this, t), t.currentStrokeStyle = n, t.currentLineCap = s, t.currentLineDash = r, t.currentLineDashOffset = o, t.currentLineJoin = a, t.currentLineWidth = l, t.currentMiterLimit = h);
  }
  endGeometry(t) {
    this.beginGeometryInstruction1_[2] = this.instructions.length, this.beginGeometryInstruction1_ = null, this.beginGeometryInstruction2_[2] = this.hitDetectionInstructions.length, this.beginGeometryInstruction2_ = null;
    const e = [U.END_GEOMETRY, t];
    this.instructions.push(e), this.hitDetectionInstructions.push(e);
  }
  getBufferedMaxExtent() {
    if (!this.bufferedMaxExtent_ && (this.bufferedMaxExtent_ = Mu(this.maxExtent), this.maxLineWidth > 0)) {
      const t = this.resolution * (this.maxLineWidth + 1) / 2;
      co(this.bufferedMaxExtent_, t, this.bufferedMaxExtent_);
    }
    return this.bufferedMaxExtent_;
  }
}
const Xs = Cm;
class Mm extends Xs {
  constructor(t, e, n, s) {
    super(t, e, n, s), this.hitDetectionImage_ = null, this.image_ = null, this.imagePixelRatio_ = void 0, this.anchorX_ = void 0, this.anchorY_ = void 0, this.height_ = void 0, this.opacity_ = void 0, this.originX_ = void 0, this.originY_ = void 0, this.rotateWithView_ = void 0, this.rotation_ = void 0, this.scale_ = void 0, this.width_ = void 0, this.declutterMode_ = void 0, this.declutterImageWithText_ = void 0;
  }
  drawPoint(t, e) {
    if (!this.image_)
      return;
    this.beginGeometry(t, e);
    const n = t.getFlatCoordinates(), s = t.getStride(), r = this.coordinates.length, o = this.appendFlatPointCoordinates(n, s);
    this.instructions.push([
      U.DRAW_IMAGE,
      r,
      o,
      this.image_,
      this.anchorX_ * this.imagePixelRatio_,
      this.anchorY_ * this.imagePixelRatio_,
      Math.ceil(this.height_ * this.imagePixelRatio_),
      this.opacity_,
      this.originX_ * this.imagePixelRatio_,
      this.originY_ * this.imagePixelRatio_,
      this.rotateWithView_,
      this.rotation_,
      [
        this.scale_[0] * this.pixelRatio / this.imagePixelRatio_,
        this.scale_[1] * this.pixelRatio / this.imagePixelRatio_
      ],
      Math.ceil(this.width_ * this.imagePixelRatio_),
      this.declutterMode_,
      this.declutterImageWithText_
    ]), this.hitDetectionInstructions.push([
      U.DRAW_IMAGE,
      r,
      o,
      this.hitDetectionImage_,
      this.anchorX_,
      this.anchorY_,
      this.height_,
      this.opacity_,
      this.originX_,
      this.originY_,
      this.rotateWithView_,
      this.rotation_,
      this.scale_,
      this.width_,
      this.declutterMode_,
      this.declutterImageWithText_
    ]), this.endGeometry(e);
  }
  drawMultiPoint(t, e) {
    if (!this.image_)
      return;
    this.beginGeometry(t, e);
    const n = t.getFlatCoordinates(), s = t.getStride(), r = this.coordinates.length, o = this.appendFlatPointCoordinates(n, s);
    this.instructions.push([
      U.DRAW_IMAGE,
      r,
      o,
      this.image_,
      this.anchorX_ * this.imagePixelRatio_,
      this.anchorY_ * this.imagePixelRatio_,
      Math.ceil(this.height_ * this.imagePixelRatio_),
      this.opacity_,
      this.originX_ * this.imagePixelRatio_,
      this.originY_ * this.imagePixelRatio_,
      this.rotateWithView_,
      this.rotation_,
      [
        this.scale_[0] * this.pixelRatio / this.imagePixelRatio_,
        this.scale_[1] * this.pixelRatio / this.imagePixelRatio_
      ],
      Math.ceil(this.width_ * this.imagePixelRatio_),
      this.declutterMode_,
      this.declutterImageWithText_
    ]), this.hitDetectionInstructions.push([
      U.DRAW_IMAGE,
      r,
      o,
      this.hitDetectionImage_,
      this.anchorX_,
      this.anchorY_,
      this.height_,
      this.opacity_,
      this.originX_,
      this.originY_,
      this.rotateWithView_,
      this.rotation_,
      this.scale_,
      this.width_,
      this.declutterMode_,
      this.declutterImageWithText_
    ]), this.endGeometry(e);
  }
  finish() {
    return this.reverseHitDetectionInstructions(), this.anchorX_ = void 0, this.anchorY_ = void 0, this.hitDetectionImage_ = null, this.image_ = null, this.imagePixelRatio_ = void 0, this.height_ = void 0, this.scale_ = void 0, this.opacity_ = void 0, this.originX_ = void 0, this.originY_ = void 0, this.rotateWithView_ = void 0, this.rotation_ = void 0, this.width_ = void 0, super.finish();
  }
  setImageStyle(t, e) {
    const n = t.getAnchor(), s = t.getSize(), r = t.getOrigin();
    this.imagePixelRatio_ = t.getPixelRatio(this.pixelRatio), this.anchorX_ = n[0], this.anchorY_ = n[1], this.hitDetectionImage_ = t.getHitDetectionImage(), this.image_ = t.getImage(this.pixelRatio), this.height_ = s[1], this.opacity_ = t.getOpacity(), this.originX_ = r[0], this.originY_ = r[1], this.rotateWithView_ = t.getRotateWithView(), this.rotation_ = t.getRotation(), this.scale_ = t.getScaleArray(), this.width_ = s[0], this.declutterMode_ = t.getDeclutterMode(), this.declutterImageWithText_ = e;
  }
}
const Em = Mm;
class wm extends Xs {
  constructor(t, e, n, s) {
    super(t, e, n, s);
  }
  drawFlatCoordinates_(t, e, n, s) {
    const r = this.coordinates.length, o = this.appendFlatLineCoordinates(
      t,
      e,
      n,
      s,
      !1,
      !1
    ), a = [
      U.MOVE_TO_LINE_TO,
      r,
      o
    ];
    return this.instructions.push(a), this.hitDetectionInstructions.push(a), n;
  }
  drawLineString(t, e) {
    const n = this.state, s = n.strokeStyle, r = n.lineWidth;
    if (s === void 0 || r === void 0)
      return;
    this.updateStrokeStyle(n, this.applyStroke), this.beginGeometry(t, e), this.hitDetectionInstructions.push(
      [
        U.SET_STROKE_STYLE,
        n.strokeStyle,
        n.lineWidth,
        n.lineCap,
        n.lineJoin,
        n.miterLimit,
        ws,
        Ss
      ],
      Bi
    );
    const o = t.getFlatCoordinates(), a = t.getStride();
    this.drawFlatCoordinates_(
      o,
      0,
      o.length,
      a
    ), this.hitDetectionInstructions.push(xi), this.endGeometry(e);
  }
  drawMultiLineString(t, e) {
    const n = this.state, s = n.strokeStyle, r = n.lineWidth;
    if (s === void 0 || r === void 0)
      return;
    this.updateStrokeStyle(n, this.applyStroke), this.beginGeometry(t, e), this.hitDetectionInstructions.push(
      [
        U.SET_STROKE_STYLE,
        n.strokeStyle,
        n.lineWidth,
        n.lineCap,
        n.lineJoin,
        n.miterLimit,
        n.lineDash,
        n.lineDashOffset
      ],
      Bi
    );
    const o = t.getEnds(), a = t.getFlatCoordinates(), l = t.getStride();
    let h = 0;
    for (let c = 0, u = o.length; c < u; ++c)
      h = this.drawFlatCoordinates_(
        a,
        h,
        o[c],
        l
      );
    this.hitDetectionInstructions.push(xi), this.endGeometry(e);
  }
  finish() {
    const t = this.state;
    return t.lastStroke != null && t.lastStroke != this.coordinates.length && this.instructions.push(xi), this.reverseHitDetectionInstructions(), this.state = null, super.finish();
  }
  applyStroke(t) {
    t.lastStroke != null && t.lastStroke != this.coordinates.length && (this.instructions.push(xi), t.lastStroke = this.coordinates.length), t.lastStroke = 0, super.applyStroke(t), this.instructions.push(Bi);
  }
}
const Sm = wm;
class Rm extends Xs {
  constructor(t, e, n, s) {
    super(t, e, n, s);
  }
  drawFlatCoordinatess_(t, e, n, s) {
    const r = this.state, o = r.fillStyle !== void 0, a = r.strokeStyle !== void 0, l = n.length;
    this.instructions.push(Bi), this.hitDetectionInstructions.push(Bi);
    for (let h = 0; h < l; ++h) {
      const c = n[h], u = this.coordinates.length, d = this.appendFlatLineCoordinates(
        t,
        e,
        c,
        s,
        !0,
        !a
      ), f = [
        U.MOVE_TO_LINE_TO,
        u,
        d
      ];
      this.instructions.push(f), this.hitDetectionInstructions.push(f), a && (this.instructions.push(Zh), this.hitDetectionInstructions.push(Zh)), e = c;
    }
    return o && (this.instructions.push(Cr), this.hitDetectionInstructions.push(Cr)), a && (this.instructions.push(xi), this.hitDetectionInstructions.push(xi)), e;
  }
  drawCircle(t, e) {
    const n = this.state, s = n.fillStyle, r = n.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), n.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_FILL_STYLE,
      ii
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_STROKE_STYLE,
      n.strokeStyle,
      n.lineWidth,
      n.lineCap,
      n.lineJoin,
      n.miterLimit,
      n.lineDash,
      n.lineDashOffset
    ]);
    const o = t.getFlatCoordinates(), a = t.getStride(), l = this.coordinates.length;
    this.appendFlatLineCoordinates(
      o,
      0,
      o.length,
      a,
      !1,
      !1
    );
    const h = [U.CIRCLE, l];
    this.instructions.push(Bi, h), this.hitDetectionInstructions.push(Bi, h), n.fillStyle !== void 0 && (this.instructions.push(Cr), this.hitDetectionInstructions.push(Cr)), n.strokeStyle !== void 0 && (this.instructions.push(xi), this.hitDetectionInstructions.push(xi)), this.endGeometry(e);
  }
  drawPolygon(t, e) {
    const n = this.state, s = n.fillStyle, r = n.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), n.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_FILL_STYLE,
      ii
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_STROKE_STYLE,
      n.strokeStyle,
      n.lineWidth,
      n.lineCap,
      n.lineJoin,
      n.miterLimit,
      n.lineDash,
      n.lineDashOffset
    ]);
    const o = t.getEnds(), a = t.getOrientedFlatCoordinates(), l = t.getStride();
    this.drawFlatCoordinatess_(
      a,
      0,
      o,
      l
    ), this.endGeometry(e);
  }
  drawMultiPolygon(t, e) {
    const n = this.state, s = n.fillStyle, r = n.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), n.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_FILL_STYLE,
      ii
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      U.SET_STROKE_STYLE,
      n.strokeStyle,
      n.lineWidth,
      n.lineCap,
      n.lineJoin,
      n.miterLimit,
      n.lineDash,
      n.lineDashOffset
    ]);
    const o = t.getEndss(), a = t.getOrientedFlatCoordinates(), l = t.getStride();
    let h = 0;
    for (let c = 0, u = o.length; c < u; ++c)
      h = this.drawFlatCoordinatess_(
        a,
        h,
        o[c],
        l
      );
    this.endGeometry(e);
  }
  finish() {
    this.reverseHitDetectionInstructions(), this.state = null;
    const t = this.tolerance;
    if (t !== 0) {
      const e = this.coordinates;
      for (let n = 0, s = e.length; n < s; ++n)
        e[n] = Di(e[n], t);
    }
    return super.finish();
  }
  setFillStrokeStyles_() {
    const t = this.state;
    t.fillStyle !== void 0 && this.updateFillStyle(t, this.createFill), t.strokeStyle !== void 0 && this.updateStrokeStyle(t, this.applyStroke);
  }
}
const Vh = Rm;
function bm(i, t, e, n, s) {
  let r = e, o = e, a = 0, l = 0, h = e, c, u, d, f, g, m, p, _, y, v;
  for (u = e; u < n; u += s) {
    const x = t[u], C = t[u + 1];
    g !== void 0 && (y = x - g, v = C - m, f = Math.sqrt(y * y + v * v), p !== void 0 && (l += d, c = Math.acos((p * y + _ * v) / (d * f)), c > i && (l > a && (a = l, r = h, o = u), l = 0, h = u - s)), d = f, p = y, _ = v), g = x, m = C;
  }
  return l += f, l > a ? [h, u] : [r, o];
}
const _s = {
  left: 0,
  end: 0,
  center: 0.5,
  right: 1,
  start: 1,
  top: 0,
  middle: 0.5,
  hanging: 0.2,
  alphabetic: 0.8,
  ideographic: 0.8,
  bottom: 1
};
class Lm extends Xs {
  constructor(t, e, n, s) {
    super(t, e, n, s), this.labels_ = null, this.text_ = "", this.textOffsetX_ = 0, this.textOffsetY_ = 0, this.textRotateWithView_ = void 0, this.textRotation_ = 0, this.textFillState_ = null, this.fillStates = {}, this.textStrokeState_ = null, this.strokeStates = {}, this.textState_ = {}, this.textStates = {}, this.textKey_ = "", this.fillKey_ = "", this.strokeKey_ = "", this.declutterImageWithText_ = void 0;
  }
  finish() {
    const t = super.finish();
    return t.textStates = this.textStates, t.fillStates = this.fillStates, t.strokeStates = this.strokeStates, t;
  }
  drawText(t, e) {
    const n = this.textFillState_, s = this.textStrokeState_, r = this.textState_;
    if (this.text_ === "" || !r || !n && !s)
      return;
    const o = this.coordinates;
    let a = o.length;
    const l = t.getType();
    let h = null, c = t.getStride();
    if (r.placement === "line" && (l == "LineString" || l == "MultiLineString" || l == "Polygon" || l == "MultiPolygon")) {
      if (!ie(this.getBufferedMaxExtent(), t.getExtent()))
        return;
      let u;
      if (h = t.getFlatCoordinates(), l == "LineString")
        u = [h.length];
      else if (l == "MultiLineString")
        u = t.getEnds();
      else if (l == "Polygon")
        u = t.getEnds().slice(0, 1);
      else if (l == "MultiPolygon") {
        const m = t.getEndss();
        u = [];
        for (let p = 0, _ = m.length; p < _; ++p)
          u.push(m[p][0]);
      }
      this.beginGeometry(t, e);
      const d = r.textAlign;
      let f = 0, g;
      for (let m = 0, p = u.length; m < p; ++m) {
        if (d == null) {
          const y = bm(
            r.maxAngle,
            h,
            f,
            u[m],
            c
          );
          f = y[0], g = y[1];
        } else
          g = u[m];
        for (let y = f; y < g; y += c)
          o.push(h[y], h[y + 1]);
        const _ = o.length;
        f = u[m], this.drawChars_(a, _), a = _;
      }
      this.endGeometry(e);
    } else {
      let u = r.overflow ? null : [];
      switch (l) {
        case "Point":
        case "MultiPoint":
          h = t.getFlatCoordinates();
          break;
        case "LineString":
          h = t.getFlatMidpoint();
          break;
        case "Circle":
          h = t.getCenter();
          break;
        case "MultiLineString":
          h = t.getFlatMidpoints(), c = 2;
          break;
        case "Polygon":
          h = t.getFlatInteriorPoint(), r.overflow || u.push(h[2] / this.resolution), c = 3;
          break;
        case "MultiPolygon":
          const p = t.getFlatInteriorPoints();
          h = [];
          for (let _ = 0, y = p.length; _ < y; _ += 3)
            r.overflow || u.push(p[_ + 2] / this.resolution), h.push(p[_], p[_ + 1]);
          if (h.length === 0)
            return;
          c = 2;
          break;
      }
      const d = this.appendFlatPointCoordinates(h, c);
      if (d === a)
        return;
      if (u && (d - a) / 2 !== h.length / c) {
        let p = a / 2;
        u = u.filter((_, y) => {
          const v = o[(p + y) * 2] === h[y * c] && o[(p + y) * 2 + 1] === h[y * c + 1];
          return v || --p, v;
        });
      }
      this.saveTextStates_(), (r.backgroundFill || r.backgroundStroke) && (this.setFillStrokeStyle(
        r.backgroundFill,
        r.backgroundStroke
      ), r.backgroundFill && (this.updateFillStyle(this.state, this.createFill), this.hitDetectionInstructions.push(this.createFill(this.state))), r.backgroundStroke && (this.updateStrokeStyle(this.state, this.applyStroke), this.hitDetectionInstructions.push(this.createStroke(this.state)))), this.beginGeometry(t, e);
      let f = r.padding;
      if (f != ki && (r.scale[0] < 0 || r.scale[1] < 0)) {
        let p = r.padding[0], _ = r.padding[1], y = r.padding[2], v = r.padding[3];
        r.scale[0] < 0 && (_ = -_, v = -v), r.scale[1] < 0 && (p = -p, y = -y), f = [p, _, y, v];
      }
      const g = this.pixelRatio;
      this.instructions.push([
        U.DRAW_IMAGE,
        a,
        d,
        null,
        NaN,
        NaN,
        NaN,
        1,
        0,
        0,
        this.textRotateWithView_,
        this.textRotation_,
        [1, 1],
        NaN,
        void 0,
        this.declutterImageWithText_,
        f == ki ? ki : f.map(function(p) {
          return p * g;
        }),
        !!r.backgroundFill,
        !!r.backgroundStroke,
        this.text_,
        this.textKey_,
        this.strokeKey_,
        this.fillKey_,
        this.textOffsetX_,
        this.textOffsetY_,
        u
      ]);
      const m = 1 / g;
      this.hitDetectionInstructions.push([
        U.DRAW_IMAGE,
        a,
        d,
        null,
        NaN,
        NaN,
        NaN,
        1,
        0,
        0,
        this.textRotateWithView_,
        this.textRotation_,
        [m, m],
        NaN,
        void 0,
        this.declutterImageWithText_,
        f,
        !!r.backgroundFill,
        !!r.backgroundStroke,
        this.text_,
        this.textKey_,
        this.strokeKey_,
        this.fillKey_,
        this.textOffsetX_,
        this.textOffsetY_,
        u
      ]), this.endGeometry(e);
    }
  }
  saveTextStates_() {
    const t = this.textStrokeState_, e = this.textState_, n = this.textFillState_, s = this.strokeKey_;
    t && (s in this.strokeStates || (this.strokeStates[s] = {
      strokeStyle: t.strokeStyle,
      lineCap: t.lineCap,
      lineDashOffset: t.lineDashOffset,
      lineWidth: t.lineWidth,
      lineJoin: t.lineJoin,
      miterLimit: t.miterLimit,
      lineDash: t.lineDash
    }));
    const r = this.textKey_;
    r in this.textStates || (this.textStates[r] = {
      font: e.font,
      textAlign: e.textAlign || Ls,
      justify: e.justify,
      textBaseline: e.textBaseline || Vr,
      scale: e.scale
    });
    const o = this.fillKey_;
    n && (o in this.fillStates || (this.fillStates[o] = {
      fillStyle: n.fillStyle
    }));
  }
  drawChars_(t, e) {
    const n = this.textStrokeState_, s = this.textState_, r = this.strokeKey_, o = this.textKey_, a = this.fillKey_;
    this.saveTextStates_();
    const l = this.pixelRatio, h = _s[s.textBaseline], c = this.textOffsetY_ * l, u = this.text_, d = n ? n.lineWidth * Math.abs(s.scale[0]) / 2 : 0;
    this.instructions.push([
      U.DRAW_CHARS,
      t,
      e,
      h,
      s.overflow,
      a,
      s.maxAngle,
      l,
      c,
      r,
      d * l,
      u,
      o,
      1
    ]), this.hitDetectionInstructions.push([
      U.DRAW_CHARS,
      t,
      e,
      h,
      s.overflow,
      a,
      s.maxAngle,
      1,
      c,
      r,
      d,
      u,
      o,
      1 / l
    ]);
  }
  setTextStyle(t, e) {
    let n, s, r;
    if (!t)
      this.text_ = "";
    else {
      const o = t.getFill();
      o ? (s = this.textFillState_, s || (s = {}, this.textFillState_ = s), s.fillStyle = Oe(
        o.getColor() || ii
      )) : (s = null, this.textFillState_ = s);
      const a = t.getStroke();
      if (!a)
        r = null, this.textStrokeState_ = r;
      else {
        r = this.textStrokeState_, r || (r = {}, this.textStrokeState_ = r);
        const g = a.getLineDash(), m = a.getLineDashOffset(), p = a.getWidth(), _ = a.getMiterLimit();
        r.lineCap = a.getLineCap() || Zr, r.lineDash = g ? g.slice() : ws, r.lineDashOffset = m === void 0 ? Ss : m, r.lineJoin = a.getLineJoin() || $n, r.lineWidth = p === void 0 ? Ts : p, r.miterLimit = _ === void 0 ? Rs : _, r.strokeStyle = Oe(
          a.getColor() || bs
        );
      }
      n = this.textState_;
      const l = t.getFont() || zu;
      q0(l);
      const h = t.getScaleArray();
      n.overflow = t.getOverflow(), n.font = l, n.maxAngle = t.getMaxAngle(), n.placement = t.getPlacement(), n.textAlign = t.getTextAlign(), n.justify = t.getJustify(), n.textBaseline = t.getTextBaseline() || Vr, n.backgroundFill = t.getBackgroundFill(), n.backgroundStroke = t.getBackgroundStroke(), n.padding = t.getPadding() || ki, n.scale = h === void 0 ? [1, 1] : h;
      const c = t.getOffsetX(), u = t.getOffsetY(), d = t.getRotateWithView(), f = t.getRotation();
      this.text_ = t.getText() || "", this.textOffsetX_ = c === void 0 ? 0 : c, this.textOffsetY_ = u === void 0 ? 0 : u, this.textRotateWithView_ = d === void 0 ? !1 : d, this.textRotation_ = f === void 0 ? 0 : f, this.strokeKey_ = r ? (typeof r.strokeStyle == "string" ? r.strokeStyle : ot(r.strokeStyle)) + r.lineCap + r.lineDashOffset + "|" + r.lineWidth + r.lineJoin + r.miterLimit + "[" + r.lineDash.join() + "]" : "", this.textKey_ = n.font + n.scale + (n.textAlign || "?") + (n.justify || "?") + (n.textBaseline || "?"), this.fillKey_ = s ? typeof s.fillStyle == "string" ? s.fillStyle : "|" + ot(s.fillStyle) : "";
    }
    this.declutterImageWithText_ = e;
  }
}
const Tm = {
  Circle: Vh,
  Default: Xs,
  Image: Em,
  LineString: Sm,
  Polygon: Vh,
  Text: Lm
};
class Im {
  constructor(t, e, n, s) {
    this.tolerance_ = t, this.maxExtent_ = e, this.pixelRatio_ = s, this.resolution_ = n, this.buildersByZIndex_ = {};
  }
  finish() {
    const t = {};
    for (const e in this.buildersByZIndex_) {
      t[e] = t[e] || {};
      const n = this.buildersByZIndex_[e];
      for (const s in n) {
        const r = n[s].finish();
        t[e][s] = r;
      }
    }
    return t;
  }
  getBuilder(t, e) {
    const n = t !== void 0 ? t.toString() : "0";
    let s = this.buildersByZIndex_[n];
    s === void 0 && (s = {}, this.buildersByZIndex_[n] = s);
    let r = s[e];
    if (r === void 0) {
      const o = Tm[e];
      r = new o(
        this.tolerance_,
        this.maxExtent_,
        this.resolution_,
        this.pixelRatio_
      ), s[e] = r;
    }
    return r;
  }
}
const Uh = Im;
class Pm extends _u {
  constructor(t) {
    super(), this.ready = !0, this.boundHandleImageChange_ = this.handleImageChange_.bind(this), this.layer_ = t, this.declutterExecutorGroup = null;
  }
  getFeatures(t) {
    return W();
  }
  getData(t) {
    return null;
  }
  prepareFrame(t) {
    return W();
  }
  renderFrame(t, e) {
    return W();
  }
  loadedTileCallback(t, e, n) {
    t[e] || (t[e] = {}), t[e][n.tileCoord.toString()] = n;
  }
  createLoadedTileFinder(t, e, n) {
    return function(s, r) {
      const o = this.loadedTileCallback.bind(this, n, s);
      return t.forEachLoadedTile(e, s, r, o);
    }.bind(this);
  }
  forEachFeatureAtCoordinate(t, e, n, s, r) {
  }
  getLayer() {
    return this.layer_;
  }
  handleFontsChanged() {
  }
  handleImageChange_(t) {
    t.target.getState() === It.LOADED && this.renderIfReadyAndVisible();
  }
  loadImage(t) {
    let e = t.getState();
    return e != It.LOADED && e != It.ERROR && t.addEventListener(X.CHANGE, this.boundHandleImageChange_), e == It.IDLE && (t.load(), e = t.getState()), e == It.LOADED;
  }
  renderIfReadyAndVisible() {
    const t = this.getLayer();
    t && t.getVisible() && t.getSourceState() === "ready" && t.changed();
  }
  disposeInternal() {
    delete this.layer_, super.disposeInternal();
  }
}
const Am = Pm, Wh = [];
let En = null;
function Om() {
  const i = document.createElement("canvas");
  i.width = 1, i.height = 1, En = i.getContext("2d");
}
class Nm extends Am {
  constructor(t) {
    super(t), this.container = null, this.renderedResolution, this.tempTransform = Fe(), this.pixelTransform = Fe(), this.inversePixelTransform = Fe(), this.context = null, this.containerReused = !1, this.pixelContext_ = null, this.frameState = null;
  }
  getImageData(t, e, n) {
    En || Om(), En.clearRect(0, 0, 1, 1);
    let s;
    try {
      En.drawImage(t, e, n, 1, 1, 0, 0, 1, 1), s = En.getImageData(0, 0, 1, 1).data;
    } catch {
      return En = null, null;
    }
    return s;
  }
  getBackground(t) {
    let n = this.getLayer().getBackground();
    return typeof n == "function" && (n = n(t.viewState.resolution)), n || void 0;
  }
  useContainer(t, e, n) {
    const s = this.getLayer().getClassName();
    let r, o;
    if (t && t.className === s && (!n || t && t.style.backgroundColor && nn(
      kr(t.style.backgroundColor),
      kr(n)
    ))) {
      const a = t.firstElementChild;
      a instanceof HTMLCanvasElement && (o = a.getContext("2d"));
    }
    if (o && o.canvas.style.transform === e ? (this.container = t, this.context = o, this.containerReused = !0) : this.containerReused && (this.container = null, this.context = null, this.containerReused = !1), !this.container) {
      r = document.createElement("div"), r.className = s;
      let a = r.style;
      a.position = "absolute", a.width = "100%", a.height = "100%", o = ge();
      const l = o.canvas;
      r.appendChild(l), a = l.style, a.position = "absolute", a.left = "0", a.transformOrigin = "top left", this.container = r, this.context = o;
    }
    !this.containerReused && n && !this.container.style.backgroundColor && (this.container.style.backgroundColor = n);
  }
  clipUnrotated(t, e, n) {
    const s = Ii(n), r = mo(n), o = go(n), a = fo(n);
    Ft(e.coordinateToPixelTransform, s), Ft(e.coordinateToPixelTransform, r), Ft(e.coordinateToPixelTransform, o), Ft(e.coordinateToPixelTransform, a);
    const l = this.inversePixelTransform;
    Ft(l, s), Ft(l, r), Ft(l, o), Ft(l, a), t.save(), t.beginPath(), t.moveTo(Math.round(s[0]), Math.round(s[1])), t.lineTo(Math.round(r[0]), Math.round(r[1])), t.lineTo(Math.round(o[0]), Math.round(o[1])), t.lineTo(Math.round(a[0]), Math.round(a[1])), t.clip();
  }
  dispatchRenderEvent_(t, e, n) {
    const s = this.getLayer();
    if (s.hasListener(t)) {
      const r = new ku(
        t,
        this.inversePixelTransform,
        n,
        e
      );
      s.dispatchEvent(r);
    }
  }
  preRender(t, e) {
    this.frameState = e, this.dispatchRenderEvent_(Ci.PRERENDER, t, e);
  }
  postRender(t, e) {
    this.dispatchRenderEvent_(Ci.POSTRENDER, t, e);
  }
  getRenderTransform(t, e, n, s, r, o, a) {
    const l = r / 2, h = o / 2, c = s / e, u = -c, d = -t[0] + a, f = -t[1];
    return Si(
      this.tempTransform,
      l,
      h,
      c,
      u,
      -n,
      d,
      f
    );
  }
  disposeInternal() {
    delete this.frameState, super.disposeInternal();
  }
}
const Ed = Nm;
function Fm(i, t, e, n, s, r, o, a, l, h, c, u) {
  let d = i[t], f = i[t + 1], g = 0, m = 0, p = 0, _ = 0;
  function y() {
    g = d, m = f, t += n, d = i[t], f = i[t + 1], _ += p, p = Math.sqrt((d - g) * (d - g) + (f - m) * (f - m));
  }
  do
    y();
  while (t < e - n && _ + p < r);
  let v = p === 0 ? 0 : (r - _) / p;
  const x = Je(g, d, v), C = Je(m, f, v), w = t - n, S = _, b = r + a * l(h, s, c);
  for (; t < e - n && _ + p < b; )
    y();
  v = p === 0 ? 0 : (b - _) / p;
  const A = Je(g, d, v), G = Je(m, f, v);
  let V;
  if (u) {
    const k = [x, C, A, G];
    qu(k, 0, 4, 2, u, k, k), V = k[0] > k[2];
  } else
    V = x > A;
  const T = Math.PI, $ = [], ft = w + n === t;
  t = w, p = 0, _ = S, d = i[t], f = i[t + 1];
  let F;
  if (ft) {
    y(), F = Math.atan2(f - m, d - g), V && (F += F > 0 ? -T : T);
    const k = (A + x) / 2, P = (G + C) / 2;
    return $[0] = [k, P, (b - r) / 2, F, s], $;
  }
  s = s.replace(/\n/g, " ");
  for (let k = 0, P = s.length; k < P; ) {
    y();
    let tt = Math.atan2(f - m, d - g);
    if (V && (tt += tt > 0 ? -T : T), F !== void 0) {
      let lt = tt - F;
      if (lt += lt > T ? -2 * T : lt < -T ? 2 * T : 0, Math.abs(lt) > o)
        return null;
    }
    F = tt;
    const Ct = k;
    let _t = 0;
    for (; k < P; ++k) {
      const lt = V ? P - k - 1 : k, gt = a * l(h, s[lt], c);
      if (t + n < e && _ + p < r + _t + gt / 2)
        break;
      _t += gt;
    }
    if (k === Ct)
      continue;
    const At = V ? s.substring(P - Ct, P - k) : s.substring(Ct, k);
    v = p === 0 ? 0 : (r + _t / 2 - _) / p;
    const L = Je(g, d, v), ae = Je(m, f, v);
    $.push([L, ae, _t / 2, tt, At]), r += _t;
  }
  return $;
}
const pn = fe(), ui = [], He = [], Xe = [], di = [];
function Hh(i) {
  return i[3].declutterBox;
}
const Dm = new RegExp(
  "[" + String.fromCharCode(1425) + "-" + String.fromCharCode(2303) + String.fromCharCode(64285) + "-" + String.fromCharCode(65023) + String.fromCharCode(65136) + "-" + String.fromCharCode(65276) + String.fromCharCode(67584) + "-" + String.fromCharCode(69631) + String.fromCharCode(124928) + "-" + String.fromCharCode(126975) + "]"
);
function Xh(i, t) {
  return (t === "start" || t === "end") && !Dm.test(i) && (t = t === "start" ? "left" : "right"), _s[t];
}
function km(i, t, e) {
  return e > 0 && i.push(`
`, ""), i.push(t, ""), i;
}
class Gm {
  constructor(t, e, n, s) {
    this.overlaps = n, this.pixelRatio = e, this.resolution = t, this.alignFill_, this.instructions = s.instructions, this.coordinates = s.coordinates, this.coordinateCache_ = {}, this.renderedTransform_ = Fe(), this.hitDetectionInstructions = s.hitDetectionInstructions, this.pixelCoordinates_ = null, this.viewRotation_ = 0, this.fillStates = s.fillStates || {}, this.strokeStates = s.strokeStates || {}, this.textStates = s.textStates || {}, this.widths_ = {}, this.labels_ = {};
  }
  createLabel(t, e, n, s) {
    const r = t + e + n + s;
    if (this.labels_[r])
      return this.labels_[r];
    const o = s ? this.strokeStates[s] : null, a = n ? this.fillStates[n] : null, l = this.textStates[e], h = this.pixelRatio, c = [
      l.scale[0] * h,
      l.scale[1] * h
    ], u = Array.isArray(t), d = l.justify ? _s[l.justify] : Xh(
      Array.isArray(t) ? t[0] : t,
      l.textAlign || Ls
    ), f = s && o.lineWidth ? o.lineWidth : 0, g = u ? t : t.split(`
`).reduce(km, []), { width: m, height: p, widths: _, heights: y, lineWidths: v } = Q0(
      l,
      g
    ), x = m + f, C = [], w = (x + 2) * c[0], S = (p + f) * c[1], b = {
      width: w < 0 ? Math.floor(w) : Math.ceil(w),
      height: S < 0 ? Math.floor(S) : Math.ceil(S),
      contextInstructions: C
    };
    (c[0] != 1 || c[1] != 1) && C.push("scale", c), s && (C.push("strokeStyle", o.strokeStyle), C.push("lineWidth", f), C.push("lineCap", o.lineCap), C.push("lineJoin", o.lineJoin), C.push("miterLimit", o.miterLimit), C.push("setLineDash", [o.lineDash]), C.push("lineDashOffset", o.lineDashOffset)), n && C.push("fillStyle", a.fillStyle), C.push("textBaseline", "middle"), C.push("textAlign", "center");
    const A = 0.5 - d;
    let G = d * x + A * f;
    const V = [], T = [];
    let $ = 0, ft = 0, F = 0, k = 0, P;
    for (let tt = 0, Ct = g.length; tt < Ct; tt += 2) {
      const _t = g[tt];
      if (_t === `
`) {
        ft += $, $ = 0, G = d * x + A * f, ++k;
        continue;
      }
      const At = g[tt + 1] || l.font;
      At !== P && (s && V.push("font", At), n && T.push("font", At), P = At), $ = Math.max($, y[F]);
      const L = [
        _t,
        G + A * _[F] + d * (_[F] - v[k]),
        0.5 * (f + $) + ft
      ];
      G += _[F], s && V.push("strokeText", L), n && T.push("fillText", L), ++F;
    }
    return Array.prototype.push.apply(C, V), Array.prototype.push.apply(C, T), this.labels_[r] = b, b;
  }
  replayTextBackground_(t, e, n, s, r, o, a) {
    t.beginPath(), t.moveTo.apply(t, e), t.lineTo.apply(t, n), t.lineTo.apply(t, s), t.lineTo.apply(t, r), t.lineTo.apply(t, e), o && (this.alignFill_ = o[2], this.fill_(t)), a && (this.setStrokeStyle_(
      t,
      a
    ), t.stroke());
  }
  calculateImageOrLabelDimensions_(t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p) {
    a *= d[0], l *= d[1];
    let _ = n - a, y = s - l;
    const v = r + h > t ? t - h : r, x = o + c > e ? e - c : o, C = g[3] + v * d[0] + g[1], w = g[0] + x * d[1] + g[2], S = _ - g[3], b = y - g[0];
    (m || u !== 0) && (ui[0] = S, di[0] = S, ui[1] = b, He[1] = b, He[0] = S + C, Xe[0] = He[0], Xe[1] = b + w, di[1] = Xe[1]);
    let A;
    return u !== 0 ? (A = Si(
      Fe(),
      n,
      s,
      1,
      1,
      u,
      -n,
      -s
    ), Ft(A, ui), Ft(A, He), Ft(A, Xe), Ft(A, di), xe(
      Math.min(ui[0], He[0], Xe[0], di[0]),
      Math.min(ui[1], He[1], Xe[1], di[1]),
      Math.max(ui[0], He[0], Xe[0], di[0]),
      Math.max(ui[1], He[1], Xe[1], di[1]),
      pn
    )) : xe(
      Math.min(S, S + C),
      Math.min(b, b + w),
      Math.max(S, S + C),
      Math.max(b, b + w),
      pn
    ), f && (_ = Math.round(_), y = Math.round(y)), {
      drawImageX: _,
      drawImageY: y,
      drawImageW: v,
      drawImageH: x,
      originX: h,
      originY: c,
      declutterBox: {
        minX: pn[0],
        minY: pn[1],
        maxX: pn[2],
        maxY: pn[3],
        value: p
      },
      canvasTransform: A,
      scale: d
    };
  }
  replayImageOrLabel_(t, e, n, s, r, o, a) {
    const l = !!(o || a), h = s.declutterBox, c = t.canvas, u = a ? a[2] * s.scale[0] / 2 : 0;
    return h.minX - u <= c.width / e && h.maxX + u >= 0 && h.minY - u <= c.height / e && h.maxY + u >= 0 && (l && this.replayTextBackground_(
      t,
      ui,
      He,
      Xe,
      di,
      o,
      a
    ), tg(
      t,
      s.canvasTransform,
      r,
      n,
      s.originX,
      s.originY,
      s.drawImageW,
      s.drawImageH,
      s.drawImageX,
      s.drawImageY,
      s.scale
    )), !0;
  }
  fill_(t) {
    if (this.alignFill_) {
      const e = Ft(this.renderedTransform_, [0, 0]), n = 512 * this.pixelRatio;
      t.save(), t.translate(e[0] % n, e[1] % n), t.rotate(this.viewRotation_);
    }
    t.fill(), this.alignFill_ && t.restore();
  }
  setStrokeStyle_(t, e) {
    t.strokeStyle = e[1], t.lineWidth = e[2], t.lineCap = e[3], t.lineJoin = e[4], t.miterLimit = e[5], t.lineDashOffset = e[7], t.setLineDash(e[6]);
  }
  drawLabelWithPointPlacement_(t, e, n, s) {
    const r = this.textStates[e], o = this.createLabel(t, e, s, n), a = this.strokeStates[n], l = this.pixelRatio, h = Xh(
      Array.isArray(t) ? t[0] : t,
      r.textAlign || Ls
    ), c = _s[r.textBaseline || Vr], u = a && a.lineWidth ? a.lineWidth : 0, d = o.width / l - 2 * r.scale[0], f = h * d + 2 * (0.5 - h) * u, g = c * o.height / l + 2 * (0.5 - c) * u;
    return {
      label: o,
      anchorX: f,
      anchorY: g
    };
  }
  execute_(t, e, n, s, r, o, a, l) {
    let h;
    this.pixelCoordinates_ && nn(n, this.renderedTransform_) ? h = this.pixelCoordinates_ : (this.pixelCoordinates_ || (this.pixelCoordinates_ = []), h = Wi(
      this.coordinates,
      0,
      this.coordinates.length,
      2,
      n,
      this.pixelCoordinates_
    ), M0(this.renderedTransform_, n));
    let c = 0;
    const u = s.length;
    let d = 0, f, g, m, p, _, y, v, x, C, w, S, b, A = 0, G = 0, V = null, T = null;
    const $ = this.coordinateCache_, ft = this.viewRotation_, F = Math.round(Math.atan2(-n[1], n[0]) * 1e12) / 1e12, k = {
      context: t,
      pixelRatio: this.pixelRatio,
      resolution: this.resolution,
      rotation: ft
    }, P = this.instructions != s || this.overlaps ? 0 : 200;
    let tt, Ct, _t, At;
    for (; c < u; ) {
      const L = s[c];
      switch (L[0]) {
        case U.BEGIN_GEOMETRY:
          tt = L[1], At = L[3], tt.getGeometry() ? a !== void 0 && !ie(a, At.getExtent()) ? c = L[2] + 1 : ++c : c = L[2];
          break;
        case U.BEGIN_PATH:
          A > P && (this.fill_(t), A = 0), G > P && (t.stroke(), G = 0), !A && !G && (t.beginPath(), p = NaN, _ = NaN), ++c;
          break;
        case U.CIRCLE:
          d = L[1];
          const lt = h[d], gt = h[d + 1], ai = h[d + 2], Te = h[d + 3], $t = ai - lt, Ze = Te - gt, ln = Math.sqrt($t * $t + Ze * Ze);
          t.moveTo(lt + ln, gt), t.arc(lt, gt, ln, 0, 2 * Math.PI, !0), ++c;
          break;
        case U.CLOSE_PATH:
          t.closePath(), ++c;
          break;
        case U.CUSTOM:
          d = L[1], f = L[2];
          const sr = L[3], hn = L[4], rr = L.length == 6 ? L[5] : void 0;
          k.geometry = sr, k.feature = tt, c in $ || ($[c] = []);
          const li = $[c];
          rr ? rr(h, d, f, 2, li) : (li[0] = h[d], li[1] = h[d + 1], li.length = 2), hn(li, k), ++c;
          break;
        case U.DRAW_IMAGE:
          d = L[1], f = L[2], x = L[3], g = L[4], m = L[5];
          let ts = L[6];
          const hi = L[7], or = L[8], ar = L[9], lr = L[10];
          let cn = L[11];
          const Ao = L[12];
          let Jt = L[13];
          const me = L[14], Me = L[15];
          if (!x && L.length >= 20) {
            C = L[19], w = L[20], S = L[21], b = L[22];
            const le = this.drawLabelWithPointPlacement_(
              C,
              w,
              S,
              b
            );
            x = le.label, L[3] = x;
            const fn = L[23];
            g = (le.anchorX - fn) * this.pixelRatio, L[4] = g;
            const pe = L[24];
            m = (le.anchorY - pe) * this.pixelRatio, L[5] = m, ts = x.height, L[6] = ts, Jt = x.width, L[13] = Jt;
          }
          let Ve;
          L.length > 25 && (Ve = L[25]);
          let un, Ai, ci;
          L.length > 17 ? (un = L[16], Ai = L[17], ci = L[18]) : (un = ki, Ai = !1, ci = !1), lr && F ? cn += ft : !lr && !F && (cn -= ft);
          let dn = 0;
          for (; d < f; d += 2) {
            if (Ve && Ve[dn++] < Jt / this.pixelRatio)
              continue;
            const le = this.calculateImageOrLabelDimensions_(
              x.width,
              x.height,
              h[d],
              h[d + 1],
              Jt,
              ts,
              g,
              m,
              or,
              ar,
              cn,
              Ao,
              r,
              un,
              Ai || ci,
              tt
            ), fn = [
              t,
              e,
              x,
              le,
              hi,
              Ai ? V : null,
              ci ? T : null
            ];
            if (l) {
              if (me === "none")
                continue;
              if (me === "obstacle") {
                l.insert(le.declutterBox);
                continue;
              } else {
                let pe, Ue;
                if (Me) {
                  const he = f - d;
                  if (!Me[he]) {
                    Me[he] = fn;
                    continue;
                  }
                  if (pe = Me[he], delete Me[he], Ue = Hh(pe), l.collides(Ue))
                    continue;
                }
                if (l.collides(le.declutterBox))
                  continue;
                pe && (l.insert(Ue), this.replayImageOrLabel_.apply(this, pe)), l.insert(le.declutterBox);
              }
            }
            this.replayImageOrLabel_.apply(this, fn);
          }
          ++c;
          break;
        case U.DRAW_CHARS:
          const hr = L[1], Ht = L[2], Oo = L[3], Uf = L[4];
          b = L[5];
          const Wf = L[6], jl = L[7], Kl = L[8];
          S = L[9];
          const No = L[10];
          C = L[11], w = L[12];
          const ql = [
            L[13],
            L[13]
          ], Fo = this.textStates[w], es = Fo.font, is = [
            Fo.scale[0] * jl,
            Fo.scale[1] * jl
          ];
          let ns;
          es in this.widths_ ? ns = this.widths_[es] : (ns = {}, this.widths_[es] = ns);
          const Jl = pd(h, hr, Ht, 2), Ql = Math.abs(is[0]) * Ch(es, C, ns);
          if (Uf || Ql <= Jl) {
            const le = this.textStates[w].textAlign, fn = (Jl - Ql) * _s[le], pe = Fm(
              h,
              hr,
              Ht,
              2,
              C,
              fn,
              Wf,
              Math.abs(is[0]),
              Ch,
              es,
              ns,
              F ? 0 : this.viewRotation_
            );
            t:
              if (pe) {
                const Ue = [];
                let he, cr, ur, Qt, _e;
                if (S)
                  for (he = 0, cr = pe.length; he < cr; ++he) {
                    _e = pe[he], ur = _e[4], Qt = this.createLabel(ur, w, "", S), g = _e[2] + (is[0] < 0 ? -No : No), m = Oo * Qt.height + (0.5 - Oo) * 2 * No * is[1] / is[0] - Kl;
                    const We = this.calculateImageOrLabelDimensions_(
                      Qt.width,
                      Qt.height,
                      _e[0],
                      _e[1],
                      Qt.width,
                      Qt.height,
                      g,
                      m,
                      0,
                      0,
                      _e[3],
                      ql,
                      !1,
                      ki,
                      !1,
                      tt
                    );
                    if (l && l.collides(We.declutterBox))
                      break t;
                    Ue.push([
                      t,
                      e,
                      Qt,
                      We,
                      1,
                      null,
                      null
                    ]);
                  }
                if (b)
                  for (he = 0, cr = pe.length; he < cr; ++he) {
                    _e = pe[he], ur = _e[4], Qt = this.createLabel(ur, w, b, ""), g = _e[2], m = Oo * Qt.height - Kl;
                    const We = this.calculateImageOrLabelDimensions_(
                      Qt.width,
                      Qt.height,
                      _e[0],
                      _e[1],
                      Qt.width,
                      Qt.height,
                      g,
                      m,
                      0,
                      0,
                      _e[3],
                      ql,
                      !1,
                      ki,
                      !1,
                      tt
                    );
                    if (l && l.collides(We.declutterBox))
                      break t;
                    Ue.push([
                      t,
                      e,
                      Qt,
                      We,
                      1,
                      null,
                      null
                    ]);
                  }
                l && l.load(Ue.map(Hh));
                for (let We = 0, Hf = Ue.length; We < Hf; ++We)
                  this.replayImageOrLabel_.apply(this, Ue[We]);
              }
          }
          ++c;
          break;
        case U.END_GEOMETRY:
          if (o !== void 0) {
            tt = L[1];
            const le = o(tt, At);
            if (le)
              return le;
          }
          ++c;
          break;
        case U.FILL:
          P ? A++ : this.fill_(t), ++c;
          break;
        case U.MOVE_TO_LINE_TO:
          for (d = L[1], f = L[2], Ct = h[d], _t = h[d + 1], y = Ct + 0.5 | 0, v = _t + 0.5 | 0, (y !== p || v !== _) && (t.moveTo(Ct, _t), p = y, _ = v), d += 2; d < f; d += 2)
            Ct = h[d], _t = h[d + 1], y = Ct + 0.5 | 0, v = _t + 0.5 | 0, (d == f - 2 || y !== p || v !== _) && (t.lineTo(Ct, _t), p = y, _ = v);
          ++c;
          break;
        case U.SET_FILL_STYLE:
          V = L, this.alignFill_ = L[2], A && (this.fill_(t), A = 0, G && (t.stroke(), G = 0)), t.fillStyle = L[1], ++c;
          break;
        case U.SET_STROKE_STYLE:
          T = L, G && (t.stroke(), G = 0), this.setStrokeStyle_(t, L), ++c;
          break;
        case U.STROKE:
          P ? G++ : t.stroke(), ++c;
          break;
        default:
          ++c;
          break;
      }
    }
    A && this.fill_(t), G && t.stroke();
  }
  execute(t, e, n, s, r, o) {
    this.viewRotation_ = s, this.execute_(
      t,
      e,
      n,
      this.instructions,
      r,
      void 0,
      void 0,
      o
    );
  }
  executeHitDetection(t, e, n, s, r) {
    return this.viewRotation_ = n, this.execute_(
      t,
      1,
      e,
      this.hitDetectionInstructions,
      !0,
      s,
      r
    );
  }
}
const $m = Gm, Ko = ["Polygon", "Circle", "LineString", "Image", "Text", "Default"];
class Bm {
  constructor(t, e, n, s, r, o) {
    this.maxExtent_ = t, this.overlaps_ = s, this.pixelRatio_ = n, this.resolution_ = e, this.renderBuffer_ = o, this.executorsByZIndex_ = {}, this.hitDetectionContext_ = null, this.hitDetectionTransform_ = Fe(), this.createExecutors_(r);
  }
  clip(t, e) {
    const n = this.getClipCoords(e);
    t.beginPath(), t.moveTo(n[0], n[1]), t.lineTo(n[2], n[3]), t.lineTo(n[4], n[5]), t.lineTo(n[6], n[7]), t.clip();
  }
  createExecutors_(t) {
    for (const e in t) {
      let n = this.executorsByZIndex_[e];
      n === void 0 && (n = {}, this.executorsByZIndex_[e] = n);
      const s = t[e];
      for (const r in s) {
        const o = s[r];
        n[r] = new $m(
          this.resolution_,
          this.pixelRatio_,
          this.overlaps_,
          o
        );
      }
    }
  }
  hasExecutors(t) {
    for (const e in this.executorsByZIndex_) {
      const n = this.executorsByZIndex_[e];
      for (let s = 0, r = t.length; s < r; ++s)
        if (t[s] in n)
          return !0;
    }
    return !1;
  }
  forEachFeatureAtCoordinate(t, e, n, s, r, o) {
    s = Math.round(s);
    const a = s * 2 + 1, l = Si(
      this.hitDetectionTransform_,
      s + 0.5,
      s + 0.5,
      1 / e,
      -1 / e,
      -n,
      -t[0],
      -t[1]
    ), h = !this.hitDetectionContext_;
    h && (this.hitDetectionContext_ = ge(
      a,
      a
    ));
    const c = this.hitDetectionContext_;
    c.canvas.width !== a || c.canvas.height !== a ? (c.canvas.width = a, c.canvas.height = a) : h || c.clearRect(0, 0, a, a);
    let u;
    this.renderBuffer_ !== void 0 && (u = fe(), gs(u, t), co(
      u,
      e * (this.renderBuffer_ + s),
      u
    ));
    const d = zm(s);
    let f;
    function g(C, w) {
      const S = c.getImageData(
        0,
        0,
        a,
        a
      ).data;
      for (let b = 0, A = d.length; b < A; b++)
        if (S[d[b]] > 0) {
          if (!o || f !== "Image" && f !== "Text" || o.includes(C)) {
            const G = (d[b] - 3) / 4, V = s - G % a, T = s - (G / a | 0), $ = r(C, w, V * V + T * T);
            if ($)
              return $;
          }
          c.clearRect(0, 0, a, a);
          break;
        }
    }
    const m = Object.keys(this.executorsByZIndex_).map(Number);
    m.sort(Yi);
    let p, _, y, v, x;
    for (p = m.length - 1; p >= 0; --p) {
      const C = m[p].toString();
      for (y = this.executorsByZIndex_[C], _ = Ko.length - 1; _ >= 0; --_)
        if (f = Ko[_], v = y[f], v !== void 0 && (x = v.executeHitDetection(
          c,
          l,
          n,
          g,
          u
        ), x))
          return x;
    }
  }
  getClipCoords(t) {
    const e = this.maxExtent_;
    if (!e)
      return null;
    const n = e[0], s = e[1], r = e[2], o = e[3], a = [n, s, n, o, r, o, r, s];
    return Wi(a, 0, 8, 2, t, a), a;
  }
  isEmpty() {
    return Gn(this.executorsByZIndex_);
  }
  execute(t, e, n, s, r, o, a) {
    const l = Object.keys(this.executorsByZIndex_).map(Number);
    l.sort(Yi), this.maxExtent_ && (t.save(), this.clip(t, n)), o = o || Ko;
    let h, c, u, d, f, g;
    for (a && l.reverse(), h = 0, c = l.length; h < c; ++h) {
      const m = l[h].toString();
      for (f = this.executorsByZIndex_[m], u = 0, d = o.length; u < d; ++u) {
        const p = o[u];
        g = f[p], g !== void 0 && g.execute(
          t,
          e,
          n,
          s,
          r,
          a
        );
      }
    }
    this.maxExtent_ && t.restore();
  }
}
const qo = {};
function zm(i) {
  if (qo[i] !== void 0)
    return qo[i];
  const t = i * 2 + 1, e = i * i, n = new Array(e + 1);
  for (let r = 0; r <= i; ++r)
    for (let o = 0; o <= i; ++o) {
      const a = r * r + o * o;
      if (a > e)
        break;
      let l = n[a];
      l || (l = [], n[a] = l), l.push(((i + r) * t + (i + o)) * 4 + 3), r > 0 && l.push(((i - r) * t + (i + o)) * 4 + 3), o > 0 && (l.push(((i + r) * t + (i - o)) * 4 + 3), r > 0 && l.push(((i - r) * t + (i - o)) * 4 + 3));
    }
  const s = [];
  for (let r = 0, o = n.length; r < o; ++r)
    n[r] && s.push(...n[r]);
  return qo[i] = s, s;
}
const Yh = Bm;
class Zm extends Md {
  constructor(t, e, n, s, r, o, a) {
    super(), this.context_ = t, this.pixelRatio_ = e, this.extent_ = n, this.transform_ = s, this.viewRotation_ = r, this.squaredTolerance_ = o, this.userTransform_ = a, this.contextFillState_ = null, this.contextStrokeState_ = null, this.contextTextState_ = null, this.fillState_ = null, this.strokeState_ = null, this.image_ = null, this.imageAnchorX_ = 0, this.imageAnchorY_ = 0, this.imageHeight_ = 0, this.imageOpacity_ = 0, this.imageOriginX_ = 0, this.imageOriginY_ = 0, this.imageRotateWithView_ = !1, this.imageRotation_ = 0, this.imageScale_ = [0, 0], this.imageWidth_ = 0, this.text_ = "", this.textOffsetX_ = 0, this.textOffsetY_ = 0, this.textRotateWithView_ = !1, this.textRotation_ = 0, this.textScale_ = [0, 0], this.textFillState_ = null, this.textStrokeState_ = null, this.textState_ = null, this.pixelCoordinates_ = [], this.tmpLocalTransform_ = Fe();
  }
  drawImages_(t, e, n, s) {
    if (!this.image_)
      return;
    const r = Wi(
      t,
      e,
      n,
      s,
      this.transform_,
      this.pixelCoordinates_
    ), o = this.context_, a = this.tmpLocalTransform_, l = o.globalAlpha;
    this.imageOpacity_ != 1 && (o.globalAlpha = l * this.imageOpacity_);
    let h = this.imageRotation_;
    this.imageRotateWithView_ && (h += this.viewRotation_);
    for (let c = 0, u = r.length; c < u; c += 2) {
      const d = r[c] - this.imageAnchorX_, f = r[c + 1] - this.imageAnchorY_;
      if (h !== 0 || this.imageScale_[0] != 1 || this.imageScale_[1] != 1) {
        const g = d + this.imageAnchorX_, m = f + this.imageAnchorY_;
        Si(
          a,
          g,
          m,
          1,
          1,
          h,
          -g,
          -m
        ), o.setTransform.apply(o, a), o.translate(g, m), o.scale(this.imageScale_[0], this.imageScale_[1]), o.drawImage(
          this.image_,
          this.imageOriginX_,
          this.imageOriginY_,
          this.imageWidth_,
          this.imageHeight_,
          -this.imageAnchorX_,
          -this.imageAnchorY_,
          this.imageWidth_,
          this.imageHeight_
        ), o.setTransform(1, 0, 0, 1, 0, 0);
      } else
        o.drawImage(
          this.image_,
          this.imageOriginX_,
          this.imageOriginY_,
          this.imageWidth_,
          this.imageHeight_,
          d,
          f,
          this.imageWidth_,
          this.imageHeight_
        );
    }
    this.imageOpacity_ != 1 && (o.globalAlpha = l);
  }
  drawText_(t, e, n, s) {
    if (!this.textState_ || this.text_ === "")
      return;
    this.textFillState_ && this.setContextFillState_(this.textFillState_), this.textStrokeState_ && this.setContextStrokeState_(this.textStrokeState_), this.setContextTextState_(this.textState_);
    const r = Wi(
      t,
      e,
      n,
      s,
      this.transform_,
      this.pixelCoordinates_
    ), o = this.context_;
    let a = this.textRotation_;
    for (this.textRotateWithView_ && (a += this.viewRotation_); e < n; e += s) {
      const l = r[e] + this.textOffsetX_, h = r[e + 1] + this.textOffsetY_;
      a !== 0 || this.textScale_[0] != 1 || this.textScale_[1] != 1 ? (o.translate(l - this.textOffsetX_, h - this.textOffsetY_), o.rotate(a), o.translate(this.textOffsetX_, this.textOffsetY_), o.scale(this.textScale_[0], this.textScale_[1]), this.textStrokeState_ && o.strokeText(this.text_, 0, 0), this.textFillState_ && o.fillText(this.text_, 0, 0), o.setTransform(1, 0, 0, 1, 0, 0)) : (this.textStrokeState_ && o.strokeText(this.text_, l, h), this.textFillState_ && o.fillText(this.text_, l, h));
    }
  }
  moveToLineTo_(t, e, n, s, r) {
    const o = this.context_, a = Wi(
      t,
      e,
      n,
      s,
      this.transform_,
      this.pixelCoordinates_
    );
    o.moveTo(a[0], a[1]);
    let l = a.length;
    r && (l -= 2);
    for (let h = 2; h < l; h += 2)
      o.lineTo(a[h], a[h + 1]);
    return r && o.closePath(), n;
  }
  drawRings_(t, e, n, s) {
    for (let r = 0, o = n.length; r < o; ++r)
      e = this.moveToLineTo_(
        t,
        e,
        n[r],
        s,
        !0
      );
    return e;
  }
  drawCircle(t) {
    if (!!ie(this.extent_, t.getExtent())) {
      if (this.fillState_ || this.strokeState_) {
        this.fillState_ && this.setContextFillState_(this.fillState_), this.strokeState_ && this.setContextStrokeState_(this.strokeState_);
        const e = zg(
          t,
          this.transform_,
          this.pixelCoordinates_
        ), n = e[2] - e[0], s = e[3] - e[1], r = Math.sqrt(n * n + s * s), o = this.context_;
        o.beginPath(), o.arc(
          e[0],
          e[1],
          r,
          0,
          2 * Math.PI
        ), this.fillState_ && o.fill(), this.strokeState_ && o.stroke();
      }
      this.text_ !== "" && this.drawText_(t.getCenter(), 0, 2, 2);
    }
  }
  setStyle(t) {
    this.setFillStrokeStyle(t.getFill(), t.getStroke()), this.setImageStyle(t.getImage()), this.setTextStyle(t.getText());
  }
  setTransform(t) {
    this.transform_ = t;
  }
  drawGeometry(t) {
    switch (t.getType()) {
      case "Point":
        this.drawPoint(
          t
        );
        break;
      case "LineString":
        this.drawLineString(
          t
        );
        break;
      case "Polygon":
        this.drawPolygon(
          t
        );
        break;
      case "MultiPoint":
        this.drawMultiPoint(
          t
        );
        break;
      case "MultiLineString":
        this.drawMultiLineString(
          t
        );
        break;
      case "MultiPolygon":
        this.drawMultiPolygon(
          t
        );
        break;
      case "GeometryCollection":
        this.drawGeometryCollection(
          t
        );
        break;
      case "Circle":
        this.drawCircle(
          t
        );
        break;
    }
  }
  drawFeature(t, e) {
    const n = e.getGeometryFunction()(t);
    !n || !ie(this.extent_, n.getExtent()) || (this.setStyle(e), this.drawGeometry(n));
  }
  drawGeometryCollection(t) {
    const e = t.getGeometriesArray();
    for (let n = 0, s = e.length; n < s; ++n)
      this.drawGeometry(e[n]);
  }
  drawPoint(t) {
    this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    ));
    const e = t.getFlatCoordinates(), n = t.getStride();
    this.image_ && this.drawImages_(e, 0, e.length, n), this.text_ !== "" && this.drawText_(e, 0, e.length, n);
  }
  drawMultiPoint(t) {
    this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    ));
    const e = t.getFlatCoordinates(), n = t.getStride();
    this.image_ && this.drawImages_(e, 0, e.length, n), this.text_ !== "" && this.drawText_(e, 0, e.length, n);
  }
  drawLineString(t) {
    if (this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    )), !!ie(this.extent_, t.getExtent())) {
      if (this.strokeState_) {
        this.setContextStrokeState_(this.strokeState_);
        const e = this.context_, n = t.getFlatCoordinates();
        e.beginPath(), this.moveToLineTo_(
          n,
          0,
          n.length,
          t.getStride(),
          !1
        ), e.stroke();
      }
      if (this.text_ !== "") {
        const e = t.getFlatMidpoint();
        this.drawText_(e, 0, 2, 2);
      }
    }
  }
  drawMultiLineString(t) {
    this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    ));
    const e = t.getExtent();
    if (!!ie(this.extent_, e)) {
      if (this.strokeState_) {
        this.setContextStrokeState_(this.strokeState_);
        const n = this.context_, s = t.getFlatCoordinates();
        let r = 0;
        const o = t.getEnds(), a = t.getStride();
        n.beginPath();
        for (let l = 0, h = o.length; l < h; ++l)
          r = this.moveToLineTo_(
            s,
            r,
            o[l],
            a,
            !1
          );
        n.stroke();
      }
      if (this.text_ !== "") {
        const n = t.getFlatMidpoints();
        this.drawText_(n, 0, n.length, 2);
      }
    }
  }
  drawPolygon(t) {
    if (this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    )), !!ie(this.extent_, t.getExtent())) {
      if (this.strokeState_ || this.fillState_) {
        this.fillState_ && this.setContextFillState_(this.fillState_), this.strokeState_ && this.setContextStrokeState_(this.strokeState_);
        const e = this.context_;
        e.beginPath(), this.drawRings_(
          t.getOrientedFlatCoordinates(),
          0,
          t.getEnds(),
          t.getStride()
        ), this.fillState_ && e.fill(), this.strokeState_ && e.stroke();
      }
      if (this.text_ !== "") {
        const e = t.getFlatInteriorPoint();
        this.drawText_(e, 0, 2, 2);
      }
    }
  }
  drawMultiPolygon(t) {
    if (this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    )), !!ie(this.extent_, t.getExtent())) {
      if (this.strokeState_ || this.fillState_) {
        this.fillState_ && this.setContextFillState_(this.fillState_), this.strokeState_ && this.setContextStrokeState_(this.strokeState_);
        const e = this.context_, n = t.getOrientedFlatCoordinates();
        let s = 0;
        const r = t.getEndss(), o = t.getStride();
        e.beginPath();
        for (let a = 0, l = r.length; a < l; ++a) {
          const h = r[a];
          s = this.drawRings_(n, s, h, o);
        }
        this.fillState_ && e.fill(), this.strokeState_ && e.stroke();
      }
      if (this.text_ !== "") {
        const e = t.getFlatInteriorPoints();
        this.drawText_(e, 0, e.length, 2);
      }
    }
  }
  setContextFillState_(t) {
    const e = this.context_, n = this.contextFillState_;
    n ? n.fillStyle != t.fillStyle && (n.fillStyle = t.fillStyle, e.fillStyle = t.fillStyle) : (e.fillStyle = t.fillStyle, this.contextFillState_ = {
      fillStyle: t.fillStyle
    });
  }
  setContextStrokeState_(t) {
    const e = this.context_, n = this.contextStrokeState_;
    n ? (n.lineCap != t.lineCap && (n.lineCap = t.lineCap, e.lineCap = t.lineCap), nn(n.lineDash, t.lineDash) || e.setLineDash(
      n.lineDash = t.lineDash
    ), n.lineDashOffset != t.lineDashOffset && (n.lineDashOffset = t.lineDashOffset, e.lineDashOffset = t.lineDashOffset), n.lineJoin != t.lineJoin && (n.lineJoin = t.lineJoin, e.lineJoin = t.lineJoin), n.lineWidth != t.lineWidth && (n.lineWidth = t.lineWidth, e.lineWidth = t.lineWidth), n.miterLimit != t.miterLimit && (n.miterLimit = t.miterLimit, e.miterLimit = t.miterLimit), n.strokeStyle != t.strokeStyle && (n.strokeStyle = t.strokeStyle, e.strokeStyle = t.strokeStyle)) : (e.lineCap = t.lineCap, e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset, e.lineJoin = t.lineJoin, e.lineWidth = t.lineWidth, e.miterLimit = t.miterLimit, e.strokeStyle = t.strokeStyle, this.contextStrokeState_ = {
      lineCap: t.lineCap,
      lineDash: t.lineDash,
      lineDashOffset: t.lineDashOffset,
      lineJoin: t.lineJoin,
      lineWidth: t.lineWidth,
      miterLimit: t.miterLimit,
      strokeStyle: t.strokeStyle
    });
  }
  setContextTextState_(t) {
    const e = this.context_, n = this.contextTextState_, s = t.textAlign ? t.textAlign : Ls;
    n ? (n.font != t.font && (n.font = t.font, e.font = t.font), n.textAlign != s && (n.textAlign = s, e.textAlign = s), n.textBaseline != t.textBaseline && (n.textBaseline = t.textBaseline, e.textBaseline = t.textBaseline)) : (e.font = t.font, e.textAlign = s, e.textBaseline = t.textBaseline, this.contextTextState_ = {
      font: t.font,
      textAlign: s,
      textBaseline: t.textBaseline
    });
  }
  setFillStrokeStyle(t, e) {
    if (!t)
      this.fillState_ = null;
    else {
      const n = t.getColor();
      this.fillState_ = {
        fillStyle: Oe(
          n || ii
        )
      };
    }
    if (!e)
      this.strokeState_ = null;
    else {
      const n = e.getColor(), s = e.getLineCap(), r = e.getLineDash(), o = e.getLineDashOffset(), a = e.getLineJoin(), l = e.getWidth(), h = e.getMiterLimit(), c = r || ws;
      this.strokeState_ = {
        lineCap: s !== void 0 ? s : Zr,
        lineDash: this.pixelRatio_ === 1 ? c : c.map((u) => u * this.pixelRatio_),
        lineDashOffset: (o || Ss) * this.pixelRatio_,
        lineJoin: a !== void 0 ? a : $n,
        lineWidth: (l !== void 0 ? l : Ts) * this.pixelRatio_,
        miterLimit: h !== void 0 ? h : Rs,
        strokeStyle: Oe(
          n || bs
        )
      };
    }
  }
  setImageStyle(t) {
    let e;
    if (!t || !(e = t.getSize())) {
      this.image_ = null;
      return;
    }
    const n = t.getPixelRatio(this.pixelRatio_), s = t.getAnchor(), r = t.getOrigin();
    this.image_ = t.getImage(this.pixelRatio_), this.imageAnchorX_ = s[0] * n, this.imageAnchorY_ = s[1] * n, this.imageHeight_ = e[1] * n, this.imageOpacity_ = t.getOpacity(), this.imageOriginX_ = r[0], this.imageOriginY_ = r[1], this.imageRotateWithView_ = t.getRotateWithView(), this.imageRotation_ = t.getRotation();
    const o = t.getScaleArray();
    this.imageScale_ = [
      o[0] * this.pixelRatio_ / n,
      o[1] * this.pixelRatio_ / n
    ], this.imageWidth_ = e[0] * n;
  }
  setTextStyle(t) {
    if (!t)
      this.text_ = "";
    else {
      const e = t.getFill();
      if (!e)
        this.textFillState_ = null;
      else {
        const f = e.getColor();
        this.textFillState_ = {
          fillStyle: Oe(
            f || ii
          )
        };
      }
      const n = t.getStroke();
      if (!n)
        this.textStrokeState_ = null;
      else {
        const f = n.getColor(), g = n.getLineCap(), m = n.getLineDash(), p = n.getLineDashOffset(), _ = n.getLineJoin(), y = n.getWidth(), v = n.getMiterLimit();
        this.textStrokeState_ = {
          lineCap: g !== void 0 ? g : Zr,
          lineDash: m || ws,
          lineDashOffset: p || Ss,
          lineJoin: _ !== void 0 ? _ : $n,
          lineWidth: y !== void 0 ? y : Ts,
          miterLimit: v !== void 0 ? v : Rs,
          strokeStyle: Oe(
            f || bs
          )
        };
      }
      const s = t.getFont(), r = t.getOffsetX(), o = t.getOffsetY(), a = t.getRotateWithView(), l = t.getRotation(), h = t.getScaleArray(), c = t.getText(), u = t.getTextAlign(), d = t.getTextBaseline();
      this.textState_ = {
        font: s !== void 0 ? s : zu,
        textAlign: u !== void 0 ? u : Ls,
        textBaseline: d !== void 0 ? d : Vr
      }, this.text_ = c !== void 0 ? Array.isArray(c) ? c.reduce((f, g, m) => f += m % 2 ? " " : g, "") : c : "", this.textOffsetX_ = r !== void 0 ? this.pixelRatio_ * r : 0, this.textOffsetY_ = o !== void 0 ? this.pixelRatio_ * o : 0, this.textRotateWithView_ = a !== void 0 ? a : !1, this.textRotation_ = l !== void 0 ? l : 0, this.textScale_ = [
        this.pixelRatio_ * h[0],
        this.pixelRatio_ * h[1]
      ];
    }
  }
}
const wd = Zm, Pe = 0.5;
function Vm(i, t, e, n, s, r, o) {
  const a = i[0] * Pe, l = i[1] * Pe, h = ge(a, l);
  h.imageSmoothingEnabled = !1;
  const c = h.canvas, u = new wd(
    h,
    Pe,
    s,
    null,
    o
  ), d = e.length, f = Math.floor((256 * 256 * 256 - 1) / d), g = {};
  for (let p = 1; p <= d; ++p) {
    const _ = e[p - 1], y = _.getStyleFunction() || n;
    if (!n)
      continue;
    let v = y(_, r);
    if (!v)
      continue;
    Array.isArray(v) || (v = [v]);
    const C = "#" + ("000000" + (p * f).toString(16)).slice(-6);
    for (let w = 0, S = v.length; w < S; ++w) {
      const b = v[w], A = b.getGeometryFunction()(_);
      if (!A || !ie(s, A.getExtent()))
        continue;
      const G = b.clone(), V = G.getFill();
      V && V.setColor(C);
      const T = G.getStroke();
      T && (T.setColor(C), T.setLineDash(null)), G.setText(void 0);
      const $ = b.getImage();
      if ($ && $.getOpacity() !== 0) {
        const k = $.getImageSize();
        if (!k)
          continue;
        const P = ge(
          k[0],
          k[1],
          void 0,
          { alpha: !1 }
        ), tt = P.canvas;
        P.fillStyle = C, P.fillRect(0, 0, tt.width, tt.height), G.setImage(
          new ps({
            img: tt,
            imgSize: k,
            anchor: $.getAnchor(),
            anchorXUnits: "pixels",
            anchorYUnits: "pixels",
            offset: $.getOrigin(),
            opacity: 1,
            size: $.getSize(),
            scale: $.getScale(),
            rotation: $.getRotation(),
            rotateWithView: $.getRotateWithView()
          })
        );
      }
      const ft = G.getZIndex() || 0;
      let F = g[ft];
      F || (F = {}, g[ft] = F, F.Polygon = [], F.Circle = [], F.LineString = [], F.Point = []), F[A.getType().replace("Multi", "")].push(
        A,
        G
      );
    }
  }
  const m = Object.keys(g).map(Number).sort(Yi);
  for (let p = 0, _ = m.length; p < _; ++p) {
    const y = g[m[p]];
    for (const v in y) {
      const x = y[v];
      for (let C = 0, w = x.length; C < w; C += 2) {
        u.setStyle(x[C + 1]);
        for (let S = 0, b = t.length; S < b; ++S)
          u.setTransform(t[S]), u.drawGeometry(x[C]);
      }
    }
  }
  return h.getImageData(0, 0, c.width, c.height);
}
function Um(i, t, e) {
  const n = [];
  if (e) {
    const s = Math.floor(Math.round(i[0]) * Pe), r = Math.floor(Math.round(i[1]) * Pe), o = (wt(s, 0, e.width - 1) + wt(r, 0, e.height - 1) * e.width) * 4, a = e.data[o], l = e.data[o + 1], c = e.data[o + 2] + 256 * (l + 256 * a), u = Math.floor((256 * 256 * 256 - 1) / t.length);
    c && c % u === 0 && n.push(t[c / u - 1]);
  }
  return n;
}
const Wm = 0.5, Sd = {
  Point: Qm,
  LineString: Km,
  Polygon: e2,
  MultiPoint: t2,
  MultiLineString: qm,
  MultiPolygon: Jm,
  GeometryCollection: jm,
  Circle: Xm
};
function Hm(i, t) {
  return parseInt(ot(i), 10) - parseInt(ot(t), 10);
}
function Rd(i, t) {
  const e = Sa(i, t);
  return e * e;
}
function Sa(i, t) {
  return Wm * i / t;
}
function Xm(i, t, e, n, s) {
  const r = e.getFill(), o = e.getStroke();
  if (r || o) {
    const l = i.getBuilder(e.getZIndex(), "Circle");
    l.setFillStrokeStyle(r, o), l.drawCircle(t, n);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || i).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, n);
  }
}
function jh(i, t, e, n, s, r, o) {
  let a = !1;
  const l = e.getImage();
  if (l) {
    const h = l.getImageState();
    h == It.LOADED || h == It.ERROR ? l.unlistenImageChange(s) : (h == It.IDLE && l.load(), l.listenImageChange(s), a = !0);
  }
  return Ym(
    i,
    t,
    e,
    n,
    r,
    o
  ), a;
}
function Ym(i, t, e, n, s, r) {
  const o = e.getGeometryFunction()(t);
  if (!o)
    return;
  const a = o.simplifyTransformed(
    n,
    s
  );
  if (e.getRenderer())
    bd(i, a, e, t);
  else {
    const h = Sd[a.getType()];
    h(
      i,
      a,
      e,
      t,
      r
    );
  }
}
function bd(i, t, e, n) {
  if (t.getType() == "GeometryCollection") {
    const r = t.getGeometries();
    for (let o = 0, a = r.length; o < a; ++o)
      bd(i, r[o], e, n);
    return;
  }
  i.getBuilder(e.getZIndex(), "Default").drawCustom(
    t,
    n,
    e.getRenderer(),
    e.getHitDetectionRenderer()
  );
}
function jm(i, t, e, n, s) {
  const r = t.getGeometriesArray();
  let o, a;
  for (o = 0, a = r.length; o < a; ++o) {
    const l = Sd[r[o].getType()];
    l(
      i,
      r[o],
      e,
      n,
      s
    );
  }
}
function Km(i, t, e, n, s) {
  const r = e.getStroke();
  if (r) {
    const a = i.getBuilder(
      e.getZIndex(),
      "LineString"
    );
    a.setFillStrokeStyle(null, r), a.drawLineString(t, n);
  }
  const o = e.getText();
  if (o && o.getText()) {
    const a = (s || i).getBuilder(
      e.getZIndex(),
      "Text"
    );
    a.setTextStyle(o), a.drawText(t, n);
  }
}
function qm(i, t, e, n, s) {
  const r = e.getStroke();
  if (r) {
    const a = i.getBuilder(
      e.getZIndex(),
      "LineString"
    );
    a.setFillStrokeStyle(null, r), a.drawMultiLineString(t, n);
  }
  const o = e.getText();
  if (o && o.getText()) {
    const a = (s || i).getBuilder(
      e.getZIndex(),
      "Text"
    );
    a.setTextStyle(o), a.drawText(t, n);
  }
}
function Jm(i, t, e, n, s) {
  const r = e.getFill(), o = e.getStroke();
  if (o || r) {
    const l = i.getBuilder(e.getZIndex(), "Polygon");
    l.setFillStrokeStyle(r, o), l.drawMultiPolygon(t, n);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || i).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, n);
  }
}
function Qm(i, t, e, n, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != It.LOADED)
      return;
    let l = i;
    if (s) {
      const c = r.getDeclutterMode();
      if (c !== "none")
        if (l = s, c === "obstacle") {
          const u = i.getBuilder(
            e.getZIndex(),
            "Image"
          );
          u.setImageStyle(r, a), u.drawPoint(t, n);
        } else
          o && o.getText() && (a = {});
    }
    const h = l.getBuilder(
      e.getZIndex(),
      "Image"
    );
    h.setImageStyle(r, a), h.drawPoint(t, n);
  }
  if (o && o.getText()) {
    let l = i;
    s && (l = s);
    const h = l.getBuilder(e.getZIndex(), "Text");
    h.setTextStyle(o, a), h.drawText(t, n);
  }
}
function t2(i, t, e, n, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != It.LOADED)
      return;
    let l = i;
    if (s) {
      const c = r.getDeclutterMode();
      if (c !== "none")
        if (l = s, c === "obstacle") {
          const u = i.getBuilder(
            e.getZIndex(),
            "Image"
          );
          u.setImageStyle(r, a), u.drawMultiPoint(t, n);
        } else
          o && o.getText() && (a = {});
    }
    const h = l.getBuilder(
      e.getZIndex(),
      "Image"
    );
    h.setImageStyle(r, a), h.drawMultiPoint(t, n);
  }
  if (o && o.getText()) {
    let l = i;
    s && (l = s);
    const h = l.getBuilder(e.getZIndex(), "Text");
    h.setTextStyle(o, a), h.drawText(t, n);
  }
}
function e2(i, t, e, n, s) {
  const r = e.getFill(), o = e.getStroke();
  if (r || o) {
    const l = i.getBuilder(e.getZIndex(), "Polygon");
    l.setFillStrokeStyle(r, o), l.drawPolygon(t, n);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || i).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, n);
  }
}
class i2 extends Ed {
  constructor(t) {
    super(t), this.boundHandleStyleImageChange_ = this.handleStyleImageChange_.bind(this), this.animatingOrInteracting_, this.hitDetectionImageData_ = null, this.renderedFeatures_ = null, this.renderedRevision_ = -1, this.renderedResolution_ = NaN, this.renderedExtent_ = fe(), this.wrappedRenderedExtent_ = fe(), this.renderedRotation_, this.renderedCenter_ = null, this.renderedProjection_ = null, this.renderedRenderOrder_ = null, this.replayGroup_ = null, this.replayGroupChanged = !0, this.declutterExecutorGroup = null, this.clipping = !0, this.compositionContext_ = null, this.opacity_ = 1;
  }
  renderWorlds(t, e, n) {
    const s = e.extent, r = e.viewState, o = r.center, a = r.resolution, l = r.projection, h = r.rotation, c = l.getExtent(), u = this.getLayer().getSource(), d = e.pixelRatio, f = e.viewHints, g = !(f[Zt.ANIMATING] || f[Zt.INTERACTING]), m = this.compositionContext_, p = Math.round(e.size[0] * d), _ = Math.round(e.size[1] * d), y = u.getWrapX() && l.canWrapX(), v = y ? mt(c) : null, x = y ? Math.ceil((s[2] - c[2]) / v) + 1 : 1;
    let C = y ? Math.floor((s[0] - c[0]) / v) : 0;
    do {
      const w = this.getRenderTransform(
        o,
        a,
        h,
        d,
        p,
        _,
        C * v
      );
      t.execute(
        m,
        1,
        w,
        h,
        g,
        void 0,
        n
      );
    } while (++C < x);
  }
  setupCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = ge(
        this.context.canvas.width,
        this.context.canvas.height,
        Wh
      );
      this.compositionContext_ = t;
    } else
      this.compositionContext_ = this.context;
  }
  releaseCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = this.context.globalAlpha;
      this.context.globalAlpha = this.opacity_, this.context.drawImage(this.compositionContext_.canvas, 0, 0), this.context.globalAlpha = t, $u(this.compositionContext_), Wh.push(this.compositionContext_.canvas), this.compositionContext_ = null;
    }
  }
  renderDeclutter(t) {
    this.declutterExecutorGroup && (this.setupCompositionContext_(), this.renderWorlds(
      this.declutterExecutorGroup,
      t,
      t.declutterTree
    ), this.releaseCompositionContext_());
  }
  renderFrame(t, e) {
    const n = t.pixelRatio, s = t.layerStatesArray[t.layerIndex];
    E0(this.pixelTransform, 1 / n, 1 / n), Ka(this.inversePixelTransform, this.pixelTransform);
    const r = Cu(this.pixelTransform);
    this.useContainer(e, r, this.getBackground(t));
    const o = this.context, a = o.canvas, l = this.replayGroup_, h = this.declutterExecutorGroup;
    if ((!l || l.isEmpty()) && (!h || h.isEmpty()))
      return null;
    const c = Math.round(t.size[0] * n), u = Math.round(t.size[1] * n);
    a.width != c || a.height != u ? (a.width = c, a.height = u, a.style.transform !== r && (a.style.transform = r)) : this.containerReused || o.clearRect(0, 0, c, u), this.preRender(o, t);
    const d = t.viewState;
    d.projection, this.opacity_ = s.opacity, this.setupCompositionContext_();
    let f = !1, g = !0;
    if (s.extent && this.clipping) {
      const m = Gi(s.extent);
      g = ie(m, t.extent), f = g && !yi(m, t.extent), f && this.clipUnrotated(this.compositionContext_, t, m);
    }
    return g && this.renderWorlds(l, t), f && this.compositionContext_.restore(), this.releaseCompositionContext_(), this.postRender(o, t), this.renderedRotation_ !== d.rotation && (this.renderedRotation_ = d.rotation, this.hitDetectionImageData_ = null), this.container;
  }
  getFeatures(t) {
    return new Promise(
      function(e) {
        if (!this.hitDetectionImageData_ && !this.animatingOrInteracting_) {
          const n = [this.context.canvas.width, this.context.canvas.height];
          Ft(this.pixelTransform, n);
          const s = this.renderedCenter_, r = this.renderedResolution_, o = this.renderedRotation_, a = this.renderedProjection_, l = this.wrappedRenderedExtent_, h = this.getLayer(), c = [], u = n[0] * Pe, d = n[1] * Pe;
          c.push(
            this.getRenderTransform(
              s,
              r,
              o,
              Pe,
              u,
              d,
              0
            ).slice()
          );
          const f = h.getSource(), g = a.getExtent();
          if (f.getWrapX() && a.canWrapX() && !yi(g, l)) {
            let m = l[0];
            const p = mt(g);
            let _ = 0, y;
            for (; m < g[0]; )
              --_, y = p * _, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  Pe,
                  u,
                  d,
                  y
                ).slice()
              ), m += p;
            for (_ = 0, m = l[2]; m > g[2]; )
              ++_, y = p * _, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  Pe,
                  u,
                  d,
                  y
                ).slice()
              ), m -= p;
          }
          this.hitDetectionImageData_ = Vm(
            n,
            c,
            this.renderedFeatures_,
            h.getStyleFunction(),
            l,
            r,
            o
          );
        }
        e(
          Um(t, this.renderedFeatures_, this.hitDetectionImageData_)
        );
      }.bind(this)
    );
  }
  forEachFeatureAtCoordinate(t, e, n, s, r) {
    if (!this.replayGroup_)
      return;
    const o = e.viewState.resolution, a = e.viewState.rotation, l = this.getLayer(), h = {}, c = function(f, g, m) {
      const p = ot(f), _ = h[p];
      if (_) {
        if (_ !== !0 && m < _.distanceSq) {
          if (m === 0)
            return h[p] = !0, r.splice(r.lastIndexOf(_), 1), s(f, l, g);
          _.geometry = g, _.distanceSq = m;
        }
      } else {
        if (m === 0)
          return h[p] = !0, s(f, l, g);
        r.push(
          h[p] = {
            feature: f,
            layer: l,
            geometry: g,
            distanceSq: m,
            callback: s
          }
        );
      }
    };
    let u;
    const d = [this.replayGroup_];
    return this.declutterExecutorGroup && d.push(this.declutterExecutorGroup), d.some((f) => u = f.forEachFeatureAtCoordinate(
      t,
      o,
      a,
      n,
      c,
      f === this.declutterExecutorGroup && e.declutterTree ? e.declutterTree.all().map((g) => g.value) : null
    )), u;
  }
  handleFontsChanged() {
    const t = this.getLayer();
    t.getVisible() && this.replayGroup_ && t.changed();
  }
  handleStyleImageChange_(t) {
    this.renderIfReadyAndVisible();
  }
  prepareFrame(t) {
    const e = this.getLayer(), n = e.getSource();
    if (!n)
      return !1;
    const s = t.viewHints[Zt.ANIMATING], r = t.viewHints[Zt.INTERACTING], o = e.getUpdateWhileAnimating(), a = e.getUpdateWhileInteracting();
    if (this.ready && !o && s || !a && r)
      return this.animatingOrInteracting_ = !0, !0;
    this.animatingOrInteracting_ = !1;
    const l = t.extent, h = t.viewState, c = h.projection, u = h.resolution, d = t.pixelRatio, f = e.getRevision(), g = e.getRenderBuffer();
    let m = e.getRenderOrder();
    m === void 0 && (m = Hm);
    const p = h.center.slice(), _ = co(
      l,
      g * u
    ), y = _.slice(), v = [_.slice()], x = c.getExtent();
    if (n.getWrapX() && c.canWrapX() && !yi(x, t.extent)) {
      const F = mt(x), k = Math.max(mt(_) / 2, F);
      _[0] = x[0] - k, _[2] = x[2] + k, Fu(p, c);
      const P = Lu(v[0], c);
      P[0] < x[0] && P[2] < x[2] ? v.push([
        P[0] + F,
        P[1],
        P[2] + F,
        P[3]
      ]) : P[0] > x[0] && P[2] > x[2] && v.push([
        P[0] - F,
        P[1],
        P[2] - F,
        P[3]
      ]);
    }
    if (this.ready && this.renderedResolution_ == u && this.renderedRevision_ == f && this.renderedRenderOrder_ == m && yi(this.wrappedRenderedExtent_, _))
      return nn(this.renderedExtent_, y) || (this.hitDetectionImageData_ = null, this.renderedExtent_ = y), this.renderedCenter_ = p, this.replayGroupChanged = !1, !0;
    this.replayGroup_ = null;
    const C = new Uh(
      Sa(u, d),
      _,
      u,
      d
    );
    let w;
    this.getLayer().getDeclutter() && (w = new Uh(
      Sa(u, d),
      _,
      u,
      d
    ));
    let S;
    for (let F = 0, k = v.length; F < k; ++F)
      n.loadFeatures(v[F], u, c);
    const b = Rd(u, d);
    let A = !0;
    const G = function(F) {
      let k;
      const P = F.getStyleFunction() || e.getStyleFunction();
      if (P && (k = P(F, u)), k) {
        const tt = this.renderFeature(
          F,
          b,
          k,
          C,
          S,
          w
        );
        A = A && !tt;
      }
    }.bind(this), V = ju(_), T = n.getFeaturesInExtent(V);
    m && T.sort(m);
    for (let F = 0, k = T.length; F < k; ++F)
      G(T[F]);
    this.renderedFeatures_ = T, this.ready = A;
    const $ = C.finish(), ft = new Yh(
      _,
      u,
      d,
      n.getOverlaps(),
      $,
      e.getRenderBuffer()
    );
    return w && (this.declutterExecutorGroup = new Yh(
      _,
      u,
      d,
      n.getOverlaps(),
      w.finish(),
      e.getRenderBuffer()
    )), this.renderedResolution_ = u, this.renderedRevision_ = f, this.renderedRenderOrder_ = m, this.renderedExtent_ = y, this.wrappedRenderedExtent_ = _, this.renderedCenter_ = p, this.renderedProjection_ = c, this.replayGroup_ = ft, this.hitDetectionImageData_ = null, this.replayGroupChanged = !0, !0;
  }
  renderFeature(t, e, n, s, r, o) {
    if (!n)
      return !1;
    let a = !1;
    if (Array.isArray(n))
      for (let l = 0, h = n.length; l < h; ++l)
        a = jh(
          s,
          t,
          n[l],
          e,
          this.boundHandleStyleImageChange_,
          r,
          o
        ) || a;
    else
      a = jh(
        s,
        t,
        n,
        e,
        this.boundHandleStyleImageChange_,
        r,
        o
      );
    return a;
  }
}
const n2 = i2;
class s2 extends vm {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new n2(this);
  }
}
const Ys = s2;
class r2 {
  constructor(t) {
    this.rbush_ = new xd(t), this.items_ = {};
  }
  insert(t, e) {
    const n = {
      minX: t[0],
      minY: t[1],
      maxX: t[2],
      maxY: t[3],
      value: e
    };
    this.rbush_.insert(n), this.items_[ot(e)] = n;
  }
  load(t, e) {
    const n = new Array(e.length);
    for (let s = 0, r = e.length; s < r; s++) {
      const o = t[s], a = e[s], l = {
        minX: o[0],
        minY: o[1],
        maxX: o[2],
        maxY: o[3],
        value: a
      };
      n[s] = l, this.items_[ot(a)] = l;
    }
    this.rbush_.load(n);
  }
  remove(t) {
    const e = ot(t), n = this.items_[e];
    return delete this.items_[e], this.rbush_.remove(n) !== null;
  }
  update(t, e) {
    const n = this.items_[ot(e)], s = [n.minX, n.minY, n.maxX, n.maxY];
    Es(s, t) || (this.remove(e), this.insert(t, e));
  }
  getAll() {
    return this.rbush_.all().map(function(e) {
      return e.value;
    });
  }
  getInExtent(t) {
    const e = {
      minX: t[0],
      minY: t[1],
      maxX: t[2],
      maxY: t[3]
    };
    return this.rbush_.search(e).map(function(s) {
      return s.value;
    });
  }
  forEach(t) {
    return this.forEach_(this.getAll(), t);
  }
  forEachInExtent(t, e) {
    return this.forEach_(this.getInExtent(t), e);
  }
  forEach_(t, e) {
    let n;
    for (let s = 0, r = t.length; s < r; s++)
      if (n = e(t[s]), n)
        return n;
    return n;
  }
  isEmpty() {
    return Gn(this.items_);
  }
  clear() {
    this.rbush_.clear(), this.items_ = {};
  }
  getExtent(t) {
    const e = this.rbush_.toJSON();
    return xe(e.minX, e.minY, e.maxX, e.maxY, t);
  }
  concat(t) {
    this.rbush_.load(t.rbush_.all());
    for (const e in t.items_)
      this.items_[e] = t.items_[e];
  }
}
const Kh = r2;
class o2 extends Ce {
  constructor(t) {
    super(), this.projection = J(t.projection), this.attributions_ = qh(t.attributions), this.attributionsCollapsible_ = t.attributionsCollapsible !== void 0 ? t.attributionsCollapsible : !0, this.loading = !1, this.state_ = t.state !== void 0 ? t.state : "ready", this.wrapX_ = t.wrapX !== void 0 ? t.wrapX : !1, this.interpolate_ = !!t.interpolate, this.viewResolver = null, this.viewRejector = null;
    const e = this;
    this.viewPromise_ = new Promise(function(n, s) {
      e.viewResolver = n, e.viewRejector = s;
    });
  }
  getAttributions() {
    return this.attributions_;
  }
  getAttributionsCollapsible() {
    return this.attributionsCollapsible_;
  }
  getProjection() {
    return this.projection;
  }
  getResolutions() {
    return W();
  }
  getView() {
    return this.viewPromise_;
  }
  getState() {
    return this.state_;
  }
  getWrapX() {
    return this.wrapX_;
  }
  getInterpolate() {
    return this.interpolate_;
  }
  refresh() {
    this.changed();
  }
  setAttributions(t) {
    this.attributions_ = qh(t), this.changed();
  }
  setState(t) {
    this.state_ = t, this.changed();
  }
}
function qh(i) {
  return i ? Array.isArray(i) ? function(t) {
    return i;
  } : typeof i == "function" ? i : function(t) {
    return [i];
  } : null;
}
const Ld = o2, we = {
  ADDFEATURE: "addfeature",
  CHANGEFEATURE: "changefeature",
  CLEAR: "clear",
  REMOVEFEATURE: "removefeature",
  FEATURESLOADSTART: "featuresloadstart",
  FEATURESLOADEND: "featuresloadend",
  FEATURESLOADERROR: "featuresloaderror"
};
function Td(i, t) {
  return [[-1 / 0, -1 / 0, 1 / 0, 1 / 0]];
}
function a2(i, t) {
  return [i];
}
let l2 = !1;
function h2(i, t, e, n, s, r, o) {
  const a = new XMLHttpRequest();
  a.open(
    "GET",
    typeof i == "function" ? i(e, n, s) : i,
    !0
  ), t.getType() == "arraybuffer" && (a.responseType = "arraybuffer"), a.withCredentials = l2, a.onload = function(l) {
    if (!a.status || a.status >= 200 && a.status < 300) {
      const h = t.getType();
      let c;
      h == "json" || h == "text" ? c = a.responseText : h == "xml" ? (c = a.responseXML, c || (c = new DOMParser().parseFromString(
        a.responseText,
        "application/xml"
      ))) : h == "arraybuffer" && (c = a.response), c ? r(
        t.readFeatures(c, {
          extent: e,
          featureProjection: s
        }),
        t.readProjection(c)
      ) : o();
    } else
      o();
  }, a.onerror = o, a.send();
}
function Jh(i, t) {
  return function(e, n, s, r, o) {
    const a = this;
    h2(
      i,
      t,
      e,
      n,
      s,
      function(l, h) {
        a.addFeatures(l), r !== void 0 && r(l);
      },
      o || ji
    );
  };
}
class fi extends Be {
  constructor(t, e, n) {
    super(t), this.feature = e, this.features = n;
  }
}
class c2 extends Ld {
  constructor(t) {
    t = t || {}, super({
      attributions: t.attributions,
      interpolate: !0,
      projection: void 0,
      state: "ready",
      wrapX: t.wrapX !== void 0 ? t.wrapX : !0
    }), this.on, this.once, this.un, this.loader_ = ji, this.format_ = t.format, this.overlaps_ = t.overlaps === void 0 ? !0 : t.overlaps, this.url_ = t.url, t.loader !== void 0 ? this.loader_ = t.loader : this.url_ !== void 0 && (Y(this.format_, 7), this.loader_ = Jh(
      this.url_,
      this.format_
    )), this.strategy_ = t.strategy !== void 0 ? t.strategy : Td;
    const e = t.useSpatialIndex !== void 0 ? t.useSpatialIndex : !0;
    this.featuresRtree_ = e ? new Kh() : null, this.loadedExtentsRtree_ = new Kh(), this.loadingExtentsCount_ = 0, this.nullGeometryFeatures_ = {}, this.idIndex_ = {}, this.uidIndex_ = {}, this.featureChangeKeys_ = {}, this.featuresCollection_ = null;
    let n, s;
    Array.isArray(t.features) ? s = t.features : t.features && (n = t.features, s = n.getArray()), !e && n === void 0 && (n = new Ae(s)), s !== void 0 && this.addFeaturesInternal(s), n !== void 0 && this.bindFeaturesCollection_(n);
  }
  addFeature(t) {
    this.addFeatureInternal(t), this.changed();
  }
  addFeatureInternal(t) {
    const e = ot(t);
    if (!this.addToIndex_(e, t)) {
      this.featuresCollection_ && this.featuresCollection_.remove(t);
      return;
    }
    this.setupChangeEvents_(e, t);
    const n = t.getGeometry();
    if (n) {
      const s = n.getExtent();
      this.featuresRtree_ && this.featuresRtree_.insert(s, t);
    } else
      this.nullGeometryFeatures_[e] = t;
    this.dispatchEvent(
      new fi(we.ADDFEATURE, t)
    );
  }
  setupChangeEvents_(t, e) {
    this.featureChangeKeys_[t] = [
      et(e, X.CHANGE, this.handleFeatureChange_, this),
      et(
        e,
        kn.PROPERTYCHANGE,
        this.handleFeatureChange_,
        this
      )
    ];
  }
  addToIndex_(t, e) {
    let n = !0;
    const s = e.getId();
    return s !== void 0 && (s.toString() in this.idIndex_ ? n = !1 : this.idIndex_[s.toString()] = e), n && (Y(!(t in this.uidIndex_), 30), this.uidIndex_[t] = e), n;
  }
  addFeatures(t) {
    this.addFeaturesInternal(t), this.changed();
  }
  addFeaturesInternal(t) {
    const e = [], n = [], s = [];
    for (let r = 0, o = t.length; r < o; r++) {
      const a = t[r], l = ot(a);
      this.addToIndex_(l, a) && n.push(a);
    }
    for (let r = 0, o = n.length; r < o; r++) {
      const a = n[r], l = ot(a);
      this.setupChangeEvents_(l, a);
      const h = a.getGeometry();
      if (h) {
        const c = h.getExtent();
        e.push(c), s.push(a);
      } else
        this.nullGeometryFeatures_[l] = a;
    }
    if (this.featuresRtree_ && this.featuresRtree_.load(e, s), this.hasListener(we.ADDFEATURE))
      for (let r = 0, o = n.length; r < o; r++)
        this.dispatchEvent(
          new fi(we.ADDFEATURE, n[r])
        );
  }
  bindFeaturesCollection_(t) {
    let e = !1;
    this.addEventListener(
      we.ADDFEATURE,
      function(n) {
        e || (e = !0, t.push(n.feature), e = !1);
      }
    ), this.addEventListener(
      we.REMOVEFEATURE,
      function(n) {
        e || (e = !0, t.remove(n.feature), e = !1);
      }
    ), t.addEventListener(
      ee.ADD,
      function(n) {
        e || (e = !0, this.addFeature(n.element), e = !1);
      }.bind(this)
    ), t.addEventListener(
      ee.REMOVE,
      function(n) {
        e || (e = !0, this.removeFeature(n.element), e = !1);
      }.bind(this)
    ), this.featuresCollection_ = t;
  }
  clear(t) {
    if (t) {
      for (const n in this.featureChangeKeys_)
        this.featureChangeKeys_[n].forEach(pt);
      this.featuresCollection_ || (this.featureChangeKeys_ = {}, this.idIndex_ = {}, this.uidIndex_ = {});
    } else if (this.featuresRtree_) {
      const n = function(s) {
        this.removeFeatureInternal(s);
      }.bind(this);
      this.featuresRtree_.forEach(n);
      for (const s in this.nullGeometryFeatures_)
        this.removeFeatureInternal(this.nullGeometryFeatures_[s]);
    }
    this.featuresCollection_ && this.featuresCollection_.clear(), this.featuresRtree_ && this.featuresRtree_.clear(), this.nullGeometryFeatures_ = {};
    const e = new fi(we.CLEAR);
    this.dispatchEvent(e), this.changed();
  }
  forEachFeature(t) {
    if (this.featuresRtree_)
      return this.featuresRtree_.forEach(t);
    this.featuresCollection_ && this.featuresCollection_.forEach(t);
  }
  forEachFeatureAtCoordinateDirect(t, e) {
    const n = [t[0], t[1], t[0], t[1]];
    return this.forEachFeatureInExtent(n, function(s) {
      if (s.getGeometry().intersectsCoordinate(t))
        return e(s);
    });
  }
  forEachFeatureInExtent(t, e) {
    if (this.featuresRtree_)
      return this.featuresRtree_.forEachInExtent(t, e);
    this.featuresCollection_ && this.featuresCollection_.forEach(e);
  }
  forEachFeatureIntersectingExtent(t, e) {
    return this.forEachFeatureInExtent(
      t,
      function(n) {
        if (n.getGeometry().intersectsExtent(t)) {
          const r = e(n);
          if (r)
            return r;
        }
      }
    );
  }
  getFeaturesCollection() {
    return this.featuresCollection_;
  }
  getFeatures() {
    let t;
    return this.featuresCollection_ ? t = this.featuresCollection_.getArray().slice(0) : this.featuresRtree_ && (t = this.featuresRtree_.getAll(), Gn(this.nullGeometryFeatures_) || Kt(t, Object.values(this.nullGeometryFeatures_))), t;
  }
  getFeaturesAtCoordinate(t) {
    const e = [];
    return this.forEachFeatureAtCoordinateDirect(t, function(n) {
      e.push(n);
    }), e;
  }
  getFeaturesInExtent(t, e) {
    if (this.featuresRtree_) {
      if (!(e && e.canWrapX() && this.getWrapX()))
        return this.featuresRtree_.getInExtent(t);
      const s = P0(t, e);
      return [].concat(
        ...s.map((r) => this.featuresRtree_.getInExtent(r))
      );
    } else
      return this.featuresCollection_ ? this.featuresCollection_.getArray().slice(0) : [];
  }
  getClosestFeatureToCoordinate(t, e) {
    const n = t[0], s = t[1];
    let r = null;
    const o = [NaN, NaN];
    let a = 1 / 0;
    const l = [-1 / 0, -1 / 0, 1 / 0, 1 / 0];
    return e = e || Ms, this.featuresRtree_.forEachInExtent(
      l,
      function(h) {
        if (e(h)) {
          const c = h.getGeometry(), u = a;
          if (a = c.closestPointXY(
            n,
            s,
            o,
            a
          ), a < u) {
            r = h;
            const d = Math.sqrt(a);
            l[0] = n - d, l[1] = s - d, l[2] = n + d, l[3] = s + d;
          }
        }
      }
    ), r;
  }
  getExtent(t) {
    return this.featuresRtree_.getExtent(t);
  }
  getFeatureById(t) {
    const e = this.idIndex_[t.toString()];
    return e !== void 0 ? e : null;
  }
  getFeatureByUid(t) {
    const e = this.uidIndex_[t];
    return e !== void 0 ? e : null;
  }
  getFormat() {
    return this.format_;
  }
  getOverlaps() {
    return this.overlaps_;
  }
  getUrl() {
    return this.url_;
  }
  handleFeatureChange_(t) {
    const e = t.target, n = ot(e), s = e.getGeometry();
    if (!s)
      n in this.nullGeometryFeatures_ || (this.featuresRtree_ && this.featuresRtree_.remove(e), this.nullGeometryFeatures_[n] = e);
    else {
      const o = s.getExtent();
      n in this.nullGeometryFeatures_ ? (delete this.nullGeometryFeatures_[n], this.featuresRtree_ && this.featuresRtree_.insert(o, e)) : this.featuresRtree_ && this.featuresRtree_.update(o, e);
    }
    const r = e.getId();
    if (r !== void 0) {
      const o = r.toString();
      this.idIndex_[o] !== e && (this.removeFromIdIndex_(e), this.idIndex_[o] = e);
    } else
      this.removeFromIdIndex_(e), this.uidIndex_[n] = e;
    this.changed(), this.dispatchEvent(
      new fi(we.CHANGEFEATURE, e)
    );
  }
  hasFeature(t) {
    const e = t.getId();
    return e !== void 0 ? e in this.idIndex_ : ot(t) in this.uidIndex_;
  }
  isEmpty() {
    return this.featuresRtree_ ? this.featuresRtree_.isEmpty() && Gn(this.nullGeometryFeatures_) : this.featuresCollection_ ? this.featuresCollection_.getLength() === 0 : !0;
  }
  loadFeatures(t, e, n) {
    const s = this.loadedExtentsRtree_, r = this.strategy_(t, e, n);
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      s.forEachInExtent(
        l,
        function(c) {
          return yi(c.extent, l);
        }
      ) || (++this.loadingExtentsCount_, this.dispatchEvent(
        new fi(we.FEATURESLOADSTART)
      ), this.loader_.call(
        this,
        l,
        e,
        n,
        function(c) {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new fi(
              we.FEATURESLOADEND,
              void 0,
              c
            )
          );
        }.bind(this),
        function() {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new fi(we.FEATURESLOADERROR)
          );
        }.bind(this)
      ), s.insert(l, { extent: l.slice() }));
    }
    this.loading = this.loader_.length < 4 ? !1 : this.loadingExtentsCount_ > 0;
  }
  refresh() {
    this.clear(!0), this.loadedExtentsRtree_.clear(), super.refresh();
  }
  removeLoadedExtent(t) {
    const e = this.loadedExtentsRtree_;
    let n;
    e.forEachInExtent(t, function(s) {
      if (Es(s.extent, t))
        return n = s, !0;
    }), n && e.remove(n);
  }
  removeFeature(t) {
    if (!t)
      return;
    const e = ot(t);
    e in this.nullGeometryFeatures_ ? delete this.nullGeometryFeatures_[e] : this.featuresRtree_ && this.featuresRtree_.remove(t), this.removeFeatureInternal(t) && this.changed();
  }
  removeFeatureInternal(t) {
    const e = ot(t), n = this.featureChangeKeys_[e];
    if (!n)
      return;
    n.forEach(pt), delete this.featureChangeKeys_[e];
    const s = t.getId();
    return s !== void 0 && delete this.idIndex_[s.toString()], delete this.uidIndex_[e], this.dispatchEvent(
      new fi(we.REMOVEFEATURE, t)
    ), t;
  }
  removeFromIdIndex_(t) {
    let e = !1;
    for (const n in this.idIndex_)
      if (this.idIndex_[n] === t) {
        delete this.idIndex_[n], e = !0;
        break;
      }
    return e;
  }
  setLoader(t) {
    this.loader_ = t;
  }
  setUrl(t) {
    Y(this.format_, 7), this.url_ = t, this.setLoader(Jh(t, this.format_));
  }
}
const Kn = c2;
function u2(i) {
  if (!(i.context instanceof CanvasRenderingContext2D))
    throw new Error("Only works for render events from Canvas 2D layers");
  const t = i.inversePixelTransform[0], e = i.frameState, n = x0(
    i.inversePixelTransform.slice(),
    e.coordinateToPixelTransform
  ), s = Rd(
    e.viewState.resolution,
    t
  );
  let r;
  return new wd(
    i.context,
    t,
    e.extent,
    n,
    e.viewState.rotation,
    s,
    r
  );
}
class d2 extends lo {
  constructor(t, e, n) {
    super(), n = n || {}, this.tileCoord = t, this.state = e, this.interimTile = null, this.key = "", this.transition_ = n.transition === void 0 ? 250 : n.transition, this.transitionStarts_ = {}, this.interpolate = !!n.interpolate;
  }
  changed() {
    this.dispatchEvent(X.CHANGE);
  }
  release() {
    this.state === z.ERROR && this.setState(z.EMPTY);
  }
  getKey() {
    return this.key + "/" + this.tileCoord;
  }
  getInterimTile() {
    if (!this.interimTile)
      return this;
    let t = this.interimTile;
    do {
      if (t.getState() == z.LOADED)
        return this.transition_ = 0, t;
      t = t.interimTile;
    } while (t);
    return this;
  }
  refreshInterimChain() {
    if (!this.interimTile)
      return;
    let t = this.interimTile, e = this;
    do {
      if (t.getState() == z.LOADED) {
        t.interimTile = null;
        break;
      } else
        t.getState() == z.LOADING ? e = t : t.getState() == z.IDLE ? e.interimTile = t.interimTile : e = t;
      t = e.interimTile;
    } while (t);
  }
  getTileCoord() {
    return this.tileCoord;
  }
  getState() {
    return this.state;
  }
  setState(t) {
    if (this.state !== z.ERROR && this.state > t)
      throw new Error("Tile load sequence violation");
    this.state = t, this.changed();
  }
  load() {
    W();
  }
  getAlpha(t, e) {
    if (!this.transition_)
      return 1;
    let n = this.transitionStarts_[t];
    if (!n)
      n = e, this.transitionStarts_[t] = n;
    else if (n === -1)
      return 1;
    const s = e - n + 1e3 / 60;
    return s >= this.transition_ ? 1 : Ku(s / this.transition_);
  }
  inTransition(t) {
    return this.transition_ ? this.transitionStarts_[t] !== -1 : !1;
  }
  endTransition(t) {
    this.transition_ && (this.transitionStarts_[t] = -1);
  }
}
const Id = d2;
class f2 extends Id {
  constructor(t, e, n, s, r, o) {
    super(t, e, o), this.crossOrigin_ = s, this.src_ = n, this.key = n, this.image_ = new Image(), s !== null && (this.image_.crossOrigin = s), this.unlisten_ = null, this.tileLoadFunction_ = r;
  }
  getImage() {
    return this.image_;
  }
  setImage(t) {
    this.image_ = t, this.state = z.LOADED, this.unlistenImage_(), this.changed();
  }
  handleImageError_() {
    this.state = z.ERROR, this.unlistenImage_(), this.image_ = g2(), this.changed();
  }
  handleImageLoad_() {
    const t = this.image_;
    t.naturalWidth && t.naturalHeight ? this.state = z.LOADED : this.state = z.EMPTY, this.unlistenImage_(), this.changed();
  }
  load() {
    this.state == z.ERROR && (this.state = z.IDLE, this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_)), this.state == z.IDLE && (this.state = z.LOADING, this.changed(), this.tileLoadFunction_(this, this.src_), this.unlisten_ = Cd(
      this.image_,
      this.handleImageLoad_.bind(this),
      this.handleImageError_.bind(this)
    ));
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function g2() {
  const i = ge(1, 1);
  return i.fillStyle = "rgba(0,0,0,0)", i.fillRect(0, 0, 1, 1), i.canvas;
}
const Pd = f2, zt = {
  ELEMENT: "element",
  MAP: "map",
  OFFSET: "offset",
  POSITION: "position",
  POSITIONING: "positioning"
};
class m2 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, this.options = t, this.id = t.id, this.insertFirst = t.insertFirst !== void 0 ? t.insertFirst : !0, this.stopEvent = t.stopEvent !== void 0 ? t.stopEvent : !0, this.element = document.createElement("div"), this.element.className = t.className !== void 0 ? t.className : "ol-overlay-container " + H0, this.element.style.position = "absolute", this.element.style.pointerEvents = "auto", this.autoPan = t.autoPan === !0 ? {} : t.autoPan || void 0, this.rendered = {
      transform_: "",
      visible: !0
    }, this.mapPostrenderListenerKey = null, this.addChangeListener(zt.ELEMENT, this.handleElementChanged), this.addChangeListener(zt.MAP, this.handleMapChanged), this.addChangeListener(zt.OFFSET, this.handleOffsetChanged), this.addChangeListener(zt.POSITION, this.handlePositionChanged), this.addChangeListener(zt.POSITIONING, this.handlePositioningChanged), t.element !== void 0 && this.setElement(t.element), this.setOffset(t.offset !== void 0 ? t.offset : [0, 0]), this.setPositioning(t.positioning || "top-left"), t.position !== void 0 && this.setPosition(t.position);
  }
  getElement() {
    return this.get(zt.ELEMENT);
  }
  getId() {
    return this.id;
  }
  getMap() {
    return this.get(zt.MAP) || null;
  }
  getOffset() {
    return this.get(zt.OFFSET);
  }
  getPosition() {
    return this.get(zt.POSITION);
  }
  getPositioning() {
    return this.get(zt.POSITIONING);
  }
  handleElementChanged() {
    Bu(this.element);
    const t = this.getElement();
    t && this.element.appendChild(t);
  }
  handleMapChanged() {
    this.mapPostrenderListenerKey && (zr(this.element), pt(this.mapPostrenderListenerKey), this.mapPostrenderListenerKey = null);
    const t = this.getMap();
    if (t) {
      this.mapPostrenderListenerKey = et(
        t,
        qe.POSTRENDER,
        this.render,
        this
      ), this.updatePixelPosition();
      const e = this.stopEvent ? t.getOverlayContainerStopEvent() : t.getOverlayContainer();
      this.insertFirst ? e.insertBefore(this.element, e.childNodes[0] || null) : e.appendChild(this.element), this.performAutoPan();
    }
  }
  render() {
    this.updatePixelPosition();
  }
  handleOffsetChanged() {
    this.updatePixelPosition();
  }
  handlePositionChanged() {
    this.updatePixelPosition(), this.performAutoPan();
  }
  handlePositioningChanged() {
    this.updatePixelPosition();
  }
  setElement(t) {
    this.set(zt.ELEMENT, t);
  }
  setMap(t) {
    this.set(zt.MAP, t);
  }
  setOffset(t) {
    this.set(zt.OFFSET, t);
  }
  setPosition(t) {
    this.set(zt.POSITION, t);
  }
  performAutoPan() {
    this.autoPan && this.panIntoView(this.autoPan);
  }
  panIntoView(t) {
    const e = this.getMap();
    if (!e || !e.getTargetElement() || !this.get(zt.POSITION))
      return;
    const n = this.getRect(e.getTargetElement(), e.getSize()), s = this.getElement(), r = this.getRect(s, [
      Y0(s),
      j0(s)
    ]);
    t = t || {};
    const o = t.margin === void 0 ? 20 : t.margin;
    if (!yi(n, r)) {
      const a = r[0] - n[0], l = n[2] - r[2], h = r[1] - n[1], c = n[3] - r[3], u = [0, 0];
      if (a < 0 ? u[0] = a - o : l < 0 && (u[0] = Math.abs(l) + o), h < 0 ? u[1] = h - o : c < 0 && (u[1] = Math.abs(c) + o), u[0] !== 0 || u[1] !== 0) {
        const d = e.getView().getCenterInternal(), f = e.getPixelFromCoordinateInternal(d);
        if (!f)
          return;
        const g = [f[0] + u[0], f[1] + u[1]], m = t.animation || {};
        e.getView().animateInternal({
          center: e.getCoordinateFromPixelInternal(g),
          duration: m.duration,
          easing: m.easing
        });
      }
    }
  }
  getRect(t, e) {
    const n = t.getBoundingClientRect(), s = n.left + window.pageXOffset, r = n.top + window.pageYOffset;
    return [s, r, s + e[0], r + e[1]];
  }
  setPositioning(t) {
    this.set(zt.POSITIONING, t);
  }
  setVisible(t) {
    this.rendered.visible !== t && (this.element.style.display = t ? "" : "none", this.rendered.visible = t);
  }
  updatePixelPosition() {
    const t = this.getMap(), e = this.getPosition();
    if (!t || !t.isRendered() || !e) {
      this.setVisible(!1);
      return;
    }
    const n = t.getPixelFromCoordinate(e), s = t.getSize();
    this.updateRenderedPosition(n, s);
  }
  updateRenderedPosition(t, e) {
    const n = this.element.style, s = this.getOffset(), r = this.getPositioning();
    this.setVisible(!0);
    const o = Math.round(t[0] + s[0]) + "px", a = Math.round(t[1] + s[1]) + "px";
    let l = "0%", h = "0%";
    r == "bottom-right" || r == "center-right" || r == "top-right" ? l = "-100%" : (r == "bottom-center" || r == "center-center" || r == "top-center") && (l = "-50%"), r == "bottom-left" || r == "bottom-center" || r == "bottom-right" ? h = "-100%" : (r == "center-left" || r == "center-center" || r == "center-right") && (h = "-50%");
    const c = `translate(${l}, ${h}) translate(${o}, ${a})`;
    this.rendered.transform_ != c && (this.rendered.transform_ = c, n.transform = c);
  }
  getOptions() {
    return this.options;
  }
}
const p2 = m2;
class _2 {
  constructor(t) {
    this.highWaterMark = t !== void 0 ? t : 2048, this.count_ = 0, this.entries_ = {}, this.oldest_ = null, this.newest_ = null;
  }
  canExpireCache() {
    return this.highWaterMark > 0 && this.getCount() > this.highWaterMark;
  }
  expireCache(t) {
    for (; this.canExpireCache(); )
      this.pop();
  }
  clear() {
    this.count_ = 0, this.entries_ = {}, this.oldest_ = null, this.newest_ = null;
  }
  containsKey(t) {
    return this.entries_.hasOwnProperty(t);
  }
  forEach(t) {
    let e = this.oldest_;
    for (; e; )
      t(e.value_, e.key_, this), e = e.newer;
  }
  get(t, e) {
    const n = this.entries_[t];
    return Y(n !== void 0, 15), n === this.newest_ || (n === this.oldest_ ? (this.oldest_ = this.oldest_.newer, this.oldest_.older = null) : (n.newer.older = n.older, n.older.newer = n.newer), n.newer = null, n.older = this.newest_, this.newest_.newer = n, this.newest_ = n), n.value_;
  }
  remove(t) {
    const e = this.entries_[t];
    return Y(e !== void 0, 15), e === this.newest_ ? (this.newest_ = e.older, this.newest_ && (this.newest_.newer = null)) : e === this.oldest_ ? (this.oldest_ = e.newer, this.oldest_ && (this.oldest_.older = null)) : (e.newer.older = e.older, e.older.newer = e.newer), delete this.entries_[t], --this.count_, e.value_;
  }
  getCount() {
    return this.count_;
  }
  getKeys() {
    const t = new Array(this.count_);
    let e = 0, n;
    for (n = this.newest_; n; n = n.older)
      t[e++] = n.key_;
    return t;
  }
  getValues() {
    const t = new Array(this.count_);
    let e = 0, n;
    for (n = this.newest_; n; n = n.older)
      t[e++] = n.value_;
    return t;
  }
  peekLast() {
    return this.oldest_.value_;
  }
  peekLastKey() {
    return this.oldest_.key_;
  }
  peekFirstKey() {
    return this.newest_.key_;
  }
  peek(t) {
    if (!!this.containsKey(t))
      return this.entries_[t].value_;
  }
  pop() {
    const t = this.oldest_;
    return delete this.entries_[t.key_], t.newer && (t.newer.older = null), this.oldest_ = t.newer, this.oldest_ || (this.newest_ = null), --this.count_, t.value_;
  }
  replace(t, e) {
    this.get(t), this.entries_[t].value_ = e;
  }
  set(t, e) {
    Y(!(t in this.entries_), 16);
    const n = {
      key_: t,
      newer: null,
      older: this.newest_,
      value_: e
    };
    this.newest_ ? this.newest_.newer = n : this.oldest_ = n, this.newest_ = n, this.entries_[t] = n, ++this.count_;
  }
  setSize(t) {
    this.highWaterMark = t;
  }
}
const y2 = _2;
function Qh(i, t, e, n) {
  return n !== void 0 ? (n[0] = i, n[1] = t, n[2] = e, n) : [i, t, e];
}
function Eo(i, t, e) {
  return i + "/" + t + "/" + e;
}
function Ad(i) {
  return Eo(i[0], i[1], i[2]);
}
function v2(i) {
  return i.split("/").map(Number);
}
function x2(i) {
  return (i[1] << i[0]) + i[2];
}
function C2(i, t) {
  const e = i[0], n = i[1], s = i[2];
  if (t.getMinZoom() > e || e > t.getMaxZoom())
    return !1;
  const r = t.getFullTileRange(e);
  return r ? r.containsXY(n, s) : !0;
}
class M2 extends y2 {
  clear() {
    for (; this.getCount() > 0; )
      this.pop().release();
    super.clear();
  }
  expireCache(t) {
    for (; this.canExpireCache() && !(this.peekLast().getKey() in t); )
      this.pop().release();
  }
  pruneExceptNewestZ() {
    if (this.getCount() === 0)
      return;
    const t = this.peekFirstKey(), n = v2(t)[0];
    this.forEach(
      function(s) {
        s.tileCoord[0] !== n && (this.remove(Ad(s.tileCoord)), s.release());
      }.bind(this)
    );
  }
}
const Od = M2;
class Nd {
  constructor(t, e, n, s) {
    this.minX = t, this.maxX = e, this.minY = n, this.maxY = s;
  }
  contains(t) {
    return this.containsXY(t[1], t[2]);
  }
  containsTileRange(t) {
    return this.minX <= t.minX && t.maxX <= this.maxX && this.minY <= t.minY && t.maxY <= this.maxY;
  }
  containsXY(t, e) {
    return this.minX <= t && t <= this.maxX && this.minY <= e && e <= this.maxY;
  }
  equals(t) {
    return this.minX == t.minX && this.minY == t.minY && this.maxX == t.maxX && this.maxY == t.maxY;
  }
  extend(t) {
    t.minX < this.minX && (this.minX = t.minX), t.maxX > this.maxX && (this.maxX = t.maxX), t.minY < this.minY && (this.minY = t.minY), t.maxY > this.maxY && (this.maxY = t.maxY);
  }
  getHeight() {
    return this.maxY - this.minY + 1;
  }
  getSize() {
    return [this.getWidth(), this.getHeight()];
  }
  getWidth() {
    return this.maxX - this.minX + 1;
  }
  intersects(t) {
    return this.minX <= t.maxX && this.maxX >= t.minX && this.minY <= t.maxY && this.maxY >= t.minY;
  }
}
function _n(i, t, e, n, s) {
  return s !== void 0 ? (s.minX = i, s.maxX = t, s.minY = e, s.maxY = n, s) : new Nd(i, t, e, n);
}
const Fd = Nd, tc = [
  "fullscreenchange",
  "webkitfullscreenchange",
  "MSFullscreenChange"
], ec = {
  ENTERFULLSCREEN: "enterfullscreen",
  LEAVEFULLSCREEN: "leavefullscreen"
};
class E2 extends kt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      target: t.target
    }), this.on, this.once, this.un, this.keys_ = t.keys !== void 0 ? t.keys : !1, this.source_ = t.source, this.isInFullscreen_ = !1, this.boundHandleMapTargetChange_ = this.handleMapTargetChange_.bind(this), this.cssClassName_ = t.className !== void 0 ? t.className : "ol-full-screen", this.documentListeners_ = [], this.activeClassName_ = t.activeClassName !== void 0 ? t.activeClassName.split(" ") : [this.cssClassName_ + "-true"], this.inactiveClassName_ = t.inactiveClassName !== void 0 ? t.inactiveClassName.split(" ") : [this.cssClassName_ + "-false"];
    const e = t.label !== void 0 ? t.label : "\u2922";
    this.labelNode_ = typeof e == "string" ? document.createTextNode(e) : e;
    const n = t.labelActive !== void 0 ? t.labelActive : "\xD7";
    this.labelActiveNode_ = typeof n == "string" ? document.createTextNode(n) : n;
    const s = t.tipLabel ? t.tipLabel : "Toggle full-screen";
    this.button_ = document.createElement("button"), this.button_.title = s, this.button_.setAttribute("type", "button"), this.button_.appendChild(this.labelNode_), this.button_.addEventListener(
      X.CLICK,
      this.handleClick_.bind(this),
      !1
    ), this.setClassName_(this.button_, this.isInFullscreen_), this.element.className = `${this.cssClassName_} ${Yn} ${_o}`, this.element.appendChild(this.button_);
  }
  handleClick_(t) {
    t.preventDefault(), this.handleFullScreen_();
  }
  handleFullScreen_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = t.getOwnerDocument();
    if (!!ic(e))
      if (nc(e))
        S2(e);
      else {
        let n;
        this.source_ ? n = typeof this.source_ == "string" ? e.getElementById(this.source_) : this.source_ : n = t.getTargetElement(), this.keys_ ? w2(n) : Dd(n);
      }
  }
  handleFullScreenChange_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = this.isInFullscreen_;
    this.isInFullscreen_ = nc(t.getOwnerDocument()), e !== this.isInFullscreen_ && (this.setClassName_(this.button_, this.isInFullscreen_), this.isInFullscreen_ ? (Br(this.labelActiveNode_, this.labelNode_), this.dispatchEvent(ec.ENTERFULLSCREEN)) : (Br(this.labelNode_, this.labelActiveNode_), this.dispatchEvent(ec.LEAVEFULLSCREEN)), t.updateSize());
  }
  setClassName_(t, e) {
    e ? (t.classList.remove(...this.inactiveClassName_), t.classList.add(...this.activeClassName_)) : (t.classList.remove(...this.activeClassName_), t.classList.add(...this.inactiveClassName_));
  }
  setMap(t) {
    const e = this.getMap();
    e && e.removeChangeListener(
      Ot.TARGET,
      this.boundHandleMapTargetChange_
    ), super.setMap(t), this.handleMapTargetChange_(), t && t.addChangeListener(
      Ot.TARGET,
      this.boundHandleMapTargetChange_
    );
  }
  handleMapTargetChange_() {
    const t = this.documentListeners_;
    for (let n = 0, s = t.length; n < s; ++n)
      pt(t[n]);
    t.length = 0;
    const e = this.getMap();
    if (e) {
      const n = e.getOwnerDocument();
      ic(n) ? this.element.classList.remove(yh) : this.element.classList.add(yh);
      for (let s = 0, r = tc.length; s < r; ++s)
        t.push(
          et(n, tc[s], this.handleFullScreenChange_, this)
        );
      this.handleFullScreenChange_();
    }
  }
}
function ic(i) {
  const t = i.body;
  return !!(t.webkitRequestFullscreen || t.requestFullscreen && i.fullscreenEnabled);
}
function nc(i) {
  return !!(i.webkitIsFullScreen || i.fullscreenElement);
}
function Dd(i) {
  i.requestFullscreen ? i.requestFullscreen() : i.webkitRequestFullscreen && i.webkitRequestFullscreen();
}
function w2(i) {
  i.webkitRequestFullscreen ? i.webkitRequestFullscreen() : Dd(i);
}
function S2(i) {
  i.exitFullscreen ? i.exitFullscreen() : i.webkitExitFullscreen && i.webkitExitFullscreen();
}
const R2 = E2, Jo = "units", b2 = [1, 2, 5], as = 25.4 / 0.28;
class L2 extends kt {
  constructor(t) {
    t = t || {};
    const e = document.createElement("div");
    e.style.pointerEvents = "none", super({
      element: e,
      render: t.render,
      target: t.target
    }), this.on, this.once, this.un;
    const n = t.className !== void 0 ? t.className : t.bar ? "ol-scale-bar" : "ol-scale-line";
    this.innerElement_ = document.createElement("div"), this.innerElement_.className = n + "-inner", this.element.className = n + " " + Yn, this.element.appendChild(this.innerElement_), this.viewState_ = null, this.minWidth_ = t.minWidth !== void 0 ? t.minWidth : 64, this.maxWidth_ = t.maxWidth, this.renderedVisible_ = !1, this.renderedWidth_ = void 0, this.renderedHTML_ = "", this.addChangeListener(Jo, this.handleUnitsChanged_), this.setUnits(t.units || "metric"), this.scaleBar_ = t.bar || !1, this.scaleBarSteps_ = t.steps || 4, this.scaleBarText_ = t.text || !1, this.dpi_ = t.dpi || void 0;
  }
  getUnits() {
    return this.get(Jo);
  }
  handleUnitsChanged_() {
    this.updateElement_();
  }
  setUnits(t) {
    this.set(Jo, t);
  }
  setDpi(t) {
    this.dpi_ = t;
  }
  updateElement_() {
    const t = this.viewState_;
    if (!t) {
      this.renderedVisible_ && (this.element.style.display = "none", this.renderedVisible_ = !1);
      return;
    }
    const e = t.center, n = t.projection, s = this.getUnits(), r = s == "degrees" ? "degrees" : "m";
    let o = Hr(
      n,
      t.resolution,
      e,
      r
    );
    const a = this.minWidth_ * (this.dpi_ || as) / as, l = this.maxWidth_ !== void 0 ? this.maxWidth_ * (this.dpi_ || as) / as : void 0;
    let h = a * o, c = "";
    if (s == "degrees") {
      const v = Bn.degrees;
      h *= v, h < v / 60 ? (c = "\u2033", o *= 3600) : h < v ? (c = "\u2032", o *= 60) : c = "\xB0";
    } else
      s == "imperial" ? h < 0.9144 ? (c = "in", o /= 0.0254) : h < 1609.344 ? (c = "ft", o /= 0.3048) : (c = "mi", o /= 1609.344) : s == "nautical" ? (o /= 1852, c = "NM") : s == "metric" ? h < 1e-3 ? (c = "\u03BCm", o *= 1e6) : h < 1 ? (c = "mm", o *= 1e3) : h < 1e3 ? c = "m" : (c = "km", o /= 1e3) : s == "us" ? h < 0.9144 ? (c = "in", o *= 39.37) : h < 1609.344 ? (c = "ft", o /= 0.30480061) : (c = "mi", o /= 1609.3472) : Y(!1, 33);
    let u = 3 * Math.floor(Math.log(a * o) / Math.log(10)), d, f, g, m, p, _;
    for (; ; ) {
      g = Math.floor(u / 3);
      const v = Math.pow(10, g);
      if (d = b2[(u % 3 + 3) % 3] * v, f = Math.round(d / o), isNaN(f)) {
        this.element.style.display = "none", this.renderedVisible_ = !1;
        return;
      }
      if (l !== void 0 && f >= l) {
        d = m, f = p, g = _;
        break;
      } else if (f >= a)
        break;
      m = d, p = f, _ = g, ++u;
    }
    const y = this.scaleBar_ ? this.createScaleBar(f, d, c) : d.toFixed(g < 0 ? -g : 0) + " " + c;
    this.renderedHTML_ != y && (this.innerElement_.innerHTML = y, this.renderedHTML_ = y), this.renderedWidth_ != f && (this.innerElement_.style.width = f + "px", this.renderedWidth_ = f), this.renderedVisible_ || (this.element.style.display = "", this.renderedVisible_ = !0);
  }
  createScaleBar(t, e, n) {
    const s = this.getScaleForResolution(), r = s < 1 ? Math.round(1 / s).toLocaleString() + " : 1" : "1 : " + Math.round(s).toLocaleString(), o = this.scaleBarSteps_, a = t / o, l = [this.createMarker("absolute")];
    for (let c = 0; c < o; ++c) {
      const u = c % 2 === 0 ? "ol-scale-singlebar-odd" : "ol-scale-singlebar-even";
      l.push(
        `<div><div class="ol-scale-singlebar ${u}" style="width: ${a}px;"></div>` + this.createMarker("relative") + (c % 2 === 0 || o === 2 ? this.createStepText(c, t, !1, e, n) : "") + "</div>"
      );
    }
    return l.push(this.createStepText(o, t, !0, e, n)), (this.scaleBarText_ ? `<div class="ol-scale-text" style="width: ${t}px;">` + r + "</div>" : "") + l.join("");
  }
  createMarker(t) {
    return `<div class="ol-scale-step-marker" style="position: ${t}; top: ${t === "absolute" ? 3 : -10}px;"></div>`;
  }
  createStepText(t, e, n, s, r) {
    const a = (t === 0 ? 0 : Math.round(s / this.scaleBarSteps_ * t * 100) / 100) + (t === 0 ? "" : " " + r), l = t === 0 ? -3 : e / this.scaleBarSteps_ * -1, h = t === 0 ? 0 : e / this.scaleBarSteps_ * 2;
    return `<div class="ol-scale-step-text" style="margin-left: ${l}px;text-align: ${t === 0 ? "left" : "center"};min-width: ${h}px;left: ${n ? e + "px" : "unset"};">` + a + "</div>";
  }
  getScaleForResolution() {
    const t = Hr(
      this.viewState_.projection,
      this.viewState_.resolution,
      this.viewState_.center,
      "m"
    ), e = this.dpi_ || as, n = 1e3 / 25.4;
    return t * n * e;
  }
  render(t) {
    const e = t.frameState;
    e ? this.viewState_ = e.viewState : this.viewState_ = null, this.updateElement_();
  }
}
const T2 = L2, I2 = 0.5, P2 = 10, sc = 0.25;
class A2 {
  constructor(t, e, n, s, r, o) {
    this.sourceProj_ = t, this.targetProj_ = e;
    let a = {};
    const l = Is(this.targetProj_, this.sourceProj_);
    this.transformInv_ = function(y) {
      const v = y[0] + "/" + y[1];
      return a[v] || (a[v] = l(y)), a[v];
    }, this.maxSourceExtent_ = s, this.errorThresholdSquared_ = r * r, this.triangles_ = [], this.wrapsXInSource_ = !1, this.canWrapXInSource_ = this.sourceProj_.canWrapX() && !!s && !!this.sourceProj_.getExtent() && mt(s) == mt(this.sourceProj_.getExtent()), this.sourceWorldWidth_ = this.sourceProj_.getExtent() ? mt(this.sourceProj_.getExtent()) : null, this.targetWorldWidth_ = this.targetProj_.getExtent() ? mt(this.targetProj_.getExtent()) : null;
    const h = Ii(n), c = mo(n), u = go(n), d = fo(n), f = this.transformInv_(h), g = this.transformInv_(c), m = this.transformInv_(u), p = this.transformInv_(d), _ = P2 + (o ? Math.max(
      0,
      Math.ceil(
        Math.log2(
          ha(n) / (o * o * 256 * 256)
        )
      )
    ) : 0);
    if (this.addQuad_(
      h,
      c,
      u,
      d,
      f,
      g,
      m,
      p,
      _
    ), this.wrapsXInSource_) {
      let y = 1 / 0;
      this.triangles_.forEach(function(v, x, C) {
        y = Math.min(
          y,
          v.source[0][0],
          v.source[1][0],
          v.source[2][0]
        );
      }), this.triangles_.forEach(
        function(v) {
          if (Math.max(
            v.source[0][0],
            v.source[1][0],
            v.source[2][0]
          ) - y > this.sourceWorldWidth_ / 2) {
            const x = [
              [v.source[0][0], v.source[0][1]],
              [v.source[1][0], v.source[1][1]],
              [v.source[2][0], v.source[2][1]]
            ];
            x[0][0] - y > this.sourceWorldWidth_ / 2 && (x[0][0] -= this.sourceWorldWidth_), x[1][0] - y > this.sourceWorldWidth_ / 2 && (x[1][0] -= this.sourceWorldWidth_), x[2][0] - y > this.sourceWorldWidth_ / 2 && (x[2][0] -= this.sourceWorldWidth_);
            const C = Math.min(
              x[0][0],
              x[1][0],
              x[2][0]
            );
            Math.max(
              x[0][0],
              x[1][0],
              x[2][0]
            ) - C < this.sourceWorldWidth_ / 2 && (v.source = x);
          }
        }.bind(this)
      );
    }
    a = {};
  }
  addTriangle_(t, e, n, s, r, o) {
    this.triangles_.push({
      source: [s, r, o],
      target: [t, e, n]
    });
  }
  addQuad_(t, e, n, s, r, o, a, l, h) {
    const c = aa([r, o, a, l]), u = this.sourceWorldWidth_ ? mt(c) / this.sourceWorldWidth_ : null, d = this.sourceWorldWidth_, f = this.sourceProj_.canWrapX() && u > 0.5 && u < 1;
    let g = !1;
    if (h > 0) {
      if (this.targetProj_.isGlobal() && this.targetWorldWidth_) {
        const p = aa([t, e, n, s]);
        g = mt(p) / this.targetWorldWidth_ > sc || g;
      }
      !f && this.sourceProj_.isGlobal() && u && (g = u > sc || g);
    }
    if (!g && this.maxSourceExtent_ && isFinite(c[0]) && isFinite(c[1]) && isFinite(c[2]) && isFinite(c[3]) && !ie(c, this.maxSourceExtent_))
      return;
    let m = 0;
    if (!g && (!isFinite(r[0]) || !isFinite(r[1]) || !isFinite(o[0]) || !isFinite(o[1]) || !isFinite(a[0]) || !isFinite(a[1]) || !isFinite(l[0]) || !isFinite(l[1]))) {
      if (h > 0)
        g = !0;
      else if (m = (!isFinite(r[0]) || !isFinite(r[1]) ? 8 : 0) + (!isFinite(o[0]) || !isFinite(o[1]) ? 4 : 0) + (!isFinite(a[0]) || !isFinite(a[1]) ? 2 : 0) + (!isFinite(l[0]) || !isFinite(l[1]) ? 1 : 0), m != 1 && m != 2 && m != 4 && m != 8)
        return;
    }
    if (h > 0) {
      if (!g) {
        const p = [(t[0] + n[0]) / 2, (t[1] + n[1]) / 2], _ = this.transformInv_(p);
        let y;
        f ? y = (An(r[0], d) + An(a[0], d)) / 2 - An(_[0], d) : y = (r[0] + a[0]) / 2 - _[0];
        const v = (r[1] + a[1]) / 2 - _[1];
        g = y * y + v * v > this.errorThresholdSquared_;
      }
      if (g) {
        if (Math.abs(t[0] - n[0]) <= Math.abs(t[1] - n[1])) {
          const p = [(e[0] + n[0]) / 2, (e[1] + n[1]) / 2], _ = this.transformInv_(p), y = [(s[0] + t[0]) / 2, (s[1] + t[1]) / 2], v = this.transformInv_(y);
          this.addQuad_(
            t,
            e,
            p,
            y,
            r,
            o,
            _,
            v,
            h - 1
          ), this.addQuad_(
            y,
            p,
            n,
            s,
            v,
            _,
            a,
            l,
            h - 1
          );
        } else {
          const p = [(t[0] + e[0]) / 2, (t[1] + e[1]) / 2], _ = this.transformInv_(p), y = [(n[0] + s[0]) / 2, (n[1] + s[1]) / 2], v = this.transformInv_(y);
          this.addQuad_(
            t,
            p,
            y,
            s,
            r,
            _,
            v,
            l,
            h - 1
          ), this.addQuad_(
            p,
            e,
            n,
            y,
            _,
            o,
            a,
            v,
            h - 1
          );
        }
        return;
      }
    }
    if (f) {
      if (!this.canWrapXInSource_)
        return;
      this.wrapsXInSource_ = !0;
    }
    (m & 11) == 0 && this.addTriangle_(t, n, s, r, a, l), (m & 14) == 0 && this.addTriangle_(t, n, e, r, a, o), m && ((m & 13) == 0 && this.addTriangle_(e, s, t, o, l, r), (m & 7) == 0 && this.addTriangle_(e, s, n, o, l, a));
  }
  calculateSourceExtent() {
    const t = fe();
    return this.triangles_.forEach(function(e, n, s) {
      const r = e.source;
      gs(t, r[0]), gs(t, r[1]), gs(t, r[2]);
    }), t;
  }
  getTriangles() {
    return this.triangles_;
  }
}
const O2 = A2;
let Qo;
const kd = [];
function rc(i, t, e, n, s) {
  i.beginPath(), i.moveTo(0, 0), i.lineTo(t, e), i.lineTo(n, s), i.closePath(), i.save(), i.clip(), i.fillRect(0, 0, Math.max(t, n) + 1, Math.max(e, s)), i.restore();
}
function ta(i, t) {
  return Math.abs(i[t * 4] - 210) > 2 || Math.abs(i[t * 4 + 3] - 0.75 * 255) > 2;
}
function N2() {
  if (Qo === void 0) {
    const i = document.createElement("canvas").getContext("2d");
    i.globalCompositeOperation = "lighter", i.fillStyle = "rgba(210, 0, 0, 0.75)", rc(i, 4, 5, 4, 0), rc(i, 4, 5, 0, 5);
    const t = i.getImageData(0, 0, 3, 3).data;
    Qo = ta(t, 0) || ta(t, 4) || ta(t, 8);
  }
  return Qo;
}
function oc(i, t, e, n) {
  const s = Xu(e, t, i);
  let r = Hr(
    t,
    n,
    e
  );
  const o = t.getMetersPerUnit();
  o !== void 0 && (r *= o);
  const a = i.getMetersPerUnit();
  a !== void 0 && (r /= a);
  const l = i.getExtent();
  if (!l || uo(l, s)) {
    const h = Hr(i, r, s) / r;
    isFinite(h) && h > 0 && (r /= h);
  }
  return r;
}
function F2(i, t, e, n) {
  const s = Ri(e);
  let r = oc(
    i,
    t,
    s,
    n
  );
  return (!isFinite(r) || r <= 0) && bu(e, function(o) {
    return r = oc(
      i,
      t,
      o,
      n
    ), isFinite(r) && r > 0;
  }), r;
}
function D2(i, t, e, n, s, r, o, a, l, h, c, u) {
  const d = ge(
    Math.round(e * i),
    Math.round(e * t),
    kd
  );
  if (u || (d.imageSmoothingEnabled = !1), l.length === 0)
    return d.canvas;
  d.scale(e, e);
  function f(x) {
    return Math.round(x * e) / e;
  }
  d.globalCompositeOperation = "lighter";
  const g = fe();
  l.forEach(function(x, C, w) {
    Su(g, x.extent);
  });
  const m = mt(g), p = ke(g), _ = ge(
    Math.round(e * m / n),
    Math.round(e * p / n)
  );
  u || (_.imageSmoothingEnabled = !1);
  const y = e / n;
  l.forEach(function(x, C, w) {
    const S = x.extent[0] - g[0], b = -(x.extent[3] - g[3]), A = mt(x.extent), G = ke(x.extent);
    x.image.width > 0 && x.image.height > 0 && _.drawImage(
      x.image,
      h,
      h,
      x.image.width - 2 * h,
      x.image.height - 2 * h,
      S * y,
      b * y,
      A * y,
      G * y
    );
  });
  const v = Ii(o);
  return a.getTriangles().forEach(function(x, C, w) {
    const S = x.source, b = x.target;
    let A = S[0][0], G = S[0][1], V = S[1][0], T = S[1][1], $ = S[2][0], ft = S[2][1];
    const F = f((b[0][0] - v[0]) / r), k = f(
      -(b[0][1] - v[1]) / r
    ), P = f((b[1][0] - v[0]) / r), tt = f(
      -(b[1][1] - v[1]) / r
    ), Ct = f((b[2][0] - v[0]) / r), _t = f(
      -(b[2][1] - v[1]) / r
    ), At = A, L = G;
    A = 0, G = 0, V -= At, T -= L, $ -= At, ft -= L;
    const ae = [
      [V, T, 0, 0, P - F],
      [$, ft, 0, 0, Ct - F],
      [0, 0, V, T, tt - k],
      [0, 0, $, ft, _t - k]
    ], lt = O0(ae);
    if (!!lt) {
      if (d.save(), d.beginPath(), N2() || !u) {
        d.moveTo(P, tt);
        const gt = 4, ai = F - P, Te = k - tt;
        for (let $t = 0; $t < gt; $t++)
          d.lineTo(
            P + f(($t + 1) * ai / gt),
            tt + f($t * Te / (gt - 1))
          ), $t != gt - 1 && d.lineTo(
            P + f(($t + 1) * ai / gt),
            tt + f(($t + 1) * Te / (gt - 1))
          );
        d.lineTo(Ct, _t);
      } else
        d.moveTo(P, tt), d.lineTo(F, k), d.lineTo(Ct, _t);
      d.clip(), d.transform(
        lt[0],
        lt[2],
        lt[1],
        lt[3],
        F,
        k
      ), d.translate(
        g[0] - At,
        g[3] - L
      ), d.scale(
        n / e,
        -n / e
      ), d.drawImage(_.canvas, 0, 0), d.restore();
    }
  }), c && (d.save(), d.globalCompositeOperation = "source-over", d.strokeStyle = "black", d.lineWidth = 1, a.getTriangles().forEach(function(x, C, w) {
    const S = x.target, b = (S[0][0] - v[0]) / r, A = -(S[0][1] - v[1]) / r, G = (S[1][0] - v[0]) / r, V = -(S[1][1] - v[1]) / r, T = (S[2][0] - v[0]) / r, $ = -(S[2][1] - v[1]) / r;
    d.beginPath(), d.moveTo(G, V), d.lineTo(b, A), d.lineTo(T, $), d.closePath(), d.stroke();
  }), d.restore()), d.canvas;
}
class k2 extends Id {
  constructor(t, e, n, s, r, o, a, l, h, c, u, d) {
    super(r, z.IDLE, { interpolate: !!d }), this.renderEdges_ = u !== void 0 ? u : !1, this.pixelRatio_ = a, this.gutter_ = l, this.canvas_ = null, this.sourceTileGrid_ = e, this.targetTileGrid_ = s, this.wrappedTileCoord_ = o || r, this.sourceTiles_ = [], this.sourcesListenerKeys_ = null, this.sourceZ_ = 0;
    const f = s.getTileCoordExtent(
      this.wrappedTileCoord_
    ), g = this.targetTileGrid_.getExtent();
    let m = this.sourceTileGrid_.getExtent();
    const p = g ? ms(f, g) : f;
    if (ha(p) === 0) {
      this.state = z.EMPTY;
      return;
    }
    const _ = t.getExtent();
    _ && (m ? m = ms(m, _) : m = _);
    const y = s.getResolution(
      this.wrappedTileCoord_[0]
    ), v = F2(
      t,
      n,
      p,
      y
    );
    if (!isFinite(v) || v <= 0) {
      this.state = z.EMPTY;
      return;
    }
    const x = c !== void 0 ? c : I2;
    if (this.triangulation_ = new O2(
      t,
      n,
      p,
      m,
      v * x,
      y
    ), this.triangulation_.getTriangles().length === 0) {
      this.state = z.EMPTY;
      return;
    }
    this.sourceZ_ = e.getZForResolution(v);
    let C = this.triangulation_.calculateSourceExtent();
    if (m && (t.canWrapX() ? (C[1] = wt(
      C[1],
      m[1],
      m[3]
    ), C[3] = wt(
      C[3],
      m[1],
      m[3]
    )) : C = ms(C, m)), !ha(C))
      this.state = z.EMPTY;
    else {
      const w = e.getTileRangeForExtentAndZ(
        C,
        this.sourceZ_
      );
      for (let S = w.minX; S <= w.maxX; S++)
        for (let b = w.minY; b <= w.maxY; b++) {
          const A = h(this.sourceZ_, S, b, a);
          A && this.sourceTiles_.push(A);
        }
      this.sourceTiles_.length === 0 && (this.state = z.EMPTY);
    }
  }
  getImage() {
    return this.canvas_;
  }
  reproject_() {
    const t = [];
    if (this.sourceTiles_.forEach(
      function(e, n, s) {
        e && e.getState() == z.LOADED && t.push({
          extent: this.sourceTileGrid_.getTileCoordExtent(e.tileCoord),
          image: e.getImage()
        });
      }.bind(this)
    ), this.sourceTiles_.length = 0, t.length === 0)
      this.state = z.ERROR;
    else {
      const e = this.wrappedTileCoord_[0], n = this.targetTileGrid_.getTileSize(e), s = typeof n == "number" ? n : n[0], r = typeof n == "number" ? n : n[1], o = this.targetTileGrid_.getResolution(e), a = this.sourceTileGrid_.getResolution(
        this.sourceZ_
      ), l = this.targetTileGrid_.getTileCoordExtent(
        this.wrappedTileCoord_
      );
      this.canvas_ = D2(
        s,
        r,
        this.pixelRatio_,
        a,
        this.sourceTileGrid_.getExtent(),
        o,
        l,
        this.triangulation_,
        t,
        this.gutter_,
        this.renderEdges_,
        this.interpolate
      ), this.state = z.LOADED;
    }
    this.changed();
  }
  load() {
    if (this.state == z.IDLE) {
      this.state = z.LOADING, this.changed();
      let t = 0;
      this.sourcesListenerKeys_ = [], this.sourceTiles_.forEach(
        function(e, n, s) {
          const r = e.getState();
          if (r == z.IDLE || r == z.LOADING) {
            t++;
            const o = et(
              e,
              X.CHANGE,
              function(a) {
                const l = e.getState();
                (l == z.LOADED || l == z.ERROR || l == z.EMPTY) && (pt(o), t--, t === 0 && (this.unlistenSources_(), this.reproject_()));
              },
              this
            );
            this.sourcesListenerKeys_.push(o);
          }
        }.bind(this)
      ), t === 0 ? setTimeout(this.reproject_.bind(this), 0) : this.sourceTiles_.forEach(function(e, n, s) {
        e.getState() == z.IDLE && e.load();
      });
    }
  }
  unlistenSources_() {
    this.sourcesListenerKeys_.forEach(pt), this.sourcesListenerKeys_ = null;
  }
  release() {
    this.canvas_ && ($u(this.canvas_.getContext("2d")), kd.push(this.canvas_), this.canvas_ = null), super.release();
  }
}
const Ra = k2, ea = {
  TILELOADSTART: "tileloadstart",
  TILELOADEND: "tileloadend",
  TILELOADERROR: "tileloaderror"
}, G2 = [0, 0, 0], gi = 5;
class $2 {
  constructor(t) {
    this.minZoom = t.minZoom !== void 0 ? t.minZoom : 0, this.resolutions_ = t.resolutions, Y(
      o0(
        this.resolutions_,
        function(s, r) {
          return r - s;
        },
        !0
      ),
      17
    );
    let e;
    if (!t.origins) {
      for (let s = 0, r = this.resolutions_.length - 1; s < r; ++s)
        if (!e)
          e = this.resolutions_[s] / this.resolutions_[s + 1];
        else if (this.resolutions_[s] / this.resolutions_[s + 1] !== e) {
          e = void 0;
          break;
        }
    }
    this.zoomFactor_ = e, this.maxZoom = this.resolutions_.length - 1, this.origin_ = t.origin !== void 0 ? t.origin : null, this.origins_ = null, t.origins !== void 0 && (this.origins_ = t.origins, Y(this.origins_.length == this.resolutions_.length, 20));
    const n = t.extent;
    n !== void 0 && !this.origin_ && !this.origins_ && (this.origin_ = Ii(n)), Y(
      !this.origin_ && this.origins_ || this.origin_ && !this.origins_,
      18
    ), this.tileSizes_ = null, t.tileSizes !== void 0 && (this.tileSizes_ = t.tileSizes, Y(this.tileSizes_.length == this.resolutions_.length, 19)), this.tileSize_ = t.tileSize !== void 0 ? t.tileSize : this.tileSizes_ ? null : il, Y(
      !this.tileSize_ && this.tileSizes_ || this.tileSize_ && !this.tileSizes_,
      22
    ), this.extent_ = n !== void 0 ? n : null, this.fullTileRanges_ = null, this.tmpSize_ = [0, 0], this.tmpExtent_ = [0, 0, 0, 0], t.sizes !== void 0 ? this.fullTileRanges_ = t.sizes.map(function(s, r) {
      const o = new Fd(
        Math.min(0, s[0]),
        Math.max(s[0] - 1, -1),
        Math.min(0, s[1]),
        Math.max(s[1] - 1, -1)
      );
      if (n) {
        const a = this.getTileRangeForExtentAndZ(n, r);
        o.minX = Math.max(a.minX, o.minX), o.maxX = Math.min(a.maxX, o.maxX), o.minY = Math.max(a.minY, o.minY), o.maxY = Math.min(a.maxY, o.maxY);
      }
      return o;
    }, this) : n && this.calculateTileRanges_(n);
  }
  forEachTileCoord(t, e, n) {
    const s = this.getTileRangeForExtentAndZ(t, e);
    for (let r = s.minX, o = s.maxX; r <= o; ++r)
      for (let a = s.minY, l = s.maxY; a <= l; ++a)
        n([e, r, a]);
  }
  forEachTileCoordParentTileRange(t, e, n, s) {
    let r, o, a, l = null, h = t[0] - 1;
    for (this.zoomFactor_ === 2 ? (o = t[1], a = t[2]) : l = this.getTileCoordExtent(t, s); h >= this.minZoom; ) {
      if (this.zoomFactor_ === 2 ? (o = Math.floor(o / 2), a = Math.floor(a / 2), r = _n(o, o, a, a, n)) : r = this.getTileRangeForExtentAndZ(
        l,
        h,
        n
      ), e(h, r))
        return !0;
      --h;
    }
    return !1;
  }
  getExtent() {
    return this.extent_;
  }
  getMaxZoom() {
    return this.maxZoom;
  }
  getMinZoom() {
    return this.minZoom;
  }
  getOrigin(t) {
    return this.origin_ ? this.origin_ : this.origins_[t];
  }
  getResolution(t) {
    return this.resolutions_[t];
  }
  getResolutions() {
    return this.resolutions_;
  }
  getTileCoordChildTileRange(t, e, n) {
    if (t[0] < this.maxZoom) {
      if (this.zoomFactor_ === 2) {
        const r = t[1] * 2, o = t[2] * 2;
        return _n(
          r,
          r + 1,
          o,
          o + 1,
          e
        );
      }
      const s = this.getTileCoordExtent(
        t,
        n || this.tmpExtent_
      );
      return this.getTileRangeForExtentAndZ(
        s,
        t[0] + 1,
        e
      );
    }
    return null;
  }
  getTileRangeForTileCoordAndZ(t, e, n) {
    if (e > this.maxZoom || e < this.minZoom)
      return null;
    const s = t[0], r = t[1], o = t[2];
    if (e === s)
      return _n(
        r,
        o,
        r,
        o,
        n
      );
    if (this.zoomFactor_) {
      const l = Math.pow(this.zoomFactor_, e - s), h = Math.floor(r * l), c = Math.floor(o * l);
      if (e < s)
        return _n(h, h, c, c, n);
      const u = Math.floor(l * (r + 1)) - 1, d = Math.floor(l * (o + 1)) - 1;
      return _n(h, u, c, d, n);
    }
    const a = this.getTileCoordExtent(t, this.tmpExtent_);
    return this.getTileRangeForExtentAndZ(a, e, n);
  }
  getTileRangeExtent(t, e, n) {
    const s = this.getOrigin(t), r = this.getResolution(t), o = ce(this.getTileSize(t), this.tmpSize_), a = s[0] + e.minX * o[0] * r, l = s[0] + (e.maxX + 1) * o[0] * r, h = s[1] + e.minY * o[1] * r, c = s[1] + (e.maxY + 1) * o[1] * r;
    return xe(a, h, l, c, n);
  }
  getTileRangeForExtentAndZ(t, e, n) {
    const s = G2;
    this.getTileCoordForXYAndZ_(t[0], t[3], e, !1, s);
    const r = s[1], o = s[2];
    return this.getTileCoordForXYAndZ_(t[2], t[1], e, !0, s), _n(
      r,
      s[1],
      o,
      s[2],
      n
    );
  }
  getTileCoordCenter(t) {
    const e = this.getOrigin(t[0]), n = this.getResolution(t[0]), s = ce(this.getTileSize(t[0]), this.tmpSize_);
    return [
      e[0] + (t[1] + 0.5) * s[0] * n,
      e[1] - (t[2] + 0.5) * s[1] * n
    ];
  }
  getTileCoordExtent(t, e) {
    const n = this.getOrigin(t[0]), s = this.getResolution(t[0]), r = ce(this.getTileSize(t[0]), this.tmpSize_), o = n[0] + t[1] * r[0] * s, a = n[1] - (t[2] + 1) * r[1] * s, l = o + r[0] * s, h = a + r[1] * s;
    return xe(o, a, l, h, e);
  }
  getTileCoordForCoordAndResolution(t, e, n) {
    return this.getTileCoordForXYAndResolution_(
      t[0],
      t[1],
      e,
      !1,
      n
    );
  }
  getTileCoordForXYAndResolution_(t, e, n, s, r) {
    const o = this.getZForResolution(n), a = n / this.getResolution(o), l = this.getOrigin(o), h = ce(this.getTileSize(o), this.tmpSize_);
    let c = a * (t - l[0]) / n / h[0], u = a * (l[1] - e) / n / h[1];
    return s ? (c = gr(c, gi) - 1, u = gr(u, gi) - 1) : (c = fr(c, gi), u = fr(u, gi)), Qh(o, c, u, r);
  }
  getTileCoordForXYAndZ_(t, e, n, s, r) {
    const o = this.getOrigin(n), a = this.getResolution(n), l = ce(this.getTileSize(n), this.tmpSize_);
    let h = (t - o[0]) / a / l[0], c = (o[1] - e) / a / l[1];
    return s ? (h = gr(h, gi) - 1, c = gr(c, gi) - 1) : (h = fr(h, gi), c = fr(c, gi)), Qh(n, h, c, r);
  }
  getTileCoordForCoordAndZ(t, e, n) {
    return this.getTileCoordForXYAndZ_(
      t[0],
      t[1],
      e,
      !1,
      n
    );
  }
  getTileCoordResolution(t) {
    return this.resolutions_[t[0]];
  }
  getTileSize(t) {
    return this.tileSize_ ? this.tileSize_ : this.tileSizes_[t];
  }
  getFullTileRange(t) {
    return this.fullTileRanges_ ? this.fullTileRanges_[t] : this.extent_ ? this.getTileRangeForExtentAndZ(this.extent_, t) : null;
  }
  getZForResolution(t, e) {
    const n = Ya(
      this.resolutions_,
      t,
      e || 0
    );
    return wt(n, this.minZoom, this.maxZoom);
  }
  tileCoordIntersectsViewport(t, e) {
    return sd(
      e,
      0,
      e.length,
      2,
      this.getTileCoordExtent(t)
    );
  }
  calculateTileRanges_(t) {
    const e = this.resolutions_.length, n = new Array(e);
    for (let s = this.minZoom; s < e; ++s)
      n[s] = this.getTileRangeForExtentAndZ(t, s);
    this.fullTileRanges_ = n;
  }
}
const Gd = $2;
function $d(i) {
  let t = i.getDefaultTileGrid();
  return t || (t = V2(i), i.setDefaultTileGrid(t)), t;
}
function B2(i, t, e) {
  const n = t[0], s = i.getTileCoordCenter(t), r = Bd(e);
  if (uo(r, s))
    return t;
  {
    const o = mt(r), a = Math.ceil(
      (r[0] - s[0]) / o
    );
    return s[0] += o * a, i.getTileCoordForCoordAndZ(s, n);
  }
}
function z2(i, t, e, n) {
  n = n !== void 0 ? n : "top-left";
  const s = Z2(i, t, e);
  return new Gd({
    extent: i,
    origin: b0(i, n),
    resolutions: s,
    tileSize: e
  });
}
function Z2(i, t, e, n) {
  t = t !== void 0 ? t : fg, e = ce(e !== void 0 ? e : il);
  const s = ke(i), r = mt(i);
  n = n > 0 ? n : Math.max(r / e[0], s / e[1]);
  const o = t + 1, a = new Array(o);
  for (let l = 0; l < o; ++l)
    a[l] = n / Math.pow(2, l);
  return a;
}
function V2(i, t, e, n) {
  const s = Bd(i);
  return z2(s, t, e, n);
}
function Bd(i) {
  i = J(i);
  let t = i.getExtent();
  if (!t) {
    const e = 180 * Bn.degrees / i.getMetersPerUnit();
    t = xe(-e, -e, e, e);
  }
  return t;
}
class U2 extends Ld {
  constructor(t) {
    super({
      attributions: t.attributions,
      attributionsCollapsible: t.attributionsCollapsible,
      projection: t.projection,
      state: t.state,
      wrapX: t.wrapX,
      interpolate: t.interpolate
    }), this.on, this.once, this.un, this.opaque_ = t.opaque !== void 0 ? t.opaque : !1, this.tilePixelRatio_ = t.tilePixelRatio !== void 0 ? t.tilePixelRatio : 1, this.tileGrid = t.tileGrid !== void 0 ? t.tileGrid : null;
    const e = [256, 256];
    this.tileGrid && ce(this.tileGrid.getTileSize(this.tileGrid.getMinZoom()), e), this.tileCache = new Od(t.cacheSize || 0), this.tmpSize = [0, 0], this.key_ = t.key || "", this.tileOptions = {
      transition: t.transition,
      interpolate: t.interpolate
    }, this.zDirection = t.zDirection ? t.zDirection : 0;
  }
  canExpireCache() {
    return this.tileCache.canExpireCache();
  }
  expireCache(t, e) {
    const n = this.getTileCacheForProjection(t);
    n && n.expireCache(e);
  }
  forEachLoadedTile(t, e, n, s) {
    const r = this.getTileCacheForProjection(t);
    if (!r)
      return !1;
    let o = !0, a, l, h;
    for (let c = n.minX; c <= n.maxX; ++c)
      for (let u = n.minY; u <= n.maxY; ++u)
        l = Eo(e, c, u), h = !1, r.containsKey(l) && (a = r.get(l), h = a.getState() === z.LOADED, h && (h = s(a) !== !1)), h || (o = !1);
    return o;
  }
  getGutterForProjection(t) {
    return 0;
  }
  getKey() {
    return this.key_;
  }
  setKey(t) {
    this.key_ !== t && (this.key_ = t, this.changed());
  }
  getOpaque(t) {
    return this.opaque_;
  }
  getResolutions() {
    return this.tileGrid ? this.tileGrid.getResolutions() : null;
  }
  getTile(t, e, n, s, r) {
    return W();
  }
  getTileGrid() {
    return this.tileGrid;
  }
  getTileGridForProjection(t) {
    return this.tileGrid ? this.tileGrid : $d(t);
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    return Y(
      e === null || Ie(e, t),
      68
    ), this.tileCache;
  }
  getTilePixelRatio(t) {
    return this.tilePixelRatio_;
  }
  getTilePixelSize(t, e, n) {
    const s = this.getTileGridForProjection(n), r = this.getTilePixelRatio(e), o = ce(s.getTileSize(t), this.tmpSize);
    return r == 1 ? o : j1(o, r, this.tmpSize);
  }
  getTileCoordForTileUrlFunction(t, e) {
    e = e !== void 0 ? e : this.getProjection();
    const n = this.getTileGridForProjection(e);
    return this.getWrapX() && e.isGlobal() && (t = B2(n, t, e)), C2(t, n) ? t : null;
  }
  clear() {
    this.tileCache.clear();
  }
  refresh() {
    this.clear(), super.refresh();
  }
  updateCacheSize(t, e) {
    const n = this.getTileCacheForProjection(e);
    t > n.highWaterMark && (n.highWaterMark = t);
  }
  useTile(t, e, n, s) {
  }
}
class W2 extends Be {
  constructor(t, e) {
    super(t), this.tile = e;
  }
}
const H2 = U2;
function X2(i, t) {
  const e = /\{z\}/g, n = /\{x\}/g, s = /\{y\}/g, r = /\{-y\}/g;
  return function(o, a, l) {
    if (o)
      return i.replace(e, o[0].toString()).replace(n, o[1].toString()).replace(s, o[2].toString()).replace(r, function() {
        const h = o[0], c = t.getFullTileRange(h);
        return Y(c, 55), (c.getHeight() - o[2] - 1).toString();
      });
  };
}
function Y2(i, t) {
  const e = i.length, n = new Array(e);
  for (let s = 0; s < e; ++s)
    n[s] = X2(i[s], t);
  return ba(n);
}
function ba(i) {
  return i.length === 1 ? i[0] : function(t, e, n) {
    if (t) {
      const s = x2(t), r = An(s, i.length);
      return i[r](t, e, n);
    } else
      return;
  };
}
function zd(i) {
  const t = [];
  let e = /\{([a-z])-([a-z])\}/.exec(i);
  if (e) {
    const n = e[1].charCodeAt(0), s = e[2].charCodeAt(0);
    let r;
    for (r = n; r <= s; ++r)
      t.push(i.replace(e[0], String.fromCharCode(r)));
    return t;
  }
  if (e = /\{(\d+)-(\d+)\}/.exec(i), e) {
    const n = parseInt(e[2], 10);
    for (let s = parseInt(e[1], 10); s <= n; s++)
      t.push(i.replace(e[0], s.toString()));
    return t;
  }
  return t.push(i), t;
}
class Ll extends H2 {
  constructor(t) {
    super({
      attributions: t.attributions,
      cacheSize: t.cacheSize,
      opaque: t.opaque,
      projection: t.projection,
      state: t.state,
      tileGrid: t.tileGrid,
      tilePixelRatio: t.tilePixelRatio,
      wrapX: t.wrapX,
      transition: t.transition,
      interpolate: t.interpolate,
      key: t.key,
      attributionsCollapsible: t.attributionsCollapsible,
      zDirection: t.zDirection
    }), this.generateTileUrlFunction_ = this.tileUrlFunction === Ll.prototype.tileUrlFunction, this.tileLoadFunction = t.tileLoadFunction, t.tileUrlFunction && (this.tileUrlFunction = t.tileUrlFunction), this.urls = null, t.urls ? this.setUrls(t.urls) : t.url && this.setUrl(t.url), this.tileLoadingKeys_ = {};
  }
  getTileLoadFunction() {
    return this.tileLoadFunction;
  }
  getTileUrlFunction() {
    return Object.getPrototypeOf(this).tileUrlFunction === this.tileUrlFunction ? this.tileUrlFunction.bind(this) : this.tileUrlFunction;
  }
  getUrls() {
    return this.urls;
  }
  handleTileChange(t) {
    const e = t.target, n = ot(e), s = e.getState();
    let r;
    s == z.LOADING ? (this.tileLoadingKeys_[n] = !0, r = ea.TILELOADSTART) : n in this.tileLoadingKeys_ && (delete this.tileLoadingKeys_[n], r = s == z.ERROR ? ea.TILELOADERROR : s == z.LOADED ? ea.TILELOADEND : void 0), r != null && this.dispatchEvent(new W2(r, e));
  }
  setTileLoadFunction(t) {
    this.tileCache.clear(), this.tileLoadFunction = t, this.changed();
  }
  setTileUrlFunction(t, e) {
    this.tileUrlFunction = t, this.tileCache.pruneExceptNewestZ(), typeof e < "u" ? this.setKey(e) : this.changed();
  }
  setUrl(t) {
    const e = zd(t);
    this.urls = e, this.setUrls(e);
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.generateTileUrlFunction_ ? this.setTileUrlFunction(Y2(t, this.tileGrid), e) : this.setKey(e);
  }
  tileUrlFunction(t, e, n) {
  }
  useTile(t, e, n) {
    const s = Eo(t, e, n);
    this.tileCache.containsKey(s) && this.tileCache.get(s);
  }
}
const j2 = Ll;
class K2 extends j2 {
  constructor(t) {
    super({
      attributions: t.attributions,
      cacheSize: t.cacheSize,
      opaque: t.opaque,
      projection: t.projection,
      state: t.state,
      tileGrid: t.tileGrid,
      tileLoadFunction: t.tileLoadFunction ? t.tileLoadFunction : q2,
      tilePixelRatio: t.tilePixelRatio,
      tileUrlFunction: t.tileUrlFunction,
      url: t.url,
      urls: t.urls,
      wrapX: t.wrapX,
      transition: t.transition,
      interpolate: t.interpolate !== void 0 ? t.interpolate : !0,
      key: t.key,
      attributionsCollapsible: t.attributionsCollapsible,
      zDirection: t.zDirection
    }), this.crossOrigin = t.crossOrigin !== void 0 ? t.crossOrigin : null, this.tileClass = t.tileClass !== void 0 ? t.tileClass : Pd, this.tileCacheForProjection = {}, this.tileGridForProjection = {}, this.reprojectionErrorThreshold_ = t.reprojectionErrorThreshold, this.renderReprojectionEdges_ = !1;
  }
  canExpireCache() {
    if (this.tileCache.canExpireCache())
      return !0;
    for (const t in this.tileCacheForProjection)
      if (this.tileCacheForProjection[t].canExpireCache())
        return !0;
    return !1;
  }
  expireCache(t, e) {
    const n = this.getTileCacheForProjection(t);
    this.tileCache.expireCache(
      this.tileCache == n ? e : {}
    );
    for (const s in this.tileCacheForProjection) {
      const r = this.tileCacheForProjection[s];
      r.expireCache(r == n ? e : {});
    }
  }
  getGutterForProjection(t) {
    return this.getProjection() && t && !Ie(this.getProjection(), t) ? 0 : this.getGutter();
  }
  getGutter() {
    return 0;
  }
  getKey() {
    let t = super.getKey();
    return this.getInterpolate() || (t += ":disable-interpolation"), t;
  }
  getOpaque(t) {
    return this.getProjection() && t && !Ie(this.getProjection(), t) ? !1 : super.getOpaque(t);
  }
  getTileGridForProjection(t) {
    const e = this.getProjection();
    if (this.tileGrid && (!e || Ie(e, t)))
      return this.tileGrid;
    {
      const n = ot(t);
      return n in this.tileGridForProjection || (this.tileGridForProjection[n] = $d(t)), this.tileGridForProjection[n];
    }
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    if (!e || Ie(e, t))
      return this.tileCache;
    {
      const n = ot(t);
      return n in this.tileCacheForProjection || (this.tileCacheForProjection[n] = new Od(
        this.tileCache.highWaterMark
      )), this.tileCacheForProjection[n];
    }
  }
  createTile_(t, e, n, s, r, o) {
    const a = [t, e, n], l = this.getTileCoordForTileUrlFunction(
      a,
      r
    ), h = l ? this.tileUrlFunction(l, s, r) : void 0, c = new this.tileClass(
      a,
      h !== void 0 ? z.IDLE : z.EMPTY,
      h !== void 0 ? h : "",
      this.crossOrigin,
      this.tileLoadFunction,
      this.tileOptions
    );
    return c.key = o, c.addEventListener(X.CHANGE, this.handleTileChange.bind(this)), c;
  }
  getTile(t, e, n, s, r) {
    const o = this.getProjection();
    if (!o || !r || Ie(o, r))
      return this.getTileInternal(
        t,
        e,
        n,
        s,
        o || r
      );
    {
      const a = this.getTileCacheForProjection(r), l = [t, e, n];
      let h;
      const c = Ad(l);
      a.containsKey(c) && (h = a.get(c));
      const u = this.getKey();
      if (h && h.key == u)
        return h;
      {
        const d = this.getTileGridForProjection(o), f = this.getTileGridForProjection(r), g = this.getTileCoordForTileUrlFunction(
          l,
          r
        ), m = new Ra(
          o,
          d,
          r,
          f,
          l,
          g,
          this.getTilePixelRatio(s),
          this.getGutter(),
          function(p, _, y, v) {
            return this.getTileInternal(p, _, y, v, o);
          }.bind(this),
          this.reprojectionErrorThreshold_,
          this.renderReprojectionEdges_,
          this.getInterpolate()
        );
        return m.key = u, h ? (m.interimTile = h, m.refreshInterimChain(), a.replace(c, m)) : a.set(c, m), m;
      }
    }
  }
  getTileInternal(t, e, n, s, r) {
    let o = null;
    const a = Eo(t, e, n), l = this.getKey();
    if (!this.tileCache.containsKey(a))
      o = this.createTile_(t, e, n, s, r, l), this.tileCache.set(a, o);
    else if (o = this.tileCache.get(a), o.key != l) {
      const h = o;
      o = this.createTile_(t, e, n, s, r, l), h.getState() == z.IDLE ? o.interimTile = h.interimTile : o.interimTile = h, o.refreshInterimChain(), this.tileCache.replace(a, o);
    }
    return o;
  }
  setRenderReprojectionEdges(t) {
    if (this.renderReprojectionEdges_ != t) {
      this.renderReprojectionEdges_ = t;
      for (const e in this.tileCacheForProjection)
        this.tileCacheForProjection[e].clear();
      this.changed();
    }
  }
  setTileGridForProjection(t, e) {
    const n = J(t);
    if (n) {
      const s = ot(n);
      s in this.tileGridForProjection || (this.tileGridForProjection[s] = e);
    }
  }
  clear() {
    super.clear();
    for (const t in this.tileCacheForProjection)
      this.tileCacheForProjection[t].clear();
  }
}
function q2(i, t) {
  i.getImage().src = t;
}
const J2 = K2;
class Q2 extends Kn {
  constructor(t) {
    super({
      attributions: t.attributions,
      wrapX: t.wrapX
    }), this.resolution = void 0, this.distance = t.distance !== void 0 ? t.distance : 20, this.minDistance = t.minDistance || 0, this.interpolationRatio = 0, this.features = [], this.geometryFunction = t.geometryFunction || function(e) {
      const n = e.getGeometry();
      return Y(n.getType() == "Point", 10), n;
    }, this.createCustomCluster_ = t.createCluster, this.source = null, this.boundRefresh_ = this.refresh.bind(this), this.updateDistance(this.distance, this.minDistance), this.setSource(t.source || null);
  }
  clear(t) {
    this.features.length = 0, super.clear(t);
  }
  getDistance() {
    return this.distance;
  }
  getSource() {
    return this.source;
  }
  loadFeatures(t, e, n) {
    this.source.loadFeatures(t, e, n), e !== this.resolution && (this.resolution = e, this.refresh());
  }
  setDistance(t) {
    this.updateDistance(t, this.minDistance);
  }
  setMinDistance(t) {
    this.updateDistance(this.distance, t);
  }
  getMinDistance() {
    return this.minDistance;
  }
  setSource(t) {
    this.source && this.source.removeEventListener(X.CHANGE, this.boundRefresh_), this.source = t, t && t.addEventListener(X.CHANGE, this.boundRefresh_), this.refresh();
  }
  refresh() {
    this.clear(), this.cluster(), this.addFeatures(this.features);
  }
  updateDistance(t, e) {
    const n = t === 0 ? 0 : Math.min(e, t) / t, s = t !== this.distance || this.interpolationRatio !== n;
    this.distance = t, this.minDistance = e, this.interpolationRatio = n, s && this.refresh();
  }
  cluster() {
    if (this.resolution === void 0 || !this.source)
      return;
    const t = fe(), e = this.distance * this.resolution, n = this.source.getFeatures(), s = {};
    for (let r = 0, o = n.length; r < o; r++) {
      const a = n[r];
      if (!(ot(a) in s)) {
        const l = this.geometryFunction(a);
        if (l) {
          const h = l.getCoordinates();
          Eu(h, t), co(t, e, t);
          const c = this.source.getFeaturesInExtent(t).filter(function(u) {
            const d = ot(u);
            return d in s ? !1 : (s[d] = !0, !0);
          });
          this.features.push(this.createCluster(c, t));
        }
      }
    }
  }
  createCluster(t, e) {
    const n = [0, 0];
    for (let a = t.length - 1; a >= 0; --a) {
      const l = this.geometryFunction(t[a]);
      l ? Ou(n, l.getCoordinates()) : t.splice(a, 1);
    }
    Nu(n, 1 / t.length);
    const s = Ri(e), r = this.interpolationRatio, o = new si([
      n[0] * (1 - r) + s[0] * r,
      n[1] * (1 - r) + s[1] * r
    ]);
    return this.createCustomCluster_ ? this.createCustomCluster_(o, t) : new on({
      geometry: o,
      features: t
    });
  }
}
const tp = Q2;
function ac(i, t) {
  const e = [];
  Object.keys(t).forEach(function(s) {
    t[s] !== null && t[s] !== void 0 && e.push(s + "=" + encodeURIComponent(t[s]));
  });
  const n = e.join("&");
  return i = i.replace(/[?&]$/, ""), i += i.includes("?") ? "&" : "?", i + n;
}
const Mr = {
  PRELOAD: "preload",
  USE_INTERIM_TILES_ON_ERROR: "useInterimTilesOnError"
};
class ep extends po {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.preload, delete e.useInterimTilesOnError, super(e), this.on, this.once, this.un, this.setPreload(t.preload !== void 0 ? t.preload : 0), this.setUseInterimTilesOnError(
      t.useInterimTilesOnError !== void 0 ? t.useInterimTilesOnError : !0
    );
  }
  getPreload() {
    return this.get(Mr.PRELOAD);
  }
  setPreload(t) {
    this.set(Mr.PRELOAD, t);
  }
  getUseInterimTilesOnError() {
    return this.get(Mr.USE_INTERIM_TILES_ON_ERROR);
  }
  setUseInterimTilesOnError(t) {
    this.set(Mr.USE_INTERIM_TILES_ON_ERROR, t);
  }
  getData(t) {
    return super.getData(t);
  }
}
const ip = ep;
class np extends Ed {
  constructor(t) {
    super(t), this.extentChanged = !0, this.renderedExtent_ = null, this.renderedPixelRatio, this.renderedProjection = null, this.renderedRevision, this.renderedTiles = [], this.newTiles_ = !1, this.tmpExtent = fe(), this.tmpTileRange_ = new Fd(0, 0, 0, 0);
  }
  isDrawableTile(t) {
    const e = this.getLayer(), n = t.getState(), s = e.getUseInterimTilesOnError();
    return n == z.LOADED || n == z.EMPTY || n == z.ERROR && !s;
  }
  getTile(t, e, n, s) {
    const r = s.pixelRatio, o = s.viewState.projection, a = this.getLayer();
    let h = a.getSource().getTile(t, e, n, r, o);
    return h.getState() == z.ERROR && a.getUseInterimTilesOnError() && a.getPreload() > 0 && (this.newTiles_ = !0), this.isDrawableTile(h) || (h = h.getInterimTile()), h;
  }
  getData(t) {
    const e = this.frameState;
    if (!e)
      return null;
    const n = this.getLayer(), s = Ft(
      e.pixelToCoordinateTransform,
      t.slice()
    ), r = n.getExtent();
    if (r && !uo(r, s))
      return null;
    const o = e.pixelRatio, a = e.viewState.projection, l = e.viewState, h = n.getRenderSource(), c = h.getTileGridForProjection(l.projection), u = h.getTilePixelRatio(e.pixelRatio);
    for (let d = c.getZForResolution(l.resolution); d >= c.getMinZoom(); --d) {
      const f = c.getTileCoordForCoordAndZ(s, d), g = h.getTile(
        d,
        f[1],
        f[2],
        o,
        a
      );
      if (!(g instanceof Pd || g instanceof Ra) || g instanceof Ra && g.getState() === z.EMPTY)
        return null;
      if (g.getState() !== z.LOADED)
        continue;
      const m = c.getOrigin(d), p = ce(c.getTileSize(d)), _ = c.getResolution(d), y = Math.floor(
        u * ((s[0] - m[0]) / _ - f[1] * p[0])
      ), v = Math.floor(
        u * ((m[1] - s[1]) / _ - f[2] * p[1])
      ), x = Math.round(
        u * h.getGutterForProjection(l.projection)
      );
      return this.getImageData(g.getImage(), y + x, v + x);
    }
    return null;
  }
  loadedTileCallback(t, e, n) {
    return this.isDrawableTile(n) ? super.loadedTileCallback(t, e, n) : !1;
  }
  prepareFrame(t) {
    return !!this.getLayer().getSource();
  }
  renderFrame(t, e) {
    const n = t.layerStatesArray[t.layerIndex], s = t.viewState, r = s.projection, o = s.resolution, a = s.center, l = s.rotation, h = t.pixelRatio, c = this.getLayer(), u = c.getSource(), d = u.getRevision(), f = u.getTileGridForProjection(r), g = f.getZForResolution(o, u.zDirection), m = f.getResolution(g);
    let p = t.extent;
    const _ = t.viewState.resolution, y = u.getTilePixelRatio(h), v = Math.round(mt(p) / _ * h), x = Math.round(ke(p) / _ * h), C = n.extent && Gi(n.extent);
    C && (p = ms(
      p,
      Gi(n.extent)
    ));
    const w = m * v / 2 / y, S = m * x / 2 / y, b = [
      a[0] - w,
      a[1] - S,
      a[0] + w,
      a[1] + S
    ], A = f.getTileRangeForExtentAndZ(p, g), G = {};
    G[g] = {};
    const V = this.createLoadedTileFinder(
      u,
      r,
      G
    ), T = this.tmpExtent, $ = this.tmpTileRange_;
    this.newTiles_ = !1;
    const ft = l ? ua(
      s.center,
      _,
      l,
      t.size
    ) : void 0;
    for (let ae = A.minX; ae <= A.maxX; ++ae)
      for (let lt = A.minY; lt <= A.maxY; ++lt) {
        if (l && !f.tileCoordIntersectsViewport([g, ae, lt], ft))
          continue;
        const gt = this.getTile(g, ae, lt, t);
        if (this.isDrawableTile(gt)) {
          const $t = ot(this);
          if (gt.getState() == z.LOADED) {
            G[g][gt.tileCoord.toString()] = gt;
            let Ze = gt.inTransition($t);
            Ze && n.opacity !== 1 && (gt.endTransition($t), Ze = !1), !this.newTiles_ && (Ze || !this.renderedTiles.includes(gt)) && (this.newTiles_ = !0);
          }
          if (gt.getAlpha($t, t.time) === 1)
            continue;
        }
        const ai = f.getTileCoordChildTileRange(
          gt.tileCoord,
          $,
          T
        );
        let Te = !1;
        ai && (Te = V(g + 1, ai)), Te || f.forEachTileCoordParentTileRange(
          gt.tileCoord,
          V,
          $,
          T
        );
      }
    const F = m / o * h / y;
    Si(
      this.pixelTransform,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / h,
      1 / h,
      l,
      -v / 2,
      -x / 2
    );
    const k = Cu(this.pixelTransform);
    this.useContainer(e, k, this.getBackground(t));
    const P = this.context, tt = P.canvas;
    Ka(this.inversePixelTransform, this.pixelTransform), Si(
      this.tempTransform,
      v / 2,
      x / 2,
      F,
      F,
      0,
      -v / 2,
      -x / 2
    ), tt.width != v || tt.height != x ? (tt.width = v, tt.height = x) : this.containerReused || P.clearRect(0, 0, v, x), C && this.clipUnrotated(P, t, C), u.getInterpolate() || (P.imageSmoothingEnabled = !1), this.preRender(P, t), this.renderedTiles.length = 0;
    let Ct = Object.keys(G).map(Number);
    Ct.sort(Yi);
    let _t, At, L;
    n.opacity === 1 && (!this.containerReused || u.getOpaque(t.viewState.projection)) ? Ct = Ct.reverse() : (_t = [], At = []);
    for (let ae = Ct.length - 1; ae >= 0; --ae) {
      const lt = Ct[ae], gt = u.getTilePixelSize(
        lt,
        h,
        r
      ), Te = f.getResolution(lt) / m, $t = gt[0] * Te * F, Ze = gt[1] * Te * F, ln = f.getTileCoordForCoordAndZ(
        Ii(b),
        lt
      ), sr = f.getTileCoordExtent(ln), hn = Ft(this.tempTransform, [
        y * (sr[0] - b[0]) / m,
        y * (b[3] - sr[3]) / m
      ]), rr = y * u.getGutterForProjection(r), li = G[lt];
      for (const ts in li) {
        const hi = li[ts], or = hi.tileCoord, ar = ln[1] - or[1], lr = Math.round(hn[0] - (ar - 1) * $t), cn = ln[2] - or[2], Ao = Math.round(hn[1] - (cn - 1) * Ze), Jt = Math.round(hn[0] - ar * $t), me = Math.round(hn[1] - cn * Ze), Me = lr - Jt, Ve = Ao - me, un = g === lt, Ai = un && hi.getAlpha(ot(this), t.time) !== 1;
        let ci = !1;
        if (!Ai)
          if (_t) {
            L = [Jt, me, Jt + Me, me, Jt + Me, me + Ve, Jt, me + Ve];
            for (let dn = 0, hr = _t.length; dn < hr; ++dn)
              if (g !== lt && lt < At[dn]) {
                const Ht = _t[dn];
                ie(
                  [Jt, me, Jt + Me, me + Ve],
                  [Ht[0], Ht[3], Ht[4], Ht[7]]
                ) && (ci || (P.save(), ci = !0), P.beginPath(), P.moveTo(L[0], L[1]), P.lineTo(L[2], L[3]), P.lineTo(L[4], L[5]), P.lineTo(L[6], L[7]), P.moveTo(Ht[6], Ht[7]), P.lineTo(Ht[4], Ht[5]), P.lineTo(Ht[2], Ht[3]), P.lineTo(Ht[0], Ht[1]), P.clip());
              }
            _t.push(L), At.push(lt);
          } else
            P.clearRect(Jt, me, Me, Ve);
        this.drawTileImage(
          hi,
          t,
          Jt,
          me,
          Me,
          Ve,
          rr,
          un
        ), _t && !Ai ? (ci && P.restore(), this.renderedTiles.unshift(hi)) : this.renderedTiles.push(hi), this.updateUsedTiles(t.usedTiles, u, hi);
      }
    }
    return this.renderedRevision = d, this.renderedResolution = m, this.extentChanged = !this.renderedExtent_ || !Es(this.renderedExtent_, b), this.renderedExtent_ = b, this.renderedPixelRatio = h, this.renderedProjection = r, this.manageTilePyramid(
      t,
      u,
      f,
      h,
      r,
      p,
      g,
      c.getPreload()
    ), this.scheduleExpireCache(t, u), this.postRender(P, t), n.extent && P.restore(), P.imageSmoothingEnabled = !0, k !== tt.style.transform && (tt.style.transform = k), this.container;
  }
  drawTileImage(t, e, n, s, r, o, a, l) {
    const h = this.getTileImage(t);
    if (!h)
      return;
    const c = ot(this), u = e.layerStatesArray[e.layerIndex], d = u.opacity * (l ? t.getAlpha(c, e.time) : 1), f = d !== this.context.globalAlpha;
    f && (this.context.save(), this.context.globalAlpha = d), this.context.drawImage(
      h,
      a,
      a,
      h.width - 2 * a,
      h.height - 2 * a,
      n,
      s,
      r,
      o
    ), f && this.context.restore(), d !== u.opacity ? e.animate = !0 : l && t.endTransition(c);
  }
  getImage() {
    const t = this.context;
    return t ? t.canvas : null;
  }
  getTileImage(t) {
    return t.getImage();
  }
  scheduleExpireCache(t, e) {
    if (e.canExpireCache()) {
      const n = function(s, r, o) {
        const a = ot(s);
        a in o.usedTiles && s.expireCache(
          o.viewState.projection,
          o.usedTiles[a]
        );
      }.bind(null, e);
      t.postRenderFunctions.push(
        n
      );
    }
  }
  updateUsedTiles(t, e, n) {
    const s = ot(e);
    s in t || (t[s] = {}), t[s][n.getKey()] = !0;
  }
  manageTilePyramid(t, e, n, s, r, o, a, l, h) {
    const c = ot(e);
    c in t.wantedTiles || (t.wantedTiles[c] = {});
    const u = t.wantedTiles[c], d = t.tileQueue, f = n.getMinZoom(), g = t.viewState.rotation, m = g ? ua(
      t.viewState.center,
      t.viewState.resolution,
      g,
      t.size
    ) : void 0;
    let p = 0, _, y, v, x, C, w;
    for (w = f; w <= a; ++w)
      for (y = n.getTileRangeForExtentAndZ(o, w, y), v = n.getResolution(w), x = y.minX; x <= y.maxX; ++x)
        for (C = y.minY; C <= y.maxY; ++C)
          g && !n.tileCoordIntersectsViewport([w, x, C], m) || (a - w <= l ? (++p, _ = e.getTile(w, x, C, s, r), _.getState() == z.IDLE && (u[_.getKey()] = !0, d.isKeyQueued(_.getKey()) || d.enqueue([
            _,
            c,
            n.getTileCoordCenter(_.tileCoord),
            v
          ])), h !== void 0 && h(_)) : e.useTile(w, x, C, r));
    e.updateCacheSize(p, r);
  }
}
const sp = np;
class rp extends ip {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new sp(this);
  }
}
const op = rp;
class ap extends Gd {
  constructor(t) {
    super({
      extent: t.extent,
      origin: t.origin,
      origins: t.origins,
      resolutions: t.resolutions,
      tileSize: t.tileSize,
      tileSizes: t.tileSizes,
      sizes: t.sizes
    }), this.matrixIds_ = t.matrixIds;
  }
  getMatrixId(t) {
    return this.matrixIds_[t];
  }
  getMatrixIds() {
    return this.matrixIds_;
  }
}
function lp(i, t, e) {
  const n = [], s = [], r = [], o = [], a = [];
  e = e !== void 0 ? e : [];
  const l = "SupportedCRS", h = "TileMatrix", c = "Identifier", u = "ScaleDenominator", d = "TopLeftCorner", f = "TileWidth", g = "TileHeight", m = i[l], p = J(m), _ = p.getMetersPerUnit(), y = p.getAxisOrientation().substr(0, 2) == "ne";
  return i[h].sort(function(v, x) {
    return x[u] - v[u];
  }), i[h].forEach(function(v) {
    let x;
    if (e.length > 0 ? x = e.find(function(C) {
      return v[c] == C[h] ? !0 : v[c].includes(":") ? !1 : i[c] + ":" + v[c] === C[h];
    }) : x = !0, x) {
      s.push(v[c]);
      const C = v[u] * 28e-5 / _, w = v[f], S = v[g];
      y ? r.push([
        v[d][1],
        v[d][0]
      ]) : r.push(v[d]), n.push(C), o.push(
        w == S ? w : [w, S]
      ), a.push([v.MatrixWidth, v.MatrixHeight]);
    }
  }), new ap({
    extent: t,
    origins: r,
    resolutions: n,
    matrixIds: s,
    tileSizes: o,
    sizes: a
  });
}
class hp extends J2 {
  constructor(t) {
    const e = t.requestEncoding !== void 0 ? t.requestEncoding : "KVP", n = t.tileGrid;
    let s = t.urls;
    s === void 0 && t.url !== void 0 && (s = zd(t.url)), super({
      attributions: t.attributions,
      attributionsCollapsible: t.attributionsCollapsible,
      cacheSize: t.cacheSize,
      crossOrigin: t.crossOrigin,
      interpolate: t.interpolate,
      projection: t.projection,
      reprojectionErrorThreshold: t.reprojectionErrorThreshold,
      tileClass: t.tileClass,
      tileGrid: n,
      tileLoadFunction: t.tileLoadFunction,
      tilePixelRatio: t.tilePixelRatio,
      urls: s,
      wrapX: t.wrapX !== void 0 ? t.wrapX : !1,
      transition: t.transition,
      zDirection: t.zDirection
    }), this.version_ = t.version !== void 0 ? t.version : "1.0.0", this.format_ = t.format !== void 0 ? t.format : "image/jpeg", this.dimensions_ = t.dimensions !== void 0 ? t.dimensions : {}, this.layer_ = t.layer, this.matrixSet_ = t.matrixSet, this.style_ = t.style, this.requestEncoding_ = e, this.setKey(this.getKeyForDimensions_()), s && s.length > 0 && (this.tileUrlFunction = ba(
      s.map(this.createFromWMTSTemplate.bind(this))
    ));
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.setTileUrlFunction(
      ba(
        t.map(this.createFromWMTSTemplate.bind(this))
      ),
      e
    );
  }
  getDimensions() {
    return this.dimensions_;
  }
  getFormat() {
    return this.format_;
  }
  getLayer() {
    return this.layer_;
  }
  getMatrixSet() {
    return this.matrixSet_;
  }
  getRequestEncoding() {
    return this.requestEncoding_;
  }
  getStyle() {
    return this.style_;
  }
  getVersion() {
    return this.version_;
  }
  getKeyForDimensions_() {
    let t = 0;
    const e = [];
    for (const n in this.dimensions_)
      e[t++] = n + "-" + this.dimensions_[n];
    return e.join("/");
  }
  updateDimensions(t) {
    Object.assign(this.dimensions_, t), this.setKey(this.getKeyForDimensions_());
  }
  createFromWMTSTemplate(t) {
    const e = this.requestEncoding_, n = {
      layer: this.layer_,
      style: this.style_,
      tilematrixset: this.matrixSet_
    };
    e == "KVP" && Object.assign(n, {
      Service: "WMTS",
      Request: "GetTile",
      Version: this.version_,
      Format: this.format_
    }), t = e == "KVP" ? ac(t, n) : t.replace(/\{(\w+?)\}/g, function(o, a) {
      return a.toLowerCase() in n ? n[a.toLowerCase()] : o;
    });
    const s = this.tileGrid, r = this.dimensions_;
    return function(o, a, l) {
      if (o) {
        const h = {
          TileMatrix: s.getMatrixId(o[0]),
          TileCol: o[1],
          TileRow: o[2]
        };
        Object.assign(h, r);
        let c = t;
        return e == "KVP" ? c = ac(c, h) : c = c.replace(/\{(\w+?)\}/g, function(u, d) {
          return h[d];
        }), c;
      } else
        return;
    };
  }
}
const cp = hp;
function up(i, t) {
  const n = i.Contents.Layer.find(function(T) {
    return T.Identifier == t.layer;
  });
  if (!n)
    return null;
  const s = i.Contents.TileMatrixSet;
  let r;
  n.TileMatrixSetLink.length > 1 ? "projection" in t ? r = n.TileMatrixSetLink.findIndex(function(T) {
    const ft = s.find(function(P) {
      return P.Identifier == T.TileMatrixSet;
    }).SupportedCRS, F = J(ft), k = J(t.projection);
    return F && k ? Ie(F, k) : ft == t.projection;
  }) : r = n.TileMatrixSetLink.findIndex(function(T) {
    return T.TileMatrixSet == t.matrixSet;
  }) : r = 0, r < 0 && (r = 0);
  const o = n.TileMatrixSetLink[r].TileMatrixSet, a = n.TileMatrixSetLink[r].TileMatrixSetLimits;
  let l = n.Format[0];
  "format" in t && (l = t.format), r = n.Style.findIndex(function(T) {
    return "style" in t ? T.Title == t.style : T.isDefault;
  }), r < 0 && (r = 0);
  const h = n.Style[r].Identifier, c = {};
  "Dimension" in n && n.Dimension.forEach(function(T, $, ft) {
    const F = T.Identifier;
    let k = T.Default;
    k === void 0 && (k = T.Value[0]), c[F] = k;
  });
  const d = i.Contents.TileMatrixSet.find(function(T) {
    return T.Identifier == o;
  });
  let f;
  const g = d.SupportedCRS;
  if (g && (f = J(g)), "projection" in t) {
    const T = J(t.projection);
    T && (!f || Ie(T, f)) && (f = T);
  }
  let m = !1;
  const p = f.getAxisOrientation().substr(0, 2) == "ne";
  let _ = d.TileMatrix[0], y = {
    MinTileCol: 0,
    MinTileRow: 0,
    MaxTileCol: _.MatrixWidth - 1,
    MaxTileRow: _.MatrixHeight - 1
  };
  if (a) {
    y = a[a.length - 1];
    const T = d.TileMatrix.find(
      ($) => $.Identifier === y.TileMatrix || d.Identifier + ":" + $.Identifier === y.TileMatrix
    );
    T && (_ = T);
  }
  const v = _.ScaleDenominator * 28e-5 / f.getMetersPerUnit(), x = p ? [_.TopLeftCorner[1], _.TopLeftCorner[0]] : _.TopLeftCorner, C = _.TileWidth * v, w = _.TileHeight * v;
  let S = d.BoundingBox;
  S && p && (S = [
    S[1],
    S[0],
    S[3],
    S[2]
  ]);
  let b = [
    x[0] + C * y.MinTileCol,
    x[1] - w * (1 + y.MaxTileRow),
    x[0] + C * (1 + y.MaxTileCol),
    x[1] - w * y.MinTileRow
  ];
  if (S !== void 0 && !yi(S, b)) {
    const T = n.WGS84BoundingBox, $ = J("EPSG:4326").getExtent();
    if (b = S, T)
      m = T[0] === $[0] && T[2] === $[2];
    else {
      const ft = Yu(
        S,
        d.SupportedCRS,
        "EPSG:4326"
      );
      m = ft[0] - 1e-10 <= $[0] && ft[2] + 1e-10 >= $[2];
    }
  }
  const A = lp(
    d,
    b,
    a
  ), G = [];
  let V = t.requestEncoding;
  if (V = V !== void 0 ? V : "", "OperationsMetadata" in i && "GetTile" in i.OperationsMetadata) {
    const T = i.OperationsMetadata.GetTile.DCP.HTTP.Get;
    for (let $ = 0, ft = T.length; $ < ft; ++$)
      if (T[$].Constraint) {
        const k = T[$].Constraint.find(function(P) {
          return P.name == "GetEncoding";
        }).AllowedValues.Value;
        if (V === "" && (V = k[0]), V === "KVP")
          k.includes("KVP") && G.push(T[$].href);
        else
          break;
      } else
        T[$].href && (V = "KVP", G.push(T[$].href));
  }
  return G.length === 0 && (V = "REST", n.ResourceURL.forEach(function(T) {
    T.resourceType === "tile" && (l = T.format, G.push(T.template));
  })), {
    urls: G,
    layer: t.layer,
    matrixSet: o,
    format: l,
    projection: f,
    requestEncoding: V,
    tileGrid: A,
    style: h,
    dimensions: c,
    wrapX: m,
    crossOrigin: t.crossOrigin
  };
}
class Zd {
  constructor() {
    this.dataProjection = void 0, this.defaultFeatureProjection = void 0, this.supportedMediaTypes = null;
  }
  getReadOptions(t, e) {
    if (e) {
      let n = e.dataProjection ? J(e.dataProjection) : this.readProjection(t);
      e.extent && n && n.getUnits() === "tile-pixels" && (n = J(n), n.setWorldExtent(e.extent)), e = {
        dataProjection: n,
        featureProjection: e.featureProjection
      };
    }
    return this.adaptOptions(e);
  }
  adaptOptions(t) {
    return Object.assign(
      {
        dataProjection: this.dataProjection,
        featureProjection: this.defaultFeatureProjection
      },
      t
    );
  }
  getType() {
    return W();
  }
  readFeature(t, e) {
    return W();
  }
  readFeatures(t, e) {
    return W();
  }
  readGeometry(t, e) {
    return W();
  }
  readProjection(t) {
    return W();
  }
  writeFeature(t, e) {
    return W();
  }
  writeFeatures(t, e) {
    return W();
  }
  writeGeometry(t, e) {
    return W();
  }
}
function js(i, t, e) {
  const n = e ? J(e.featureProjection) : null, s = e ? J(e.dataProjection) : null;
  let r;
  if (n && s && !Ie(n, s) ? r = (t ? i.clone() : i).transform(
    t ? n : s,
    t ? s : n
  ) : r = i, t && e && e.decimals !== void 0) {
    const o = Math.pow(10, e.decimals), a = function(l) {
      for (let h = 0, c = l.length; h < c; ++h)
        l[h] = Math.round(l[h] * o) / o;
      return l;
    };
    r === i && (r = i.clone()), r.applyTransform(a);
  }
  return r;
}
function Tl(i, t) {
  const e = t ? J(t.featureProjection) : null, n = t ? J(t.dataProjection) : null;
  return e && n && !Ie(e, n) ? Yu(i, n, e) : i;
}
class jr extends rn {
  constructor(t, e, n) {
    if (super(), this.ends_ = [], this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, Array.isArray(t[0]))
      this.setCoordinates(
        t,
        e
      );
    else if (e !== void 0 && n)
      this.setFlatCoordinates(
        e,
        t
      ), this.ends_ = n;
    else {
      let s = this.getLayout();
      const r = t, o = [], a = [];
      for (let l = 0, h = r.length; l < h; ++l) {
        const c = r[l];
        l === 0 && (s = c.getLayout()), Kt(o, c.getFlatCoordinates()), a.push(o.length);
      }
      this.setFlatCoordinates(s, o), this.ends_ = a;
    }
  }
  appendLineString(t) {
    this.flatCoordinates ? Kt(this.flatCoordinates, t.getFlatCoordinates().slice()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new jr(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < sn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      ul(
        this.flatCoordinates,
        0,
        this.ends_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), fl(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      this.maxDelta_,
      !1,
      t,
      e,
      n,
      s
    ));
  }
  getCoordinateAtM(t, e, n) {
    return this.layout != "XYM" && this.layout != "XYZM" || this.flatCoordinates.length === 0 ? null : (e = e !== void 0 ? e : !1, n = n !== void 0 ? n : !1, nm(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t,
      e,
      n
    ));
  }
  getCoordinates() {
    return Ps(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride
    );
  }
  getEnds() {
    return this.ends_;
  }
  getLineString(t) {
    return t < 0 || this.ends_.length <= t ? null : new As(
      this.flatCoordinates.slice(
        t === 0 ? 0 : this.ends_[t - 1],
        this.ends_[t]
      ),
      this.layout
    );
  }
  getLineStrings() {
    const t = this.flatCoordinates, e = this.ends_, n = this.layout, s = [];
    let r = 0;
    for (let o = 0, a = e.length; o < a; ++o) {
      const l = e[o], h = new As(
        t.slice(r, l),
        n
      );
      s.push(h), r = l;
    }
    return s;
  }
  getFlatMidpoints() {
    const t = [], e = this.flatCoordinates;
    let n = 0;
    const s = this.ends_, r = this.stride;
    for (let o = 0, a = s.length; o < a; ++o) {
      const l = s[o], h = md(
        e,
        n,
        l,
        r,
        0.5
      );
      Kt(t, h), n = l;
    }
    return t;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], n = [];
    return e.length = Hg(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t,
      e,
      0,
      n
    ), new jr(e, "XY", n);
  }
  getType() {
    return "MultiLineString";
  }
  intersectsExtent(t) {
    return Qg(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 2), this.flatCoordinates || (this.flatCoordinates = []);
    const n = gl(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.ends_
    );
    this.flatCoordinates.length = n.length === 0 ? 0 : n[n.length - 1], this.changed();
  }
}
const Il = jr;
class Pl extends rn {
  constructor(t, e) {
    super(), e && !Array.isArray(t[0]) ? this.setFlatCoordinates(
      e,
      t
    ) : this.setCoordinates(
      t,
      e
    );
  }
  appendPoint(t) {
    this.flatCoordinates ? Kt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.changed();
  }
  clone() {
    const t = new Pl(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    if (s < sn(this.getExtent(), t, e))
      return s;
    const r = this.flatCoordinates, o = this.stride;
    for (let a = 0, l = r.length; a < l; a += o) {
      const h = Vi(
        t,
        e,
        r[a],
        r[a + 1]
      );
      if (h < s) {
        s = h;
        for (let c = 0; c < o; ++c)
          n[c] = r[a + c];
        n.length = o;
      }
    }
    return s;
  }
  getCoordinates() {
    return vi(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getPoint(t) {
    const e = this.flatCoordinates ? this.flatCoordinates.length / this.stride : 0;
    return t < 0 || e <= t ? null : new si(
      this.flatCoordinates.slice(
        t * this.stride,
        (t + 1) * this.stride
      ),
      this.layout
    );
  }
  getPoints() {
    const t = this.flatCoordinates, e = this.layout, n = this.stride, s = [];
    for (let r = 0, o = t.length; r < o; r += n) {
      const a = new si(t.slice(r, r + n), e);
      s.push(a);
    }
    return s;
  }
  getType() {
    return "MultiPoint";
  }
  intersectsExtent(t) {
    const e = this.flatCoordinates, n = this.stride;
    for (let s = 0, r = e.length; s < r; s += n) {
      const o = e[s], a = e[s + 1];
      if (qa(t, o, a))
        return !0;
    }
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = xo(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const wo = Pl;
function dp(i, t, e, n) {
  const s = [];
  let r = fe();
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = wu(
      i,
      t,
      l[0],
      n
    ), s.push((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), t = l[l.length - 1];
  }
  return s;
}
class Kr extends rn {
  constructor(t, e, n) {
    if (super(), this.endss_ = [], this.flatInteriorPointsRevision_ = -1, this.flatInteriorPoints_ = null, this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, this.orientedRevision_ = -1, this.orientedFlatCoordinates_ = null, !n && !Array.isArray(t[0])) {
      let s = this.getLayout();
      const r = t, o = [], a = [];
      for (let l = 0, h = r.length; l < h; ++l) {
        const c = r[l];
        l === 0 && (s = c.getLayout());
        const u = o.length, d = c.getEnds();
        for (let f = 0, g = d.length; f < g; ++f)
          d[f] += u;
        Kt(o, c.getFlatCoordinates()), a.push(d);
      }
      e = s, t = o, n = a;
    }
    e !== void 0 && n ? (this.setFlatCoordinates(
      e,
      t
    ), this.endss_ = n) : this.setCoordinates(
      t,
      e
    );
  }
  appendPolygon(t) {
    let e;
    if (!this.flatCoordinates)
      this.flatCoordinates = t.getFlatCoordinates().slice(), e = t.getEnds().slice(), this.endss_.push();
    else {
      const n = this.flatCoordinates.length;
      Kt(this.flatCoordinates, t.getFlatCoordinates()), e = t.getEnds().slice();
      for (let s = 0, r = e.length; s < r; ++s)
        e[s] += n;
    }
    this.endss_.push(e), this.changed();
  }
  clone() {
    const t = this.endss_.length, e = new Array(t);
    for (let s = 0; s < t; ++s)
      e[s] = this.endss_[s].slice();
    const n = new Kr(
      this.flatCoordinates.slice(),
      this.layout,
      e
    );
    return n.applyProperties(this), n;
  }
  closestPointXY(t, e, n, s) {
    return s < sn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Zg(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), Vg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      n,
      s
    ));
  }
  containsXY(t, e) {
    return qg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return jg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), Nh(
      e,
      0,
      this.endss_,
      this.stride,
      t
    )) : e = this.flatCoordinates, va(
      e,
      0,
      this.endss_,
      this.stride
    );
  }
  getEndss() {
    return this.endss_;
  }
  getFlatInteriorPoints() {
    if (this.flatInteriorPointsRevision_ != this.getRevision()) {
      const t = dp(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride
      );
      this.flatInteriorPoints_ = Jg(
        this.getOrientedFlatCoordinates(),
        0,
        this.endss_,
        this.stride,
        t
      ), this.flatInteriorPointsRevision_ = this.getRevision();
    }
    return this.flatInteriorPoints_;
  }
  getInteriorPoints() {
    return new wo(this.getFlatInteriorPoints().slice(), "XYM");
  }
  getOrientedFlatCoordinates() {
    if (this.orientedRevision_ != this.getRevision()) {
      const t = this.flatCoordinates;
      i1(t, 0, this.endss_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = Nh(
        this.orientedFlatCoordinates_,
        0,
        this.endss_,
        this.stride
      )), this.orientedRevision_ = this.getRevision();
    }
    return this.orientedFlatCoordinates_;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], n = [];
    return e.length = Yg(
      this.flatCoordinates,
      0,
      this.endss_,
      this.stride,
      Math.sqrt(t),
      e,
      0,
      n
    ), new Kr(e, "XY", n);
  }
  getPolygon(t) {
    if (t < 0 || this.endss_.length <= t)
      return null;
    let e;
    if (t === 0)
      e = 0;
    else {
      const r = this.endss_[t - 1];
      e = r[r.length - 1];
    }
    const n = this.endss_[t].slice(), s = n[n.length - 1];
    if (e !== 0)
      for (let r = 0, o = n.length; r < o; ++r)
        n[r] -= e;
    return new Vn(
      this.flatCoordinates.slice(e, s),
      this.layout,
      n
    );
  }
  getPolygons() {
    const t = this.layout, e = this.flatCoordinates, n = this.endss_, s = [];
    let r = 0;
    for (let o = 0, a = n.length; o < a; ++o) {
      const l = n[o].slice(), h = l[l.length - 1];
      if (r !== 0)
        for (let u = 0, d = l.length; u < d; ++u)
          l[u] -= r;
      const c = new Vn(
        e.slice(r, h),
        t,
        l
      );
      s.push(c), r = h;
    }
    return s;
  }
  getType() {
    return "MultiPolygon";
  }
  intersectsExtent(t) {
    return t1(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 3), this.flatCoordinates || (this.flatCoordinates = []);
    const n = Wg(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.endss_
    );
    if (n.length === 0)
      this.flatCoordinates.length = 0;
    else {
      const s = n[n.length - 1];
      this.flatCoordinates.length = s.length === 0 ? 0 : s[s.length - 1];
    }
    this.changed();
  }
}
const Al = Kr;
class qr extends Ju {
  constructor(t) {
    super(), this.geometries_ = t || null, this.changeEventsKeys_ = [], this.listenGeometriesChange_();
  }
  unlistenGeometriesChange_() {
    this.changeEventsKeys_.forEach(pt), this.changeEventsKeys_.length = 0;
  }
  listenGeometriesChange_() {
    if (!!this.geometries_)
      for (let t = 0, e = this.geometries_.length; t < e; ++t)
        this.changeEventsKeys_.push(
          et(this.geometries_[t], X.CHANGE, this.changed, this)
        );
  }
  clone() {
    const t = new qr(null);
    return t.setGeometries(this.geometries_), t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    if (s < sn(this.getExtent(), t, e))
      return s;
    const r = this.geometries_;
    for (let o = 0, a = r.length; o < a; ++o)
      s = r[o].closestPointXY(
        t,
        e,
        n,
        s
      );
    return s;
  }
  containsXY(t, e) {
    const n = this.geometries_;
    for (let s = 0, r = n.length; s < r; ++s)
      if (n[s].containsXY(t, e))
        return !0;
    return !1;
  }
  computeExtent(t) {
    Zs(t);
    const e = this.geometries_;
    for (let n = 0, s = e.length; n < s; ++n)
      Su(t, e[n].getExtent());
    return t;
  }
  getGeometries() {
    return lc(this.geometries_);
  }
  getGeometriesArray() {
    return this.geometries_;
  }
  getGeometriesArrayRecursive() {
    let t = [];
    const e = this.geometries_;
    for (let n = 0, s = e.length; n < s; ++n)
      e[n].getType() === this.getType() ? t = t.concat(
        e[n].getGeometriesArrayRecursive()
      ) : t.push(e[n]);
    return t;
  }
  getSimplifiedGeometry(t) {
    if (this.simplifiedGeometryRevision !== this.getRevision() && (this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = this.getRevision()), t < 0 || this.simplifiedGeometryMaxMinSquaredTolerance !== 0 && t < this.simplifiedGeometryMaxMinSquaredTolerance)
      return this;
    const e = [], n = this.geometries_;
    let s = !1;
    for (let r = 0, o = n.length; r < o; ++r) {
      const a = n[r], l = a.getSimplifiedGeometry(t);
      e.push(l), l !== a && (s = !0);
    }
    if (s) {
      const r = new qr(null);
      return r.setGeometriesArray(e), r;
    } else
      return this.simplifiedGeometryMaxMinSquaredTolerance = t, this;
  }
  getType() {
    return "GeometryCollection";
  }
  intersectsExtent(t) {
    const e = this.geometries_;
    for (let n = 0, s = e.length; n < s; ++n)
      if (e[n].intersectsExtent(t))
        return !0;
    return !1;
  }
  isEmpty() {
    return this.geometries_.length === 0;
  }
  rotate(t, e) {
    const n = this.geometries_;
    for (let s = 0, r = n.length; s < r; ++s)
      n[s].rotate(t, e);
    this.changed();
  }
  scale(t, e, n) {
    n || (n = Ri(this.getExtent()));
    const s = this.geometries_;
    for (let r = 0, o = s.length; r < o; ++r)
      s[r].scale(t, e, n);
    this.changed();
  }
  setGeometries(t) {
    this.setGeometriesArray(lc(t));
  }
  setGeometriesArray(t) {
    this.unlistenGeometriesChange_(), this.geometries_ = t, this.listenGeometriesChange_(), this.changed();
  }
  applyTransform(t) {
    const e = this.geometries_;
    for (let n = 0, s = e.length; n < s; ++n)
      e[n].applyTransform(t);
    this.changed();
  }
  translate(t, e) {
    const n = this.geometries_;
    for (let s = 0, r = n.length; s < r; ++s)
      n[s].translate(t, e);
    this.changed();
  }
  disposeInternal() {
    this.unlistenGeometriesChange_(), super.disposeInternal();
  }
}
function lc(i) {
  const t = [];
  for (let e = 0, n = i.length; e < n; ++e)
    t.push(i[e].clone());
  return t;
}
const Vd = qr;
class fp extends Zd {
  constructor() {
    super();
  }
  getType() {
    return "json";
  }
  readFeature(t, e) {
    return this.readFeatureFromObject(
      Er(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatures(t, e) {
    return this.readFeaturesFromObject(
      Er(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatureFromObject(t, e) {
    return W();
  }
  readFeaturesFromObject(t, e) {
    return W();
  }
  readGeometry(t, e) {
    return this.readGeometryFromObject(
      Er(t),
      this.getReadOptions(t, e)
    );
  }
  readGeometryFromObject(t, e) {
    return W();
  }
  readProjection(t) {
    return this.readProjectionFromObject(Er(t));
  }
  readProjectionFromObject(t) {
    return W();
  }
  writeFeature(t, e) {
    return JSON.stringify(this.writeFeatureObject(t, e));
  }
  writeFeatureObject(t, e) {
    return W();
  }
  writeFeatures(t, e) {
    return JSON.stringify(this.writeFeaturesObject(t, e));
  }
  writeFeaturesObject(t, e) {
    return W();
  }
  writeGeometry(t, e) {
    return JSON.stringify(this.writeGeometryObject(t, e));
  }
  writeGeometryObject(t, e) {
    return W();
  }
}
function Er(i) {
  if (typeof i == "string") {
    const t = JSON.parse(i);
    return t || null;
  } else
    return i !== null ? i : null;
}
const gp = fp;
class mp extends gp {
  constructor(t) {
    t = t || {}, super(), this.dataProjection = J(
      t.dataProjection ? t.dataProjection : "EPSG:4326"
    ), t.featureProjection && (this.defaultFeatureProjection = J(t.featureProjection)), this.geometryName_ = t.geometryName, this.extractGeometryName_ = t.extractGeometryName, this.supportedMediaTypes = [
      "application/geo+json",
      "application/vnd.geo+json"
    ];
  }
  readFeatureFromObject(t, e) {
    let n = null;
    t.type === "Feature" ? n = t : n = {
      type: "Feature",
      geometry: t,
      properties: null
    };
    const s = La(n.geometry, e), r = new on();
    return this.geometryName_ ? r.setGeometryName(this.geometryName_) : this.extractGeometryName_ && "geometry_name" in n !== void 0 && r.setGeometryName(n.geometry_name), r.setGeometry(s), "id" in n && r.setId(n.id), n.properties && r.setProperties(n.properties, !0), r;
  }
  readFeaturesFromObject(t, e) {
    const n = t;
    let s = null;
    if (n.type === "FeatureCollection") {
      const r = t;
      s = [];
      const o = r.features;
      for (let a = 0, l = o.length; a < l; ++a)
        s.push(this.readFeatureFromObject(o[a], e));
    } else
      s = [this.readFeatureFromObject(t, e)];
    return s;
  }
  readGeometryFromObject(t, e) {
    return La(t, e);
  }
  readProjectionFromObject(t) {
    const e = t.crs;
    let n;
    return e ? e.type == "name" ? n = J(e.properties.name) : e.type === "EPSG" ? n = J("EPSG:" + e.properties.code) : Y(!1, 36) : n = this.dataProjection, n;
  }
  writeFeatureObject(t, e) {
    e = this.adaptOptions(e);
    const n = {
      type: "Feature",
      geometry: null,
      properties: null
    }, s = t.getId();
    if (s !== void 0 && (n.id = s), !t.hasProperties())
      return n;
    const r = t.getProperties(), o = t.getGeometry();
    return o && (n.geometry = Ta(o, e), delete r[t.getGeometryName()]), Gn(r) || (n.properties = r), n;
  }
  writeFeaturesObject(t, e) {
    e = this.adaptOptions(e);
    const n = [];
    for (let s = 0, r = t.length; s < r; ++s)
      n.push(this.writeFeatureObject(t[s], e));
    return {
      type: "FeatureCollection",
      features: n
    };
  }
  writeGeometryObject(t, e) {
    return Ta(t, this.adaptOptions(e));
  }
}
function La(i, t) {
  if (!i)
    return null;
  let e;
  switch (i.type) {
    case "Point": {
      e = _p(i);
      break;
    }
    case "LineString": {
      e = yp(
        i
      );
      break;
    }
    case "Polygon": {
      e = Mp(i);
      break;
    }
    case "MultiPoint": {
      e = xp(
        i
      );
      break;
    }
    case "MultiLineString": {
      e = vp(
        i
      );
      break;
    }
    case "MultiPolygon": {
      e = Cp(
        i
      );
      break;
    }
    case "GeometryCollection": {
      e = pp(
        i
      );
      break;
    }
    default:
      throw new Error("Unsupported GeoJSON type: " + i.type);
  }
  return js(e, !1, t);
}
function pp(i, t) {
  const e = i.geometries.map(
    function(n) {
      return La(n, t);
    }
  );
  return new Vd(e);
}
function _p(i) {
  return new si(i.coordinates);
}
function yp(i) {
  return new As(i.coordinates);
}
function vp(i) {
  return new Il(i.coordinates);
}
function xp(i) {
  return new wo(i.coordinates);
}
function Cp(i) {
  return new Al(i.coordinates);
}
function Mp(i) {
  return new Vn(i.coordinates);
}
function Ta(i, t) {
  i = js(i, !0, t);
  const e = i.getType();
  let n;
  switch (e) {
    case "Point": {
      n = Lp(i);
      break;
    }
    case "LineString": {
      n = wp(
        i
      );
      break;
    }
    case "Polygon": {
      n = Tp(
        i,
        t
      );
      break;
    }
    case "MultiPoint": {
      n = Rp(
        i
      );
      break;
    }
    case "MultiLineString": {
      n = Sp(
        i
      );
      break;
    }
    case "MultiPolygon": {
      n = bp(
        i,
        t
      );
      break;
    }
    case "GeometryCollection": {
      n = Ep(
        i,
        t
      );
      break;
    }
    case "Circle": {
      n = {
        type: "GeometryCollection",
        geometries: []
      };
      break;
    }
    default:
      throw new Error("Unsupported geometry type: " + e);
  }
  return n;
}
function Ep(i, t) {
  return t = Object.assign({}, t), delete t.featureProjection, {
    type: "GeometryCollection",
    geometries: i.getGeometriesArray().map(function(n) {
      return Ta(n, t);
    })
  };
}
function wp(i, t) {
  return {
    type: "LineString",
    coordinates: i.getCoordinates()
  };
}
function Sp(i, t) {
  return {
    type: "MultiLineString",
    coordinates: i.getCoordinates()
  };
}
function Rp(i, t) {
  return {
    type: "MultiPoint",
    coordinates: i.getCoordinates()
  };
}
function bp(i, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "MultiPolygon",
    coordinates: i.getCoordinates(e)
  };
}
function Lp(i, t) {
  return {
    type: "Point",
    coordinates: i.getCoordinates()
  };
}
function Tp(i, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "Polygon",
    coordinates: i.getCoordinates(e)
  };
}
const Ia = mp;
class it {
  static sendEvent(t, e) {
    dispatchEvent(new CustomEvent(t, { detail: e }));
  }
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ud = { ATTRIBUTE: 1, CHILD: 2, PROPERTY: 3, BOOLEAN_ATTRIBUTE: 4, EVENT: 5, ELEMENT: 6 }, Ol = (i) => (...t) => ({ _$litDirective$: i, values: t });
class Nl {
  constructor(t) {
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AT(t, e, n) {
    this._$Ct = t, this._$AM = e, this._$Ci = n;
  }
  _$AS(t, e) {
    return this.update(t, e);
  }
  update(t, e) {
    return this.render(...e);
  }
}
/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const { I: Ip } = Qf, wr = (i, t) => t === void 0 ? (i == null ? void 0 : i._$litType$) !== void 0 : (i == null ? void 0 : i._$litType$) === t, hc = () => document.createComment(""), cc = (i, t, e) => {
  var n;
  const s = i._$AA.parentNode, r = t === void 0 ? i._$AB : t._$AA;
  if (e === void 0) {
    const o = s.insertBefore(hc(), r), a = s.insertBefore(hc(), r);
    e = new Ip(o, a, i, i.options);
  } else {
    const o = e._$AB.nextSibling, a = e._$AM, l = a !== i;
    if (l) {
      let h;
      (n = e._$AQ) === null || n === void 0 || n.call(e, i), e._$AM = i, e._$AP !== void 0 && (h = i._$AU) !== a._$AU && e._$AP(h);
    }
    if (o !== r || l) {
      let h = e._$AA;
      for (; h !== o; ) {
        const c = h.nextSibling;
        s.insertBefore(h, r), h = c;
      }
    }
  }
  return e;
}, Pp = {}, uc = (i, t = Pp) => i._$AH = t, dc = (i) => i._$AH, Ap = (i) => {
  i._$AR();
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Wd = Ol(class extends Nl {
  constructor(i) {
    super(i), this.et = /* @__PURE__ */ new WeakMap();
  }
  render(i) {
    return [i];
  }
  update(i, [t]) {
    if (wr(this.it) && (!wr(t) || this.it.strings !== t.strings)) {
      const e = dc(i).pop();
      let n = this.et.get(this.it.strings);
      if (n === void 0) {
        const s = document.createDocumentFragment();
        n = mu(bt, s), n.setConnected(!1), this.et.set(this.it.strings, n);
      }
      uc(n, [e]), cc(n, void 0, e);
    }
    if (wr(t)) {
      if (!wr(this.it) || this.it.strings !== t.strings) {
        const e = this.et.get(t.strings);
        if (e !== void 0) {
          const n = dc(e).pop();
          Ap(i), cc(i, void 0, n), uc(i, [n]);
        }
      }
      this.it = t;
    } else
      this.it = void 0;
    return this.render(t);
  }
});
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class Pa extends Nl {
  constructor(t) {
    if (super(t), this.it = bt, t.type !== Ud.CHILD)
      throw Error(this.constructor.directiveName + "() can only be used in child bindings");
  }
  render(t) {
    if (t === bt || t == null)
      return this._t = void 0, this.it = t;
    if (t === Ei)
      return t;
    if (typeof t != "string")
      throw Error(this.constructor.directiveName + "() called with a non-string value");
    if (t === this.it)
      return this._t;
    this.it = t;
    const e = [t];
    return e.raw = e, this._t = { _$litType$: this.constructor.resultType, strings: e, values: [] };
  }
}
Pa.directiveName = "unsafeHTML", Pa.resultType = 1;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class Aa extends Pa {
}
Aa.directiveName = "unsafeSVG", Aa.resultType = 2;
const Le = Ol(Aa);
let Hd = "", Xd = !1, Yd = "", jd, Kd, qd, Ge = [], Jd, Qd = -1, tf = -1;
function Op(i) {
  Hd = i;
}
function Np() {
  return Hd;
}
function Fp(i) {
  Xd = i;
}
function Dp() {
  return Xd;
}
function kp(i) {
  Yd = i;
}
function Gp() {
  return Yd;
}
function $p(i) {
  jd = i;
}
function Bp() {
  return jd;
}
function zp(i) {
  Kd = i;
}
function Zp() {
  return Kd;
}
function Vp(i) {
  qd = i;
}
function Up() {
  return qd;
}
function Wp(i, t, e) {
  Ge.push({
    id: t,
    type: e,
    feature: i
  });
}
function Hp(i) {
  const t = Ge.findIndex((e) => e.id === i);
  t !== -1 && Ge.splice(t, 1);
}
function Xp() {
  Ge.splice(-1);
}
function Yp(i) {
  const t = Ge.findIndex((e) => e.id === i);
  return t !== -1 ? Ge[t].feature : void 0;
}
function jp(i) {
  const t = Ge.findIndex((e) => e.id === i);
  return t !== -1 ? Ge[t].type : "";
}
function Kp() {
  var i;
  (i = Ge.find((t) => t.feature.get("isSelected"))) == null || i.feature.set("isSelected", void 0);
}
function qp() {
  return Ge.map((i) => i.feature);
}
function Jp(i) {
  Jd = i;
}
function Qp() {
  return Jd;
}
function t_(i) {
  Qd = i;
}
function e_() {
  return Qd;
}
function i_(i) {
  tf = i;
}
function n_() {
  return tf;
}
function M() {
  return {
    setTheme: Op,
    getTheme: Np,
    setCustomDisplay: Fp,
    isCustomDisplay: Dp,
    setTargetBoxSize: kp,
    getTargetBoxSize: Gp,
    setGeolocation: $p,
    getGeolocation: Bp,
    setOptions: zp,
    getOptions: Zp,
    setMap: Vp,
    getMap: Up,
    addSelectedFeature: Wp,
    removeSelectedFeature: Hp,
    removeLastSelectedFeature: Xp,
    getSelectedFeature: Yp,
    getCurrentFeatureType: jp,
    getSelectedFeatures: qp,
    unselectFeatures: Kp,
    setBorderConstraint: Jp,
    getBorderConstraint: Qp,
    setCurrentItemId: t_,
    getCurrentItemId: e_,
    setMaxElement: i_,
    getMaxElement: n_
  };
}
const s_ = `@media only screen and (min-width: 351px) and (max-width: 995px){.box-element{left:calc(50% - 167px);width:calc(100% - 30px);max-width:302px}}@media only screen and (max-width: 350px){.box-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 996px){.box-element{left:calc((100% - (var(--select-box-width) + 30px)) / 2);width:calc(var(--select-box-width))}}.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color);font-family:sans-serif;display:flex;z-index:5}.box-text-container{width:calc(100% - 80px)}.box-icon-container{width:80px;display:flex}.box-element-title{display:flex}.box-element-title-text{width:900%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color);width:90%}.position-icon{display:flex;justify-content:flex-end;width:50%}.icon-container{width:36px;height:36px;background-color:var(--select-icon-background);border-radius:var(--icon-border-radius)}.icon-container>svg{display:block;margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size)!important;height:var(--svg-icon-size)!important}.icon-container>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
class Wt {
  static setEvent(t, e) {
    M().getMap().getView().on(t, e);
  }
  static unsetEvent(t, e) {
    M().getMap().getView().on(t, e);
  }
  static registerWindowListener(t, e, n) {
    window.addEventListener(t, () => {
      Wt.unsetEvent(e, n), Wt.setEvent(e, n);
    });
  }
  static registerBorderConstaintMapEvent(t, e) {
    M().getOptions().border.url !== "" && Wt.registerWindowListener(
      "border-contraint-enabled",
      t,
      e
    ), Wt.setEvent(t, e);
  }
  static setCursorEvent() {
    M().getMap().on("movestart", () => {
      M().getMap().getViewport().style.cursor = "all-scroll";
    }), M().getMap().on("moveend", () => {
      M().getMap().getViewport().style.cursor = "default";
    });
  }
  static setResizeEvent(t, e) {
    const n = M().getMap().getSize();
    n && t.style.setProperty(e, n[0] * 0.33 + "px"), window.addEventListener("resize", () => {
      const s = M().getMap().getSize();
      s && t.style.setProperty(e, s[0] * 0.33 + "px");
    });
  }
}
class ef {
  static getAddressFromCoordinate(t) {
    return fetch(`https://api3.geo.admin.ch/rest/services/api/MapServer/identify?mapExtent=0,0,100,100&imageDisplay=100,100,100&tolerance=20&geometryType=esriGeometryPoint&geometry=${t[0]},${t[1]}&layers=all:ch.bfs.gebaeude_wohnungs_register&returnGeometry=false&sr=2056`).then((e) => e.json());
  }
}
class rt {
  static zoomInLabel() {
    const t = document.createElement("div"), e = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    return e.setAttributeNS(null, "width", "32"), e.setAttributeNS(null, "height", "32"), e.setAttributeNS(null, "viewBox", "0 0 32 32"), e.innerHTML = ` 
                      <g class="Plus" clip-path="url(#a)">
                        <g class="icon">
                          <path d="M5 16H27M16 5V27" class="Vector"/>
                        </g>
                      </g>
                      <defs>
                        <clipPath id="a" class="a">
                          <path fill="#fff" d="M0 0H32V32H0z"/>
                        </clipPath>
                      </defs>
                    `, t.appendChild(e), t;
  }
  static zoomOutLabel() {
    const t = document.createElement("div"), e = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    return e.setAttributeNS(null, "width", "32"), e.setAttributeNS(null, "height", "32"), e.setAttributeNS(null, "viewBox", "0 0 32 32"), e.innerHTML = ` 
                      <g class="Minus" clip-path="url(#a)">
                      <g class="icon">
                        <path d="M5 16H27" class="Vector"/>
                      </g>
                    </g>
                    <defs>
                      <clipPath id="a" class="a">
                        <path fill="#fff" d="M0 0H32V32H0z"/>
                      </clipPath>
                    </defs>
                    `, t.appendChild(e), t;
  }
  static fullScreenLabel() {
    const t = document.createElement("div"), e = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    return e.setAttributeNS(null, "width", "32"), e.setAttributeNS(null, "height", "32"), e.setAttributeNS(null, "viewBox", "0 0 32 32"), e.innerHTML = ` 
                      <g class="ArrowsOut" clip-path="url(#a)">
                        <g class="icon">
                          <path d="M21 6H26V11M19 13 26 6M11 26H6V21M13 19 6 26M26 21V26H21M19 19 26 26M6 11V6H11M13 13 6 6" class="Vector"/>
                        </g>
                      </g>
                      <defs>
                        <clipPath id="a" class="a">
                          <path fill="#fff" d="M0 0H32V32H0z"/>
                        </clipPath>
                      </defs>
                    `, t.appendChild(e), t;
  }
  static fullScreenLabelActive() {
    const t = document.createElement("div"), e = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    return e.setAttributeNS(null, "width", "32"), e.setAttributeNS(null, "height", "32"), e.setAttributeNS(null, "viewBox", "0 0 32 32"), e.innerHTML = ` 
                        <g class="ArrowsIn" clip-path="url(#a)">
                        <g class="icon">
                          <path d="M24 13H19V8M26 6 19 13M8 19H13V24M6 26 13 19M19 24V19H24M26 26 19 19M13 8V13H8M6 6 13 13" class="Vector"/>
                        </g>
                      </g>
                      <defs>
                        <clipPath id="a" class="a">
                          <path fill="#fff" d="M0 0H32V32H0z"/>
                        </clipPath>
                      </defs>
                    `, t.appendChild(e), t;
  }
}
rt.info = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
        <g class="Info" clip-path="url(#a)">
            <g class="icon">
            <path d="M16 28C22.6274 28 28 22.6274 28 16C28 9.37258 22.6274 4 16 4C9.37258 4 4 9.37258 4 16C4 22.6274 9.37258 28 16 28Z" class="Vector"/>
            <path d="M15 15H16V22H17M16 10V11" class="Vector"/>
            </g>
        </g>
        <defs>
            <clipPath id="a" class="a">
            <path fill="#fff" d="M0 0H32V32H0z"/>
            </clipPath>
        </defs>
    </svg>
  `;
rt.warning = `
  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <g class="Warning" clip-path="url(#a)">
    <g class="icon">
      <path d="M16 13V18M14.275 5 3.275 24C3.1 24.304 3.007 24.648 3.007 24.998 3.007 25.349 3.099 25.693 3.273 25.997 3.448 26.301 3.699 26.553 4.003 26.729 4.306 26.906 4.65 26.999 5 27H27C27.351 26.999 27.695 26.906 27.998 26.729 28.301 26.553 28.552 26.301 28.727 25.997 28.902 25.693 28.993 25.349 28.993 24.998 28.993 24.648 28.9 24.304 28.725 24L17.725 5C17.551 4.696 17.3 4.444 16.997 4.268 16.694 4.092 16.35 4 16 4 15.65 4 15.306 4.092 15.003 4.268 14.7 4.444 14.449 4.696 14.275 5V5ZM16 22V23" class="Vector"/>
    </g>
  </g>
  <defs>
    <clipPath id="a" class="a">
      <path fill="#fff" d="M0 0H32V32H0z"/>
    </clipPath>
  </defs>
</svg>

  `;
rt.error = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
        <g class="WarningOctagon" clip-path="url(#a)">
            <g class="icon">
            <path d="M16 10V17" class="Vector"/>
            <path d="M20.9706 4L28 11.0294V20.9706L20.9706 28H11.0294L4 20.9706L4 11.0294L11.0294 4L20.9706 4Z" class="Path"/>
            <path d="M16 21V22" class="Vector"/>
            </g>
        </g>
        <defs>
            <clipPath id="a" class="a">
            <path fill="#fff" d="M0 0H32V32H0z"/>
            </clipPath>
        </defs>
    </svg>
  `;
rt.mapPin = `
    <svg width="42" height="54" viewBox="0 0 42 54" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g filter="url(#filter0_d_244_8096)">
        <mask id="path-1-outside-1_244_8096" maskUnits="userSpaceOnUse" x="6" y="7" width="30" height="42" fill="black">
          <rect fill="white" x="6" y="7" width="30" height="42"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z"/>
        </mask>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z" fill="#F59E0B"/>
        <path d="M34.6425 21.9701L33.6426 21.9596L33.6426 21.9632L34.6425 21.9701ZM20.8217 47.9998L20.2053 47.2124C19.9631 47.4019 19.8217 47.6923 19.8217 47.9998H20.8217ZM20.8217 48L20.2095 48.7907C20.5112 49.0243 20.9195 49.0658 21.262 48.8978C21.6046 48.7298 21.8217 48.3815 21.8217 48H20.8217ZM20.8216 47.9999L21.4337 47.2092C21.0763 46.9325 20.5778 46.9299 20.2175 47.2029L20.8216 47.9999ZM20.8215 48H19.8215C19.8215 48.3797 20.0365 48.7266 20.3765 48.8955C20.7165 49.0645 21.1229 49.0263 21.4255 48.797L20.8215 48ZM20.8215 47.9998H21.8215C21.8215 47.6923 21.68 47.4019 21.4378 47.2124L20.8215 47.9998ZM7.00022 21.9002L6.00022 21.903L6.00023 21.9043L7.00022 21.9002ZM7 21.8217L5.99999 21.8212L6 21.8244L7 21.8217ZM7 21.8099L8.00001 21.8104L8 21.8096L7 21.8099ZM7 21.7941V20.7941C6.73473 20.7941 6.48033 20.8995 6.29278 21.0871C6.10524 21.2747 5.99992 21.5291 6 21.7944L7 21.7941ZM7.00003 21.7941V22.7941C7.55155 22.7941 7.99895 22.3476 8.00002 21.7961L7.00003 21.7941ZM35.6425 21.9806C35.643 21.9277 35.6433 21.8747 35.6433 21.8217H33.6433C33.6433 21.8677 33.6431 21.9136 33.6426 21.9596L35.6425 21.9806ZM21.438 48.7873C21.5042 48.7355 25.0075 45.9857 28.5151 41.2966C32.0176 36.6144 35.5883 29.9124 35.6425 21.9769L33.6426 21.9632C33.5924 29.3062 30.2812 35.5968 26.9136 40.0986C23.5512 44.5937 20.1962 47.2195 20.2053 47.2124L21.438 48.7873ZM21.8217 48V47.9998H19.8217V48H21.8217ZM20.2094 48.7906L20.2095 48.7907L21.4338 47.2093L21.4337 47.2092L20.2094 48.7906ZM21.4255 48.797L21.4256 48.7969L20.2175 47.2029L20.2175 47.203L21.4255 48.797ZM19.8215 47.9998V48H21.8215V47.9998H19.8215ZM6.00023 21.9043C6.033 29.8595 9.60407 36.5798 13.112 41.2752C16.625 45.9774 20.1388 48.7354 20.2051 48.7873L21.4378 47.2124C21.447 47.2195 18.0817 44.5856 14.7142 40.0781C11.3415 35.5638 8.03053 29.2566 8.00021 21.8961L6.00023 21.9043ZM6 21.8244L6.00022 21.903L8.00021 21.8974L8 21.8189L6 21.8244ZM6 21.8095L6 21.8212L8 21.8221L8 21.8104L6 21.8095ZM6 21.7944L6 21.8102L8 21.8096L8 21.7938L6 21.7944ZM7.00003 20.7941H7V22.7941H7.00003V20.7941ZM20.8217 7C12.6457 7 6.01597 13.6199 6.00003 21.7922L8.00002 21.7961C8.01382 14.7266 13.749 9 20.8217 9V7ZM35.6433 21.8217C35.6433 13.6359 29.0074 7 20.8217 7V9C27.9029 9 33.6433 14.7405 33.6433 21.8217H35.6433ZM20.8217 27.3415C23.8701 27.3415 26.3413 24.8702 26.3413 21.8218H24.3413C24.3413 23.7656 22.7655 25.3415 20.8217 25.3415V27.3415ZM15.302 21.8218C15.302 24.8702 17.7732 27.3415 20.8217 27.3415V25.3415C18.8778 25.3415 17.302 23.7656 17.302 21.8218H15.302ZM20.8217 16.3021C17.7732 16.3021 15.302 18.7733 15.302 21.8218H17.302C17.302 19.8779 18.8778 18.3021 20.8217 18.3021V16.3021ZM26.3413 21.8218C26.3413 18.7733 23.8701 16.3021 20.8217 16.3021V18.3021C22.7655 18.3021 24.3413 19.8779 24.3413 21.8218H26.3413Z" fill="white" mask="url(#path-1-outside-1_244_8096)"/>
      </g>
      <mask id="path-3-inside-2_244_8096" fill="white">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z"/>
      </mask>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z" fill="#3B82F6"/>
      <path d="M34.6425 21.9701L32.6426 21.9491L32.6426 21.9564L34.6425 21.9701ZM20.8217 47.9998L19.589 46.4249L18.8217 47.0255V47.9998H20.8217ZM20.8217 48L19.5973 49.5814L22.8217 52.0777V48H20.8217ZM20.8216 47.9999L22.0459 46.4185L20.8345 45.4806L19.6135 46.406L20.8216 47.9999ZM20.8215 48H18.8215V52.0253L22.0295 49.5939L20.8215 48ZM20.8215 47.9998H22.8215V47.0255L22.0542 46.4249L20.8215 47.9998ZM7.00022 21.9002L5.00022 21.9058L5.00024 21.9085L7.00022 21.9002ZM7 21.8217L4.99999 21.8208L5.00001 21.8272L7 21.8217ZM7 21.8099L9.00001 21.8108L9 21.8093L7 21.8099ZM7 21.7941V19.7941H4.99939L5 21.7947L7 21.7941ZM7.00003 21.7941V23.7941H8.99613L9.00002 21.798L7.00003 21.7941ZM36.6424 21.9911C36.643 21.9347 36.6433 21.8782 36.6433 21.8217H32.6433C32.6433 21.8642 32.6431 21.9066 32.6426 21.9491L36.6424 21.9911ZM22.0543 49.5748C22.1583 49.4935 25.7356 46.6818 29.3159 41.8956C32.8858 37.1232 36.5863 30.2156 36.6425 21.9837L32.6426 21.9564C32.5945 29.003 29.413 35.0879 26.1129 39.4996C22.823 43.8976 19.5421 46.4616 19.589 46.4249L22.0543 49.5748ZM22.8217 48V47.9998H18.8217V48H22.8217ZM19.5972 49.5814L19.5973 49.5814L22.046 46.4185L22.0459 46.4185L19.5972 49.5814ZM22.0295 49.5939L22.0296 49.5939L19.6135 46.406L19.6134 46.406L22.0295 49.5939ZM18.8215 47.9998V48H22.8215V47.9998H18.8215ZM5.00024 21.9085C5.03423 30.161 8.73536 37.0878 12.3109 41.8737C15.8966 46.6732 19.4848 49.4934 19.5888 49.5748L22.0542 46.4249C22.101 46.4616 18.8101 43.8898 15.5153 39.4796C12.2102 35.0557 9.0293 28.9552 9.0002 21.892L5.00024 21.9085ZM5.00001 21.8272L5.00023 21.9058L9.00021 21.8947L8.99999 21.8161L5.00001 21.8272ZM5.00001 21.8091L5 21.8208L9 21.8225L9 21.8108L5.00001 21.8091ZM5 21.7947L5.00001 21.8105L9 21.8093L9 21.7935L5 21.7947ZM7.00003 19.7941H7V23.7941H7.00003V19.7941ZM20.8217 6C12.0941 6 5.01705 13.0666 5.00003 21.7902L9.00002 21.798C9.01274 15.28 14.3006 10 20.8217 10V6ZM36.6433 21.8217C36.6433 13.0836 29.5597 6 20.8217 6V10C27.3506 10 32.6433 15.2927 32.6433 21.8217H36.6433ZM20.8217 28.3415C24.4224 28.3415 27.3413 25.4225 27.3413 21.8218H23.3413C23.3413 23.2134 22.2132 24.3415 20.8217 24.3415V28.3415ZM14.302 21.8218C14.302 25.4225 17.2209 28.3415 20.8217 28.3415V24.3415C19.4301 24.3415 18.302 23.2134 18.302 21.8218H14.302ZM20.8217 15.3021C17.2209 15.3021 14.302 18.2211 14.302 21.8218H18.302C18.302 20.4302 19.4301 19.3021 20.8217 19.3021V15.3021ZM27.3413 21.8218C27.3413 18.2211 24.4224 15.3021 20.8217 15.3021V19.3021C22.2132 19.3021 23.3413 20.4302 23.3413 21.8218H27.3413Z" fill="#2563EB" mask="url(#path-3-inside-2_244_8096)"/>
      <defs>
        <filter id="filter0_d_244_8096" x="0" y="0" width="41.6436" height="54" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
          <feFlood flood-opacity="0" result="BackgroundImageFix"/>
          <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
          <feOffset dy="-1"/>
          <feGaussianBlur stdDeviation="3"/>
          <feComposite in2="hardAlpha" operator="out"/>
          <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.5 0"/>
          <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_244_8096"/>
          <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_244_8096" result="shape"/>
        </filter>
      </defs>
    </svg>

  `;
rt.mapPinClick = `
  <svg width="42" height="54" viewBox="0 0 42 54" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g filter="url(#filter0_d_654_6531)">
      <mask id="path-1-outside-1_654_6531" maskUnits="userSpaceOnUse" x="6" y="7" width="30" height="42" fill="black">
        <rect fill="white" x="6" y="7" width="30" height="42"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z"/>
      </mask>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z" fill="#F59E0B"/>
    <path d="M34.6425 21.9701L33.6426 21.9596L33.6426 21.9632L34.6425 21.9701ZM20.8217 47.9998L20.2053 47.2124C19.9631 47.4019 19.8217 47.6923 19.8217 47.9998H20.8217ZM20.8217 48L20.2095 48.7907C20.5112 49.0243 20.9195 49.0658 21.262 48.8978C21.6046 48.7298 21.8217 48.3815 21.8217 48H20.8217ZM20.8216 47.9999L21.4337 47.2092C21.0763 46.9325 20.5778 46.9299 20.2175 47.2029L20.8216 47.9999ZM20.8215 48H19.8215C19.8215 48.3797 20.0365 48.7266 20.3765 48.8955C20.7165 49.0645 21.1229 49.0263 21.4255 48.797L20.8215 48ZM20.8215 47.9998H21.8215C21.8215 47.6923 21.68 47.4019 21.4378 47.2124L20.8215 47.9998ZM7.00022 21.9002L6.00022 21.903L6.00023 21.9043L7.00022 21.9002ZM7 21.8217L5.99999 21.8212L6 21.8244L7 21.8217ZM7 21.8099L8.00001 21.8104L8 21.8096L7 21.8099ZM7 21.7941V20.7941C6.73473 20.7941 6.48033 20.8995 6.29278 21.0871C6.10524 21.2747 5.99992 21.5291 6 21.7944L7 21.7941ZM7.00003 21.7941V22.7941C7.55155 22.7941 7.99895 22.3476 8.00002 21.7961L7.00003 21.7941ZM35.6425 21.9806C35.643 21.9277 35.6433 21.8747 35.6433 21.8217H33.6433C33.6433 21.8677 33.6431 21.9136 33.6426 21.9596L35.6425 21.9806ZM21.438 48.7873C21.5042 48.7355 25.0075 45.9857 28.5151 41.2966C32.0176 36.6144 35.5883 29.9124 35.6425 21.9769L33.6426 21.9632C33.5924 29.3062 30.2812 35.5968 26.9136 40.0986C23.5512 44.5937 20.1962 47.2195 20.2053 47.2124L21.438 48.7873ZM21.8217 48V47.9998H19.8217V48H21.8217ZM20.2094 48.7906L20.2095 48.7907L21.4338 47.2093L21.4337 47.2092L20.2094 48.7906ZM21.4255 48.797L21.4256 48.7969L20.2175 47.2029L20.2175 47.203L21.4255 48.797ZM19.8215 47.9998V48H21.8215V47.9998H19.8215ZM6.00023 21.9043C6.033 29.8595 9.60407 36.5798 13.112 41.2752C16.625 45.9774 20.1388 48.7354 20.2051 48.7873L21.4378 47.2124C21.447 47.2195 18.0817 44.5856 14.7142 40.0781C11.3415 35.5638 8.03053 29.2566 8.00021 21.8961L6.00023 21.9043ZM6 21.8244L6.00022 21.903L8.00021 21.8974L8 21.8189L6 21.8244ZM6 21.8095L6 21.8212L8 21.8221L8 21.8104L6 21.8095ZM6 21.7944L6 21.8102L8 21.8096L8 21.7938L6 21.7944ZM7.00003 20.7941H7V22.7941H7.00003V20.7941ZM20.8217 7C12.6457 7 6.01597 13.6199 6.00003 21.7922L8.00002 21.7961C8.01382 14.7266 13.749 9 20.8217 9V7ZM35.6433 21.8217C35.6433 13.6359 29.0074 7 20.8217 7V9C27.9029 9 33.6433 14.7405 33.6433 21.8217H35.6433ZM20.8217 27.3415C23.8701 27.3415 26.3413 24.8702 26.3413 21.8218H24.3413C24.3413 23.7656 22.7655 25.3415 20.8217 25.3415V27.3415ZM15.302 21.8218C15.302 24.8702 17.7732 27.3415 20.8217 27.3415V25.3415C18.8778 25.3415 17.302 23.7656 17.302 21.8218H15.302ZM20.8217 16.3021C17.7732 16.3021 15.302 18.7733 15.302 21.8218H17.302C17.302 19.8779 18.8778 18.3021 20.8217 18.3021V16.3021ZM26.3413 21.8218C26.3413 18.7733 23.8701 16.3021 20.8217 16.3021V18.3021C22.7655 18.3021 24.3413 19.8779 24.3413 21.8218H26.3413Z" fill="white" mask="url(#path-1-outside-1_654_6531)"/>
    </g>
    <mask id="path-3-inside-2_654_6531" fill="white">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z"/>
    </mask>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M34.6433 21.8217C34.6433 21.8712 34.6431 21.9207 34.6425 21.9701C34.5382 37.2486 20.8787 47.9552 20.8217 47.9998V48L20.8216 47.9999L20.8215 48V47.9998C20.7643 47.9551 7.06331 37.2159 7.00022 21.9002L7 21.8217L7 21.8099L7 21.7941H7.00003C7.01489 14.1733 13.1974 8 20.8217 8C28.4551 8 34.6433 14.1882 34.6433 21.8217ZM25.3413 21.8218C25.3413 24.3179 23.3178 26.3415 20.8217 26.3415C18.3255 26.3415 16.302 24.3179 16.302 21.8218C16.302 19.3256 18.3255 17.3021 20.8217 17.3021C23.3178 17.3021 25.3413 19.3256 25.3413 21.8218Z" fill="#EF4444"/>
    <path d="M34.6425 21.9701L32.6426 21.9491L32.6426 21.9564L34.6425 21.9701ZM20.8217 47.9998L19.589 46.4249L18.8217 47.0254V47.9998H20.8217ZM20.8217 48L19.5973 49.5814L22.8217 52.0777V48H20.8217ZM20.8216 47.9999L22.0459 46.4185L20.8345 45.4806L19.6135 46.406L20.8216 47.9999ZM20.8215 48H18.8215V52.0253L22.0295 49.5939L20.8215 48ZM20.8215 47.9998H22.8215V47.0254L22.0542 46.4249L20.8215 47.9998ZM7.00022 21.9002L5.00022 21.9058L5.00024 21.9085L7.00022 21.9002ZM7 21.8217L4.99999 21.8208L5.00001 21.8272L7 21.8217ZM7 21.8099L9.00001 21.8108L9 21.8093L7 21.8099ZM7 21.7941V19.7941H4.99939L5 21.7947L7 21.7941ZM7.00003 21.7941V23.7941H8.99613L9.00002 21.798L7.00003 21.7941ZM36.6424 21.9911C36.643 21.9347 36.6433 21.8782 36.6433 21.8217H32.6433C32.6433 21.8642 32.6431 21.9066 32.6426 21.9491L36.6424 21.9911ZM22.0543 49.5748C22.1583 49.4935 25.7356 46.6818 29.3159 41.8956C32.8858 37.1232 36.5863 30.2156 36.6425 21.9837L32.6426 21.9564C32.5945 29.003 29.413 35.0879 26.1129 39.4996C22.823 43.8976 19.5421 46.4616 19.589 46.4249L22.0543 49.5748ZM22.8217 48V47.9998H18.8217V48H22.8217ZM19.5972 49.5814L19.5973 49.5814L22.046 46.4185L22.0459 46.4185L19.5972 49.5814ZM22.0295 49.5939L22.0296 49.5939L19.6135 46.406L19.6134 46.406L22.0295 49.5939ZM18.8215 47.9998V48H22.8215V47.9998H18.8215ZM5.00024 21.9085C5.03423 30.161 8.73536 37.0878 12.3109 41.8737C15.8966 46.6732 19.4848 49.4934 19.5888 49.5748L22.0542 46.4249C22.101 46.4616 18.8101 43.8898 15.5153 39.4796C12.2102 35.0557 9.0293 28.9552 9.0002 21.892L5.00024 21.9085ZM5.00001 21.8272L5.00023 21.9058L9.00021 21.8947L8.99999 21.8161L5.00001 21.8272ZM5.00001 21.8091L5 21.8208L9 21.8225L9 21.8108L5.00001 21.8091ZM5 21.7947L5 21.8106L9 21.8093L9 21.7935L5 21.7947ZM7.00003 19.7941H7V23.7941H7.00003V19.7941ZM20.8217 6C12.0941 6 5.01705 13.0666 5.00003 21.7902L9.00002 21.798C9.01274 15.28 14.3006 10 20.8217 10V6ZM36.6433 21.8217C36.6433 13.0836 29.5597 6 20.8217 6V10C27.3506 10 32.6433 15.2927 32.6433 21.8217H36.6433ZM20.8217 28.3415C24.4224 28.3415 27.3413 25.4225 27.3413 21.8218H23.3413C23.3413 23.2134 22.2132 24.3415 20.8217 24.3415V28.3415ZM14.302 21.8218C14.302 25.4225 17.2209 28.3415 20.8217 28.3415V24.3415C19.4301 24.3415 18.302 23.2134 18.302 21.8218H14.302ZM20.8217 15.3021C17.2209 15.3021 14.302 18.2211 14.302 21.8218H18.302C18.302 20.4302 19.4301 19.3021 20.8217 19.3021V15.3021ZM27.3413 21.8218C27.3413 18.2211 24.4224 15.3021 20.8217 15.3021V19.3021C22.2132 19.3021 23.3413 20.4302 23.3413 21.8218H27.3413Z" fill="#DC2626" mask="url(#path-3-inside-2_654_6531)"/>
    <defs>
      <filter id="filter0_d_654_6531" x="0" y="0" width="41.6433" height="54" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
        <feOffset dy="-1"/>
        <feGaussianBlur stdDeviation="3"/>
        <feComposite in2="hardAlpha" operator="out"/>
        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.5 0"/>
        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_654_6531"/>
        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_654_6531" result="shape"/>
      </filter>
    </defs>
  </svg>
  `;
rt.mapPinSelect = `
  <svg width="44" height="56" viewBox="0 0 44 56" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g filter="url(#filter0_d_429_5817)">
      <mask id="path-1-outside-1_429_5817" maskUnits="userSpaceOnUse" x="6" y="7" width="32" height="44" fill="black">
        <rect fill="white" x="6" y="7" width="32" height="44"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M35.6433 22.8217C35.6433 22.8712 35.6431 22.9207 35.6425 22.9701C35.5382 38.2486 21.8787 48.9552 21.8217 48.9998V49L21.8216 48.9999L21.8215 49V48.9998C21.7643 48.9551 8.06331 38.2159 8.00022 22.9002L8 22.8217L8 22.8099L8 22.7941H8.00003C8.01489 15.1733 14.1974 9 21.8217 9C29.4551 9 35.6433 15.1882 35.6433 22.8217ZM26.3413 22.8218C26.3413 25.3179 24.3178 27.3415 21.8217 27.3415C19.3255 27.3415 17.302 25.3179 17.302 22.8218C17.302 20.3256 19.3255 18.3021 21.8217 18.3021C24.3178 18.3021 26.3413 20.3256 26.3413 22.8218Z"/>
      </mask>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M35.6433 22.8217C35.6433 22.8712 35.6431 22.9207 35.6425 22.9701C35.5382 38.2486 21.8787 48.9552 21.8217 48.9998V49L21.8216 48.9999L21.8215 49V48.9998C21.7643 48.9551 8.06331 38.2159 8.00022 22.9002L8 22.8217L8 22.8099L8 22.7941H8.00003C8.01489 15.1733 14.1974 9 21.8217 9C29.4551 9 35.6433 15.1882 35.6433 22.8217ZM26.3413 22.8218C26.3413 25.3179 24.3178 27.3415 21.8217 27.3415C19.3255 27.3415 17.302 25.3179 17.302 22.8218C17.302 20.3256 19.3255 18.3021 21.8217 18.3021C24.3178 18.3021 26.3413 20.3256 26.3413 22.8218Z" fill="#F59E0B"/>
      <path d="M35.6425 22.9701L33.6426 22.9491L33.6426 22.9564L35.6425 22.9701ZM21.8217 48.9998L20.589 47.4249C20.1046 47.804 19.8217 48.3848 19.8217 48.9998H21.8217ZM21.8217 49L20.5973 50.5814C21.2007 51.0486 22.0173 51.1316 22.7024 50.7956C23.3875 50.4596 23.8217 49.763 23.8217 49H21.8217ZM21.8216 48.9999L23.0459 47.4185C22.3311 46.8651 21.334 46.86 20.6135 47.406L21.8216 48.9999ZM21.8215 49H19.8215C19.8215 49.7593 20.2515 50.4532 20.9316 50.7911C21.6116 51.129 22.4243 51.0526 23.0295 50.5939L21.8215 49ZM21.8215 48.9998H23.8215C23.8215 48.3848 23.5385 47.804 23.0542 47.4249L21.8215 48.9998ZM8.00022 22.9002L6.00022 22.9058L6.00024 22.9085L8.00022 22.9002ZM8 22.8217L5.99999 22.8208L6.00001 22.8272L8 22.8217ZM8 22.8099L10 22.8108L10 22.8093L8 22.8099ZM8 22.7941V20.7941C7.46946 20.7941 6.96066 21.0049 6.58557 21.3801C6.21048 21.7553 5.99984 22.2642 6 22.7947L8 22.7941ZM8.00003 22.7941V24.7941C9.10307 24.7941 9.99787 23.9011 10 22.798L8.00003 22.7941ZM37.6424 22.9911C37.643 22.9347 37.6433 22.8782 37.6433 22.8217H33.6433C33.6433 22.8642 33.6431 22.9066 33.6426 22.9491L37.6424 22.9911ZM23.0543 50.5748C23.1583 50.4935 26.7356 47.6818 30.3159 42.8956C33.8858 38.1232 37.5863 31.2156 37.6425 22.9837L33.6426 22.9564C33.5945 30.003 30.413 36.0879 27.1129 40.4996C23.823 44.8976 20.5421 47.4616 20.589 47.4249L23.0543 50.5748ZM23.8217 49V48.9998H19.8217V49H23.8217ZM20.5972 50.5814L20.5973 50.5814L23.046 47.4185L23.0459 47.4185L20.5972 50.5814ZM23.0295 50.5939L23.0296 50.5939L20.6135 47.406L20.6134 47.406L23.0295 50.5939ZM19.8215 48.9998V49H23.8215V48.9998H19.8215ZM6.00024 22.9085C6.03423 31.161 9.73536 38.0878 13.3109 42.8737C16.8966 47.6732 20.4848 50.4934 20.5888 50.5748L23.0542 47.4249C23.101 47.4616 19.8101 44.8898 16.5153 40.4796C13.2102 36.0557 10.0293 29.9552 10.0002 22.892L6.00024 22.9085ZM6.00001 22.8272L6.00023 22.9058L10.0002 22.8947L9.99999 22.8161L6.00001 22.8272ZM6.00001 22.8091L6 22.8208L10 22.8225L10 22.8108L6.00001 22.8091ZM6 22.7947L6.00001 22.8105L10 22.8093L10 22.7935L6 22.7947ZM8.00003 20.7941H8V24.7941H8.00003V20.7941ZM21.8217 7C13.0941 7 6.01705 14.0666 6.00003 22.7902L10 22.798C10.0127 16.28 15.3006 11 21.8217 11V7ZM37.6433 22.8217C37.6433 14.0836 30.5597 7 21.8217 7V11C28.3506 11 33.6433 16.2927 33.6433 22.8217H37.6433ZM21.8217 29.3415C25.4224 29.3415 28.3413 26.4225 28.3413 22.8218H24.3413C24.3413 24.2134 23.2132 25.3415 21.8217 25.3415V29.3415ZM15.302 22.8218C15.302 26.4225 18.2209 29.3415 21.8217 29.3415V25.3415C20.4301 25.3415 19.302 24.2134 19.302 22.8218H15.302ZM21.8217 16.3021C18.2209 16.3021 15.302 19.2211 15.302 22.8218H19.302C19.302 21.4302 20.4301 20.3021 21.8217 20.3021V16.3021ZM28.3413 22.8218C28.3413 19.2211 25.4224 16.3021 21.8217 16.3021V20.3021C23.2132 20.3021 24.3413 21.4302 24.3413 22.8218H28.3413Z" fill="white" mask="url(#path-1-outside-1_429_5817)"/>
    </g>
    <mask id="path-3-inside-2_429_5817" fill="white">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M35.6433 22.8217C35.6433 22.8712 35.6431 22.9207 35.6425 22.9701C35.5382 38.2486 21.8787 48.9552 21.8217 48.9998V49L21.8216 48.9999L21.8215 49V48.9998C21.7643 48.9551 8.06331 38.2159 8.00022 22.9002L8 22.8217L8 22.8099L8 22.7941H8.00003C8.01489 15.1733 14.1974 9 21.8217 9C29.4551 9 35.6433 15.1882 35.6433 22.8217ZM26.3413 22.8218C26.3413 25.3179 24.3178 27.3415 21.8217 27.3415C19.3255 27.3415 17.302 25.3179 17.302 22.8218C17.302 20.3256 19.3255 18.3021 21.8217 18.3021C24.3178 18.3021 26.3413 20.3256 26.3413 22.8218Z"/>
    </mask>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M35.6433 22.8217C35.6433 22.8712 35.6431 22.9207 35.6425 22.9701C35.5382 38.2486 21.8787 48.9552 21.8217 48.9998V49L21.8216 48.9999L21.8215 49V48.9998C21.7643 48.9551 8.06331 38.2159 8.00022 22.9002L8 22.8217L8 22.8099L8 22.7941H8.00003C8.01489 15.1733 14.1974 9 21.8217 9C29.4551 9 35.6433 15.1882 35.6433 22.8217ZM26.3413 22.8218C26.3413 25.3179 24.3178 27.3415 21.8217 27.3415C19.3255 27.3415 17.302 25.3179 17.302 22.8218C17.302 20.3256 19.3255 18.3021 21.8217 18.3021C24.3178 18.3021 26.3413 20.3256 26.3413 22.8218Z" fill="#EF4444"/>
    <path d="M35.6425 22.9701L33.6426 22.9491L33.6426 22.9564L35.6425 22.9701ZM21.8217 48.9998L20.589 47.4249L19.8217 48.0255V48.9998H21.8217ZM21.8217 49L20.5973 50.5814L23.8217 53.0777V49H21.8217ZM21.8216 48.9999L23.0459 47.4185L21.8345 46.4806L20.6135 47.406L21.8216 48.9999ZM21.8215 49H19.8215V53.0253L23.0295 50.5939L21.8215 49ZM21.8215 48.9998H23.8215V48.0255L23.0542 47.4249L21.8215 48.9998ZM8.00022 22.9002L6.00022 22.9058L6.00024 22.9085L8.00022 22.9002ZM8 22.8217L5.99999 22.8208L6.00001 22.8272L8 22.8217ZM8 22.8099L10 22.8108L10 22.8093L8 22.8099ZM8 22.7941V20.7941H5.99939L6 22.7947L8 22.7941ZM8.00003 22.7941V24.7941H9.99613L10 22.798L8.00003 22.7941ZM37.6424 22.9911C37.643 22.9347 37.6433 22.8782 37.6433 22.8217H33.6433C33.6433 22.8642 33.6431 22.9066 33.6426 22.9491L37.6424 22.9911ZM23.0543 50.5748C23.1583 50.4935 26.7356 47.6818 30.3159 42.8956C33.8858 38.1232 37.5863 31.2156 37.6425 22.9837L33.6426 22.9564C33.5945 30.003 30.413 36.0879 27.1129 40.4996C23.823 44.8976 20.5421 47.4616 20.589 47.4249L23.0543 50.5748ZM23.8217 49V48.9998H19.8217V49H23.8217ZM20.5972 50.5814L20.5973 50.5814L23.046 47.4185L23.0459 47.4185L20.5972 50.5814ZM23.0295 50.5939L23.0296 50.5939L20.6135 47.406L20.6134 47.406L23.0295 50.5939ZM19.8215 48.9998V49H23.8215V48.9998H19.8215ZM6.00024 22.9085C6.03423 31.161 9.73536 38.0878 13.3109 42.8737C16.8966 47.6732 20.4848 50.4934 20.5888 50.5748L23.0542 47.4249C23.101 47.4616 19.8101 44.8898 16.5153 40.4796C13.2102 36.0557 10.0293 29.9552 10.0002 22.892L6.00024 22.9085ZM6.00001 22.8272L6.00023 22.9058L10.0002 22.8947L9.99999 22.8161L6.00001 22.8272ZM6.00001 22.8091L6 22.8208L10 22.8225L10 22.8108L6.00001 22.8091ZM6 22.7947L6.00001 22.8105L10 22.8093L10 22.7935L6 22.7947ZM8.00003 20.7941H8V24.7941H8.00003V20.7941ZM21.8217 7C13.0941 7 6.01705 14.0666 6.00003 22.7902L10 22.798C10.0127 16.28 15.3006 11 21.8217 11V7ZM37.6433 22.8217C37.6433 14.0836 30.5597 7 21.8217 7V11C28.3506 11 33.6433 16.2927 33.6433 22.8217H37.6433ZM21.8217 29.3415C25.4224 29.3415 28.3413 26.4225 28.3413 22.8218H24.3413C24.3413 24.2134 23.2132 25.3415 21.8217 25.3415V29.3415ZM15.302 22.8218C15.302 26.4225 18.2209 29.3415 21.8217 29.3415V25.3415C20.4301 25.3415 19.302 24.2134 19.302 22.8218H15.302ZM21.8217 16.3021C18.2209 16.3021 15.302 19.2211 15.302 22.8218H19.302C19.302 21.4302 20.4301 20.3021 21.8217 20.3021V16.3021ZM28.3413 22.8218C28.3413 19.2211 25.4224 16.3021 21.8217 16.3021V20.3021C23.2132 20.3021 24.3413 21.4302 24.3413 22.8218H28.3413Z" fill="#DC2626" mask="url(#path-3-inside-2_429_5817)"/>
    <defs>
      <filter id="filter0_d_429_5817" x="0" y="0" width="43.6433" height="56" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
        <feOffset dy="-1"/>
        <feGaussianBlur stdDeviation="3"/>
        <feComposite in2="hardAlpha" operator="out"/>
        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.5 0"/>
        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_429_5817"/>
        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_429_5817" result="shape"/>
      </filter>
    </defs>
    </svg>
  `;
rt.information = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" class="dfasdfs">
      <g class="Info" clip-path="url(#a)">
        <g class="icon">
          <path d="M16 28C22.6274 28 28 22.6274 28 16C28 9.37258 22.6274 4 16 4C9.37258 4 4 9.37258 4 16C4 22.6274 9.37258 28 16 28Z" class="Vector"/>
          <path d="M15 15H16V22H17M16 10V11" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>
  `;
rt.geolocation = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="CrosshairSimple" clip-path="url(#a)">
        <g class="icon">
          <path d="M16 27.5C22.351 27.5 27.5 22.351 27.5 16 27.5 9.649 22.351 4.5 16 4.5 9.649 4.5 4.5 9.649 4.5 16 4.5 22.351 9.649 27.5 16 27.5ZM16 4.5V9.5M4.5 16H9.5M16 27.5V22.5M27.5 16H22.5" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>
  `;
rt.rotation = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="North">
        <g class="icon">
          <path d="M12 27.2375L16.2375 23L20.475 27.2375" class="Vector"/>
          <path d="M12 18V7L20.5 18V7" class="Vector 3"/>
        </g>
      </g>
    </svg>
  `;
rt.iconRecenter = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="ArrowsInCardinal" clip-path="url(#a)">
        <g class="icon">
          <path d="M19.537 23.538 16 20 12.462 23.538M16 29V20M12.462 8.462 16 12 19.537 8.462M16 3V12M8.462 19.537 12 16 8.462 12.462M3 16H12M23.538 12.462 20 16 23.538 19.537M29 16H20" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>
  `;
rt.iconRemoveSelection = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="RemoveSelection">
        <g class="icon">
          <path d="M16 28C22.627 28 28 22.627 28 16 28 9.373 22.627 4 16 4 9.373 4 4 9.373 4 16 4 22.627 9.373 28 16 28ZM20 12 12 20M20 20 12 12" class="Vector"/>
        </g>
      </g>
    </svg>
  `;
rt.search = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="MagnifyingGlass" clip-path="url(#a)">
        <g class="icon">
          <path d="M14.5 25C20.299 25 25 20.299 25 14.5 25 8.701 20.299 4 14.5 4 8.701 4 4 8.701 4 14.5 4 20.299 8.701 25 14.5 25ZM21.925 21.925 28 28" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>
  `;
rt.cross = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="X" clip-path="url(#a)">
        <g class="icon">
          <path d="M25 7 7 25M25 25 7 7" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>  
  `;
rt.stack = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="Stack" clip-path="url(#a)">
        <g class="icon">
          <path d="M4 22L16 29L28 22" class="Vector"/>
          <path d="M4 16L16 23L28 16" class="Vector"/>
          <path d="M4 10L16 17L28 10L16 3L4 10Z" class="Vector"/>
        </g>
      </g>
      <defs>
        <clipPath id="a" class="a">
          <path fill="#fff" d="M0 0H32V32H0z"/>
        </clipPath>
      </defs>
    </svg>
  `;
var r_ = Object.defineProperty, o_ = Object.getOwnPropertyDescriptor, So = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? o_(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && r_(t, e, s), s;
};
let Un = class extends Pt {
  constructor() {
    super(), this.currentPosition = [0, 0], this._isRecenterButton = !0, this._currentPosition = "", Wt.registerBorderConstaintMapEvent("change:center", () => this.setCenterChange()), window.addEventListener("open-select-create-box", (i) => {
      ef.getAddressFromCoordinate(i.detail).then((t) => {
        this._currentPosition = t.results.length > 0 ? `\xC0 proximit\xE9 de ${t.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
      }), this.setCenterChange();
    });
  }
  setCenterChange() {
    const i = M().getSelectedFeature(M().getCurrentItemId());
    if (i) {
      const t = i.get("geom");
      this._isRecenterButton = t.intersectsExtent(M().getMap().getView().calculateExtent(M().getMap().getSize()));
    }
  }
  connectedCallback() {
    super.connectedCallback();
  }
  render() {
    return Lt`
      <div class="information-box-${M().getTheme()} box-element">
        <div class="box-text-container">
            <div class="box-element-title">
            <div class="box-element-title-text">${M().getOptions().selectionTargetBoxMessage}</div>
            </div>
            <div class="box-element-content">${this._currentPosition}</div>
        </div>
        <div class="box-icon-container">
          <div class="position-icon">
          ${Wd(
      this._isRecenterButton ? Lt`` : Lt`<div class="icon-container" @click="${this.recenter}">
                      ${Le(rt.iconRecenter)}
                    </div>`
    )}
          </div>
          <div class="position-icon">
            <div class="icon-container" @click="${this.unselect}">
              ${Le(rt.iconRemoveSelection)}
            </div>
          </div>
        </div>
      </div>
    `;
  }
  recenter() {
    it.sendEvent("recenter-selected-element", void 0);
  }
  unselect() {
    const i = M().getOptions();
    let t = "";
    switch (i.mode.type === "mix" ? t = M().getCurrentFeatureType(M().getCurrentItemId()) : t = i.mode.type, t) {
      case "select":
        it.sendEvent("icon-clicked", M().getCurrentItemId());
        break;
      case "create":
        it.sendEvent("icon-removed", void 0);
        break;
    }
  }
};
Un.styles = [yt(s_)];
So([
  Ti()
], Un.prototype, "currentPosition", 2);
So([
  Dt()
], Un.prototype, "_isRecenterButton", 2);
So([
  Dt()
], Un.prototype, "_currentPosition", 2);
Un = So([
  qt("select-information-box-element")
], Un);
class nf extends kt {
  constructor() {
    const t = document.createElement("select-information-box-element");
    super({ element: t }), this.div = t, Wt.setResizeEvent(this.div, "--select-box-width");
  }
  disable() {
    this.div.classList.add("disabled");
  }
  show() {
    this.div.classList.remove("fade-out"), this.div.classList.remove("disabled"), this.div.classList.add("fade-in");
  }
  hide() {
    this.div.classList.remove("fade-in"), this.div.classList.add("fade-out");
  }
}
class a_ {
  constructor() {
    this.clickImage = document.createElement("img"), this.clickImage.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(rt.mapPinClick), this.selectImage = document.createElement("img"), this.selectImage.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(rt.mapPinSelect);
  }
  clusterWithIcon(t) {
    const e = t.get("features").length;
    let n;
    return e === 1 && t.get("features")[0].get("isSelected") ? n = new Ut({
      zIndex: 1,
      image: new ps({
        img: this.selectImage,
        imgSize: [42, 54],
        anchor: [0.52, 55],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && t.get("features")[0].get("isClick") ? n = new Ut({
      zIndex: 1,
      image: new ps({
        img: this.clickImage,
        imgSize: [42, 54],
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && !t.get("features")[0].get("isClick") ? n = new Ut({
      zIndex: 1,
      image: new ps({
        src: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(rt.mapPin),
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : t.get("features").find((s) => s.get("isClick")) ? n = new Ut({
      image: new ei({
        radius: 15,
        stroke: new Re({
          color: "#fff"
        }),
        fill: new Yt({
          color: "#EF4444"
        })
      }),
      text: new wa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Yt({
          color: "#fff"
        })
      })
    }) : n = new Ut({
      image: new ei({
        radius: 15,
        stroke: new Re({
          color: "#fff"
        }),
        fill: new Yt({
          color: "#334155"
        })
      }),
      text: new wa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Yt({
          color: "#fff"
        })
      })
    }), n;
  }
}
class sf {
  static setCustomStyleWithouInfoBox() {
    const t = M().getOptions();
    M().setCustomDisplay(t.search.displaySearch);
    const e = t.search.displaySearch ? "small" : "no-box";
    M().setTargetBoxSize(e);
  }
}
const Oa = "http://www.w3.org/2001/XMLSchema-instance";
function K(i, t) {
  return lf().createElementNS(i, t);
}
function Ki(i, t) {
  return rf(i, t, []).join("");
}
function rf(i, t, e) {
  if (i.nodeType == Node.CDATA_SECTION_NODE || i.nodeType == Node.TEXT_NODE)
    t ? e.push(String(i.nodeValue).replace(/(\r\n|\r|\n)/g, "")) : e.push(i.nodeValue);
  else {
    let n;
    for (n = i.firstChild; n; n = n.nextSibling)
      rf(n, t, e);
  }
  return e;
}
function zi(i) {
  return "documentElement" in i;
}
function l_(i, t, e) {
  return i.getAttributeNS(t, e) || "";
}
function Zi(i) {
  return new DOMParser().parseFromString(i, "application/xml");
}
function of(i, t) {
  return function(e, n) {
    const s = i.call(
      t !== void 0 ? t : this,
      e,
      n
    );
    if (s !== void 0) {
      const r = n[n.length - 1];
      Kt(r, s);
    }
  };
}
function H(i, t) {
  return function(e, n) {
    const s = i.call(
      t !== void 0 ? t : this,
      e,
      n
    );
    s !== void 0 && n[n.length - 1].push(s);
  };
}
function Z(i, t) {
  return function(e, n) {
    const s = i.call(
      t !== void 0 ? t : this,
      e,
      n
    );
    s !== void 0 && (n[n.length - 1] = s);
  };
}
function ue(i, t, e) {
  return function(n, s) {
    const r = i.call(
      e !== void 0 ? e : this,
      n,
      s
    );
    if (r !== void 0) {
      const o = s[s.length - 1], a = t !== void 0 ? t : n.localName;
      let l;
      a in o ? l = o[a] : (l = [], o[a] = l), l.push(r);
    }
  };
}
function N(i, t, e) {
  return function(n, s) {
    const r = i.call(
      e !== void 0 ? e : this,
      n,
      s
    );
    if (r !== void 0) {
      const o = s[s.length - 1], a = t !== void 0 ? t : n.localName;
      o[a] = r;
    }
  };
}
function E(i, t) {
  return function(e, n, s) {
    i.call(
      t !== void 0 ? t : this,
      e,
      n,
      s
    ), s[s.length - 1].node.appendChild(e);
  };
}
function de(i, t) {
  return function(e, n, s) {
    const o = n[n.length - 1].node;
    let a = i;
    a === void 0 && (a = s);
    const l = t !== void 0 ? t : o.namespaceURI;
    return K(l, a);
  };
}
const af = de();
function ut(i, t, e) {
  e = e !== void 0 ? e : {};
  let n, s;
  for (n = 0, s = i.length; n < s; ++n)
    e[i[n]] = t;
  return e;
}
function Hi(i, t, e, n) {
  let s;
  for (s = t.firstElementChild; s; s = s.nextElementSibling) {
    const r = i[s.namespaceURI];
    if (r !== void 0) {
      const o = r[s.localName];
      o !== void 0 && o.call(n, s, e);
    }
  }
}
function B(i, t, e, n, s) {
  return n.push(i), Hi(t, e, n, s), n.pop();
}
function h_(i, t, e, n, s, r) {
  const o = (s !== void 0 ? s : e).length;
  let a, l;
  for (let h = 0; h < o; ++h)
    a = e[h], a !== void 0 && (l = t.call(
      r !== void 0 ? r : this,
      a,
      n,
      s !== void 0 ? s[h] : void 0
    ), l !== void 0 && i[l.namespaceURI][l.localName].call(
      r,
      l,
      a,
      n
    ));
}
function Et(i, t, e, n, s, r, o) {
  return s.push(i), h_(t, e, n, s, r, o), s.pop();
}
let ia;
function c_() {
  return ia === void 0 && typeof XMLSerializer < "u" && (ia = new XMLSerializer()), ia;
}
let na;
function lf() {
  return na === void 0 && typeof document < "u" && (na = document.implementation.createDocument("", "", null)), na;
}
class u_ extends Zd {
  constructor() {
    super(), this.xmlSerializer_ = c_();
  }
  getType() {
    return "xml";
  }
  readFeature(t, e) {
    if (t)
      if (typeof t == "string") {
        const n = Zi(t);
        return this.readFeatureFromDocument(n, e);
      } else
        return zi(t) ? this.readFeatureFromDocument(
          t,
          e
        ) : this.readFeatureFromNode(t, e);
    else
      return null;
  }
  readFeatureFromDocument(t, e) {
    const n = this.readFeaturesFromDocument(t, e);
    return n.length > 0 ? n[0] : null;
  }
  readFeatureFromNode(t, e) {
    return null;
  }
  readFeatures(t, e) {
    if (t)
      if (typeof t == "string") {
        const n = Zi(t);
        return this.readFeaturesFromDocument(n, e);
      } else
        return zi(t) ? this.readFeaturesFromDocument(
          t,
          e
        ) : this.readFeaturesFromNode(
          t,
          e
        );
    else
      return [];
  }
  readFeaturesFromDocument(t, e) {
    const n = [];
    for (let s = t.firstChild; s; s = s.nextSibling)
      s.nodeType == Node.ELEMENT_NODE && Kt(
        n,
        this.readFeaturesFromNode(s, e)
      );
    return n;
  }
  readFeaturesFromNode(t, e) {
    return W();
  }
  readGeometry(t, e) {
    if (t)
      if (typeof t == "string") {
        const n = Zi(t);
        return this.readGeometryFromDocument(n, e);
      } else
        return zi(t) ? this.readGeometryFromDocument(
          t,
          e
        ) : this.readGeometryFromNode(
          t,
          e
        );
    else
      return null;
  }
  readGeometryFromDocument(t, e) {
    return null;
  }
  readGeometryFromNode(t, e) {
    return null;
  }
  readProjection(t) {
    if (t)
      if (typeof t == "string") {
        const e = Zi(t);
        return this.readProjectionFromDocument(e);
      } else
        return zi(t) ? this.readProjectionFromDocument(t) : this.readProjectionFromNode(t);
    else
      return null;
  }
  readProjectionFromDocument(t) {
    return this.dataProjection;
  }
  readProjectionFromNode(t) {
    return this.dataProjection;
  }
  writeFeature(t, e) {
    const n = this.writeFeatureNode(t, e);
    return this.xmlSerializer_.serializeToString(n);
  }
  writeFeatureNode(t, e) {
    return null;
  }
  writeFeatures(t, e) {
    const n = this.writeFeaturesNode(t, e);
    return this.xmlSerializer_.serializeToString(n);
  }
  writeFeaturesNode(t, e) {
    return null;
  }
  writeGeometry(t, e) {
    const n = this.writeGeometryNode(t, e);
    return this.xmlSerializer_.serializeToString(n);
  }
  writeGeometryNode(t, e) {
    return null;
  }
}
const hf = u_, ni = "http://www.opengis.net/gml", d_ = /^\s*$/;
class St extends hf {
  constructor(t) {
    super(), t = t || {}, this.featureType = t.featureType, this.featureNS = t.featureNS, this.srsName = t.srsName, this.schemaLocation = "", this.FEATURE_COLLECTION_PARSERS = {}, this.FEATURE_COLLECTION_PARSERS[this.namespace] = {
      featureMember: H(this.readFeaturesInternal),
      featureMembers: Z(this.readFeaturesInternal)
    }, this.supportedMediaTypes = ["application/gml+xml"];
  }
  readFeaturesInternal(t, e) {
    const n = t.localName;
    let s = null;
    if (n == "FeatureCollection")
      s = B(
        [],
        this.FEATURE_COLLECTION_PARSERS,
        t,
        e,
        this
      );
    else if (n == "featureMembers" || n == "featureMember" || n == "member") {
      const r = e[0];
      let o = r.featureType, a = r.featureNS;
      const l = "p", h = "p0";
      if (!o && t.childNodes) {
        o = [], a = {};
        for (let d = 0, f = t.childNodes.length; d < f; ++d) {
          const g = t.childNodes[d];
          if (g.nodeType === 1) {
            const m = g.nodeName.split(":").pop();
            if (!o.includes(m)) {
              let p = "", _ = 0;
              const y = g.namespaceURI;
              for (const v in a) {
                if (a[v] === y) {
                  p = v;
                  break;
                }
                ++_;
              }
              p || (p = l + _, a[p] = y), o.push(p + ":" + m);
            }
          }
        }
        n != "featureMember" && (r.featureType = o, r.featureNS = a);
      }
      if (typeof a == "string") {
        const d = a;
        a = {}, a[h] = d;
      }
      const c = {}, u = Array.isArray(o) ? o : [o];
      for (const d in a) {
        const f = {};
        for (let g = 0, m = u.length; g < m; ++g)
          (u[g].includes(":") ? u[g].split(":")[0] : h) === d && (f[u[g].split(":").pop()] = n == "featureMembers" ? H(this.readFeatureElement, this) : Z(this.readFeatureElement, this));
        c[a[d]] = f;
      }
      n == "featureMember" || n == "member" ? s = B(void 0, c, t, e) : s = B([], c, t, e);
    }
    return s === null && (s = []), s;
  }
  readGeometryOrExtent(t, e) {
    const n = e[0];
    return n.srsName = t.firstElementChild.getAttribute("srsName"), n.srsDimension = t.firstElementChild.getAttribute("srsDimension"), B(
      null,
      this.GEOMETRY_PARSERS,
      t,
      e,
      this
    );
  }
  readExtentElement(t, e) {
    const n = e[0], s = this.readGeometryOrExtent(t, e);
    return s ? Tl(s, n) : void 0;
  }
  readGeometryElement(t, e) {
    const n = e[0], s = this.readGeometryOrExtent(t, e);
    return s ? js(s, !1, n) : void 0;
  }
  readFeatureElementInternal(t, e, n) {
    let s;
    const r = {};
    for (let o = t.firstElementChild; o; o = o.nextElementSibling) {
      let a;
      const l = o.localName;
      o.childNodes.length === 0 || o.childNodes.length === 1 && (o.firstChild.nodeType === 3 || o.firstChild.nodeType === 4) ? (a = Ki(o, !1), d_.test(a) && (a = void 0)) : (n && (a = l === "boundedBy" ? this.readExtentElement(o, e) : this.readGeometryElement(o, e)), a ? l !== "boundedBy" && (s = l) : a = this.readFeatureElementInternal(o, e, !1));
      const h = o.attributes.length;
      if (h > 0) {
        a = { _content_: a };
        for (let c = 0; c < h; c++) {
          const u = o.attributes[c].name;
          a[u] = o.attributes[c].value;
        }
      }
      r[l] ? (r[l] instanceof Array || (r[l] = [r[l]]), r[l].push(a)) : r[l] = a;
    }
    if (n) {
      const o = new on(r);
      s && o.setGeometryName(s);
      const a = t.getAttribute("fid") || l_(t, this.namespace, "id");
      return a && o.setId(a), o;
    } else
      return r;
  }
  readFeatureElement(t, e) {
    return this.readFeatureElementInternal(t, e, !0);
  }
  readPoint(t, e) {
    const n = this.readFlatCoordinatesFromNode(t, e);
    if (n)
      return new si(n, "XYZ");
  }
  readMultiPoint(t, e) {
    const n = B(
      [],
      this.MULTIPOINT_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new wo(n);
  }
  readMultiLineString(t, e) {
    const n = B(
      [],
      this.MULTILINESTRING_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Il(n);
  }
  readMultiPolygon(t, e) {
    const n = B(
      [],
      this.MULTIPOLYGON_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Al(n);
  }
  pointMemberParser(t, e) {
    Hi(this.POINTMEMBER_PARSERS, t, e, this);
  }
  lineStringMemberParser(t, e) {
    Hi(this.LINESTRINGMEMBER_PARSERS, t, e, this);
  }
  polygonMemberParser(t, e) {
    Hi(this.POLYGONMEMBER_PARSERS, t, e, this);
  }
  readLineString(t, e) {
    const n = this.readFlatCoordinatesFromNode(t, e);
    if (n)
      return new As(n, "XYZ");
  }
  readFlatLinearRing(t, e) {
    const n = B(
      null,
      this.GEOMETRY_FLAT_COORDINATES_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return n;
  }
  readLinearRing(t, e) {
    const n = this.readFlatCoordinatesFromNode(t, e);
    if (n)
      return new xa(n, "XYZ");
  }
  readPolygon(t, e) {
    const n = B(
      [null],
      this.FLAT_LINEAR_RINGS_PARSERS,
      t,
      e,
      this
    );
    if (n && n[0]) {
      const s = n[0], r = [s.length];
      let o, a;
      for (o = 1, a = n.length; o < a; ++o)
        Kt(s, n[o]), r.push(s.length);
      return new Vn(s, "XYZ", r);
    } else
      return;
  }
  readFlatCoordinatesFromNode(t, e) {
    return B(
      null,
      this.GEOMETRY_FLAT_COORDINATES_PARSERS,
      t,
      e,
      this
    );
  }
  readGeometryFromNode(t, e) {
    const n = this.readGeometryElement(t, [
      this.getReadOptions(t, e || {})
    ]);
    return n || null;
  }
  readFeaturesFromNode(t, e) {
    const n = {
      featureType: this.featureType,
      featureNS: this.featureNS
    };
    return n && Object.assign(n, this.getReadOptions(t, e)), this.readFeaturesInternal(t, [n]) || [];
  }
  readProjectionFromNode(t) {
    return J(
      this.srsName ? this.srsName : t.firstElementChild.getAttribute("srsName")
    );
  }
}
St.prototype.namespace = ni;
St.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {}
};
St.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {}
};
St.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {}
};
St.prototype.MULTIPOINT_PARSERS = {
  "http://www.opengis.net/gml": {
    pointMember: H(St.prototype.pointMemberParser),
    pointMembers: H(St.prototype.pointMemberParser)
  }
};
St.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: H(
      St.prototype.lineStringMemberParser
    ),
    lineStringMembers: H(
      St.prototype.lineStringMemberParser
    )
  }
};
St.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml": {
    polygonMember: H(St.prototype.polygonMemberParser),
    polygonMembers: H(St.prototype.polygonMemberParser)
  }
};
St.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: H(St.prototype.readFlatCoordinatesFromNode)
  }
};
St.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: H(St.prototype.readLineString)
  }
};
St.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: H(St.prototype.readPolygon)
  }
};
St.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: Z(St.prototype.readFlatLinearRing)
  }
};
const q = St;
function f_(i) {
  const t = Ki(i, !1);
  return g_(t);
}
function g_(i) {
  const t = /^\s*([+\-]?\d*\.?\d+(?:e[+\-]?\d+)?)\s*$/i.exec(i);
  if (t)
    return parseFloat(t[1]);
}
function ne(i) {
  const t = Ki(i, !1);
  return Rn(t);
}
function Rn(i) {
  const t = /^\s*(\d+)\s*$/.exec(i);
  if (t)
    return parseInt(t[1], 10);
}
function st(i) {
  return Ki(i, !1).trim();
}
function Tt(i, t) {
  i.appendChild(lf().createTextNode(t));
}
const m_ = ni + " http://schemas.opengis.net/gml/2.1.2/feature.xsd", p_ = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class nt extends q {
  constructor(t) {
    t = t || {}, super(t), this.FEATURE_COLLECTION_PARSERS[ni].featureMember = H(
      this.readFeaturesInternal
    ), this.schemaLocation = t.schemaLocation ? t.schemaLocation : m_;
  }
  readFlatCoordinates(t, e) {
    const n = Ki(t, !1).replace(/^\s*|\s*$/g, ""), r = e[0].srsName;
    let o = "enu";
    if (r) {
      const h = J(r);
      h && (o = h.getAxisOrientation());
    }
    const a = n.trim().split(/\s+/), l = [];
    for (let h = 0, c = a.length; h < c; h++) {
      const u = a[h].split(/,+/), d = parseFloat(u[0]), f = parseFloat(u[1]), g = u.length === 3 ? parseFloat(u[2]) : 0;
      o.substr(0, 2) === "en" ? l.push(d, f, g) : l.push(f, d, g);
    }
    return l;
  }
  readBox(t, e) {
    const n = B(
      [null],
      this.BOX_PARSERS_,
      t,
      e,
      this
    );
    return xe(
      n[1][0],
      n[1][1],
      n[1][3],
      n[1][4]
    );
  }
  innerBoundaryIsParser(t, e) {
    const n = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    n && e[e.length - 1].push(n);
  }
  outerBoundaryIsParser(t, e) {
    const n = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    if (n) {
      const s = e[e.length - 1];
      s[0] = n;
    }
  }
  GEOMETRY_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.multiSurface, o = s.surface, a = s.multiCurve;
    return Array.isArray(t) ? n = "Envelope" : (n = t.getType(), n === "MultiPolygon" && r === !0 ? n = "MultiSurface" : n === "Polygon" && o === !0 ? n = "Surface" : n === "MultiLineString" && a === !0 && (n = "MultiCurve")), K("http://www.opengis.net/gml", n);
  }
  writeFeatureElement(t, e, n) {
    const s = e.getId();
    s && t.setAttribute("fid", s);
    const r = n[n.length - 1], o = r.featureNS, a = e.getGeometryName();
    r.serializers || (r.serializers = {}, r.serializers[o] = {});
    const l = [], h = [];
    if (e.hasProperties()) {
      const u = e.getProperties();
      for (const d in u) {
        const f = u[d];
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = E(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = E(Tt)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, Et(
      c,
      r.serializers,
      de(void 0, o),
      h,
      n,
      l
    );
  }
  writeCurveOrLineString(t, e, n) {
    const r = n[n.length - 1].srsName;
    if (t.nodeName !== "LineStringSegment" && r && t.setAttribute("srsName", r), t.nodeName === "LineString" || t.nodeName === "LineStringSegment") {
      const o = this.createCoordinatesNode_(t.namespaceURI);
      t.appendChild(o), this.writeCoordinates_(o, e, n);
    } else if (t.nodeName === "Curve") {
      const o = K(t.namespaceURI, "segments");
      t.appendChild(o), this.writeCurveSegments_(o, e, n);
    }
  }
  writeLineStringOrCurveMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeCurveOrLineString(s, e, n));
  }
  writeMultiCurveOrLineString(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = s.curve;
    o && t.setAttribute("srsName", o);
    const l = e.getLineStrings();
    Et(
      { node: t, hasZ: r, srsName: o, curve: a },
      this.LINESTRINGORCURVEMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      n,
      void 0,
      this
    );
  }
  writeGeometryElement(t, e, n) {
    const s = n[n.length - 1], r = Object.assign({}, s);
    r.node = t;
    let o;
    Array.isArray(e) ? o = Tl(
      e,
      s
    ) : o = js(
      e,
      !0,
      s
    ), Et(
      r,
      this.GEOMETRY_SERIALIZERS,
      this.GEOMETRY_NODE_FACTORY_,
      [o],
      n,
      void 0,
      this
    );
  }
  createCoordinatesNode_(t) {
    const e = K(t, "coordinates");
    return e.setAttribute("decimal", "."), e.setAttribute("cs", ","), e.setAttribute("ts", " "), e;
  }
  writeCoordinates_(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = e.getCoordinates(), l = a.length, h = new Array(l);
    for (let c = 0; c < l; ++c) {
      const u = a[c];
      h[c] = this.getCoords_(u, o, r);
    }
    Tt(t, h.join(" "));
  }
  writeCurveSegments_(t, e, n) {
    const s = K(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, n);
  }
  writeSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      Et(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        n,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = K(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, n);
    }
  }
  RING_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), K(
      r.namespaceURI,
      o !== void 0 ? "innerBoundaryIs" : "outerBoundaryIs"
    );
  }
  writeSurfacePatches_(t, e, n) {
    const s = K(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n);
  }
  writeRing(t, e, n) {
    const s = K(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, n);
  }
  getCoords_(t, e, n) {
    let s = "enu";
    e && (s = J(e).getAxisOrientation());
    let r = s.substr(0, 2) === "en" ? t[0] + "," + t[1] : t[1] + "," + t[0];
    if (n) {
      const o = t[2] || 0;
      r += "," + o;
    }
    return r;
  }
  writePoint(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    o && t.setAttribute("srsName", o);
    const a = this.createCoordinatesNode_(t.namespaceURI);
    t.appendChild(a);
    const l = e.getCoordinates(), h = this.getCoords_(l, o, r);
    Tt(a, h);
  }
  writeMultiPoint(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    o && t.setAttribute("srsName", o);
    const a = e.getPoints();
    Et(
      { node: t, hasZ: r, srsName: o },
      this.POINTMEMBER_SERIALIZERS,
      de("pointMember"),
      a,
      n,
      void 0,
      this
    );
  }
  writePointMember(t, e, n) {
    const s = K(t.namespaceURI, "Point");
    t.appendChild(s), this.writePoint(s, e, n);
  }
  writeLinearRing(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = this.createCoordinatesNode_(t.namespaceURI);
    t.appendChild(o), this.writeCoordinates_(o, e, n);
  }
  writeMultiSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = s.surface;
    o && t.setAttribute("srsName", o);
    const l = e.getPolygons();
    Et(
      { node: t, hasZ: r, srsName: o, surface: a },
      this.SURFACEORPOLYGONMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      n,
      void 0,
      this
    );
  }
  writeSurfaceOrPolygonMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n));
  }
  writeEnvelope(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = ["lowerCorner", "upperCorner"], a = [e[0] + " " + e[1], e[2] + " " + e[3]];
    Et(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      af,
      a,
      n,
      o,
      this
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1].node;
    return K(
      "http://www.opengis.net/gml",
      p_[s.nodeName]
    );
  }
}
nt.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    coordinates: Z(nt.prototype.readFlatCoordinates)
  }
};
nt.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {
    innerBoundaryIs: nt.prototype.innerBoundaryIsParser,
    outerBoundaryIs: nt.prototype.outerBoundaryIsParser
  }
};
nt.prototype.BOX_PARSERS_ = {
  "http://www.opengis.net/gml": {
    coordinates: H(nt.prototype.readFlatCoordinates)
  }
};
nt.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: Z(q.prototype.readPoint),
    MultiPoint: Z(q.prototype.readMultiPoint),
    LineString: Z(q.prototype.readLineString),
    MultiLineString: Z(q.prototype.readMultiLineString),
    LinearRing: Z(q.prototype.readLinearRing),
    Polygon: Z(q.prototype.readPolygon),
    MultiPolygon: Z(q.prototype.readMultiPolygon),
    Box: Z(nt.prototype.readBox)
  }
};
nt.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: E(nt.prototype.writeCurveOrLineString),
    MultiCurve: E(nt.prototype.writeMultiCurveOrLineString),
    Point: E(nt.prototype.writePoint),
    MultiPoint: E(nt.prototype.writeMultiPoint),
    LineString: E(nt.prototype.writeCurveOrLineString),
    MultiLineString: E(
      nt.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: E(nt.prototype.writeLinearRing),
    Polygon: E(nt.prototype.writeSurfaceOrPolygon),
    MultiPolygon: E(
      nt.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: E(nt.prototype.writeSurfaceOrPolygon),
    MultiSurface: E(
      nt.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: E(nt.prototype.writeEnvelope)
  }
};
nt.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: E(
      nt.prototype.writeLineStringOrCurveMember
    ),
    curveMember: E(
      nt.prototype.writeLineStringOrCurveMember
    )
  }
};
nt.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    outerBoundaryIs: E(nt.prototype.writeRing),
    innerBoundaryIs: E(nt.prototype.writeRing)
  }
};
nt.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: E(nt.prototype.writePointMember)
  }
};
nt.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: E(
      nt.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: E(
      nt.prototype.writeSurfaceOrPolygonMember
    )
  }
};
nt.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: E(Tt),
    upperCorner: E(Tt)
  }
};
const Ks = nt, __ = ni + " http://schemas.opengis.net/gml/3.1.1/profiles/gmlsfProfile/1.0.0/gmlsf.xsd", y_ = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class D extends q {
  constructor(t) {
    t = t || {}, super(t), this.surface_ = t.surface !== void 0 ? t.surface : !1, this.curve_ = t.curve !== void 0 ? t.curve : !1, this.multiCurve_ = t.multiCurve !== void 0 ? t.multiCurve : !0, this.multiSurface_ = t.multiSurface !== void 0 ? t.multiSurface : !0, this.schemaLocation = t.schemaLocation ? t.schemaLocation : __, this.hasZ = t.hasZ !== void 0 ? t.hasZ : !1;
  }
  readMultiCurve(t, e) {
    const n = B(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Il(n);
  }
  readFlatCurveRing(t, e) {
    const n = B(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    ), s = [];
    for (let r = 0, o = n.length; r < o; ++r)
      Kt(s, n[r].getFlatCoordinates());
    return s;
  }
  readMultiSurface(t, e) {
    const n = B(
      [],
      this.MULTISURFACE_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Al(n);
  }
  curveMemberParser(t, e) {
    Hi(this.CURVEMEMBER_PARSERS, t, e, this);
  }
  surfaceMemberParser(t, e) {
    Hi(this.SURFACEMEMBER_PARSERS, t, e, this);
  }
  readPatch(t, e) {
    return B(
      [null],
      this.PATCHES_PARSERS,
      t,
      e,
      this
    );
  }
  readSegment(t, e) {
    return B([], this.SEGMENTS_PARSERS, t, e, this);
  }
  readPolygonPatch(t, e) {
    return B(
      [null],
      this.FLAT_LINEAR_RINGS_PARSERS,
      t,
      e,
      this
    );
  }
  readLineStringSegment(t, e) {
    return B(
      [null],
      this.GEOMETRY_FLAT_COORDINATES_PARSERS,
      t,
      e,
      this
    );
  }
  interiorParser(t, e) {
    const n = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    n && e[e.length - 1].push(n);
  }
  exteriorParser(t, e) {
    const n = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    if (n) {
      const s = e[e.length - 1];
      s[0] = n;
    }
  }
  readSurface(t, e) {
    const n = B(
      [null],
      this.SURFACE_PARSERS,
      t,
      e,
      this
    );
    if (n && n[0]) {
      const s = n[0], r = [s.length];
      let o, a;
      for (o = 1, a = n.length; o < a; ++o)
        Kt(s, n[o]), r.push(s.length);
      return new Vn(s, "XYZ", r);
    } else
      return;
  }
  readCurve(t, e) {
    const n = B(
      [null],
      this.CURVE_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new As(n, "XYZ");
  }
  readEnvelope(t, e) {
    const n = B(
      [null],
      this.ENVELOPE_PARSERS,
      t,
      e,
      this
    );
    return xe(
      n[1][0],
      n[1][1],
      n[2][0],
      n[2][1]
    );
  }
  readFlatPos(t, e) {
    let n = Ki(t, !1);
    const s = /^\s*([+\-]?\d*\.?\d+(?:[eE][+\-]?\d+)?)\s*/, r = [];
    let o;
    for (; o = s.exec(n); )
      r.push(parseFloat(o[1])), n = n.substr(o[0].length);
    if (n !== "")
      return;
    const l = e[0].srsName;
    let h = "enu";
    if (l && (h = J(l).getAxisOrientation()), h === "neu") {
      let u, d;
      for (u = 0, d = r.length; u < d; u += 3) {
        const f = r[u], g = r[u + 1];
        r[u] = g, r[u + 1] = f;
      }
    }
    const c = r.length;
    if (c == 2 && r.push(0), c !== 0)
      return r;
  }
  readFlatPosList(t, e) {
    const n = Ki(t, !1).replace(/^\s*|\s*$/g, ""), s = e[0], r = s.srsName, o = s.srsDimension;
    let a = "enu";
    r && (a = J(r).getAxisOrientation());
    const l = n.split(/\s+/);
    let h = 2;
    t.getAttribute("srsDimension") ? h = Rn(t.getAttribute("srsDimension")) : t.getAttribute("dimension") ? h = Rn(t.getAttribute("dimension")) : t.parentNode.getAttribute("srsDimension") ? h = Rn(
      t.parentNode.getAttribute("srsDimension")
    ) : o && (h = Rn(o));
    let c, u, d;
    const f = [];
    for (let g = 0, m = l.length; g < m; g += h)
      c = parseFloat(l[g]), u = parseFloat(l[g + 1]), d = h === 3 ? parseFloat(l[g + 2]) : 0, a.substr(0, 2) === "en" ? f.push(c, u, d) : f.push(u, c, d);
    return f;
  }
  writePos_(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = r ? "3" : "2";
    t.setAttribute("srsDimension", o);
    const a = s.srsName;
    let l = "enu";
    a && (l = J(a).getAxisOrientation());
    const h = e.getCoordinates();
    let c;
    if (l.substr(0, 2) === "en" ? c = h[0] + " " + h[1] : c = h[1] + " " + h[0], r) {
      const u = h[2] || 0;
      c += " " + u;
    }
    Tt(t, c);
  }
  getCoords_(t, e, n) {
    let s = "enu";
    e && (s = J(e).getAxisOrientation());
    let r = s.substr(0, 2) === "en" ? t[0] + " " + t[1] : t[1] + " " + t[0];
    if (n) {
      const o = t[2] || 0;
      r += " " + o;
    }
    return r;
  }
  writePosList_(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = r ? "3" : "2";
    t.setAttribute("srsDimension", o);
    const a = s.srsName, l = e.getCoordinates(), h = l.length, c = new Array(h);
    let u;
    for (let d = 0; d < h; ++d)
      u = l[d], c[d] = this.getCoords_(u, a, r);
    Tt(t, c.join(" "));
  }
  writePoint(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = K(t.namespaceURI, "pos");
    t.appendChild(o), this.writePos_(o, e, n);
  }
  writeEnvelope(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = ["lowerCorner", "upperCorner"], a = [e[0] + " " + e[1], e[2] + " " + e[3]];
    Et(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      af,
      a,
      n,
      o,
      this
    );
  }
  writeLinearRing(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = K(t.namespaceURI, "posList");
    t.appendChild(o), this.writePosList_(o, e, n);
  }
  RING_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), K(
      r.namespaceURI,
      o !== void 0 ? "interior" : "exterior"
    );
  }
  writeSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      Et(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        n,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = K(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, n);
    }
  }
  writeCurveOrLineString(t, e, n) {
    const r = n[n.length - 1].srsName;
    if (t.nodeName !== "LineStringSegment" && r && t.setAttribute("srsName", r), t.nodeName === "LineString" || t.nodeName === "LineStringSegment") {
      const o = K(t.namespaceURI, "posList");
      t.appendChild(o), this.writePosList_(o, e, n);
    } else if (t.nodeName === "Curve") {
      const o = K(t.namespaceURI, "segments");
      t.appendChild(o), this.writeCurveSegments_(o, e, n);
    }
  }
  writeMultiSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = s.surface;
    o && t.setAttribute("srsName", o);
    const l = e.getPolygons();
    Et(
      { node: t, hasZ: r, srsName: o, surface: a },
      this.SURFACEORPOLYGONMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      n,
      void 0,
      this
    );
  }
  writeMultiPoint(t, e, n) {
    const s = n[n.length - 1], r = s.srsName, o = s.hasZ;
    r && t.setAttribute("srsName", r);
    const a = e.getPoints();
    Et(
      { node: t, hasZ: o, srsName: r },
      this.POINTMEMBER_SERIALIZERS,
      de("pointMember"),
      a,
      n,
      void 0,
      this
    );
  }
  writeMultiCurveOrLineString(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = s.curve;
    o && t.setAttribute("srsName", o);
    const l = e.getLineStrings();
    Et(
      { node: t, hasZ: r, srsName: o, curve: a },
      this.LINESTRINGORCURVEMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      n,
      void 0,
      this
    );
  }
  writeRing(t, e, n) {
    const s = K(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, n);
  }
  writeSurfaceOrPolygonMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n));
  }
  writePointMember(t, e, n) {
    const s = K(t.namespaceURI, "Point");
    t.appendChild(s), this.writePoint(s, e, n);
  }
  writeLineStringOrCurveMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeCurveOrLineString(s, e, n));
  }
  writeSurfacePatches_(t, e, n) {
    const s = K(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n);
  }
  writeCurveSegments_(t, e, n) {
    const s = K(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, n);
  }
  writeGeometryElement(t, e, n) {
    const s = n[n.length - 1], r = Object.assign({}, s);
    r.node = t;
    let o;
    Array.isArray(e) ? o = Tl(
      e,
      s
    ) : o = js(
      e,
      !0,
      s
    ), Et(
      r,
      this.GEOMETRY_SERIALIZERS,
      this.GEOMETRY_NODE_FACTORY_,
      [o],
      n,
      void 0,
      this
    );
  }
  writeFeatureElement(t, e, n) {
    const s = e.getId();
    s && t.setAttribute("fid", s);
    const r = n[n.length - 1], o = r.featureNS, a = e.getGeometryName();
    r.serializers || (r.serializers = {}, r.serializers[o] = {});
    const l = [], h = [];
    if (e.hasProperties()) {
      const u = e.getProperties();
      for (const d in u) {
        const f = u[d];
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = E(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = E(Tt)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, Et(
      c,
      r.serializers,
      de(void 0, o),
      h,
      n,
      l
    );
  }
  writeFeatureMembers_(t, e, n) {
    const s = n[n.length - 1], r = s.featureType, o = s.featureNS, a = {};
    a[o] = {}, a[o][r] = E(
      this.writeFeatureElement,
      this
    );
    const l = Object.assign({}, s);
    l.node = t, Et(
      l,
      a,
      de(r, o),
      e,
      n
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1].node;
    return K(
      this.namespace,
      y_[s.nodeName]
    );
  }
  GEOMETRY_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.multiSurface, o = s.surface, a = s.curve, l = s.multiCurve;
    return Array.isArray(t) ? n = "Envelope" : (n = t.getType(), n === "MultiPolygon" && r === !0 ? n = "MultiSurface" : n === "Polygon" && o === !0 ? n = "Surface" : n === "LineString" && a === !0 ? n = "Curve" : n === "MultiLineString" && l === !0 && (n = "MultiCurve")), K(this.namespace, n);
  }
  writeGeometryNode(t, e) {
    e = this.adaptOptions(e);
    const n = K(this.namespace, "geom"), s = {
      node: n,
      hasZ: this.hasZ,
      srsName: this.srsName,
      curve: this.curve_,
      surface: this.surface_,
      multiSurface: this.multiSurface_,
      multiCurve: this.multiCurve_
    };
    return e && Object.assign(s, e), this.writeGeometryElement(n, t, [s]), n;
  }
  writeFeaturesNode(t, e) {
    e = this.adaptOptions(e);
    const n = K(this.namespace, "featureMembers");
    n.setAttributeNS(
      Oa,
      "xsi:schemaLocation",
      this.schemaLocation
    );
    const s = {
      srsName: this.srsName,
      hasZ: this.hasZ,
      curve: this.curve_,
      surface: this.surface_,
      multiSurface: this.multiSurface_,
      multiCurve: this.multiCurve_,
      featureNS: this.featureNS,
      featureType: this.featureType
    };
    return e && Object.assign(s, e), this.writeFeatureMembers_(n, t, [s]), n;
  }
}
D.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    pos: Z(D.prototype.readFlatPos),
    posList: Z(D.prototype.readFlatPosList),
    coordinates: Z(Ks.prototype.readFlatCoordinates)
  }
};
D.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {
    interior: D.prototype.interiorParser,
    exterior: D.prototype.exteriorParser
  }
};
D.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: Z(q.prototype.readPoint),
    MultiPoint: Z(q.prototype.readMultiPoint),
    LineString: Z(q.prototype.readLineString),
    MultiLineString: Z(q.prototype.readMultiLineString),
    LinearRing: Z(q.prototype.readLinearRing),
    Polygon: Z(q.prototype.readPolygon),
    MultiPolygon: Z(q.prototype.readMultiPolygon),
    Surface: Z(D.prototype.readSurface),
    MultiSurface: Z(D.prototype.readMultiSurface),
    Curve: Z(D.prototype.readCurve),
    MultiCurve: Z(D.prototype.readMultiCurve),
    Envelope: Z(D.prototype.readEnvelope)
  }
};
D.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml": {
    curveMember: H(D.prototype.curveMemberParser),
    curveMembers: H(D.prototype.curveMemberParser)
  }
};
D.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: H(D.prototype.surfaceMemberParser),
    surfaceMembers: H(D.prototype.surfaceMemberParser)
  }
};
D.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: H(q.prototype.readLineString),
    Curve: H(D.prototype.readCurve)
  }
};
D.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: H(q.prototype.readPolygon),
    Surface: H(D.prototype.readSurface)
  }
};
D.prototype.SURFACE_PARSERS = {
  "http://www.opengis.net/gml": {
    patches: Z(D.prototype.readPatch)
  }
};
D.prototype.CURVE_PARSERS = {
  "http://www.opengis.net/gml": {
    segments: Z(D.prototype.readSegment)
  }
};
D.prototype.ENVELOPE_PARSERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: H(D.prototype.readFlatPosList),
    upperCorner: H(D.prototype.readFlatPosList)
  }
};
D.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml": {
    PolygonPatch: Z(D.prototype.readPolygonPatch)
  }
};
D.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml": {
    LineStringSegment: of(
      D.prototype.readLineStringSegment
    )
  }
};
q.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: Z(q.prototype.readFlatLinearRing),
    Ring: Z(D.prototype.readFlatCurveRing)
  }
};
D.prototype.writeFeatures;
D.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    exterior: E(D.prototype.writeRing),
    interior: E(D.prototype.writeRing)
  }
};
D.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: E(Tt),
    upperCorner: E(Tt)
  }
};
D.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: E(
      D.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: E(
      D.prototype.writeSurfaceOrPolygonMember
    )
  }
};
D.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: E(D.prototype.writePointMember)
  }
};
D.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: E(
      D.prototype.writeLineStringOrCurveMember
    ),
    curveMember: E(
      D.prototype.writeLineStringOrCurveMember
    )
  }
};
D.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: E(D.prototype.writeCurveOrLineString),
    MultiCurve: E(D.prototype.writeMultiCurveOrLineString),
    Point: E(D.prototype.writePoint),
    MultiPoint: E(D.prototype.writeMultiPoint),
    LineString: E(D.prototype.writeCurveOrLineString),
    MultiLineString: E(
      D.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: E(D.prototype.writeLinearRing),
    Polygon: E(D.prototype.writeSurfaceOrPolygon),
    MultiPolygon: E(
      D.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: E(D.prototype.writeSurfaceOrPolygon),
    MultiSurface: E(
      D.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: E(D.prototype.writeEnvelope)
  }
};
const Q = D;
class at extends Q {
  constructor(t) {
    t = t || {}, super(t), this.schemaLocation = t.schemaLocation ? t.schemaLocation : this.namespace + " http://schemas.opengis.net/gml/3.2.1/gml.xsd";
  }
}
at.prototype.namespace = "http://www.opengis.net/gml/3.2";
at.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pos: Z(Q.prototype.readFlatPos),
    posList: Z(Q.prototype.readFlatPosList),
    coordinates: Z(Ks.prototype.readFlatCoordinates)
  }
};
at.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    interior: Q.prototype.interiorParser,
    exterior: Q.prototype.exteriorParser
  }
};
at.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: Z(q.prototype.readPoint),
    MultiPoint: Z(q.prototype.readMultiPoint),
    LineString: Z(q.prototype.readLineString),
    MultiLineString: Z(q.prototype.readMultiLineString),
    LinearRing: Z(q.prototype.readLinearRing),
    Polygon: Z(q.prototype.readPolygon),
    MultiPolygon: Z(q.prototype.readMultiPolygon),
    Surface: Z(at.prototype.readSurface),
    MultiSurface: Z(Q.prototype.readMultiSurface),
    Curve: Z(at.prototype.readCurve),
    MultiCurve: Z(Q.prototype.readMultiCurve),
    Envelope: Z(at.prototype.readEnvelope)
  }
};
at.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    curveMember: H(Q.prototype.curveMemberParser),
    curveMembers: H(Q.prototype.curveMemberParser)
  }
};
at.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: H(Q.prototype.surfaceMemberParser),
    surfaceMembers: H(Q.prototype.surfaceMemberParser)
  }
};
at.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: H(q.prototype.readLineString),
    Curve: H(Q.prototype.readCurve)
  }
};
at.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: H(q.prototype.readPolygon),
    Surface: H(Q.prototype.readSurface)
  }
};
at.prototype.SURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    patches: Z(Q.prototype.readPatch)
  }
};
at.prototype.CURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    segments: Z(Q.prototype.readSegment)
  }
};
at.prototype.ENVELOPE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: H(Q.prototype.readFlatPosList),
    upperCorner: H(Q.prototype.readFlatPosList)
  }
};
at.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    PolygonPatch: Z(Q.prototype.readPolygonPatch)
  }
};
at.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineStringSegment: of(
      Q.prototype.readLineStringSegment
    )
  }
};
at.prototype.MULTIPOINT_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: H(q.prototype.pointMemberParser),
    pointMembers: H(q.prototype.pointMemberParser)
  }
};
at.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: H(
      q.prototype.lineStringMemberParser
    ),
    lineStringMembers: H(
      q.prototype.lineStringMemberParser
    )
  }
};
at.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    polygonMember: H(q.prototype.polygonMemberParser),
    polygonMembers: H(q.prototype.polygonMemberParser)
  }
};
at.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: H(q.prototype.readFlatCoordinatesFromNode)
  }
};
at.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: H(q.prototype.readLineString)
  }
};
at.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: H(q.prototype.readPolygon)
  }
};
at.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LinearRing: Z(q.prototype.readFlatLinearRing),
    Ring: Z(at.prototype.readFlatCurveRing)
  }
};
at.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    exterior: E(Q.prototype.writeRing),
    interior: E(Q.prototype.writeRing)
  }
};
at.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: E(Tt),
    upperCorner: E(Tt)
  }
};
at.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: E(
      Q.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: E(
      Q.prototype.writeSurfaceOrPolygonMember
    )
  }
};
at.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: E(Q.prototype.writePointMember)
  }
};
at.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: E(
      Q.prototype.writeLineStringOrCurveMember
    ),
    curveMember: E(
      Q.prototype.writeLineStringOrCurveMember
    )
  }
};
at.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    Curve: E(Q.prototype.writeCurveOrLineString),
    MultiCurve: E(Q.prototype.writeMultiCurveOrLineString),
    Point: E(at.prototype.writePoint),
    MultiPoint: E(Q.prototype.writeMultiPoint),
    LineString: E(Q.prototype.writeCurveOrLineString),
    MultiLineString: E(
      Q.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: E(Q.prototype.writeLinearRing),
    Polygon: E(Q.prototype.writeSurfaceOrPolygon),
    MultiPolygon: E(
      Q.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: E(Q.prototype.writeSurfaceOrPolygon),
    MultiSurface: E(
      Q.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: E(Q.prototype.writeEnvelope)
  }
};
const Fl = at;
class v_ {
  constructor(t) {
    this.tagName_ = t;
  }
  getTagName() {
    return this.tagName_;
  }
}
const cf = v_;
class x_ extends cf {
  constructor(t, e) {
    super(t), this.conditions = e, Y(this.conditions.length >= 2, 57);
  }
}
const C_ = x_;
class M_ extends C_ {
  constructor(t) {
    super("And", Array.prototype.slice.call(arguments));
  }
}
const E_ = M_;
class w_ extends cf {
  constructor(t, e, n) {
    if (super("BBOX"), this.geometryName = t, this.extent = e, e.length !== 4)
      throw new Error(
        "Expected an extent with four values ([minX, minY, maxX, maxY])"
      );
    this.srsName = n;
  }
}
const S_ = w_;
function R_(i) {
  const t = [null].concat(Array.prototype.slice.call(arguments));
  return new (Function.prototype.bind.apply(E_, t))();
}
function b_(i, t, e) {
  return new S_(i, t, e);
}
const fc = {
  "http://www.opengis.net/gml": {
    boundedBy: N(
      q.prototype.readExtentElement,
      "bounds"
    )
  },
  "http://www.opengis.net/wfs/2.0": {
    member: H(q.prototype.readFeaturesInternal)
  }
}, L_ = {
  "http://www.opengis.net/wfs": {
    totalInserted: N(ne),
    totalUpdated: N(ne),
    totalDeleted: N(ne)
  },
  "http://www.opengis.net/wfs/2.0": {
    totalInserted: N(ne),
    totalUpdated: N(ne),
    totalDeleted: N(ne)
  }
}, T_ = {
  "http://www.opengis.net/wfs": {
    TransactionSummary: N(
      mc,
      "transactionSummary"
    ),
    InsertResults: N(_c, "insertIds")
  },
  "http://www.opengis.net/wfs/2.0": {
    TransactionSummary: N(
      mc,
      "transactionSummary"
    ),
    InsertResults: N(_c, "insertIds")
  }
}, I_ = {
  "http://www.opengis.net/wfs": {
    PropertyName: E(Tt)
  },
  "http://www.opengis.net/wfs/2.0": {
    PropertyName: E(Tt)
  }
}, uf = {
  "http://www.opengis.net/wfs": {
    Insert: E(yc),
    Update: E(xc),
    Delete: E(vc),
    Property: E(Cc),
    Native: E(Mc)
  },
  "http://www.opengis.net/wfs/2.0": {
    Insert: E(yc),
    Update: E(xc),
    Delete: E(vc),
    Property: E(Cc),
    Native: E(Mc)
  }
}, df = "feature", Dl = "http://www.w3.org/2000/xmlns/", kl = {
  "2.0.0": "http://www.opengis.net/ogc/1.1",
  "1.1.0": "http://www.opengis.net/ogc",
  "1.0.0": "http://www.opengis.net/ogc"
}, Na = {
  "2.0.0": "http://www.opengis.net/wfs/2.0",
  "1.1.0": "http://www.opengis.net/wfs",
  "1.0.0": "http://www.opengis.net/wfs"
}, Gl = {
  "2.0.0": "http://www.opengis.net/fes/2.0",
  "1.1.0": "http://www.opengis.net/fes",
  "1.0.0": "http://www.opengis.net/fes"
}, gc = {
  "2.0.0": "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd",
  "1.1.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd",
  "1.0.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/wfs.xsd"
}, $l = {
  "2.0.0": Fl,
  "1.1.0": Q,
  "1.0.0": Ks
}, P_ = "1.1.0";
class A_ extends hf {
  constructor(t) {
    super(), t = t || {}, this.version_ = t.version ? t.version : P_, this.featureType_ = t.featureType, this.featureNS_ = t.featureNS, this.gmlFormat_ = t.gmlFormat ? t.gmlFormat : new $l[this.version_](), this.schemaLocation_ = t.schemaLocation ? t.schemaLocation : gc[this.version_];
  }
  getFeatureType() {
    return this.featureType_;
  }
  setFeatureType(t) {
    this.featureType_ = t;
  }
  readFeaturesFromNode(t, e) {
    const n = {
      node: t
    };
    Object.assign(n, {
      featureType: this.featureType_,
      featureNS: this.featureNS_
    }), Object.assign(n, this.getReadOptions(t, e || {}));
    const s = [n];
    let r;
    this.version_ === "2.0.0" ? r = fc : r = this.gmlFormat_.FEATURE_COLLECTION_PARSERS;
    let o = B(
      [],
      r,
      t,
      s,
      this.gmlFormat_
    );
    return o || (o = []), o;
  }
  readTransactionResponse(t) {
    if (t)
      if (typeof t == "string") {
        const e = Zi(t);
        return this.readTransactionResponseFromDocument(e);
      } else
        return zi(t) ? this.readTransactionResponseFromDocument(
          t
        ) : this.readTransactionResponseFromNode(
          t
        );
    else
      return;
  }
  readFeatureCollectionMetadata(t) {
    if (t)
      if (typeof t == "string") {
        const e = Zi(t);
        return this.readFeatureCollectionMetadataFromDocument(e);
      } else
        return zi(t) ? this.readFeatureCollectionMetadataFromDocument(
          t
        ) : this.readFeatureCollectionMetadataFromNode(
          t
        );
    else
      return;
  }
  readFeatureCollectionMetadataFromDocument(t) {
    for (let e = t.firstChild; e; e = e.nextSibling)
      if (e.nodeType == Node.ELEMENT_NODE)
        return this.readFeatureCollectionMetadataFromNode(
          e
        );
  }
  readFeatureCollectionMetadataFromNode(t) {
    const e = {}, n = Rn(
      t.getAttribute("numberOfFeatures")
    );
    return e.numberOfFeatures = n, B(
      e,
      fc,
      t,
      [],
      this.gmlFormat_
    );
  }
  readTransactionResponseFromDocument(t) {
    for (let e = t.firstChild; e; e = e.nextSibling)
      if (e.nodeType == Node.ELEMENT_NODE)
        return this.readTransactionResponseFromNode(e);
  }
  readTransactionResponseFromNode(t) {
    return B(
      {},
      T_,
      t,
      []
    );
  }
  writeGetFeature(t) {
    const e = K(Na[this.version_], "GetFeature");
    e.setAttribute("service", "WFS"), e.setAttribute("version", this.version_), t.handle && e.setAttribute("handle", t.handle), t.outputFormat && e.setAttribute("outputFormat", t.outputFormat), t.maxFeatures !== void 0 && e.setAttribute("maxFeatures", String(t.maxFeatures)), t.resultType && e.setAttribute("resultType", t.resultType), t.startIndex !== void 0 && e.setAttribute("startIndex", String(t.startIndex)), t.count !== void 0 && e.setAttribute("count", String(t.count)), t.viewParams !== void 0 && e.setAttribute("viewParams", t.viewParams), e.setAttributeNS(
      Oa,
      "xsi:schemaLocation",
      this.schemaLocation_
    );
    const n = {
      node: e
    };
    if (Object.assign(n, {
      version: this.version_,
      srsName: t.srsName,
      featureNS: t.featureNS ? t.featureNS : this.featureNS_,
      featurePrefix: t.featurePrefix,
      propertyNames: t.propertyNames ? t.propertyNames : []
    }), Y(Array.isArray(t.featureTypes), 11), typeof t.featureTypes[0] == "string") {
      let s = t.filter;
      t.bbox && (Y(t.geometryName, 12), s = this.combineBboxAndFilter(
        t.geometryName,
        t.bbox,
        t.srsName,
        s
      )), Object.assign(n, {
        geometryName: t.geometryName,
        filter: s
      }), Ac(
        e,
        t.featureTypes,
        [n]
      );
    } else
      t.featureTypes.forEach((s) => {
        const r = this.combineBboxAndFilter(
          s.geometryName,
          s.bbox,
          t.srsName,
          t.filter
        );
        Object.assign(n, {
          geometryName: s.geometryName,
          filter: r
        }), Ac(e, [s.name], [n]);
      });
    return e;
  }
  combineBboxAndFilter(t, e, n, s) {
    const r = b_(t, e, n);
    return s ? R_(s, r) : r;
  }
  writeTransaction(t, e, n, s) {
    const r = [], o = s.version ? s.version : this.version_, a = K(Na[o], "Transaction");
    a.setAttribute("service", "WFS"), a.setAttribute("version", o);
    let l;
    s && (l = s.gmlOptions ? s.gmlOptions : {}, s.handle && a.setAttribute("handle", s.handle)), a.setAttributeNS(
      Oa,
      "xsi:schemaLocation",
      gc[o]
    );
    const h = O_(a, l, o, s);
    return t && Sr("Insert", t, r, h), e && Sr("Update", e, r, h), n && Sr("Delete", n, r, h), s.nativeElements && Sr(
      "Native",
      s.nativeElements,
      r,
      h
    ), a;
  }
  readProjectionFromDocument(t) {
    for (let e = t.firstChild; e; e = e.nextSibling)
      if (e.nodeType == Node.ELEMENT_NODE)
        return this.readProjectionFromNode(e);
    return null;
  }
  readProjectionFromNode(t) {
    if (t.firstElementChild && t.firstElementChild.firstElementChild) {
      t = t.firstElementChild.firstElementChild;
      for (let e = t.firstElementChild; e; e = e.nextElementSibling)
        if (!(e.childNodes.length === 0 || e.childNodes.length === 1 && e.firstChild.nodeType === 3)) {
          const n = [{}];
          return this.gmlFormat_.readGeometryElement(e, n), J(n.pop().srsName);
        }
    }
    return null;
  }
}
function O_(i, t, e, n) {
  const s = n.featurePrefix ? n.featurePrefix : df;
  let r;
  return e === "1.0.0" ? r = 2 : e === "1.1.0" ? r = 3 : e === "2.0.0" && (r = 3.2), Object.assign(
    { node: i },
    {
      version: e,
      featureNS: n.featureNS,
      featureType: n.featureType,
      featurePrefix: s,
      gmlVersion: r,
      hasZ: n.hasZ,
      srsName: n.srsName
    },
    t
  );
}
function Sr(i, t, e, n) {
  Et(
    n,
    uf,
    de(i),
    t,
    e
  );
}
function mc(i, t) {
  return B({}, L_, i, t);
}
const N_ = {
  "http://www.opengis.net/ogc": {
    FeatureId: H(function(i, t) {
      return i.getAttribute("fid");
    })
  },
  "http://www.opengis.net/ogc/1.1": {
    FeatureId: H(function(i, t) {
      return i.getAttribute("fid");
    })
  }
};
function pc(i, t) {
  Hi(N_, i, t);
}
const F_ = {
  "http://www.opengis.net/wfs": {
    Feature: pc
  },
  "http://www.opengis.net/wfs/2.0": {
    Feature: pc
  }
};
function _c(i, t) {
  return B([], F_, i, t);
}
function yc(i, t, e) {
  const n = e[e.length - 1], s = n.featureType, r = n.featureNS, o = n.gmlVersion, a = K(r, s);
  i.appendChild(a), o === 2 ? Ks.prototype.writeFeatureElement(a, t, e) : o === 3 ? Q.prototype.writeFeatureElement(a, t, e) : Fl.prototype.writeFeatureElement(a, t, e);
}
function ff(i, t, e) {
  const s = e[e.length - 1].version, r = kl[s], o = K(r, "Filter"), a = K(r, "FeatureId");
  o.appendChild(a), a.setAttribute("fid", t), i.appendChild(o);
}
function Bl(i, t) {
  i = i || df;
  const e = i + ":";
  return t.startsWith(e) ? t : e + t;
}
function vc(i, t, e) {
  const n = e[e.length - 1];
  Y(t.getId() !== void 0, 26);
  const s = n.featureType, r = n.featurePrefix, o = n.featureNS, a = Bl(r, s);
  i.setAttribute("typeName", a), i.setAttributeNS(Dl, "xmlns:" + r, o);
  const l = t.getId();
  l !== void 0 && ff(i, l, e);
}
function xc(i, t, e) {
  const n = e[e.length - 1];
  Y(t.getId() !== void 0, 27);
  const s = n.version, r = n.featureType, o = n.featurePrefix, a = n.featureNS, l = Bl(o, r), h = t.getGeometryName();
  i.setAttribute("typeName", l), i.setAttributeNS(Dl, "xmlns:" + o, a);
  const c = t.getId();
  if (c !== void 0) {
    const u = t.getKeys(), d = [];
    for (let f = 0, g = u.length; f < g; f++) {
      const m = t.get(u[f]);
      if (m !== void 0) {
        let p = u[f];
        m && typeof m.getSimplifiedGeometry == "function" && (p = h), d.push({ name: p, value: m });
      }
    }
    Et(
      {
        version: s,
        gmlVersion: n.gmlVersion,
        node: i,
        hasZ: n.hasZ,
        srsName: n.srsName
      },
      uf,
      de("Property"),
      d,
      e
    ), ff(i, c, e);
  }
}
function Cc(i, t, e) {
  const n = e[e.length - 1], s = n.version, r = Na[s], o = K(r, "Name"), a = n.gmlVersion;
  if (i.appendChild(o), Tt(o, t.name), t.value !== void 0 && t.value !== null) {
    const l = K(r, "Value");
    i.appendChild(l), t.value && typeof t.value.getSimplifiedGeometry == "function" ? a === 2 ? Ks.prototype.writeGeometryElement(l, t.value, e) : a === 3 ? Q.prototype.writeGeometryElement(l, t.value, e) : Fl.prototype.writeGeometryElement(l, t.value, e) : Tt(l, t.value);
  }
}
function Mc(i, t, e) {
  t.vendorId && i.setAttribute("vendorId", t.vendorId), t.safeToIgnore !== void 0 && i.setAttribute("safeToIgnore", String(t.safeToIgnore)), t.value !== void 0 && Tt(i, t.value);
}
const Ro = {
  "http://www.opengis.net/wfs": {
    Query: E(Ec)
  },
  "http://www.opengis.net/wfs/2.0": {
    Query: E(Ec)
  },
  "http://www.opengis.net/ogc": {
    During: E(Rc),
    And: E(Rr),
    Or: E(Rr),
    Not: E(bc),
    BBOX: E(wc),
    Contains: E(pi),
    Intersects: E(pi),
    Within: E(pi),
    DWithin: E(Sc),
    PropertyIsEqualTo: E(ye),
    PropertyIsNotEqualTo: E(ye),
    PropertyIsLessThan: E(ye),
    PropertyIsLessThanOrEqualTo: E(ye),
    PropertyIsGreaterThan: E(ye),
    PropertyIsGreaterThanOrEqualTo: E(ye),
    PropertyIsNull: E(Lc),
    PropertyIsBetween: E(Tc),
    PropertyIsLike: E(Ic)
  },
  "http://www.opengis.net/fes/2.0": {
    During: E(Rc),
    And: E(Rr),
    Or: E(Rr),
    Not: E(bc),
    BBOX: E(wc),
    Contains: E(pi),
    Disjoint: E(pi),
    Intersects: E(pi),
    ResourceId: E(k_),
    Within: E(pi),
    DWithin: E(Sc),
    PropertyIsEqualTo: E(ye),
    PropertyIsNotEqualTo: E(ye),
    PropertyIsLessThan: E(ye),
    PropertyIsLessThanOrEqualTo: E(ye),
    PropertyIsGreaterThan: E(ye),
    PropertyIsGreaterThanOrEqualTo: E(ye),
    PropertyIsNull: E(Lc),
    PropertyIsBetween: E(Tc),
    PropertyIsLike: E(Ic)
  }
};
function Ec(i, t, e) {
  const n = e[e.length - 1], s = n.version, r = n.featurePrefix, o = n.featureNS, a = n.propertyNames, l = n.srsName;
  let h;
  r ? h = Bl(r, t) : h = t;
  let c;
  s === "2.0.0" ? c = "typeNames" : c = "typeName", i.setAttribute(c, h), l && i.setAttribute("srsName", l), o && i.setAttributeNS(Dl, "xmlns:" + r, o);
  const u = Object.assign({}, n);
  u.node = i, Et(
    u,
    I_,
    de("PropertyName"),
    a,
    e
  );
  const d = n.filter;
  if (d) {
    const f = K(bo(s), "Filter");
    i.appendChild(f), D_(f, d, e);
  }
}
function D_(i, t, e) {
  const n = e[e.length - 1], s = { node: i };
  Object.assign(s, { context: n }), Et(
    s,
    Ro,
    de(t.getTagName()),
    [t],
    e
  );
}
function wc(i, t, e) {
  const n = e[e.length - 1], r = n.context.version;
  n.srsName = t.srsName;
  const o = $l[r];
  qn(r, i, t.geometryName), o.prototype.writeGeometryElement(i, t.extent, e);
}
function k_(i, t, e) {
  i.setAttribute("rid", t.rid);
}
function pi(i, t, e) {
  const n = e[e.length - 1], r = n.context.version;
  n.srsName = t.srsName;
  const o = $l[r];
  qn(r, i, t.geometryName), o.prototype.writeGeometryElement(i, t.geometry, e);
}
function Sc(i, t, e) {
  const r = e[e.length - 1].context.version;
  pi(i, t, e);
  const o = K(bo(r), "Distance");
  Tt(o, t.distance.toString()), r === "2.0.0" ? o.setAttribute("uom", t.unit) : o.setAttribute("units", t.unit), i.appendChild(o);
}
function Rc(i, t, e) {
  const r = e[e.length - 1].context.version;
  Jr(Gl[r], "ValueReference", i, t.propertyName);
  const o = K(ni, "TimePeriod");
  i.appendChild(o);
  const a = K(ni, "begin");
  o.appendChild(a), Pc(a, t.begin);
  const l = K(ni, "end");
  o.appendChild(l), Pc(l, t.end);
}
function Rr(i, t, e) {
  const s = e[e.length - 1].context, r = { node: i };
  Object.assign(r, { context: s });
  const o = t.conditions;
  for (let a = 0, l = o.length; a < l; ++a) {
    const h = o[a];
    Et(
      r,
      Ro,
      de(h.getTagName()),
      [h],
      e
    );
  }
}
function bc(i, t, e) {
  const s = e[e.length - 1].context, r = { node: i };
  Object.assign(r, { context: s });
  const o = t.condition;
  Et(
    r,
    Ro,
    de(o.getTagName()),
    [o],
    e
  );
}
function ye(i, t, e) {
  const r = e[e.length - 1].context.version;
  t.matchCase !== void 0 && i.setAttribute("matchCase", t.matchCase.toString()), qn(r, i, t.propertyName), Qr(r, i, "" + t.expression);
}
function Lc(i, t, e) {
  const r = e[e.length - 1].context.version;
  qn(r, i, t.propertyName);
}
function Tc(i, t, e) {
  const r = e[e.length - 1].context.version, o = bo(r);
  qn(r, i, t.propertyName);
  const a = K(o, "LowerBoundary");
  i.appendChild(a), Qr(r, a, "" + t.lowerBoundary);
  const l = K(o, "UpperBoundary");
  i.appendChild(l), Qr(r, l, "" + t.upperBoundary);
}
function Ic(i, t, e) {
  const r = e[e.length - 1].context.version;
  i.setAttribute("wildCard", t.wildCard), i.setAttribute("singleChar", t.singleChar), i.setAttribute("escapeChar", t.escapeChar), t.matchCase !== void 0 && i.setAttribute("matchCase", t.matchCase.toString()), qn(r, i, t.propertyName), Qr(r, i, "" + t.pattern);
}
function Jr(i, t, e, n) {
  const s = K(i, t);
  Tt(s, n), e.appendChild(s);
}
function Qr(i, t, e) {
  Jr(bo(i), "Literal", t, e);
}
function qn(i, t, e) {
  i === "2.0.0" ? Jr(Gl[i], "ValueReference", t, e) : Jr(kl[i], "PropertyName", t, e);
}
function Pc(i, t) {
  const e = K(ni, "TimeInstant");
  i.appendChild(e);
  const n = K(ni, "timePosition");
  e.appendChild(n), Tt(n, t);
}
function Ac(i, t, e) {
  const n = e[e.length - 1], s = Object.assign({}, n);
  s.node = i, Et(
    s,
    Ro,
    de("Query"),
    t,
    e
  );
}
function bo(i) {
  let t;
  return i === "2.0.0" ? t = Gl[i] : t = kl[i], t;
}
const G_ = A_;
class gf {
  static getSource(t, e, n) {
    return new Kn({
      format: new G_({
        version: "2.0.0"
      }),
      url: (s) => {
        let r = t;
        if (e === "")
          r + "" + s.join(",");
        else if (e.includes("<BBOX>")) {
          const o = `<BBOX><ValueReference>geometry</ValueReference><Envelope srsName="urn:ogc:def:crs:EPSG::2056"><lowerCorner>${s[0]} ${s[1]}</lowerCorner><upperCorner>${s[2]} ${s[3]}</upperCorner></Envelope></BBOX>`;
          r = `${r}&${e}`.replace("<BBOX>", o);
        } else
          console.error("The replacement string <BBOX> cannot be found. You lose the BBOX optimization."), r = `${r}&${e}`;
        return r;
      },
      strategy: n ? a2 : Td
    });
  }
}
class Oc {
  constructor(t, e) {
    this.control = new nf(), this.store = M(), this.states = e, this.renderUtils = t;
    const n = this.store.getMap(), s = this.store.getOptions(), r = new Ys();
    this.vectorSource = gf.getSource(M().getOptions().wfs.url, "", !1), this.displayDataOnMap(n, r, s, this.vectorSource), this.states.readonly || n.on("click", (o) => {
      n.forEachFeatureAtPixel(o.pixel, (a) => {
        var l;
        a && ((l = a.getGeometry()) == null ? void 0 : l.getType()) === "Point" && (a.getProperties().features && a.getProperties().features.length === 1 ? (this.store.getSelectedFeature(a.getProperties().features[0].get("objectid")) === void 0 && this.store.addSelectedFeature(a.getProperties().features[0], a.getProperties().features[0].get("objectid"), "select"), it.sendEvent("icon-clicked", a.getProperties().features[0].get("objectid"))) : this.control.hide());
      });
    }), window.addEventListener("recenter-selected-element", () => {
      var l;
      const o = this.store.getCurrentItemId(), a = (l = this.store.getSelectedFeature(o)) == null ? void 0 : l.get("geom").getCoordinates();
      n.getView().setCenter(a);
    });
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementSelectMode(this.vectorSource, t);
  }
  setChangeResolution(t, e, n) {
    const s = t.getView().getZoom();
    s && s >= n.maxZoom ? e.setDistance(0) : e.setDistance(n.cluster.distance);
  }
  displayDataOnMap(t, e, n, s) {
    const r = new tp({
      distance: n.cluster.distance,
      minDistance: n.cluster.minDistance,
      source: s
    }), o = new a_();
    e.setSource(r), e.setStyle(function(a) {
      return o.clusterWithIcon(a);
    }), t.addLayer(e), this.control.disable(), this.states.readonly || (t.addControl(this.control), this.toogleDataSelection(e)), Wt.registerBorderConstaintMapEvent("change:resolution", () => this.setChangeResolution(t, r, n));
  }
  setCurrentElement(t) {
    var e;
    (e = this.store.getSelectedFeature(this.store.getCurrentItemId())) == null || e.set("isSelected", void 0), this.store.setCurrentItemId(t.get("objectid"));
  }
  setIconToDisplay(t, e) {
    t.set("isClick", e), t.set("isSelected", e);
  }
  removeSelectedItem(t) {
    this.removeItem(t), this.control.hide(), it.sendEvent("rule-validation", void 0), sf.setCustomStyleWithouInfoBox();
  }
  removeItem(t) {
    this.setIconToDisplay(t, void 0), this.store.removeSelectedFeature(t.get("objectid"));
  }
  setInformationBox(t) {
    this.setIconToDisplay(t, !0), this.control.show(), it.sendEvent("open-select-create-box", t.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select");
  }
  toogleDataSelection(t) {
    window.addEventListener("authorize-clicked", (e) => {
      var s;
      const n = this.store.getSelectedFeature(e.detail);
      n && (n.get("isClick") ? this.store.getMaxElement() === 1 || this.store.getCurrentItemId() === n.get("objectid") ? this.removeSelectedItem(n) : (this.setCurrentElement(n), n.set("isSelected", !0), it.sendEvent("open-select-create-box", n.get("geom").getCoordinates()), this.control.show()) : this.store.getMaxElement() === 1 ? ((s = t.getSource()) == null || s.getFeatures().forEach((o) => {
        o.get("features").forEach((a) => {
          a.get("isClick") && (this.setIconToDisplay(a, void 0), this.store.removeSelectedFeature(a.get("objectid")));
        });
      }), this.store.setCurrentItemId(n.get("objectid")), it.sendEvent("rule-validation", void 0), this.setInformationBox(n)) : this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement() ? (this.setCurrentElement(n), this.setInformationBox(n)) : this.removeItem(n)), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
    });
  }
}
class $_ {
  read(t) {
    if (t)
      if (typeof t == "string") {
        const e = Zi(t);
        return this.readFromDocument(e);
      } else
        return zi(t) ? this.readFromDocument(t) : this.readFromNode(t);
    else
      return null;
  }
  readFromDocument(t) {
    for (let e = t.firstChild; e; e = e.nextSibling)
      if (e.nodeType == Node.ELEMENT_NODE)
        return this.readFromNode(e);
    return null;
  }
  readFromNode(t) {
  }
}
const mf = $_, B_ = "http://www.w3.org/1999/xlink";
function zl(i) {
  return i.getAttributeNS(B_, "href");
}
const re = [null, "http://www.opengis.net/ows/1.1"], z_ = ut(re, {
  ServiceIdentification: N(dy),
  ServiceProvider: N(gy),
  OperationsMetadata: N(cy)
});
class Z_ extends mf {
  constructor() {
    super();
  }
  readFromNode(t) {
    const e = B({}, z_, t, []);
    return e || null;
  }
}
const V_ = ut(re, {
  DeliveryPoint: N(st),
  City: N(st),
  AdministrativeArea: N(st),
  PostalCode: N(st),
  Country: N(st),
  ElectronicMailAddress: N(st)
}), U_ = ut(re, {
  Value: ue(my)
}), W_ = ut(re, {
  AllowedValues: N(ny)
}), H_ = ut(re, {
  Phone: N(uy),
  Address: N(iy)
}), X_ = ut(re, {
  HTTP: N(ly)
}), Y_ = ut(re, {
  Get: ue(ay),
  Post: void 0
}), j_ = ut(re, {
  DCP: N(oy)
}), K_ = ut(re, {
  Operation: hy
}), q_ = ut(re, {
  Voice: N(st),
  Facsimile: N(st)
}), J_ = ut(re, {
  Constraint: ue(sy)
}), Q_ = ut(re, {
  IndividualName: N(st),
  PositionName: N(st),
  ContactInfo: N(ry)
}), ty = ut(re, {
  Abstract: N(st),
  AccessConstraints: N(st),
  Fees: N(st),
  Title: N(st),
  ServiceTypeVersion: N(st),
  ServiceType: N(st)
}), ey = ut(re, {
  ProviderName: N(st),
  ProviderSite: N(zl),
  ServiceContact: N(fy)
});
function iy(i, t) {
  return B({}, V_, i, t);
}
function ny(i, t) {
  return B({}, U_, i, t);
}
function sy(i, t) {
  const e = i.getAttribute("name");
  if (!!e)
    return B({ name: e }, W_, i, t);
}
function ry(i, t) {
  return B({}, H_, i, t);
}
function oy(i, t) {
  return B({}, X_, i, t);
}
function ay(i, t) {
  const e = zl(i);
  if (!!e)
    return B(
      { href: e },
      J_,
      i,
      t
    );
}
function ly(i, t) {
  return B({}, Y_, i, t);
}
function hy(i, t) {
  const e = i.getAttribute("name"), n = B({}, j_, i, t);
  if (!n)
    return;
  const s = t[t.length - 1];
  s[e] = n;
}
function cy(i, t) {
  return B({}, K_, i, t);
}
function uy(i, t) {
  return B({}, q_, i, t);
}
function dy(i, t) {
  return B({}, ty, i, t);
}
function fy(i, t) {
  return B({}, Q_, i, t);
}
function gy(i, t) {
  return B({}, ey, i, t);
}
function my(i, t) {
  return st(i);
}
const py = Z_, ze = [null, "http://www.opengis.net/wmts/1.0"], Jn = [null, "http://www.opengis.net/ows/1.1"], _y = ut(ze, {
  Contents: N(Ty)
});
class yy extends mf {
  constructor() {
    super(), this.owsParser_ = new py();
  }
  readFromNode(t) {
    let e = t.getAttribute("version");
    e && (e = e.trim());
    let n = this.owsParser_.readFromNode(t);
    return n ? (n.version = e, n = B(
      n,
      _y,
      t,
      []
    ), n || null) : null;
  }
}
const vy = ut(ze, {
  Layer: ue(Iy),
  TileMatrixSet: ue(Py)
}), xy = ut(
  ze,
  {
    Style: ue(Ay),
    Format: ue(st),
    TileMatrixSetLink: ue(Oy),
    Dimension: ue(Ny),
    ResourceURL: ue(Fy)
  },
  ut(Jn, {
    Title: N(st),
    Abstract: N(st),
    WGS84BoundingBox: N(pf),
    Identifier: N(st)
  })
), Cy = ut(
  ze,
  {
    LegendURL: ue(Dy)
  },
  ut(Jn, {
    Title: N(st),
    Identifier: N(st)
  })
), My = ut(ze, {
  TileMatrixSet: N(st),
  TileMatrixSetLimits: N(Gy)
}), Ey = ut(ze, {
  TileMatrixLimits: H($y)
}), wy = ut(ze, {
  TileMatrix: N(st),
  MinTileRow: N(ne),
  MaxTileRow: N(ne),
  MinTileCol: N(ne),
  MaxTileCol: N(ne)
}), Sy = ut(
  ze,
  {
    Default: N(st),
    Value: ue(st)
  },
  ut(Jn, {
    Identifier: N(st)
  })
), Ry = ut(Jn, {
  LowerCorner: H(Fa),
  UpperCorner: H(Fa)
}), by = ut(
  ze,
  {
    WellKnownScaleSet: N(st),
    TileMatrix: ue(ky)
  },
  ut(Jn, {
    SupportedCRS: N(st),
    Identifier: N(st),
    BoundingBox: N(pf)
  })
), Ly = ut(
  ze,
  {
    TopLeftCorner: N(Fa),
    ScaleDenominator: N(f_),
    TileWidth: N(ne),
    TileHeight: N(ne),
    MatrixWidth: N(ne),
    MatrixHeight: N(ne)
  },
  ut(Jn, {
    Identifier: N(st)
  })
);
function Ty(i, t) {
  return B({}, vy, i, t);
}
function Iy(i, t) {
  return B({}, xy, i, t);
}
function Py(i, t) {
  return B({}, by, i, t);
}
function Ay(i, t) {
  const e = B({}, Cy, i, t);
  if (!e)
    return;
  const n = i.getAttribute("isDefault") === "true";
  return e.isDefault = n, e;
}
function Oy(i, t) {
  return B({}, My, i, t);
}
function Ny(i, t) {
  return B({}, Sy, i, t);
}
function Fy(i, t) {
  const e = i.getAttribute("format"), n = i.getAttribute("template"), s = i.getAttribute("resourceType"), r = {};
  return e && (r.format = e), n && (r.template = n), s && (r.resourceType = s), r;
}
function pf(i, t) {
  const e = B(
    [],
    Ry,
    i,
    t
  );
  if (e.length == 2)
    return aa(e);
}
function Dy(i, t) {
  const e = {};
  return e.format = i.getAttribute("format"), e.href = zl(i), e;
}
function Fa(i, t) {
  const e = st(i).split(/\s+/);
  if (!e || e.length != 2)
    return;
  const n = +e[0], s = +e[1];
  if (!(isNaN(n) || isNaN(s)))
    return [n, s];
}
function ky(i, t) {
  return B({}, Ly, i, t);
}
function Gy(i, t) {
  return B([], Ey, i, t);
}
function $y(i, t) {
  return B({}, wy, i, t);
}
const By = yy;
class zy {
  constructor() {
    const t = new By(), e = M().getOptions();
    let n = !0;
    const s = [];
    Promise.all(e.wmts.map((r) => {
      fetch(r.capability).then((o) => o.text()).then(function(o) {
        var c, u;
        const a = new op({
          opacity: 1
        }), l = t.read(o), h = up(l, {
          layer: r.layer,
          matrixSet: r.projection
        });
        h && (a.setSource(new cp(h)), a.setVisible(n), s.push(a), M().getMap().getLayers().insertAt(0, a), n = !1, M().getBorderConstraint() && a.setExtent((u = (c = M().getBorderConstraint()) == null ? void 0 : c.getSource()) == null ? void 0 : u.getExtent()), a.on("postrender", function(d) {
          var m, p;
          const f = u2(d), g = d.context;
          g && (g.globalCompositeOperation = "destination-in", (p = (m = M().getBorderConstraint()) == null ? void 0 : m.getSource()) == null || p.forEachFeature(function(_) {
            const y = new Ut({
              fill: new Yt({
                color: "white"
              })
            });
            f.drawFeature(_, y);
          }), g.globalCompositeOperation = "source-over");
        }));
      });
    })), e.border.url !== "" && window.addEventListener("border-contraint-enabled", () => {
      s.forEach((r) => {
        var o, a;
        return r.setExtent((a = (o = M().getBorderConstraint()) == null ? void 0 : o.getSource()) == null ? void 0 : a.getExtent());
      });
    }), window.addEventListener("layer-selected", (r) => {
      var o;
      s.forEach((a) => a.setVisible(!1)), (o = s.find((a) => {
        const l = a.getSource();
        return l && l.getLayer() === r.detail.layer ? a : void 0;
      })) == null || o.setVisible(!0);
    });
  }
}
const Zy = `:root,:host{--ol-background-color: white;--ol-accent-background-color: #F5F5F5;--ol-subtle-background-color: rgba(128, 128, 128, .25);--ol-partial-background-color: rgba(255, 255, 255, .75);--ol-foreground-color: #333333;--ol-subtle-foreground-color: #666666;--ol-brand-color: #00AAFF}.ol-box{box-sizing:border-box;border-radius:2px;border:1.5px solid var(--ol-background-color);background-color:var(--ol-partial-background-color)}.ol-mouse-position{top:8px;right:8px;position:absolute}.ol-scale-line{background:var(--ol-partial-background-color);border-radius:4px;bottom:8px;left:8px;padding:2px;position:absolute}.ol-scale-line-inner{border:1px solid var(--ol-subtle-foreground-color);border-top:none;color:var(--ol-foreground-color);font-size:10px;text-align:center;margin:1px;will-change:contents,width;transition:all .25s}.ol-scale-bar{position:absolute;bottom:8px;left:8px}.ol-scale-bar-inner{display:flex}.ol-scale-step-marker{width:1px;height:15px;background-color:var(--ol-foreground-color);float:right;z-index:10}.ol-scale-step-text{position:absolute;bottom:-5px;font-size:10px;z-index:11;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-text{position:absolute;font-size:12px;text-align:center;bottom:25px;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-singlebar{position:relative;height:10px;z-index:9;box-sizing:border-box;border:1px solid var(--ol-foreground-color)}.ol-scale-singlebar-even{background-color:var(--ol-subtle-foreground-color)}.ol-scale-singlebar-odd{background-color:var(--ol-background-color)}.ol-unsupported{display:none}.ol-viewport,.ol-unselectable{-webkit-touch-callout:none;-webkit-user-select:none;-moz-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}.ol-viewport canvas{all:unset}.ol-selectable{-webkit-touch-callout:default;-webkit-user-select:text;-moz-user-select:text;user-select:text}.ol-grabbing{cursor:-webkit-grabbing;cursor:-moz-grabbing;cursor:grabbing}.ol-grab{cursor:move;cursor:-webkit-grab;cursor:-moz-grab;cursor:grab}.ol-control{position:absolute;background-color:var(--ol-subtle-background-color);border-radius:4px}.ol-zoom{top:.5em;left:.5em}.ol-rotate{top:.5em;right:.5em;transition:opacity .25s linear,visibility 0s linear}.ol-rotate.ol-hidden{opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s linear .25s}.ol-zoom-extent{top:4.643em;left:.5em}.ol-full-screen{right:.5em;top:.5em}.ol-control button{display:block;margin:1px;padding:0;color:var(--ol-subtle-foreground-color);font-weight:700;text-decoration:none;font-size:inherit;text-align:center;height:1.375em;width:1.375em;line-height:.4em;background-color:var(--ol-background-color);border:none;border-radius:2px}.ol-control button::-moz-focus-inner{border:none;padding:0}.ol-zoom-extent button{line-height:1.4em}.ol-compass{display:block;font-weight:400;will-change:transform}.ol-touch .ol-control button{font-size:1.5em}.ol-touch .ol-zoom-extent{top:5.5em}.ol-control button:hover,.ol-control button:focus{text-decoration:none;outline:1px solid var(--ol-subtle-foreground-color);color:var(--ol-foreground-color)}.ol-zoom .ol-zoom-in{border-radius:2px 2px 0 0}.ol-zoom .ol-zoom-out{border-radius:0 0 2px 2px}.ol-attribution{text-align:right;bottom:.5em;right:.5em;max-width:calc(100% - 1.3em);display:flex;flex-flow:row-reverse;align-items:center}.ol-attribution a{color:var(--ol-subtle-foreground-color);text-decoration:none}.ol-attribution ul{margin:0;padding:1px .5em;color:var(--ol-foreground-color);text-shadow:0 0 2px var(--ol-background-color);font-size:12px}.ol-attribution li{display:inline;list-style:none}.ol-attribution li:not(:last-child):after{content:" "}.ol-attribution img{max-height:2em;max-width:inherit;vertical-align:middle}.ol-attribution button{flex-shrink:0}.ol-attribution.ol-collapsed ul{display:none}.ol-attribution:not(.ol-collapsed){background:var(--ol-partial-background-color)}.ol-attribution.ol-uncollapsible{bottom:0;right:0;border-radius:4px 0 0}.ol-attribution.ol-uncollapsible img{margin-top:-.2em;max-height:1.6em}.ol-attribution.ol-uncollapsible button{display:none}.ol-zoomslider{top:4.5em;left:.5em;height:200px}.ol-zoomslider button{position:relative;height:10px}.ol-touch .ol-zoomslider{top:5.5em}.ol-overviewmap{left:.5em;bottom:.5em}.ol-overviewmap.ol-uncollapsible{bottom:0;left:0;border-radius:0 4px 0 0}.ol-overviewmap .ol-overviewmap-map,.ol-overviewmap button{display:block}.ol-overviewmap .ol-overviewmap-map{border:1px solid var(--ol-subtle-foreground-color);height:150px;width:150px}.ol-overviewmap:not(.ol-collapsed) button{bottom:0;left:0;position:absolute}.ol-overviewmap.ol-collapsed .ol-overviewmap-map,.ol-overviewmap.ol-uncollapsible button{display:none}.ol-overviewmap:not(.ol-collapsed){background:var(--ol-subtle-background-color)}.ol-overviewmap-box{border:1.5px dotted var(--ol-subtle-foreground-color)}.ol-overviewmap .ol-overviewmap-box:hover{cursor:move}
`, Vy = `#map{width:100%;height:100%;background-color:#fff}.ol-layer{background-color:#80808020}.map-overlay{width:100vw;height:100vh;background-color:gray;opacity:.3}.overlay-index{z-index:10}
`, Lo = `.left-buttons-control-container{display:flex;position:absolute;width:var(--icon-width);flex-direction:column;left:var(--side-distance)}.right-buttons-control-container{display:flex;position:absolute;right:var(--side-distance);width:var(--icon-width);flex-direction:column}.ol-control{background-color:transparent}.ol-control button:hover{background-color:var(--control-background-color-hover);outline:none}.ol-control button:focus{background-color:var(--control-background-color-hover);outline:none}.ol-zoom{position:relative;top:0px;left:0px;margin-bottom:var(--top-distance)}.ol-zoom>.ol-zoom-in{margin-bottom:1px}.ol-full-screen{position:relative;width:var(--icon-width);top:0px;right:0px;margin-bottom:var(--top-distance)}.center-control,.information-control{margin-bottom:var(--top-distance)}.ol-zoom>button{margin:0}.ol-full-screen>button,.ol-full-screen-custom-small>button,.ol-full-screen-custom-medium>button,.ol-full-screen-custom-large>button{border-radius:var(--icon-border-radius);margin:0;cursor:pointer}.ol-control button{background-color:var(--control-background-color);width:var(--icon-width);height:var(--icon-height)}.ol-zoom-in,.ol-zoom-out,.information-control,.center-control,.rotation-control,.ol-full-screen-true,.ol-full-screen-false{z-index:0;position:relative;width:var(--icon-width);height:var(--icon-height);background-color:var(--control-background-color);border-radius:var(--icon-border-radius);cursor:pointer}.ol-zoom-in:hover,.ol-zoom-out:hover,.information-control:hover,.center-control:hover,.rotation-control:hover,.ol-full-screen-true:hover,.ol-full-screen-false:hover,.information-control:focus,.center-control:focus,.rotation-control:focus{background-color:var(--control-background-color-hover);outline:none}.ol-zoom-in{border-top-right-radius:var(--icon-border-radius);border-top-left-radius:var(--icon-border-radius)}.ol-zoom-out{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}.ol-zoom-in>div>svg,.ol-zoom-out>div>svg,.ol-full-screen-true>div>svg,.ol-full-screen-false>div>svg{width:var(--svg-icon-size);height:var(--svg-icon-size)}.ol-zoom-in>div>svg>g>.icon,.ol-zoom-out>div>svg>g>.icon,.ol-full-screen-true>div>svg>g>.icon,.ol-full-screen-false>div>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}@media only screen and (min-width: 420px){.left-buttons-control-container,.right-buttons-control-container{top:var(--top-distance)}}@media only screen and (max-width: 419px){.left-buttons-control-container,.right-buttons-control-container{top:calc(calc(var(--top-distance) * 2) + var(--box-height))}}
`, _f = `.notification-element-info-light{--notification-background-color: #DBEAFE;--notification-stroke-color: #1D4ED8;--notification-text-color: #1D4ED8}.notification-element-info-dark{--notification-background-color: #2563EB;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-warning-light{--notification-background-color: #FEF3C7;--notification-stroke-color: #B45309;--notification-text-color: #B45309}.notification-element-warning-dark{--notification-background-color: #D97706;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-error-light{--notification-background-color: #FEE2E2;--notification-stroke-color: #B91C1C;--notification-text-color: #B91C1C}.notification-element-error-dark{--notification-background-color: #DC2626;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}@media only screen and (max-width: 350px){.notification-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 351px) and (max-width: 995px){.notification-element{left:calc((100% - 334px)/2);width:100%;max-width:302px}}@media only screen and (min-width: 996px){.notification-element{left:calc((100% - (var(--notification-width) + 30px)) / 2);width:var(--notification-width)}}.notification-element{position:absolute;bottom:10px;display:block;font-family:sans-serif;--icon-size: 32px;background-color:var(--notification-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);z-index:5;grid-template-columns:100%;grid-template-rows:100%}.notification-title>div>svg{display:block;width:var(--icon-size);height:var(--icon-size);padding-right:10px}.notification-icon-container{height:100%}.notification-title>div>svg>g>.icon{fill:none;stroke:var(--notification-stroke-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round}.notification-title{display:flex}.notification-title-text{font-weight:400;font-size:12px;line-height:15px;color:var(--notification-text-color)}
`;
var Uy = Object.defineProperty, Wy = Object.getOwnPropertyDescriptor, qs = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Wy(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Uy(t, e, s), s;
};
let qi = class extends Pt {
  constructor() {
    super(), this.type = "info", this.message = "", this.icon = "", this.theme = "";
  }
  firstUpdated() {
    switch (this.type) {
      case "info":
        this.icon = rt.info, this.theme = `notification-element-info-${M().getTheme()}`;
        break;
      case "warning":
        this.icon = rt.warning, this.theme = `notification-element-warning-${M().getTheme()}`;
        break;
      case "error":
        this.icon = rt.error, this.theme = `notification-element-error-${M().getTheme()}`;
        break;
    }
  }
  render() {
    return Lt`
      <div class="notification-element ${this.theme}">
        <div class="notification-title">
          <div class="notification-icon-container">
            ${Le(this.icon)}
          </div>
          <div class="notification-title-text">${this.message}</div>
        </div>  
      </div>
    `;
  }
};
qi.styles = [yt(_f)];
qs([
  Ti()
], qi.prototype, "type", 2);
qs([
  Ti()
], qi.prototype, "message", 2);
qs([
  Dt()
], qi.prototype, "icon", 2);
qs([
  Dt()
], qi.prototype, "theme", 2);
qi = qs([
  qt("notification-box")
], qi);
class yn extends kt {
  constructor(t) {
    const e = document.createElement(
      "notification-box"
    );
    e.type = t.type, e.message = t.message, super({ element: e }), this.ruleType = t.rule.type, this.div = e, Wt.setResizeEvent(this.div, "--notification-width");
  }
  disable() {
    this.div.classList.add("disabled");
  }
  show() {
    this.div.classList.remove("fade-out"), this.div.classList.remove("disabled"), this.div.classList.add("fade-in");
  }
  hide() {
    this.div.classList.remove("fade-in"), this.div.classList.add("fade-out");
  }
}
class Hy {
  constructor() {
    this.validZoomConstraint = !0, this.validAreaConstraint = !0, this.validBorderContraint = !0, this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1;
    const t = M().getOptions();
    switch (t.mode.type) {
      case "target":
        this.setupTargetMode();
        break;
      case "select":
        this.setupSelectMode();
        break;
      case "create":
        this.setupCreateMode();
        break;
      case "mix":
        this.setupMixMode();
        break;
      default:
        M().getMap().addControl(new yn({
          type: "error",
          message: "Veuillez s\xE9lectionner un mode de fonctionnement valide.",
          rule: {
            type: "NOT_VALID_MODE"
          }
        }));
    }
    this.setup(t.notifications), this.displayRightNotification();
  }
  displayRightNotification() {
    var t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p, _, y, v, x, C, w, S, b, A;
    this.validZoomConstraint ? this.validBorderContraint ? this.validAreaConstraint ? this.displayMaxElementConstraint ? ((p = this.zoomNotificationControl) == null || p.hide(), (_ = this.inclusionNotificationControl) == null || _.hide(), (y = this.maxElementNotificationControl) == null || y.show(), (v = this.infosNotificationControl) == null || v.hide(), (x = this.borderContraintNotificationControl) == null || x.hide()) : ((C = this.zoomNotificationControl) == null || C.hide(), (w = this.inclusionNotificationControl) == null || w.hide(), (S = this.maxElementNotificationControl) == null || S.hide(), (b = this.infosNotificationControl) == null || b.show(), (A = this.borderContraintNotificationControl) == null || A.hide()) : ((u = this.zoomNotificationControl) == null || u.hide(), (d = this.inclusionNotificationControl) == null || d.show(), (f = this.maxElementNotificationControl) == null || f.hide(), (g = this.infosNotificationControl) == null || g.hide(), (m = this.borderContraintNotificationControl) == null || m.hide()) : ((o = this.zoomNotificationControl) == null || o.hide(), (a = this.inclusionNotificationControl) == null || a.hide(), (l = this.maxElementNotificationControl) == null || l.hide(), (h = this.infosNotificationControl) == null || h.hide(), (c = this.borderContraintNotificationControl) == null || c.show()) : ((t = this.zoomNotificationControl) == null || t.show(), (e = this.inclusionNotificationControl) == null || e.hide(), (n = this.maxElementNotificationControl) == null || n.hide(), (s = this.infosNotificationControl) == null || s.hide(), (r = this.borderContraintNotificationControl) == null || r.hide());
  }
  setupTargetMode() {
    window.addEventListener("current-center-position", (t) => {
      this.validZoomConstraint && this.validAreaConstraint && it.sendEvent("position-selected", this.generateTargetGeometry(t.detail));
    });
  }
  iconClickedListener() {
    window.addEventListener("icon-clicked", (t) => {
      const e = M().getSelectedFeatures();
      this.validZoomConstraint && e.length > 0 && (this.checkMaxElementContraint(e), this.validMaxElementConstraint && it.sendEvent("position-selected", this.generateExportData(e)), it.sendEvent("authorize-clicked", t.detail)), this.displayRightNotification();
    });
  }
  setupSelectMode() {
    this.iconClickedListener(), this.ruleValidationListener();
  }
  iconCreatedListener() {
    window.addEventListener("icon-created", (t) => {
      const e = M().getSelectedFeatures();
      this.checkMaxElementContraint(e), this.checkIsInBorder(e), this.validZoomConstraint && this.validMaxElementConstraint && e.length > 0 && this.validBorderContraint ? (it.sendEvent("position-selected", this.generateExportData(e)), it.sendEvent("authorize-created", t.detail)) : it.sendEvent("refused-created", t.detail), this.displayRightNotification();
    }), window.addEventListener("icon-removed", () => {
      it.sendEvent("position-selected", void 0), it.sendEvent("remove-created-icon", void 0);
    });
  }
  setupCreateMode() {
    this.iconCreatedListener(), this.ruleValidationListener();
  }
  ruleValidationListener() {
    window.addEventListener("rule-validation", () => {
      const t = M().getSelectedFeatures();
      this.checkMaxElementContraint(t), this.validZoomConstraint && this.validMaxElementConstraint && t.length > 0 ? it.sendEvent("position-selected", this.generateExportData(t)) : it.sendEvent("position-selected", void 0), this.displayRightNotification();
    });
  }
  setupMixMode() {
    this.iconClickedListener(), this.iconCreatedListener(), this.ruleValidationListener();
  }
  setup(t) {
    t.forEach((e) => {
      e.rule.type === "ZOOM_CONSTRAINT" && this.setupZoomContraint(e), e.rule.type === "AREA_CONSTRAINT" && this.setupInclusionAreaConstraint(e), e.rule.type === "MAX_SELECTION" && this.setupMaxSelectionConstraint(e), e.type === "info" && (this.infosNotificationControl = new yn(e), M().getMap().addControl(this.infosNotificationControl));
    }), M().getOptions().border.url !== "" && (this.borderContraintNotificationControl = new yn({
      type: "warning",
      message: M().getOptions().border.notification,
      rule: {
        type: "BORDER_CONSTRAINT"
      }
    }), this.borderContraintNotificationControl.hide(), M().getMap().addControl(this.borderContraintNotificationControl));
  }
  setupZoomContraint(t) {
    this.zoomNotificationControl = new yn(t), this.zoomNotificationControl.disable(), M().getMap().addControl(this.zoomNotificationControl), this.hasValidZoom(t) && (this.validZoomConstraint = !1), Wt.registerBorderConstaintMapEvent("change:resolution", () => {
      this.checkZoomConstraint(t), this.displayRightNotification();
    });
  }
  setupInclusionAreaConstraint(t) {
    this.inclusionNotificationControl = new yn(t), this.inclusionNotificationControl.disable(), M().getMap().addControl(this.inclusionNotificationControl), window.addEventListener("inclusion-area-included", (e) => {
      this.checkInclusionAreaConstraint(e.detail, t.rule.couldBypass), this.displayRightNotification();
    });
  }
  setupMaxSelectionConstraint(t) {
    const e = t.rule.maxElement;
    e !== void 0 && M().setMaxElement(e), t.message = t.message.replace("{x}", `${e}`), this.maxElementNotificationControl = new yn(t), this.maxElementNotificationControl.disable(), M().getMap().addControl(this.maxElementNotificationControl);
  }
  hasValidZoom(t) {
    const e = M().getMap().getView().getZoom();
    return e && t.rule.minZoom && e < t.rule.minZoom;
  }
  checkZoomConstraint(t) {
    this.hasValidZoom(t) ? (this.validZoomConstraint = !1, it.sendEvent("position-selected", void 0)) : (this.validZoomConstraint = !0, it.sendEvent("rule-validation", void 0));
  }
  checkInclusionAreaConstraint(t, e) {
    t ? this.validAreaConstraint = !0 : e ? this.validAreaConstraint = !0 : (this.validAreaConstraint = !1, it.sendEvent("position-selected", void 0));
  }
  checkMaxElementContraint(t) {
    M().getMaxElement() >= 0 && (t.length >= M().getMaxElement() ? M().getMaxElement() === 1 && t.length === M().getMaxElement() ? (this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1) : t.length > M().getMaxElement() && (this.validMaxElementConstraint = !1, this.displayMaxElementConstraint = !0) : (this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1));
  }
  checkIsInBorder(t) {
    var e, n, s;
    if (M().getOptions().border.url !== "") {
      const o = t[t.length - 1].getGeometry();
      ((s = (n = (e = M().getBorderConstraint()) == null ? void 0 : e.getSource()) == null ? void 0 : n.getFeatures()[0].getGeometry()) == null ? void 0 : s.intersectsCoordinate(o.getCoordinates())) ? this.validBorderContraint = !0 : (this.validBorderContraint = !1, this.displayRightNotification(), setTimeout(() => {
        this.validBorderContraint = !0, this.displayRightNotification();
      }, 2e3));
    } else
      this.validBorderContraint = !0;
  }
  convertToMultiPoint(t) {
    return new on({
      geometry: new wo([[t[0], t[1]]])
    });
  }
  formatGeometryCollection(t) {
    const e = new Ia(), n = new Vd(t);
    return e.writeGeometry(n, {
      decimals: 2
    });
  }
  generateGeometryCollection(t) {
    const e = [];
    return t.forEach((n) => {
      const s = n.getGeometry();
      if (s) {
        const r = s, o = this.convertToMultiPoint(r.getCoordinates()).getGeometry();
        o && e.push(o);
      }
    }), this.formatGeometryCollection(e);
  }
  formatFeatureCollection(t) {
    return new Ia().writeFeatures(t, {
      decimals: 2
    });
  }
  generateFeatureCollection(t) {
    const e = [];
    return t.forEach((n) => {
      const s = n.getGeometry();
      if (s) {
        const r = s, o = this.convertToMultiPoint(r.getCoordinates());
        if (o) {
          const a = n.get("objectid");
          a && M().getCurrentFeatureType(a) === "select" && o.set("objectid", a), e.push(o);
        }
      }
    }), this.formatFeatureCollection(e);
  }
  generateTargetGeometry(t) {
    const e = this.convertToMultiPoint(t);
    if (e) {
      if (M().getOptions().outputFormat === "GeometryCollection") {
        const n = e.getGeometry();
        return n ? this.formatGeometryCollection([n]) : void 0;
      }
      return this.formatFeatureCollection([e]);
    }
  }
  generateExportData(t) {
    return M().getOptions().outputFormat === "GeometryCollection" ? this.generateGeometryCollection(t) : this.generateFeatureCollection(t);
  }
}
const Xy = `:host>.no-box{--box-height: 0px;--top-distance: 10px}:host>.select{--box-height: 68px;--top-distance: 10px}:host>.large{--box-height: 79px;--top-distance: 10px}:host>.medium{--box-height: 64px;--top-distance: 10px}:host>.small{--box-height: 49px;--top-distance: 10px}:host>.light{--control-background-color: rgb(30 41 59 / 75%);--control-background-color-hover: rgb(30 41 59 / 100%);--control-icon-color: white;--information-box-background-color: white;--information-box-title-color: #1E293B;--information-cross-hover-color: rgb(30 41 59 / 75%);--information-box-text-color: #334155;--suggestion-box-text-color: #334155;--select-icon-background: #1E293B;--icon-border-color: #CBD5E1}:host>.dark{--control-background-color: rgb(255 255 255 / 75%);--control-background-color-hover: rgb(255 255 255 / 100%);--control-icon-color: #1E293B;--information-box-background-color: #1F2937;--information-box-title-color: #F3F4F6;--information-cross-hover-color: rgb(255 255 255 / 75%);--information-box-text-color: #9CA3AF;--suggestion-box-text-color: #F1F5F9;--select-icon-background: rgb(255,255,255, .75);--icon-border-color: #334155}:host>#map{--icon-width: 36px;--icon-height: 36px;--side-distance: 10px;--icon-border-radius: 4px;--box-border-radius: 4px;--svg-icon-size: 26px;--icon-stroke-width: 2px;font-family:sans-serif}
`, Yy = `@keyframes fadeIn{0%{opacity:0;visibility:inherit}to{opacity:1}}@keyframes fadeOut{0%{opacity:1}to{opacity:0;visibility:hidden}}.fade-in{animation:fadeIn .3s forwards}.fade-out{animation:fadeOut .3s forwards}.disabled{visibility:hidden}
`, jy = `@media only screen and (min-width: 513px){.layer-container-position{right:55px;width:100%}}@media only screen and (min-width: 315px) and (max-width: 512px){.layer-container-position{left:calc(50% - 151px);width:100%}}@media only screen and (max-width: 314px){.layer-container-position{left:10px;width:calc(100% - 20px)}}.layer-container-position{z-index:1;max-width:302px;top:var(--top-distance);position:absolute}@media only screen and (min-width: 513px){.custom-popup-element-position{right:55px;width:100%}}@media only screen and (min-width: 315px) and (max-width: 512px){.custom-popup-element-position{left:calc(50% - 151px);width:100%}}@media only screen and (max-width: 314px){.custom-popup-element-position{left:10px;width:calc(100% - 20px)}}.custom-popup-element-position{font-family:sans-serif;position:absolute;top:10px;z-index:2;max-width:302px}
`;
class Ky {
  constructor(t) {
    const e = {
      zoom: 15,
      minZoom: 1,
      maxZoom: 20,
      interaction: {
        displayZoom: !0,
        displayScaleLine: !1,
        fullscreen: !0,
        enableGeolocation: !1,
        enableCenterButton: !0,
        enableRotation: !0
      },
      defaultCenter: [2539057, 1181111],
      information: {
        duration: 5e3,
        title: "This is a title",
        content: "This is a content"
      },
      mode: {
        type: ""
      },
      cluster: {
        distance: 40,
        minDistance: 30
      },
      geolocationInformation: {
        displayBox: !0,
        reverseLocation: !1,
        currentLocation: !1
      },
      notifications: [],
      wfs: {
        url: ""
      },
      wmts: [{
        capability: "https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml",
        layer: "ch.swisstopo.pixelkarte-grau",
        projection: "EPSG:2056",
        name: "",
        thumbnail: ""
      }],
      inclusionArea: {
        url: "",
        filter: ""
      },
      selectionTargetBoxMessage: "",
      search: {
        displaySearch: !0,
        requestWithoutCustomValue: "https://api3.geo.admin.ch/rest/services/api/SearchServer?limit=5&&type=locations&sr=2056&lang=fr&origins=address%2Cparcel",
        bboxRestiction: "2523099.818000,1167985.282000,2549752.141000,1192697.773000"
      },
      border: {
        url: "",
        notification: ""
      },
      outputFormat: "GeometryCollection"
    };
    t.zoom !== void 0 && (e.zoom = t.zoom), t.minZoom !== void 0 && (e.minZoom = t.minZoom), t.maxZoom !== void 0 && (e.maxZoom = t.maxZoom), t.interaction !== void 0 && (e.interaction = t.interaction), t.search !== void 0 && (e.search = t.search), t.defaultCenter !== void 0 && t.defaultCenter[0] !== null && (e.defaultCenter = t.defaultCenter), t.information !== void 0 && (e.information = t.information), t.notifications !== void 0 && t.notifications.length > 0 && (e.notifications = t.notifications), t.mode !== void 0 && (e.mode = t.mode), t.cluster !== void 0 && (e.cluster = t.cluster), t.geolocationInformation !== void 0 && (e.geolocationInformation = t.geolocationInformation), t.wfs !== void 0 && (e.wfs = t.wfs), t.wmts !== void 0 && (e.wmts = t.wmts), t.inclusionArea !== void 0 && (e.inclusionArea = t.inclusionArea), t.selectionTargetBoxMessage !== void 0 && (e.selectionTargetBoxMessage = t.selectionTargetBoxMessage), t.border !== void 0 && (e.border = t.border), t.outputFormat !== void 0 && (e.outputFormat = t.outputFormat), M().setOptions(e);
  }
}
class qy {
  static setupStyle() {
    return new Ut({
      stroke: new Re({
        color: "#C026D3",
        width: 1
      }),
      fill: new Yt({
        color: "rgb(191, 38, 211, 0.10)"
      })
    });
  }
}
class Jy {
  constructor() {
    const t = gf.getSource(M().getOptions().inclusionArea.url, M().getOptions().inclusionArea.filter, !0), e = new Ys({
      source: t,
      style: qy.setupStyle()
    });
    M().getMap().addLayer(e), window.addEventListener("current-center-position", (n) => {
      var r;
      const s = t.getClosestFeatureToCoordinate(
        n.detail
      );
      if (((r = s.getGeometry()) == null ? void 0 : r.getType()) === "Polygon") {
        const o = s.getGeometry();
        it.sendEvent("inclusion-area-included", o == null ? void 0 : o.intersectsCoordinate(n.detail));
      }
    });
  }
}
const To = `svg{margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size);height:var(--svg-icon-size)}svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
var Qy = Object.defineProperty, tv = Object.getOwnPropertyDescriptor, ev = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? tv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Qy(t, e, s), s;
};
let Da = class extends Pt {
  constructor() {
    super();
  }
  render() {
    return Lt`<div class="ol-unselectable ol-control center-control" tabindex="0">
                  <div>
                    <div class="control-${M().getTheme()}">
                      ${Le(rt.geolocation)}
                    </div>
                  </div>
                </div>
    `;
  }
};
Da.styles = [yt(To), yt(Lo)];
Da = ev([
  qt("geolocation-control-button")
], Da);
class iv extends kt {
  constructor(t) {
    const e = document.createElement("geolocation-control-button");
    super({
      element: e
    }), e.addEventListener("click", this.centerMap.bind(this), !1), this.setTarget(t);
  }
  centerMap() {
    const t = M().getGeolocation();
    if (t) {
      const e = t.getPosition(), n = this.getMap();
      if (n) {
        const s = n.getView();
        e && s.setCenter(e);
      }
    }
  }
}
var nv = Object.defineProperty, sv = Object.getOwnPropertyDescriptor, rv = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? sv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && nv(t, e, s), s;
};
let ka = class extends Pt {
  render() {
    return Lt`<div class="control-${M().getTheme()}" tabindex="0">${Le(rt.rotation)}</div>`;
  }
};
ka.styles = [yt(To)];
ka = rv([
  qt("rotation-control-button")
], ka);
class Nc extends kt {
  constructor(t) {
    const e = document.createElement("div"), n = document.createElement("rotation-control-button");
    e.appendChild(n);
    const s = document.createElement("div");
    s.className = "rotation-control ", s.appendChild(e), super({
      element: s
    }), e.addEventListener("click", this.resetRotation.bind(this), !1), this.setTarget(t);
  }
  resetRotation() {
    M().getMap().getView().setRotation(0);
  }
}
const ov = `.custom-popup-element{background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:0 11px 11px;border-radius:var(--box-border-radius)}.custom-popup-element:after{content:"";width:var(--progress-width);height:4px;background:#008C6F;position:absolute;bottom:-1px;left:0;border-bottom-left-radius:4px;border-bottom-right-radius:var(--border-radius-right)}.custom-popup-title{display:flex;height:36px}.custom-popup-title-text{width:calc(100% - var(--svg-icon-size));font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color);align-items:center;display:flex}.custom-popup-title-svg-container{width:29px;height:36px;justify-content:flex-end;display:flex;align-items:center}.custom-popup-title-svg{width:10%;justify-content:flex-end;display:flex;fill:none;stroke:var(--information-box-title-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round;cursor:pointer}.custom-popup-title-svg:hover{stroke:var(--information-cross-hover-color)}.custom-popup-content{width:calc(100% - var(--svg-icon-size));font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var av = Object.defineProperty, lv = Object.getOwnPropertyDescriptor, Zl = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? lv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && av(t, e, s), s;
};
let Fs = class extends Pt {
  constructor() {
    super(), this._width = 100, this._borderRadiusRight = 0, window.addEventListener("clear-information-box-interval", this.clear.bind(this), !0), window.addEventListener("open-information-box", () => {
      this._width = 100;
      const i = M().getOptions().information.duration / 100;
      this.interval = setInterval(() => {
        this._width > 0 ? (this._width < 100 && (this._borderRadiusRight = 0), this._width--) : this.closeBox();
      }, i);
    });
  }
  render() {
    return Lt`
      <div class="information-box-${M().getTheme()} custom-popup-element" style="--progress-width: ${this._width}%; --border-radius-right: ${this._borderRadiusRight}px">
        <div class="custom-popup-title">
          <div class="custom-popup-title-text">${M().getOptions().information.title}</div>
          <div class="custom-popup-title-svg-container">
            <div class="cross-div" @click="${this.closeBox}">
              ${Le(rt.cross)}
            </div>
          </div>
        </div>
        <div class="custom-popup-content">${M().getOptions().information.content}</div>
        <div class="custom-progress-element"></div>
      </div>`;
  }
  clear() {
    clearInterval(this.interval);
  }
  closeBox() {
    clearInterval(this.interval), it.sendEvent("close-information-box", {});
  }
};
Fs.styles = [yt(ov)];
Zl([
  Dt()
], Fs.prototype, "_width", 2);
Zl([
  Dt()
], Fs.prototype, "_borderRadiusRight", 2);
Fs = Zl([
  qt("information-box")
], Fs);
class hv extends kt {
  constructor() {
    const t = document.createElement("information-box");
    super({ element: t }), this.div = t, this.div.classList.add("custom-popup-element-position");
  }
  show() {
    this.div.classList.remove("fade-out"), this.div.classList.add("fade-in");
  }
  hide() {
    this.div.classList.remove("fade-in"), this.div.classList.add("fade-out");
  }
}
var cv = Object.defineProperty, uv = Object.getOwnPropertyDescriptor, dv = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? uv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && cv(t, e, s), s;
};
let Ga = class extends Pt {
  constructor() {
    super();
  }
  render() {
    return Lt`<div class="information-control" tabindex="0">
                  <div>
                    <div class="control-${M().getTheme()}">
                      ${Le(rt.information)}
                    </div>
                  </div>
                </div>
    `;
  }
};
Ga.styles = [yt(To), yt(Lo)];
Ga = dv([
  qt("information-control-button")
], Ga);
class fv extends kt {
  constructor(t) {
    const e = document.createElement("information-control-button");
    super({
      element: e
    }), this.informationIsOpen = !0, e.addEventListener("click", this.toogleInformationBox.bind(this), !1), window.addEventListener("close-information-box", this.closeInformationBox.bind(this), !1), this.control = new hv(), M().getMap().addControl(this.control), this.openInformationBox(), this.setTarget(t);
  }
  closeInformationBox() {
    it.sendEvent("clear-information-box-interval", {}), this.control.hide(), this.informationIsOpen = !1;
  }
  openInformationBox() {
    this.control.show(), it.sendEvent("open-information-box", {}), this.informationIsOpen = !0;
  }
  toogleInformationBox() {
    this.informationIsOpen ? this.closeInformationBox() : this.openInformationBox();
  }
}
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const gv = Ol(class extends Nl {
  constructor(i) {
    var t;
    if (super(i), i.type !== Ud.ATTRIBUTE || i.name !== "class" || ((t = i.strings) === null || t === void 0 ? void 0 : t.length) > 2)
      throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.");
  }
  render(i) {
    return " " + Object.keys(i).filter((t) => i[t]).join(" ") + " ";
  }
  update(i, [t]) {
    var e, n;
    if (this.nt === void 0) {
      this.nt = /* @__PURE__ */ new Set(), i.strings !== void 0 && (this.st = new Set(i.strings.join(" ").split(/\s/).filter((r) => r !== "")));
      for (const r in t)
        t[r] && !(!((e = this.st) === null || e === void 0) && e.has(r)) && this.nt.add(r);
      return this.render(t);
    }
    const s = i.element.classList;
    this.nt.forEach((r) => {
      r in t || (s.remove(r), this.nt.delete(r));
    });
    for (const r in t) {
      const o = !!t[r];
      o === this.nt.has(r) || ((n = this.st) === null || n === void 0 ? void 0 : n.has(r)) || (o ? (s.add(r), this.nt.add(r)) : (s.remove(r), this.nt.delete(r)));
    }
    return Ei;
  }
}), yf = `.layer-container{font-family:sans-serif}.layer-title-container{border-radius:var(--icon-border-radius) var(--icon-border-radius) 0px 0px;border-bottom:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color)}.layer-text{width:calc(100% - 13px);height:36px;padding:0;font-weight:400;background-color:var(--information-box-background-color);font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color);margin:0 0 0 11px;align-items:center;display:flex}.layer-svg-container{width:29px;height:36px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-bottom-left-radius:var(--icon-border-radius);border-bottom-right-radius:var(--icon-border-radius)}li{height:64px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--information-box-text-color)}li>.image-container{width:56px;display:flex;align-items:center;justify-content:center;height:inherit;padding-right:9px}li>.image-container>img{width:46px;height:46px;border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color)}.selected-layer{border:2px solid #dc2626!important;border-radius:var(--icon-border-radius)}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var mv = Object.defineProperty, pv = Object.getOwnPropertyDescriptor, Vl = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? pv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && mv(t, e, s), s;
};
let to = class extends Pt {
  constructor() {
    super(...arguments), this._currentSelectedIndex = 0;
  }
  selectLayer(i, t) {
    it.sendEvent("layer-selected", i), this._currentSelectedIndex = t;
  }
  render() {
    return Lt`
                <ul>
                  ${M().getOptions().wmts.map(
      (i, t) => Lt`<li tabindex="0" @click=${() => this.selectLayer(i, t)}>
                          <div class="image-container">
                            <img class=${gv({ "selected-layer": this._currentSelectedIndex === t })} src="${i.thumbnail}"/>
                          </div>
                          <p>${i.name}</p>
                        </li>`
    )}
                </ul>
              `;
  }
};
to.styles = [yt(yf)];
Vl([
  Dt()
], to.prototype, "_currentSelectedIndex", 2);
to = Vl([
  qt("layer-list")
], to);
let $a = class extends Pt {
  render() {
    return Lt`<div class="layer-container">
                  <div class="layer-title-container">
                      <p class="layer-text">Affichage de la carte</p>
                      <div class="layer-svg-container">
                        <div class="cross-div" @click="${this.closeBox}">
                          ${Le(rt.cross)}
                        </div>
                      </div>
                  </div>
                  <layer-list />
              </div>`;
  }
  closeBox() {
    it.sendEvent("layer-selection-closed", void 0);
  }
};
$a.styles = [yt(yf)];
$a = Vl([
  qt("layer-selection")
], $a);
class _v extends kt {
  constructor() {
    const t = document.createElement("layer-selection");
    super({ element: t }), this.element.classList.add("layer-container-position");
  }
  disable() {
    this.element.classList.add("disabled");
  }
  show() {
    this.element.classList.remove("fade-out"), this.element.classList.remove("disabled"), this.element.classList.add("fade-in");
  }
  hide() {
    this.element.classList.remove("fade-in"), this.element.classList.add("fade-out");
  }
}
var yv = Object.defineProperty, vv = Object.getOwnPropertyDescriptor, xv = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? vv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && yv(t, e, s), s;
};
let Ba = class extends Pt {
  render() {
    return Lt`<div class="ol-unselectable ol-control center-control" tabindex="0">
                  <div>
                    <div class="control-${M().getTheme()}">
                      ${Le(rt.stack)}
                    </div>
                  </div>
                </div> `;
  }
};
Ba.styles = [yt(To), yt(Lo)];
Ba = xv([
  qt("geo-layer-control-button")
], Ba);
class Cv extends kt {
  constructor(t) {
    const e = document.createElement(
      "geo-layer-control-button"
    );
    super({
      element: e
    }), this.isOpen = !1, this.layerSelection = new _v(), this.layerSelection.disable(), M().getMap().addControl(this.layerSelection), e.addEventListener("click", () => {
      this.toogleSelection();
    }), window.addEventListener("layer-selection-closed", () => this.close()), this.setTarget(t);
  }
  toogleSelection() {
    this.isOpen = !this.isOpen, this.isOpen ? this.layerSelection.show() : this.layerSelection.hide();
  }
  close() {
    this.isOpen = !1, this.layerSelection.hide();
  }
}
class Fc extends kt {
  constructor(t) {
    const e = document.createElement("div");
    e.className = t, super({
      element: e
    }), this.div = e;
  }
}
class Mv {
  static setupIcon(t) {
    const e = M().getOptions(), n = t.readonly, s = M().getMap(), r = new Fc("left-buttons-control-container");
    s.addControl(r);
    const o = new Fc("right-buttons-control-container");
    s.addControl(o), n || s.addControl(new fv(o.div)), e.interaction.fullscreen && s.addControl(
      new R2({
        label: rt.fullScreenLabel(),
        labelActive: rt.fullScreenLabelActive(),
        className: "ol-full-screen",
        target: o.div
      })
    ), s.addControl(new Cv(o.div)), e.interaction.displayZoom && s.addControl(
      new ld({
        zoomInLabel: rt.zoomInLabel(),
        zoomOutLabel: rt.zoomOutLabel(),
        className: "ol-zoom",
        target: r.div
      })
    ), e.interaction.enableCenterButton && !n && s.addControl(new iv(r.div)), e.interaction.enableRotation && Wt.registerBorderConstaintMapEvent("change:rotation", (a) => Ev(s, a, r.div));
  }
}
function Ev(i, t, e) {
  i.getControls().forEach((n) => {
    n instanceof Nc && i.removeControl(n);
  }), t.target.getRotation() !== 0 && i.addControl(new Nc(e));
}
var wv = Object.defineProperty, Sv = Object.getOwnPropertyDescriptor, Rv = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Sv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && wv(t, e, s), s;
};
class bv {
  constructor() {
    M().getMap().getView().on("change:center", (t) => {
      it.sendEvent("current-center-position", t.target.getCenter());
    }), M().getOptions().border.url !== "" && Wt.registerWindowListener("border-contraint-enabled", "change:center", (t) => {
      it.sendEvent("current-center-position", t.target.getCenter());
    });
  }
}
let Dc = class extends Pt {
  constructor() {
    super();
  }
  render() {
    return Lt`
        <div style="position: relative; top: calc(50% - 64px); left: calc(50% - 64px); width: 128px">
            <svg width="128" height="128" viewBox="0 0 128 128" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g filter="url(#filter0_d_244_6943)">
                    <mask id="path-1-outside-1_244_6943" maskUnits="userSpaceOnUse" x="16" y="16" width="96" height="96" fill="black">
                        <rect fill="white" x="16" y="16" width="96" height="96"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M64 19C39.1472 19 19 39.1472 19 64C19 88.8528 39.1472 109 64 109C88.8528 109 109 88.8528 109 64C109 39.1472 88.8528 19 64 19ZM17 64C17 38.0426 38.0426 17 64 17C89.9574 17 111 38.0426 111 64C111 89.9574 89.9574 111 64 111C38.0426 111 17 89.9574 17 64Z"/>
                    </mask>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M64 19C39.1472 19 19 39.1472 19 64C19 88.8528 39.1472 109 64 109C88.8528 109 109 88.8528 109 64C109 39.1472 88.8528 19 64 19ZM17 64C17 38.0426 38.0426 17 64 17C89.9574 17 111 38.0426 111 64C111 89.9574 89.9574 111 64 111C38.0426 111 17 89.9574 17 64Z" fill="#EF4444"/>
                    <path d="M20 64C20 39.6995 39.6995 20 64 20V18C38.5949 18 18 38.5949 18 64H20ZM64 108C39.6995 108 20 88.3005 20 64H18C18 89.4051 38.5949 110 64 110V108ZM108 64C108 88.3005 88.3005 108 64 108V110C89.4051 110 110 89.4051 110 64H108ZM64 20C88.3005 20 108 39.6995 108 64H110C110 38.5949 89.4051 18 64 18V20ZM64 16C37.4903 16 16 37.4903 16 64H18C18 38.5949 38.5949 18 64 18V16ZM112 64C112 37.4903 90.5097 16 64 16V18C89.4051 18 110 38.5949 110 64H112ZM64 112C90.5097 112 112 90.5097 112 64H110C110 89.4051 89.4051 110 64 110V112ZM16 64C16 90.5097 37.4903 112 64 112V110C38.5949 110 18 89.4051 18 64H16Z" fill="white" mask="url(#path-1-outside-1_244_6943)"/>
                    <circle cx="64" cy="64" r="2.5" fill="#EF4444" stroke="white"/>
                </g>
                <defs>
                    <filter id="filter0_d_244_6943" x="10" y="10" width="108" height="108" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                        <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                        <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                        <feOffset/>
                        <feGaussianBlur stdDeviation="3"/>
                        <feComposite in2="hardAlpha" operator="out"/>
                        <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.75 0"/>
                        <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_244_6943"/>
                        <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_244_6943" result="shape"/>
                    </filter>
                </defs>
            </svg>        
        </div>
        `;
  }
};
Dc = Rv([
  qt("target-element")
], Dc);
class Lv extends kt {
  constructor() {
    const t = document.createElement("target-element");
    super({ element: t }), new bv();
  }
}
const Tv = `@media only screen and (min-width: 351px) and (max-width: 995px){.box-element{left:calc(50% - 167px);width:calc(100% - 30px);max-width:302px}}@media only screen and (max-width: 350px){.box-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 996px){.box-element{left:calc((100% - (var(--target-box-width) + 30px)) / 2);width:calc(var(--target-box-width))}}.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color)}.box-element-title{display:flex}.box-element-title-text{width:90%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}
`;
var Iv = Object.defineProperty, Pv = Object.getOwnPropertyDescriptor, Js = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Pv(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Iv(t, e, s), s;
};
let Ji = class extends Pt {
  constructor() {
    super(), this.defaultPosition = [0, 0], this._currentPosition = "", this._reversePosition = "", this._lastPosition = this.defaultPosition;
    const i = 20;
    window.addEventListener("current-center-position", (t) => {
      M().getOptions().geolocationInformation.reverseLocation ? (Math.abs(this._lastPosition[0] - t.detail[0]) > i || Math.abs(this._lastPosition[1] - t.detail[1]) > i) && (this._lastPosition = t.detail, this.searchAddress(t.detail)) : this._reversePosition = "", this._currentPosition = M().getOptions().geolocationInformation.currentLocation ? `${t.detail[0].toFixed(6)}, ${t.detail[1].toFixed(6)}` : "";
    });
  }
  connectedCallback() {
    super.connectedCallback();
  }
  searchAddress(i) {
    ef.getAddressFromCoordinate(i).then((t) => {
      this._reversePosition = t.results.length > 0 ? `\xC0 proximit\xE9 de ${t.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
    });
  }
  firstUpdated() {
    M().getOptions().geolocationInformation.reverseLocation ? this.searchAddress(this.defaultPosition) : this._reversePosition = "", this._currentPosition = M().getOptions().geolocationInformation.currentLocation ? `${this.defaultPosition[0].toFixed(6)}, ${this.defaultPosition[1].toFixed(6)}` : "";
  }
  render() {
    return Lt`
      <div class="information-box-${M().getTheme()} box-element">
        <div class="box-element-title">
          <div class="box-element-title-text">${M().getOptions().selectionTargetBoxMessage}</div>
        </div>
        <div class="box-element-content">${this._reversePosition}</div>
        <div class="box-element-content">${this._currentPosition}</div>
      </div>
    `;
  }
};
Ji.styles = [yt(Tv)];
Js([
  Ti()
], Ji.prototype, "defaultPosition", 2);
Js([
  Dt()
], Ji.prototype, "_currentPosition", 2);
Js([
  Dt()
], Ji.prototype, "_reversePosition", 2);
Js([
  Dt()
], Ji.prototype, "_lastPosition", 2);
Ji = Js([
  qt("target-information-box-element")
], Ji);
class Av extends kt {
  constructor() {
    const t = document.createElement("target-information-box-element");
    t.defaultPosition = M().getOptions().defaultCenter, super({ element: t }), Wt.setResizeEvent(this.element, "--target-box-width");
  }
}
function Ov(i) {
  i("EPSG:4326", "+title=WGS 84 (long/lat) +proj=longlat +ellps=WGS84 +datum=WGS84 +units=degrees"), i("EPSG:4269", "+title=NAD83 (long/lat) +proj=longlat +a=6378137.0 +b=6356752.31414036 +ellps=GRS80 +datum=NAD83 +units=degrees"), i("EPSG:3857", "+title=WGS 84 / Pseudo-Mercator +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"), i.WGS84 = i["EPSG:4326"], i["EPSG:3785"] = i["EPSG:3857"], i.GOOGLE = i["EPSG:3857"], i["EPSG:900913"] = i["EPSG:3857"], i["EPSG:102113"] = i["EPSG:3857"];
}
var Qi = 1, tn = 2, Ir = 3, Nv = 4, za = 5, kc = 6378137, Fv = 6356752314e-3, Gc = 0.0066943799901413165, ys = 484813681109536e-20, R = Math.PI / 2, Dv = 0.16666666666666666, kv = 0.04722222222222222, Gv = 0.022156084656084655, I = 1e-10, Bt = 0.017453292519943295, Ne = 57.29577951308232, ht = Math.PI / 4, Ds = Math.PI * 2, Rt = 3.14159265359, oe = {};
oe.greenwich = 0;
oe.lisbon = -9.131906111111;
oe.paris = 2.337229166667;
oe.bogota = -74.080916666667;
oe.madrid = -3.687938888889;
oe.rome = 12.452333333333;
oe.bern = 7.439583333333;
oe.jakarta = 106.807719444444;
oe.ferro = -17.666666666667;
oe.brussels = 4.367975;
oe.stockholm = 18.058277777778;
oe.athens = 23.7163375;
oe.oslo = 10.722916666667;
const $v = {
  ft: { to_meter: 0.3048 },
  "us-ft": { to_meter: 1200 / 3937 }
};
var $c = /[\s_\-\/\(\)]/g;
function bi(i, t) {
  if (i[t])
    return i[t];
  for (var e = Object.keys(i), n = t.toLowerCase().replace($c, ""), s = -1, r, o; ++s < e.length; )
    if (r = e[s], o = r.toLowerCase().replace($c, ""), o === n)
      return i[r];
}
function Za(i) {
  var t = {}, e = i.split("+").map(function(a) {
    return a.trim();
  }).filter(function(a) {
    return a;
  }).reduce(function(a, l) {
    var h = l.split("=");
    return h.push(!0), a[h[0].toLowerCase()] = h[1], a;
  }, {}), n, s, r, o = {
    proj: "projName",
    datum: "datumCode",
    rf: function(a) {
      t.rf = parseFloat(a);
    },
    lat_0: function(a) {
      t.lat0 = a * Bt;
    },
    lat_1: function(a) {
      t.lat1 = a * Bt;
    },
    lat_2: function(a) {
      t.lat2 = a * Bt;
    },
    lat_ts: function(a) {
      t.lat_ts = a * Bt;
    },
    lon_0: function(a) {
      t.long0 = a * Bt;
    },
    lon_1: function(a) {
      t.long1 = a * Bt;
    },
    lon_2: function(a) {
      t.long2 = a * Bt;
    },
    alpha: function(a) {
      t.alpha = parseFloat(a) * Bt;
    },
    gamma: function(a) {
      t.rectified_grid_angle = parseFloat(a);
    },
    lonc: function(a) {
      t.longc = a * Bt;
    },
    x_0: function(a) {
      t.x0 = parseFloat(a);
    },
    y_0: function(a) {
      t.y0 = parseFloat(a);
    },
    k_0: function(a) {
      t.k0 = parseFloat(a);
    },
    k: function(a) {
      t.k0 = parseFloat(a);
    },
    a: function(a) {
      t.a = parseFloat(a);
    },
    b: function(a) {
      t.b = parseFloat(a);
    },
    r_a: function() {
      t.R_A = !0;
    },
    zone: function(a) {
      t.zone = parseInt(a, 10);
    },
    south: function() {
      t.utmSouth = !0;
    },
    towgs84: function(a) {
      t.datum_params = a.split(",").map(function(l) {
        return parseFloat(l);
      });
    },
    to_meter: function(a) {
      t.to_meter = parseFloat(a);
    },
    units: function(a) {
      t.units = a;
      var l = bi($v, a);
      l && (t.to_meter = l.to_meter);
    },
    from_greenwich: function(a) {
      t.from_greenwich = a * Bt;
    },
    pm: function(a) {
      var l = bi(oe, a);
      t.from_greenwich = (l || parseFloat(a)) * Bt;
    },
    nadgrids: function(a) {
      a === "@null" ? t.datumCode = "none" : t.nadgrids = a;
    },
    axis: function(a) {
      var l = "ewnsud";
      a.length === 3 && l.indexOf(a.substr(0, 1)) !== -1 && l.indexOf(a.substr(1, 1)) !== -1 && l.indexOf(a.substr(2, 1)) !== -1 && (t.axis = a);
    },
    approx: function() {
      t.approx = !0;
    }
  };
  for (n in e)
    s = e[n], n in o ? (r = o[n], typeof r == "function" ? r(s) : t[r] = s) : t[n] = s;
  return typeof t.datumCode == "string" && t.datumCode !== "WGS84" && (t.datumCode = t.datumCode.toLowerCase()), t;
}
var ks = 1, vf = 2, xf = 3, eo = 4, Cf = 5, Ul = -1, Bv = /\s/, zv = /[A-Za-z]/, Zv = /[A-Za-z84_]/, Io = /[,\]]/, Mf = /[\d\.E\-\+]/;
function oi(i) {
  if (typeof i != "string")
    throw new Error("not a string");
  this.text = i.trim(), this.level = 0, this.place = 0, this.root = null, this.stack = [], this.currentObject = null, this.state = ks;
}
oi.prototype.readCharicter = function() {
  var i = this.text[this.place++];
  if (this.state !== eo)
    for (; Bv.test(i); ) {
      if (this.place >= this.text.length)
        return;
      i = this.text[this.place++];
    }
  switch (this.state) {
    case ks:
      return this.neutral(i);
    case vf:
      return this.keyword(i);
    case eo:
      return this.quoted(i);
    case Cf:
      return this.afterquote(i);
    case xf:
      return this.number(i);
    case Ul:
      return;
  }
};
oi.prototype.afterquote = function(i) {
  if (i === '"') {
    this.word += '"', this.state = eo;
    return;
  }
  if (Io.test(i)) {
    this.word = this.word.trim(), this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in afterquote yet, index ' + this.place);
};
oi.prototype.afterItem = function(i) {
  if (i === ",") {
    this.word !== null && this.currentObject.push(this.word), this.word = null, this.state = ks;
    return;
  }
  if (i === "]") {
    this.level--, this.word !== null && (this.currentObject.push(this.word), this.word = null), this.state = ks, this.currentObject = this.stack.pop(), this.currentObject || (this.state = Ul);
    return;
  }
};
oi.prototype.number = function(i) {
  if (Mf.test(i)) {
    this.word += i;
    return;
  }
  if (Io.test(i)) {
    this.word = parseFloat(this.word), this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in number yet, index ' + this.place);
};
oi.prototype.quoted = function(i) {
  if (i === '"') {
    this.state = Cf;
    return;
  }
  this.word += i;
};
oi.prototype.keyword = function(i) {
  if (Zv.test(i)) {
    this.word += i;
    return;
  }
  if (i === "[") {
    var t = [];
    t.push(this.word), this.level++, this.root === null ? this.root = t : this.currentObject.push(t), this.stack.push(this.currentObject), this.currentObject = t, this.state = ks;
    return;
  }
  if (Io.test(i)) {
    this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in keyword yet, index ' + this.place);
};
oi.prototype.neutral = function(i) {
  if (zv.test(i)) {
    this.word = i, this.state = vf;
    return;
  }
  if (i === '"') {
    this.word = "", this.state = eo;
    return;
  }
  if (Mf.test(i)) {
    this.word = i, this.state = xf;
    return;
  }
  if (Io.test(i)) {
    this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in neutral yet, index ' + this.place);
};
oi.prototype.output = function() {
  for (; this.place < this.text.length; )
    this.readCharicter();
  if (this.state === Ul)
    return this.root;
  throw new Error('unable to parse string "' + this.text + '". State is ' + this.state);
};
function Vv(i) {
  var t = new oi(i);
  return t.output();
}
function Bc(i, t, e) {
  Array.isArray(t) && (e.unshift(t), t = null);
  var n = t ? {} : i, s = e.reduce(function(r, o) {
    return bn(o, r), r;
  }, n);
  t && (i[t] = s);
}
function bn(i, t) {
  if (!Array.isArray(i)) {
    t[i] = !0;
    return;
  }
  var e = i.shift();
  if (e === "PARAMETER" && (e = i.shift()), i.length === 1) {
    if (Array.isArray(i[0])) {
      t[e] = {}, bn(i[0], t[e]);
      return;
    }
    t[e] = i[0];
    return;
  }
  if (!i.length) {
    t[e] = !0;
    return;
  }
  if (e === "TOWGS84") {
    t[e] = i;
    return;
  }
  if (e === "AXIS") {
    e in t || (t[e] = []), t[e].push(i);
    return;
  }
  Array.isArray(e) || (t[e] = {});
  var n;
  switch (e) {
    case "UNIT":
    case "PRIMEM":
    case "VERT_DATUM":
      t[e] = {
        name: i[0].toLowerCase(),
        convert: i[1]
      }, i.length === 3 && bn(i[2], t[e]);
      return;
    case "SPHEROID":
    case "ELLIPSOID":
      t[e] = {
        name: i[0],
        a: i[1],
        rf: i[2]
      }, i.length === 4 && bn(i[3], t[e]);
      return;
    case "PROJECTEDCRS":
    case "PROJCRS":
    case "GEOGCS":
    case "GEOCCS":
    case "PROJCS":
    case "LOCAL_CS":
    case "GEODCRS":
    case "GEODETICCRS":
    case "GEODETICDATUM":
    case "EDATUM":
    case "ENGINEERINGDATUM":
    case "VERT_CS":
    case "VERTCRS":
    case "VERTICALCRS":
    case "COMPD_CS":
    case "COMPOUNDCRS":
    case "ENGINEERINGCRS":
    case "ENGCRS":
    case "FITTED_CS":
    case "LOCAL_DATUM":
    case "DATUM":
      i[0] = ["name", i[0]], Bc(t, e, i);
      return;
    default:
      for (n = -1; ++n < i.length; )
        if (!Array.isArray(i[n]))
          return bn(i, t[e]);
      return Bc(t, e, i);
  }
}
var Uv = 0.017453292519943295;
function Wv(i, t) {
  var e = t[0], n = t[1];
  !(e in i) && n in i && (i[e] = i[n], t.length === 3 && (i[e] = t[2](i[e])));
}
function Ye(i) {
  return i * Uv;
}
function Hv(i) {
  if (i.type === "GEOGCS" ? i.projName = "longlat" : i.type === "LOCAL_CS" ? (i.projName = "identity", i.local = !0) : typeof i.PROJECTION == "object" ? i.projName = Object.keys(i.PROJECTION)[0] : i.projName = i.PROJECTION, i.AXIS) {
    for (var t = "", e = 0, n = i.AXIS.length; e < n; ++e) {
      var s = [i.AXIS[e][0].toLowerCase(), i.AXIS[e][1].toLowerCase()];
      s[0].indexOf("north") !== -1 || (s[0] === "y" || s[0] === "lat") && s[1] === "north" ? t += "n" : s[0].indexOf("south") !== -1 || (s[0] === "y" || s[0] === "lat") && s[1] === "south" ? t += "s" : s[0].indexOf("east") !== -1 || (s[0] === "x" || s[0] === "lon") && s[1] === "east" ? t += "e" : (s[0].indexOf("west") !== -1 || (s[0] === "x" || s[0] === "lon") && s[1] === "west") && (t += "w");
    }
    t.length === 2 && (t += "u"), t.length === 3 && (i.axis = t);
  }
  i.UNIT && (i.units = i.UNIT.name.toLowerCase(), i.units === "metre" && (i.units = "meter"), i.UNIT.convert && (i.type === "GEOGCS" ? i.DATUM && i.DATUM.SPHEROID && (i.to_meter = i.UNIT.convert * i.DATUM.SPHEROID.a) : i.to_meter = i.UNIT.convert));
  var r = i.GEOGCS;
  i.type === "GEOGCS" && (r = i), r && (r.DATUM ? i.datumCode = r.DATUM.name.toLowerCase() : i.datumCode = r.name.toLowerCase(), i.datumCode.slice(0, 2) === "d_" && (i.datumCode = i.datumCode.slice(2)), (i.datumCode === "new_zealand_geodetic_datum_1949" || i.datumCode === "new_zealand_1949") && (i.datumCode = "nzgd49"), (i.datumCode === "wgs_1984" || i.datumCode === "world_geodetic_system_1984") && (i.PROJECTION === "Mercator_Auxiliary_Sphere" && (i.sphere = !0), i.datumCode = "wgs84"), i.datumCode.slice(-6) === "_ferro" && (i.datumCode = i.datumCode.slice(0, -6)), i.datumCode.slice(-8) === "_jakarta" && (i.datumCode = i.datumCode.slice(0, -8)), ~i.datumCode.indexOf("belge") && (i.datumCode = "rnb72"), r.DATUM && r.DATUM.SPHEROID && (i.ellps = r.DATUM.SPHEROID.name.replace("_19", "").replace(/[Cc]larke\_18/, "clrk"), i.ellps.toLowerCase().slice(0, 13) === "international" && (i.ellps = "intl"), i.a = r.DATUM.SPHEROID.a, i.rf = parseFloat(r.DATUM.SPHEROID.rf, 10)), r.DATUM && r.DATUM.TOWGS84 && (i.datum_params = r.DATUM.TOWGS84), ~i.datumCode.indexOf("osgb_1936") && (i.datumCode = "osgb36"), ~i.datumCode.indexOf("osni_1952") && (i.datumCode = "osni52"), (~i.datumCode.indexOf("tm65") || ~i.datumCode.indexOf("geodetic_datum_of_1965")) && (i.datumCode = "ire65"), i.datumCode === "ch1903+" && (i.datumCode = "ch1903"), ~i.datumCode.indexOf("israel") && (i.datumCode = "isr93")), i.b && !isFinite(i.b) && (i.b = i.a);
  function o(h) {
    var c = i.to_meter || 1;
    return h * c;
  }
  var a = function(h) {
    return Wv(i, h);
  }, l = [
    ["standard_parallel_1", "Standard_Parallel_1"],
    ["standard_parallel_1", "Latitude of 1st standard parallel"],
    ["standard_parallel_2", "Standard_Parallel_2"],
    ["standard_parallel_2", "Latitude of 2nd standard parallel"],
    ["false_easting", "False_Easting"],
    ["false_easting", "False easting"],
    ["false-easting", "Easting at false origin"],
    ["false_northing", "False_Northing"],
    ["false_northing", "False northing"],
    ["false_northing", "Northing at false origin"],
    ["central_meridian", "Central_Meridian"],
    ["central_meridian", "Longitude of natural origin"],
    ["central_meridian", "Longitude of false origin"],
    ["latitude_of_origin", "Latitude_Of_Origin"],
    ["latitude_of_origin", "Central_Parallel"],
    ["latitude_of_origin", "Latitude of natural origin"],
    ["latitude_of_origin", "Latitude of false origin"],
    ["scale_factor", "Scale_Factor"],
    ["k0", "scale_factor"],
    ["latitude_of_center", "Latitude_Of_Center"],
    ["latitude_of_center", "Latitude_of_center"],
    ["lat0", "latitude_of_center", Ye],
    ["longitude_of_center", "Longitude_Of_Center"],
    ["longitude_of_center", "Longitude_of_center"],
    ["longc", "longitude_of_center", Ye],
    ["x0", "false_easting", o],
    ["y0", "false_northing", o],
    ["long0", "central_meridian", Ye],
    ["lat0", "latitude_of_origin", Ye],
    ["lat0", "standard_parallel_1", Ye],
    ["lat1", "standard_parallel_1", Ye],
    ["lat2", "standard_parallel_2", Ye],
    ["azimuth", "Azimuth"],
    ["alpha", "azimuth", Ye],
    ["srsCode", "name"]
  ];
  l.forEach(a), !i.long0 && i.longc && (i.projName === "Albers_Conic_Equal_Area" || i.projName === "Lambert_Azimuthal_Equal_Area") && (i.long0 = i.longc), !i.lat_ts && i.lat1 && (i.projName === "Stereographic_South_Pole" || i.projName === "Polar Stereographic (variant B)") && (i.lat0 = Ye(i.lat1 > 0 ? 90 : -90), i.lat_ts = i.lat1);
}
function Ef(i) {
  var t = Vv(i), e = t.shift(), n = t.shift();
  t.unshift(["name", n]), t.unshift(["type", e]);
  var s = {};
  return bn(t, s), Hv(s), s;
}
function Xt(i) {
  var t = this;
  if (arguments.length === 2) {
    var e = arguments[1];
    typeof e == "string" ? e.charAt(0) === "+" ? Xt[i] = Za(arguments[1]) : Xt[i] = Ef(arguments[1]) : Xt[i] = e;
  } else if (arguments.length === 1) {
    if (Array.isArray(i))
      return i.map(function(n) {
        Array.isArray(n) ? Xt.apply(t, n) : Xt(n);
      });
    if (typeof i == "string") {
      if (i in Xt)
        return Xt[i];
    } else
      "EPSG" in i ? Xt["EPSG:" + i.EPSG] = i : "ESRI" in i ? Xt["ESRI:" + i.ESRI] = i : "IAU2000" in i ? Xt["IAU2000:" + i.IAU2000] = i : console.log(i);
    return;
  }
}
Ov(Xt);
function Xv(i) {
  return typeof i == "string";
}
function Yv(i) {
  return i in Xt;
}
var jv = ["PROJECTEDCRS", "PROJCRS", "GEOGCS", "GEOCCS", "PROJCS", "LOCAL_CS", "GEODCRS", "GEODETICCRS", "GEODETICDATUM", "ENGCRS", "ENGINEERINGCRS"];
function Kv(i) {
  return jv.some(function(t) {
    return i.indexOf(t) > -1;
  });
}
var qv = ["3857", "900913", "3785", "102113"];
function Jv(i) {
  var t = bi(i, "authority");
  if (!!t) {
    var e = bi(t, "epsg");
    return e && qv.indexOf(e) > -1;
  }
}
function Qv(i) {
  var t = bi(i, "extension");
  if (!!t)
    return bi(t, "proj4");
}
function tx(i) {
  return i[0] === "+";
}
function ex(i) {
  if (Xv(i)) {
    if (Yv(i))
      return Xt[i];
    if (Kv(i)) {
      var t = Ef(i);
      if (Jv(t))
        return Xt["EPSG:3857"];
      var e = Qv(t);
      return e ? Za(e) : t;
    }
    if (tx(i))
      return Za(i);
  } else
    return i;
}
function zc(i, t) {
  i = i || {};
  var e, n;
  if (!t)
    return i;
  for (n in t)
    e = t[n], e !== void 0 && (i[n] = e);
  return i;
}
function $e(i, t, e) {
  var n = i * t;
  return e / Math.sqrt(1 - n * n);
}
function Qs(i) {
  return i < 0 ? -1 : 1;
}
function O(i) {
  return Math.abs(i) <= Rt ? i : i - Qs(i) * Ds;
}
function be(i, t, e) {
  var n = i * e, s = 0.5 * i;
  return n = Math.pow((1 - n) / (1 + n), s), Math.tan(0.5 * (R - t)) / n;
}
function Gs(i, t) {
  for (var e = 0.5 * i, n, s, r = R - 2 * Math.atan(t), o = 0; o <= 15; o++)
    if (n = i * Math.sin(r), s = R - 2 * Math.atan(t * Math.pow((1 - n) / (1 + n), e)) - r, r += s, Math.abs(s) <= 1e-10)
      return r;
  return -9999;
}
function ix() {
  var i = this.b / this.a;
  this.es = 1 - i * i, "x0" in this || (this.x0 = 0), "y0" in this || (this.y0 = 0), this.e = Math.sqrt(this.es), this.lat_ts ? this.sphere ? this.k0 = Math.cos(this.lat_ts) : this.k0 = $e(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) : this.k0 || (this.k ? this.k0 = this.k : this.k0 = 1);
}
function nx(i) {
  var t = i.x, e = i.y;
  if (e * Ne > 90 && e * Ne < -90 && t * Ne > 180 && t * Ne < -180)
    return null;
  var n, s;
  if (Math.abs(Math.abs(e) - R) <= I)
    return null;
  if (this.sphere)
    n = this.x0 + this.a * this.k0 * O(t - this.long0), s = this.y0 + this.a * this.k0 * Math.log(Math.tan(ht + 0.5 * e));
  else {
    var r = Math.sin(e), o = be(this.e, e, r);
    n = this.x0 + this.a * this.k0 * O(t - this.long0), s = this.y0 - this.a * this.k0 * Math.log(o);
  }
  return i.x = n, i.y = s, i;
}
function sx(i) {
  var t = i.x - this.x0, e = i.y - this.y0, n, s;
  if (this.sphere)
    s = R - 2 * Math.atan(Math.exp(-e / (this.a * this.k0)));
  else {
    var r = Math.exp(-e / (this.a * this.k0));
    if (s = Gs(this.e, r), s === -9999)
      return null;
  }
  return n = O(this.long0 + t / (this.a * this.k0)), i.x = n, i.y = s, i;
}
var rx = ["Mercator", "Popular Visualisation Pseudo Mercator", "Mercator_1SP", "Mercator_Auxiliary_Sphere", "merc"];
const ox = {
  init: ix,
  forward: nx,
  inverse: sx,
  names: rx
};
function ax() {
}
function Zc(i) {
  return i;
}
var lx = ["longlat", "identity"];
const hx = {
  init: ax,
  forward: Zc,
  inverse: Zc,
  names: lx
};
var cx = [ox, hx], Pr = {}, io = [];
function wf(i, t) {
  var e = io.length;
  return i.names ? (io[e] = i, i.names.forEach(function(n) {
    Pr[n.toLowerCase()] = e;
  }), this) : (console.log(t), !0);
}
function ux(i) {
  if (!i)
    return !1;
  var t = i.toLowerCase();
  if (typeof Pr[t] < "u" && io[Pr[t]])
    return io[Pr[t]];
}
function dx() {
  cx.forEach(wf);
}
const fx = {
  start: dx,
  add: wf,
  get: ux
};
var j = {};
j.MERIT = {
  a: 6378137,
  rf: 298.257,
  ellipseName: "MERIT 1983"
};
j.SGS85 = {
  a: 6378136,
  rf: 298.257,
  ellipseName: "Soviet Geodetic System 85"
};
j.GRS80 = {
  a: 6378137,
  rf: 298.257222101,
  ellipseName: "GRS 1980(IUGG, 1980)"
};
j.IAU76 = {
  a: 6378140,
  rf: 298.257,
  ellipseName: "IAU 1976"
};
j.airy = {
  a: 6377563396e-3,
  b: 635625691e-2,
  ellipseName: "Airy 1830"
};
j.APL4 = {
  a: 6378137,
  rf: 298.25,
  ellipseName: "Appl. Physics. 1965"
};
j.NWL9D = {
  a: 6378145,
  rf: 298.25,
  ellipseName: "Naval Weapons Lab., 1965"
};
j.mod_airy = {
  a: 6377340189e-3,
  b: 6356034446e-3,
  ellipseName: "Modified Airy"
};
j.andrae = {
  a: 637710443e-2,
  rf: 300,
  ellipseName: "Andrae 1876 (Den., Iclnd.)"
};
j.aust_SA = {
  a: 6378160,
  rf: 298.25,
  ellipseName: "Australian Natl & S. Amer. 1969"
};
j.GRS67 = {
  a: 6378160,
  rf: 298.247167427,
  ellipseName: "GRS 67(IUGG 1967)"
};
j.bessel = {
  a: 6377397155e-3,
  rf: 299.1528128,
  ellipseName: "Bessel 1841"
};
j.bess_nam = {
  a: 6377483865e-3,
  rf: 299.1528128,
  ellipseName: "Bessel 1841 (Namibia)"
};
j.clrk66 = {
  a: 63782064e-1,
  b: 63565838e-1,
  ellipseName: "Clarke 1866"
};
j.clrk80 = {
  a: 6378249145e-3,
  rf: 293.4663,
  ellipseName: "Clarke 1880 mod."
};
j.clrk58 = {
  a: 6378293645208759e-9,
  rf: 294.2606763692654,
  ellipseName: "Clarke 1858"
};
j.CPM = {
  a: 63757387e-1,
  rf: 334.29,
  ellipseName: "Comm. des Poids et Mesures 1799"
};
j.delmbr = {
  a: 6376428,
  rf: 311.5,
  ellipseName: "Delambre 1810 (Belgium)"
};
j.engelis = {
  a: 637813605e-2,
  rf: 298.2566,
  ellipseName: "Engelis 1985"
};
j.evrst30 = {
  a: 6377276345e-3,
  rf: 300.8017,
  ellipseName: "Everest 1830"
};
j.evrst48 = {
  a: 6377304063e-3,
  rf: 300.8017,
  ellipseName: "Everest 1948"
};
j.evrst56 = {
  a: 6377301243e-3,
  rf: 300.8017,
  ellipseName: "Everest 1956"
};
j.evrst69 = {
  a: 6377295664e-3,
  rf: 300.8017,
  ellipseName: "Everest 1969"
};
j.evrstSS = {
  a: 6377298556e-3,
  rf: 300.8017,
  ellipseName: "Everest (Sabah & Sarawak)"
};
j.fschr60 = {
  a: 6378166,
  rf: 298.3,
  ellipseName: "Fischer (Mercury Datum) 1960"
};
j.fschr60m = {
  a: 6378155,
  rf: 298.3,
  ellipseName: "Fischer 1960"
};
j.fschr68 = {
  a: 6378150,
  rf: 298.3,
  ellipseName: "Fischer 1968"
};
j.helmert = {
  a: 6378200,
  rf: 298.3,
  ellipseName: "Helmert 1906"
};
j.hough = {
  a: 6378270,
  rf: 297,
  ellipseName: "Hough"
};
j.intl = {
  a: 6378388,
  rf: 297,
  ellipseName: "International 1909 (Hayford)"
};
j.kaula = {
  a: 6378163,
  rf: 298.24,
  ellipseName: "Kaula 1961"
};
j.lerch = {
  a: 6378139,
  rf: 298.257,
  ellipseName: "Lerch 1979"
};
j.mprts = {
  a: 6397300,
  rf: 191,
  ellipseName: "Maupertius 1738"
};
j.new_intl = {
  a: 63781575e-1,
  b: 63567722e-1,
  ellipseName: "New International 1967"
};
j.plessis = {
  a: 6376523,
  rf: 6355863,
  ellipseName: "Plessis 1817 (France)"
};
j.krass = {
  a: 6378245,
  rf: 298.3,
  ellipseName: "Krassovsky, 1942"
};
j.SEasia = {
  a: 6378155,
  b: 63567733205e-4,
  ellipseName: "Southeast Asia"
};
j.walbeck = {
  a: 6376896,
  b: 63558348467e-4,
  ellipseName: "Walbeck"
};
j.WGS60 = {
  a: 6378165,
  rf: 298.3,
  ellipseName: "WGS 60"
};
j.WGS66 = {
  a: 6378145,
  rf: 298.25,
  ellipseName: "WGS 66"
};
j.WGS7 = {
  a: 6378135,
  rf: 298.26,
  ellipseName: "WGS 72"
};
var gx = j.WGS84 = {
  a: 6378137,
  rf: 298.257223563,
  ellipseName: "WGS 84"
};
j.sphere = {
  a: 6370997,
  b: 6370997,
  ellipseName: "Normal Sphere (r=6370997)"
};
function mx(i, t, e, n) {
  var s = i * i, r = t * t, o = (s - r) / s, a = 0;
  n ? (i *= 1 - o * (Dv + o * (kv + o * Gv)), s = i * i, o = 0) : a = Math.sqrt(o);
  var l = (s - r) / r;
  return {
    es: o,
    e: a,
    ep2: l
  };
}
function px(i, t, e, n, s) {
  if (!i) {
    var r = bi(j, n);
    r || (r = gx), i = r.a, t = r.b, e = r.rf;
  }
  return e && !t && (t = (1 - 1 / e) * i), (e === 0 || Math.abs(i - t) < I) && (s = !0, t = i), {
    a: i,
    b: t,
    rf: e,
    sphere: s
  };
}
var Gt = {};
Gt.wgs84 = {
  towgs84: "0,0,0",
  ellipse: "WGS84",
  datumName: "WGS84"
};
Gt.ch1903 = {
  towgs84: "674.374,15.056,405.346",
  ellipse: "bessel",
  datumName: "swiss"
};
Gt.ggrs87 = {
  towgs84: "-199.87,74.79,246.62",
  ellipse: "GRS80",
  datumName: "Greek_Geodetic_Reference_System_1987"
};
Gt.nad83 = {
  towgs84: "0,0,0",
  ellipse: "GRS80",
  datumName: "North_American_Datum_1983"
};
Gt.nad27 = {
  nadgrids: "@conus,@alaska,@ntv2_0.gsb,@ntv1_can.dat",
  ellipse: "clrk66",
  datumName: "North_American_Datum_1927"
};
Gt.potsdam = {
  towgs84: "598.1,73.7,418.2,0.202,0.045,-2.455,6.7",
  ellipse: "bessel",
  datumName: "Potsdam Rauenberg 1950 DHDN"
};
Gt.carthage = {
  towgs84: "-263.0,6.0,431.0",
  ellipse: "clark80",
  datumName: "Carthage 1934 Tunisia"
};
Gt.hermannskogel = {
  towgs84: "577.326,90.129,463.919,5.137,1.474,5.297,2.4232",
  ellipse: "bessel",
  datumName: "Hermannskogel"
};
Gt.osni52 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "airy",
  datumName: "Irish National"
};
Gt.ire65 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "mod_airy",
  datumName: "Ireland 1965"
};
Gt.rassadiran = {
  towgs84: "-133.63,-157.5,-158.62",
  ellipse: "intl",
  datumName: "Rassadiran"
};
Gt.nzgd49 = {
  towgs84: "59.47,-5.04,187.44,0.47,-0.1,1.024,-4.5993",
  ellipse: "intl",
  datumName: "New Zealand Geodetic Datum 1949"
};
Gt.osgb36 = {
  towgs84: "446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894",
  ellipse: "airy",
  datumName: "Airy 1830"
};
Gt.s_jtsk = {
  towgs84: "589,76,480",
  ellipse: "bessel",
  datumName: "S-JTSK (Ferro)"
};
Gt.beduaram = {
  towgs84: "-106,-87,188",
  ellipse: "clrk80",
  datumName: "Beduaram"
};
Gt.gunung_segara = {
  towgs84: "-403,684,41",
  ellipse: "bessel",
  datumName: "Gunung Segara Jakarta"
};
Gt.rnb72 = {
  towgs84: "106.869,-52.2978,103.724,-0.33657,0.456955,-1.84218,1",
  ellipse: "intl",
  datumName: "Reseau National Belge 1972"
};
function _x(i, t, e, n, s, r, o) {
  var a = {};
  return i === void 0 || i === "none" ? a.datum_type = za : a.datum_type = Nv, t && (a.datum_params = t.map(parseFloat), (a.datum_params[0] !== 0 || a.datum_params[1] !== 0 || a.datum_params[2] !== 0) && (a.datum_type = Qi), a.datum_params.length > 3 && (a.datum_params[3] !== 0 || a.datum_params[4] !== 0 || a.datum_params[5] !== 0 || a.datum_params[6] !== 0) && (a.datum_type = tn, a.datum_params[3] *= ys, a.datum_params[4] *= ys, a.datum_params[5] *= ys, a.datum_params[6] = a.datum_params[6] / 1e6 + 1)), o && (a.datum_type = Ir, a.grids = o), a.a = e, a.b = n, a.es = s, a.ep2 = r, a;
}
var Sf = {};
function yx(i, t) {
  var e = new DataView(t), n = Cx(e), s = Mx(e, n);
  s.nSubgrids > 1 && console.log("Only single NTv2 subgrids are currently supported, subsequent sub grids are ignored");
  var r = Ex(e, s, n), o = { header: s, subgrids: r };
  return Sf[i] = o, o;
}
function vx(i) {
  if (i === void 0)
    return null;
  var t = i.split(",");
  return t.map(xx);
}
function xx(i) {
  if (i.length === 0)
    return null;
  var t = i[0] === "@";
  return t && (i = i.slice(1)), i === "null" ? { name: "null", mandatory: !t, grid: null, isNull: !0 } : {
    name: i,
    mandatory: !t,
    grid: Sf[i] || null,
    isNull: !1
  };
}
function Ln(i) {
  return i / 3600 * Math.PI / 180;
}
function Cx(i) {
  var t = i.getInt32(8, !1);
  return t === 11 ? !1 : (t = i.getInt32(8, !0), t !== 11 && console.warn("Failed to detect nadgrid endian-ness, defaulting to little-endian"), !0);
}
function Mx(i, t) {
  return {
    nFields: i.getInt32(8, t),
    nSubgridFields: i.getInt32(24, t),
    nSubgrids: i.getInt32(40, t),
    shiftType: Va(i, 56, 56 + 8).trim(),
    fromSemiMajorAxis: i.getFloat64(120, t),
    fromSemiMinorAxis: i.getFloat64(136, t),
    toSemiMajorAxis: i.getFloat64(152, t),
    toSemiMinorAxis: i.getFloat64(168, t)
  };
}
function Va(i, t, e) {
  return String.fromCharCode.apply(null, new Uint8Array(i.buffer.slice(t, e)));
}
function Ex(i, t, e) {
  for (var n = 176, s = [], r = 0; r < t.nSubgrids; r++) {
    var o = Sx(i, n, e), a = Rx(i, n, o, e), l = Math.round(
      1 + (o.upperLongitude - o.lowerLongitude) / o.longitudeInterval
    ), h = Math.round(
      1 + (o.upperLatitude - o.lowerLatitude) / o.latitudeInterval
    );
    s.push({
      ll: [Ln(o.lowerLongitude), Ln(o.lowerLatitude)],
      del: [Ln(o.longitudeInterval), Ln(o.latitudeInterval)],
      lim: [l, h],
      count: o.gridNodeCount,
      cvs: wx(a)
    });
  }
  return s;
}
function wx(i) {
  return i.map(function(t) {
    return [Ln(t.longitudeShift), Ln(t.latitudeShift)];
  });
}
function Sx(i, t, e) {
  return {
    name: Va(i, t + 8, t + 16).trim(),
    parent: Va(i, t + 24, t + 24 + 8).trim(),
    lowerLatitude: i.getFloat64(t + 72, e),
    upperLatitude: i.getFloat64(t + 88, e),
    lowerLongitude: i.getFloat64(t + 104, e),
    upperLongitude: i.getFloat64(t + 120, e),
    latitudeInterval: i.getFloat64(t + 136, e),
    longitudeInterval: i.getFloat64(t + 152, e),
    gridNodeCount: i.getInt32(t + 168, e)
  };
}
function Rx(i, t, e, n) {
  for (var s = t + 176, r = 16, o = [], a = 0; a < e.gridNodeCount; a++) {
    var l = {
      latitudeShift: i.getFloat32(s + a * r, n),
      longitudeShift: i.getFloat32(s + a * r + 4, n),
      latitudeAccuracy: i.getFloat32(s + a * r + 8, n),
      longitudeAccuracy: i.getFloat32(s + a * r + 12, n)
    };
    o.push(l);
  }
  return o;
}
function De(i, t) {
  if (!(this instanceof De))
    return new De(i);
  t = t || function(h) {
    if (h)
      throw h;
  };
  var e = ex(i);
  if (typeof e != "object") {
    t(i);
    return;
  }
  var n = De.projections.get(e.projName);
  if (!n) {
    t(i);
    return;
  }
  if (e.datumCode && e.datumCode !== "none") {
    var s = bi(Gt, e.datumCode);
    s && (e.datum_params = e.datum_params || (s.towgs84 ? s.towgs84.split(",") : null), e.ellps = s.ellipse, e.datumName = s.datumName ? s.datumName : e.datumCode);
  }
  e.k0 = e.k0 || 1, e.axis = e.axis || "enu", e.ellps = e.ellps || "wgs84", e.lat1 = e.lat1 || e.lat0;
  var r = px(e.a, e.b, e.rf, e.ellps, e.sphere), o = mx(r.a, r.b, r.rf, e.R_A), a = vx(e.nadgrids), l = e.datum || _x(
    e.datumCode,
    e.datum_params,
    r.a,
    r.b,
    o.es,
    o.ep2,
    a
  );
  zc(this, e), zc(this, n), this.a = r.a, this.b = r.b, this.rf = r.rf, this.sphere = r.sphere, this.es = o.es, this.e = o.e, this.ep2 = o.ep2, this.datum = l, this.init(), t(null, this);
}
De.projections = fx;
De.projections.start();
function bx(i, t) {
  return i.datum_type !== t.datum_type || i.a !== t.a || Math.abs(i.es - t.es) > 5e-11 ? !1 : i.datum_type === Qi ? i.datum_params[0] === t.datum_params[0] && i.datum_params[1] === t.datum_params[1] && i.datum_params[2] === t.datum_params[2] : i.datum_type === tn ? i.datum_params[0] === t.datum_params[0] && i.datum_params[1] === t.datum_params[1] && i.datum_params[2] === t.datum_params[2] && i.datum_params[3] === t.datum_params[3] && i.datum_params[4] === t.datum_params[4] && i.datum_params[5] === t.datum_params[5] && i.datum_params[6] === t.datum_params[6] : !0;
}
function Rf(i, t, e) {
  var n = i.x, s = i.y, r = i.z ? i.z : 0, o, a, l, h;
  if (s < -R && s > -1.001 * R)
    s = -R;
  else if (s > R && s < 1.001 * R)
    s = R;
  else {
    if (s < -R)
      return { x: -1 / 0, y: -1 / 0, z: i.z };
    if (s > R)
      return { x: 1 / 0, y: 1 / 0, z: i.z };
  }
  return n > Math.PI && (n -= 2 * Math.PI), a = Math.sin(s), h = Math.cos(s), l = a * a, o = e / Math.sqrt(1 - t * l), {
    x: (o + r) * h * Math.cos(n),
    y: (o + r) * h * Math.sin(n),
    z: (o * (1 - t) + r) * a
  };
}
function bf(i, t, e, n) {
  var s = 1e-12, r = s * s, o = 30, a, l, h, c, u, d, f, g, m, p, _, y, v, x = i.x, C = i.y, w = i.z ? i.z : 0, S, b, A;
  if (a = Math.sqrt(x * x + C * C), l = Math.sqrt(x * x + C * C + w * w), a / e < s) {
    if (S = 0, l / e < s)
      return b = R, A = -n, {
        x: i.x,
        y: i.y,
        z: i.z
      };
  } else
    S = Math.atan2(C, x);
  h = w / l, c = a / l, u = 1 / Math.sqrt(1 - t * (2 - t) * c * c), g = c * (1 - t) * u, m = h * u, v = 0;
  do
    v++, f = e / Math.sqrt(1 - t * m * m), A = a * g + w * m - f * (1 - t * m * m), d = t * f / (f + A), u = 1 / Math.sqrt(1 - d * (2 - d) * c * c), p = c * (1 - d) * u, _ = h * u, y = _ * g - p * m, g = p, m = _;
  while (y * y > r && v < o);
  return b = Math.atan(_ / Math.abs(p)), {
    x: S,
    y: b,
    z: A
  };
}
function Lx(i, t, e) {
  if (t === Qi)
    return {
      x: i.x + e[0],
      y: i.y + e[1],
      z: i.z + e[2]
    };
  if (t === tn) {
    var n = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6];
    return {
      x: h * (i.x - l * i.y + a * i.z) + n,
      y: h * (l * i.x + i.y - o * i.z) + s,
      z: h * (-a * i.x + o * i.y + i.z) + r
    };
  }
}
function Tx(i, t, e) {
  if (t === Qi)
    return {
      x: i.x - e[0],
      y: i.y - e[1],
      z: i.z - e[2]
    };
  if (t === tn) {
    var n = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6], c = (i.x - n) / h, u = (i.y - s) / h, d = (i.z - r) / h;
    return {
      x: c + l * u - a * d,
      y: -l * c + u + o * d,
      z: a * c - o * u + d
    };
  }
}
function br(i) {
  return i === Qi || i === tn;
}
function Ix(i, t, e) {
  if (bx(i, t) || i.datum_type === za || t.datum_type === za)
    return e;
  var n = i.a, s = i.es;
  if (i.datum_type === Ir) {
    var r = Vc(i, !1, e);
    if (r !== 0)
      return;
    n = kc, s = Gc;
  }
  var o = t.a, a = t.b, l = t.es;
  if (t.datum_type === Ir && (o = kc, a = Fv, l = Gc), s === l && n === o && !br(i.datum_type) && !br(t.datum_type))
    return e;
  if (e = Rf(e, s, n), br(i.datum_type) && (e = Lx(e, i.datum_type, i.datum_params)), br(t.datum_type) && (e = Tx(e, t.datum_type, t.datum_params)), e = bf(e, l, o, a), t.datum_type === Ir) {
    var h = Vc(t, !0, e);
    if (h !== 0)
      return;
  }
  return e;
}
function Vc(i, t, e) {
  if (i.grids === null || i.grids.length === 0)
    return console.log("Grid shift grids not found"), -1;
  for (var n = { x: -e.x, y: e.y }, s = { x: Number.NaN, y: Number.NaN }, r = [], o = 0; o < i.grids.length; o++) {
    var a = i.grids[o];
    if (r.push(a.name), a.isNull) {
      s = n;
      break;
    }
    if (a.mandatory, a.grid === null) {
      if (a.mandatory)
        return console.log("Unable to find mandatory grid '" + a.name + "'"), -1;
      continue;
    }
    var l = a.grid.subgrids[0], h = (Math.abs(l.del[1]) + Math.abs(l.del[0])) / 1e4, c = l.ll[0] - h, u = l.ll[1] - h, d = l.ll[0] + (l.lim[0] - 1) * l.del[0] + h, f = l.ll[1] + (l.lim[1] - 1) * l.del[1] + h;
    if (!(u > n.y || c > n.x || f < n.y || d < n.x) && (s = Px(n, t, l), !isNaN(s.x)))
      break;
  }
  return isNaN(s.x) ? (console.log("Failed to find a grid shift table for location '" + -n.x * Ne + " " + n.y * Ne + " tried: '" + r + "'"), -1) : (e.x = -s.x, e.y = s.y, 0);
}
function Px(i, t, e) {
  var n = { x: Number.NaN, y: Number.NaN };
  if (isNaN(i.x))
    return n;
  var s = { x: i.x, y: i.y };
  s.x -= e.ll[0], s.y -= e.ll[1], s.x = O(s.x - Math.PI) + Math.PI;
  var r = Uc(s, e);
  if (t) {
    if (isNaN(r.x))
      return n;
    r.x = s.x - r.x, r.y = s.y - r.y;
    var o = 9, a = 1e-12, l, h;
    do {
      if (h = Uc(r, e), isNaN(h.x)) {
        console.log("Inverse grid shift iteration failed, presumably at grid edge.  Using first approximation.");
        break;
      }
      l = { x: s.x - (h.x + r.x), y: s.y - (h.y + r.y) }, r.x += l.x, r.y += l.y;
    } while (o-- && Math.abs(l.x) > a && Math.abs(l.y) > a);
    if (o < 0)
      return console.log("Inverse grid shift iterator failed to converge."), n;
    n.x = O(r.x + e.ll[0]), n.y = r.y + e.ll[1];
  } else
    isNaN(r.x) || (n.x = i.x + r.x, n.y = i.y + r.y);
  return n;
}
function Uc(i, t) {
  var e = { x: i.x / t.del[0], y: i.y / t.del[1] }, n = { x: Math.floor(e.x), y: Math.floor(e.y) }, s = { x: e.x - 1 * n.x, y: e.y - 1 * n.y }, r = { x: Number.NaN, y: Number.NaN }, o;
  if (n.x < 0 || n.x >= t.lim[0] || n.y < 0 || n.y >= t.lim[1])
    return r;
  o = n.y * t.lim[0] + n.x;
  var a = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o++;
  var l = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o += t.lim[0];
  var h = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o--;
  var c = { x: t.cvs[o][0], y: t.cvs[o][1] }, u = s.x * s.y, d = s.x * (1 - s.y), f = (1 - s.x) * (1 - s.y), g = (1 - s.x) * s.y;
  return r.x = f * a.x + d * l.x + g * c.x + u * h.x, r.y = f * a.y + d * l.y + g * c.y + u * h.y, r;
}
function Wc(i, t, e) {
  var n = e.x, s = e.y, r = e.z || 0, o, a, l, h = {};
  for (l = 0; l < 3; l++)
    if (!(t && l === 2 && e.z === void 0))
      switch (l === 0 ? (o = n, "ew".indexOf(i.axis[l]) !== -1 ? a = "x" : a = "y") : l === 1 ? (o = s, "ns".indexOf(i.axis[l]) !== -1 ? a = "y" : a = "x") : (o = r, a = "z"), i.axis[l]) {
        case "e":
          h[a] = o;
          break;
        case "w":
          h[a] = -o;
          break;
        case "n":
          h[a] = o;
          break;
        case "s":
          h[a] = -o;
          break;
        case "u":
          e[a] !== void 0 && (h.z = o);
          break;
        case "d":
          e[a] !== void 0 && (h.z = -o);
          break;
        default:
          return null;
      }
  return h;
}
function Lf(i) {
  var t = {
    x: i[0],
    y: i[1]
  };
  return i.length > 2 && (t.z = i[2]), i.length > 3 && (t.m = i[3]), t;
}
function Ax(i) {
  Hc(i.x), Hc(i.y);
}
function Hc(i) {
  if (typeof Number.isFinite == "function") {
    if (Number.isFinite(i))
      return;
    throw new TypeError("coordinates must be finite numbers");
  }
  if (typeof i != "number" || i !== i || !isFinite(i))
    throw new TypeError("coordinates must be finite numbers");
}
function Ox(i, t) {
  return (i.datum.datum_type === Qi || i.datum.datum_type === tn) && t.datumCode !== "WGS84" || (t.datum.datum_type === Qi || t.datum.datum_type === tn) && i.datumCode !== "WGS84";
}
function no(i, t, e, n) {
  var s;
  if (Array.isArray(e) && (e = Lf(e)), Ax(e), i.datum && t.datum && Ox(i, t) && (s = new De("WGS84"), e = no(i, s, e, n), i = s), n && i.axis !== "enu" && (e = Wc(i, !1, e)), i.projName === "longlat")
    e = {
      x: e.x * Bt,
      y: e.y * Bt,
      z: e.z || 0
    };
  else if (i.to_meter && (e = {
    x: e.x * i.to_meter,
    y: e.y * i.to_meter,
    z: e.z || 0
  }), e = i.inverse(e), !e)
    return;
  if (i.from_greenwich && (e.x += i.from_greenwich), e = Ix(i.datum, t.datum, e), !!e)
    return t.from_greenwich && (e = {
      x: e.x - t.from_greenwich,
      y: e.y,
      z: e.z || 0
    }), t.projName === "longlat" ? e = {
      x: e.x * Ne,
      y: e.y * Ne,
      z: e.z || 0
    } : (e = t.forward(e), t.to_meter && (e = {
      x: e.x / t.to_meter,
      y: e.y / t.to_meter,
      z: e.z || 0
    })), n && t.axis !== "enu" ? Wc(t, !0, e) : e;
}
var Xc = De("WGS84");
function sa(i, t, e, n) {
  var s, r, o;
  return Array.isArray(e) ? (s = no(i, t, e, n) || { x: NaN, y: NaN }, e.length > 2 ? typeof i.name < "u" && i.name === "geocent" || typeof t.name < "u" && t.name === "geocent" ? typeof s.z == "number" ? [s.x, s.y, s.z].concat(e.splice(3)) : [s.x, s.y, e[2]].concat(e.splice(3)) : [s.x, s.y].concat(e.splice(2)) : [s.x, s.y]) : (r = no(i, t, e, n), o = Object.keys(e), o.length === 2 || o.forEach(function(a) {
    if (typeof i.name < "u" && i.name === "geocent" || typeof t.name < "u" && t.name === "geocent") {
      if (a === "x" || a === "y" || a === "z")
        return;
    } else if (a === "x" || a === "y")
      return;
    r[a] = e[a];
  }), r);
}
function Yc(i) {
  return i instanceof De ? i : i.oProj ? i.oProj : De(i);
}
function se(i, t, e) {
  i = Yc(i);
  var n = !1, s;
  return typeof t > "u" ? (t = i, i = Xc, n = !0) : (typeof t.x < "u" || Array.isArray(t)) && (e = t, t = i, i = Xc, n = !0), t = Yc(t), e ? sa(i, t, e) : (s = {
    forward: function(r, o) {
      return sa(i, t, r, o);
    },
    inverse: function(r, o) {
      return sa(t, i, r, o);
    }
  }, n && (s.oProj = t), s);
}
var jc = 6, Tf = "AJSAJS", If = "AFAFAF", Tn = 65, te = 73, ve = 79, us = 86, ds = 90;
const Nx = {
  forward: Pf,
  inverse: Fx,
  toPoint: Af
};
function Pf(i, t) {
  return t = t || 5, Gx(Dx({
    lat: i[1],
    lon: i[0]
  }), t);
}
function Fx(i) {
  var t = Wl(Nf(i.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat, t.lon, t.lat] : [t.left, t.bottom, t.right, t.top];
}
function Af(i) {
  var t = Wl(Nf(i.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat] : [(t.left + t.right) / 2, (t.top + t.bottom) / 2];
}
function ra(i) {
  return i * (Math.PI / 180);
}
function Kc(i) {
  return 180 * (i / Math.PI);
}
function Dx(i) {
  var t = i.lat, e = i.lon, n = 6378137, s = 669438e-8, r = 0.9996, o, a, l, h, c, u, d, f = ra(t), g = ra(e), m, p;
  p = Math.floor((e + 180) / 6) + 1, e === 180 && (p = 60), t >= 56 && t < 64 && e >= 3 && e < 12 && (p = 32), t >= 72 && t < 84 && (e >= 0 && e < 9 ? p = 31 : e >= 9 && e < 21 ? p = 33 : e >= 21 && e < 33 ? p = 35 : e >= 33 && e < 42 && (p = 37)), o = (p - 1) * 6 - 180 + 3, m = ra(o), a = s / (1 - s), l = n / Math.sqrt(1 - s * Math.sin(f) * Math.sin(f)), h = Math.tan(f) * Math.tan(f), c = a * Math.cos(f) * Math.cos(f), u = Math.cos(f) * (g - m), d = n * ((1 - s / 4 - 3 * s * s / 64 - 5 * s * s * s / 256) * f - (3 * s / 8 + 3 * s * s / 32 + 45 * s * s * s / 1024) * Math.sin(2 * f) + (15 * s * s / 256 + 45 * s * s * s / 1024) * Math.sin(4 * f) - 35 * s * s * s / 3072 * Math.sin(6 * f));
  var _ = r * l * (u + (1 - h + c) * u * u * u / 6 + (5 - 18 * h + h * h + 72 * c - 58 * a) * u * u * u * u * u / 120) + 5e5, y = r * (d + l * Math.tan(f) * (u * u / 2 + (5 - h + 9 * c + 4 * c * c) * u * u * u * u / 24 + (61 - 58 * h + h * h + 600 * c - 330 * a) * u * u * u * u * u * u / 720));
  return t < 0 && (y += 1e7), {
    northing: Math.round(y),
    easting: Math.round(_),
    zoneNumber: p,
    zoneLetter: kx(t)
  };
}
function Wl(i) {
  var t = i.northing, e = i.easting, n = i.zoneLetter, s = i.zoneNumber;
  if (s < 0 || s > 60)
    return null;
  var r = 0.9996, o = 6378137, a = 669438e-8, l, h = (1 - Math.sqrt(1 - a)) / (1 + Math.sqrt(1 - a)), c, u, d, f, g, m, p, _, y, v = e - 5e5, x = t;
  n < "N" && (x -= 1e7), p = (s - 1) * 6 - 180 + 3, l = a / (1 - a), m = x / r, _ = m / (o * (1 - a / 4 - 3 * a * a / 64 - 5 * a * a * a / 256)), y = _ + (3 * h / 2 - 27 * h * h * h / 32) * Math.sin(2 * _) + (21 * h * h / 16 - 55 * h * h * h * h / 32) * Math.sin(4 * _) + 151 * h * h * h / 96 * Math.sin(6 * _), c = o / Math.sqrt(1 - a * Math.sin(y) * Math.sin(y)), u = Math.tan(y) * Math.tan(y), d = l * Math.cos(y) * Math.cos(y), f = o * (1 - a) / Math.pow(1 - a * Math.sin(y) * Math.sin(y), 1.5), g = v / (c * r);
  var C = y - c * Math.tan(y) / f * (g * g / 2 - (5 + 3 * u + 10 * d - 4 * d * d - 9 * l) * g * g * g * g / 24 + (61 + 90 * u + 298 * d + 45 * u * u - 252 * l - 3 * d * d) * g * g * g * g * g * g / 720);
  C = Kc(C);
  var w = (g - (1 + 2 * u + d) * g * g * g / 6 + (5 - 2 * d + 28 * u - 3 * d * d + 8 * l + 24 * u * u) * g * g * g * g * g / 120) / Math.cos(y);
  w = p + Kc(w);
  var S;
  if (i.accuracy) {
    var b = Wl({
      northing: i.northing + i.accuracy,
      easting: i.easting + i.accuracy,
      zoneLetter: i.zoneLetter,
      zoneNumber: i.zoneNumber
    });
    S = {
      top: b.lat,
      right: b.lon,
      bottom: C,
      left: w
    };
  } else
    S = {
      lat: C,
      lon: w
    };
  return S;
}
function kx(i) {
  var t = "Z";
  return 84 >= i && i >= 72 ? t = "X" : 72 > i && i >= 64 ? t = "W" : 64 > i && i >= 56 ? t = "V" : 56 > i && i >= 48 ? t = "U" : 48 > i && i >= 40 ? t = "T" : 40 > i && i >= 32 ? t = "S" : 32 > i && i >= 24 ? t = "R" : 24 > i && i >= 16 ? t = "Q" : 16 > i && i >= 8 ? t = "P" : 8 > i && i >= 0 ? t = "N" : 0 > i && i >= -8 ? t = "M" : -8 > i && i >= -16 ? t = "L" : -16 > i && i >= -24 ? t = "K" : -24 > i && i >= -32 ? t = "J" : -32 > i && i >= -40 ? t = "H" : -40 > i && i >= -48 ? t = "G" : -48 > i && i >= -56 ? t = "F" : -56 > i && i >= -64 ? t = "E" : -64 > i && i >= -72 ? t = "D" : -72 > i && i >= -80 && (t = "C"), t;
}
function Gx(i, t) {
  var e = "00000" + i.easting, n = "00000" + i.northing;
  return i.zoneNumber + i.zoneLetter + $x(i.easting, i.northing, i.zoneNumber) + e.substr(e.length - 5, t) + n.substr(n.length - 5, t);
}
function $x(i, t, e) {
  var n = Of(e), s = Math.floor(i / 1e5), r = Math.floor(t / 1e5) % 20;
  return Bx(s, r, n);
}
function Of(i) {
  var t = i % jc;
  return t === 0 && (t = jc), t;
}
function Bx(i, t, e) {
  var n = e - 1, s = Tf.charCodeAt(n), r = If.charCodeAt(n), o = s + i - 1, a = r + t, l = !1;
  o > ds && (o = o - ds + Tn - 1, l = !0), (o === te || s < te && o > te || (o > te || s < te) && l) && o++, (o === ve || s < ve && o > ve || (o > ve || s < ve) && l) && (o++, o === te && o++), o > ds && (o = o - ds + Tn - 1), a > us ? (a = a - us + Tn - 1, l = !0) : l = !1, (a === te || r < te && a > te || (a > te || r < te) && l) && a++, (a === ve || r < ve && a > ve || (a > ve || r < ve) && l) && (a++, a === te && a++), a > us && (a = a - us + Tn - 1);
  var h = String.fromCharCode(o) + String.fromCharCode(a);
  return h;
}
function Nf(i) {
  if (i && i.length === 0)
    throw "MGRSPoint coverting from nothing";
  for (var t = i.length, e = null, n = "", s, r = 0; !/[A-Z]/.test(s = i.charAt(r)); ) {
    if (r >= 2)
      throw "MGRSPoint bad conversion from: " + i;
    n += s, r++;
  }
  var o = parseInt(n, 10);
  if (r === 0 || r + 3 > t)
    throw "MGRSPoint bad conversion from: " + i;
  var a = i.charAt(r++);
  if (a <= "A" || a === "B" || a === "Y" || a >= "Z" || a === "I" || a === "O")
    throw "MGRSPoint zone letter " + a + " not handled: " + i;
  e = i.substring(r, r += 2);
  for (var l = Of(o), h = zx(e.charAt(0), l), c = Zx(e.charAt(1), l); c < Vx(a); )
    c += 2e6;
  var u = t - r;
  if (u % 2 !== 0)
    throw `MGRSPoint has to have an even number 
of digits after the zone letter and two 100km letters - front 
half for easting meters, second half for 
northing meters` + i;
  var d = u / 2, f = 0, g = 0, m, p, _, y, v;
  return d > 0 && (m = 1e5 / Math.pow(10, d), p = i.substring(r, r + d), f = parseFloat(p) * m, _ = i.substring(r + d), g = parseFloat(_) * m), y = f + h, v = g + c, {
    easting: y,
    northing: v,
    zoneLetter: a,
    zoneNumber: o,
    accuracy: m
  };
}
function zx(i, t) {
  for (var e = Tf.charCodeAt(t - 1), n = 1e5, s = !1; e !== i.charCodeAt(0); ) {
    if (e++, e === te && e++, e === ve && e++, e > ds) {
      if (s)
        throw "Bad character: " + i;
      e = Tn, s = !0;
    }
    n += 1e5;
  }
  return n;
}
function Zx(i, t) {
  if (i > "V")
    throw "MGRSPoint given invalid Northing " + i;
  for (var e = If.charCodeAt(t - 1), n = 0, s = !1; e !== i.charCodeAt(0); ) {
    if (e++, e === te && e++, e === ve && e++, e > us) {
      if (s)
        throw "Bad character: " + i;
      e = Tn, s = !0;
    }
    n += 1e5;
  }
  return n;
}
function Vx(i) {
  var t;
  switch (i) {
    case "C":
      t = 11e5;
      break;
    case "D":
      t = 2e6;
      break;
    case "E":
      t = 28e5;
      break;
    case "F":
      t = 37e5;
      break;
    case "G":
      t = 46e5;
      break;
    case "H":
      t = 55e5;
      break;
    case "J":
      t = 64e5;
      break;
    case "K":
      t = 73e5;
      break;
    case "L":
      t = 82e5;
      break;
    case "M":
      t = 91e5;
      break;
    case "N":
      t = 0;
      break;
    case "P":
      t = 8e5;
      break;
    case "Q":
      t = 17e5;
      break;
    case "R":
      t = 26e5;
      break;
    case "S":
      t = 35e5;
      break;
    case "T":
      t = 44e5;
      break;
    case "U":
      t = 53e5;
      break;
    case "V":
      t = 62e5;
      break;
    case "W":
      t = 7e6;
      break;
    case "X":
      t = 79e5;
      break;
    default:
      t = -1;
  }
  if (t >= 0)
    return t;
  throw "Invalid zone letter: " + i;
}
function Wn(i, t, e) {
  if (!(this instanceof Wn))
    return new Wn(i, t, e);
  if (Array.isArray(i))
    this.x = i[0], this.y = i[1], this.z = i[2] || 0;
  else if (typeof i == "object")
    this.x = i.x, this.y = i.y, this.z = i.z || 0;
  else if (typeof i == "string" && typeof t > "u") {
    var n = i.split(",");
    this.x = parseFloat(n[0], 10), this.y = parseFloat(n[1], 10), this.z = parseFloat(n[2], 10) || 0;
  } else
    this.x = i, this.y = t, this.z = e || 0;
  console.warn("proj4.Point will be removed in version 3, use proj4.toPoint");
}
Wn.fromMGRS = function(i) {
  return new Wn(Af(i));
};
Wn.prototype.toMGRS = function(i) {
  return Pf([this.x, this.y], i);
};
var Ux = 1, Wx = 0.25, qc = 0.046875, Jc = 0.01953125, Qc = 0.01068115234375, Hx = 0.75, Xx = 0.46875, Yx = 0.013020833333333334, jx = 0.007120768229166667, Kx = 0.3645833333333333, qx = 0.005696614583333333, Jx = 0.3076171875;
function Ff(i) {
  var t = [];
  t[0] = Ux - i * (Wx + i * (qc + i * (Jc + i * Qc))), t[1] = i * (Hx - i * (qc + i * (Jc + i * Qc)));
  var e = i * i;
  return t[2] = e * (Xx - i * (Yx + i * jx)), e *= i, t[3] = e * (Kx - i * qx), t[4] = e * i * Jx, t;
}
function Po(i, t, e, n) {
  return e *= t, t *= t, n[0] * i - e * (n[1] + t * (n[2] + t * (n[3] + t * n[4])));
}
var Qx = 20;
function Df(i, t, e) {
  for (var n = 1 / (1 - t), s = i, r = Qx; r; --r) {
    var o = Math.sin(s), a = 1 - t * o * o;
    if (a = (Po(s, o, Math.cos(s), e) - i) * (a * Math.sqrt(a)) * n, s -= a, Math.abs(a) < I)
      return s;
  }
  return s;
}
function t3() {
  this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.es && (this.en = Ff(this.es), this.ml0 = Po(this.lat0, Math.sin(this.lat0), Math.cos(this.lat0), this.en));
}
function e3(i) {
  var t = i.x, e = i.y, n = O(t - this.long0), s, r, o, a = Math.sin(e), l = Math.cos(e);
  if (this.es) {
    var c = l * n, u = Math.pow(c, 2), d = this.ep2 * Math.pow(l, 2), f = Math.pow(d, 2), g = Math.abs(l) > I ? Math.tan(e) : 0, m = Math.pow(g, 2), p = Math.pow(m, 2);
    s = 1 - this.es * Math.pow(a, 2), c = c / Math.sqrt(s);
    var _ = Po(e, a, l, this.en);
    r = this.a * (this.k0 * c * (1 + u / 6 * (1 - m + d + u / 20 * (5 - 18 * m + p + 14 * d - 58 * m * d + u / 42 * (61 + 179 * p - p * m - 479 * m))))) + this.x0, o = this.a * (this.k0 * (_ - this.ml0 + a * n * c / 2 * (1 + u / 12 * (5 - m + 9 * d + 4 * f + u / 30 * (61 + p - 58 * m + 270 * d - 330 * m * d + u / 56 * (1385 + 543 * p - p * m - 3111 * m)))))) + this.y0;
  } else {
    var h = l * Math.sin(n);
    if (Math.abs(Math.abs(h) - 1) < I)
      return 93;
    if (r = 0.5 * this.a * this.k0 * Math.log((1 + h) / (1 - h)) + this.x0, o = l * Math.cos(n) / Math.sqrt(1 - Math.pow(h, 2)), h = Math.abs(o), h >= 1) {
      if (h - 1 > I)
        return 93;
      o = 0;
    } else
      o = Math.acos(o);
    e < 0 && (o = -o), o = this.a * this.k0 * (o - this.lat0) + this.y0;
  }
  return i.x = r, i.y = o, i;
}
function i3(i) {
  var t, e, n, s, r = (i.x - this.x0) * (1 / this.a), o = (i.y - this.y0) * (1 / this.a);
  if (this.es)
    if (t = this.ml0 + o / this.k0, e = Df(t, this.es, this.en), Math.abs(e) < R) {
      var u = Math.sin(e), d = Math.cos(e), f = Math.abs(d) > I ? Math.tan(e) : 0, g = this.ep2 * Math.pow(d, 2), m = Math.pow(g, 2), p = Math.pow(f, 2), _ = Math.pow(p, 2);
      t = 1 - this.es * Math.pow(u, 2);
      var y = r * Math.sqrt(t) / this.k0, v = Math.pow(y, 2);
      t = t * f, n = e - t * v / (1 - this.es) * 0.5 * (1 - v / 12 * (5 + 3 * p - 9 * g * p + g - 4 * m - v / 30 * (61 + 90 * p - 252 * g * p + 45 * _ + 46 * g - v / 56 * (1385 + 3633 * p + 4095 * _ + 1574 * _ * p)))), s = O(this.long0 + y * (1 - v / 6 * (1 + 2 * p + g - v / 20 * (5 + 28 * p + 24 * _ + 8 * g * p + 6 * g - v / 42 * (61 + 662 * p + 1320 * _ + 720 * _ * p)))) / d);
    } else
      n = R * Qs(o), s = 0;
  else {
    var a = Math.exp(r / this.k0), l = 0.5 * (a - 1 / a), h = this.lat0 + o / this.k0, c = Math.cos(h);
    t = Math.sqrt((1 - Math.pow(c, 2)) / (1 + Math.pow(l, 2))), n = Math.asin(t), o < 0 && (n = -n), l === 0 && c === 0 ? s = 0 : s = O(Math.atan2(l, c) + this.long0);
  }
  return i.x = s, i.y = n, i;
}
var n3 = ["Fast_Transverse_Mercator", "Fast Transverse Mercator"];
const Ar = {
  init: t3,
  forward: e3,
  inverse: i3,
  names: n3
};
function kf(i) {
  var t = Math.exp(i);
  return t = (t - 1 / t) / 2, t;
}
function Se(i, t) {
  i = Math.abs(i), t = Math.abs(t);
  var e = Math.max(i, t), n = Math.min(i, t) / (e || 1);
  return e * Math.sqrt(1 + Math.pow(n, 2));
}
function s3(i) {
  var t = 1 + i, e = t - 1;
  return e === 0 ? i : i * Math.log(t) / e;
}
function r3(i) {
  var t = Math.abs(i);
  return t = s3(t * (1 + t / (Se(1, t) + 1))), i < 0 ? -t : t;
}
function Hl(i, t) {
  for (var e = 2 * Math.cos(2 * t), n = i.length - 1, s = i[n], r = 0, o; --n >= 0; )
    o = -r + e * s + i[n], r = s, s = o;
  return t + o * Math.sin(2 * t);
}
function o3(i, t) {
  for (var e = 2 * Math.cos(t), n = i.length - 1, s = i[n], r = 0, o; --n >= 0; )
    o = -r + e * s + i[n], r = s, s = o;
  return Math.sin(t) * o;
}
function a3(i) {
  var t = Math.exp(i);
  return t = (t + 1 / t) / 2, t;
}
function Gf(i, t, e) {
  for (var n = Math.sin(t), s = Math.cos(t), r = kf(e), o = a3(e), a = 2 * s * o, l = -2 * n * r, h = i.length - 1, c = i[h], u = 0, d = 0, f = 0, g, m; --h >= 0; )
    g = d, m = u, d = c, u = f, c = -g + a * d - l * u + i[h], f = -m + l * d + a * u;
  return a = n * o, l = s * r, [a * c - l * f, a * f + l * c];
}
function l3() {
  if (!this.approx && (isNaN(this.es) || this.es <= 0))
    throw new Error('Incorrect elliptical usage. Try using the +approx option in the proj string, or PROJECTION["Fast_Transverse_Mercator"] in the WKT.');
  this.approx && (Ar.init.apply(this), this.forward = Ar.forward, this.inverse = Ar.inverse), this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.cgb = [], this.cbg = [], this.utg = [], this.gtu = [];
  var i = this.es / (1 + Math.sqrt(1 - this.es)), t = i / (2 - i), e = t;
  this.cgb[0] = t * (2 + t * (-2 / 3 + t * (-2 + t * (116 / 45 + t * (26 / 45 + t * (-2854 / 675)))))), this.cbg[0] = t * (-2 + t * (2 / 3 + t * (4 / 3 + t * (-82 / 45 + t * (32 / 45 + t * (4642 / 4725)))))), e = e * t, this.cgb[1] = e * (7 / 3 + t * (-8 / 5 + t * (-227 / 45 + t * (2704 / 315 + t * (2323 / 945))))), this.cbg[1] = e * (5 / 3 + t * (-16 / 15 + t * (-13 / 9 + t * (904 / 315 + t * (-1522 / 945))))), e = e * t, this.cgb[2] = e * (56 / 15 + t * (-136 / 35 + t * (-1262 / 105 + t * (73814 / 2835)))), this.cbg[2] = e * (-26 / 15 + t * (34 / 21 + t * (8 / 5 + t * (-12686 / 2835)))), e = e * t, this.cgb[3] = e * (4279 / 630 + t * (-332 / 35 + t * (-399572 / 14175))), this.cbg[3] = e * (1237 / 630 + t * (-12 / 5 + t * (-24832 / 14175))), e = e * t, this.cgb[4] = e * (4174 / 315 + t * (-144838 / 6237)), this.cbg[4] = e * (-734 / 315 + t * (109598 / 31185)), e = e * t, this.cgb[5] = e * (601676 / 22275), this.cbg[5] = e * (444337 / 155925), e = Math.pow(t, 2), this.Qn = this.k0 / (1 + t) * (1 + e * (1 / 4 + e * (1 / 64 + e / 256))), this.utg[0] = t * (-0.5 + t * (2 / 3 + t * (-37 / 96 + t * (1 / 360 + t * (81 / 512 + t * (-96199 / 604800)))))), this.gtu[0] = t * (0.5 + t * (-2 / 3 + t * (5 / 16 + t * (41 / 180 + t * (-127 / 288 + t * (7891 / 37800)))))), this.utg[1] = e * (-1 / 48 + t * (-1 / 15 + t * (437 / 1440 + t * (-46 / 105 + t * (1118711 / 3870720))))), this.gtu[1] = e * (13 / 48 + t * (-3 / 5 + t * (557 / 1440 + t * (281 / 630 + t * (-1983433 / 1935360))))), e = e * t, this.utg[2] = e * (-17 / 480 + t * (37 / 840 + t * (209 / 4480 + t * (-5569 / 90720)))), this.gtu[2] = e * (61 / 240 + t * (-103 / 140 + t * (15061 / 26880 + t * (167603 / 181440)))), e = e * t, this.utg[3] = e * (-4397 / 161280 + t * (11 / 504 + t * (830251 / 7257600))), this.gtu[3] = e * (49561 / 161280 + t * (-179 / 168 + t * (6601661 / 7257600))), e = e * t, this.utg[4] = e * (-4583 / 161280 + t * (108847 / 3991680)), this.gtu[4] = e * (34729 / 80640 + t * (-3418889 / 1995840)), e = e * t, this.utg[5] = e * (-20648693 / 638668800), this.gtu[5] = e * (212378941 / 319334400);
  var n = Hl(this.cbg, this.lat0);
  this.Zb = -this.Qn * (n + o3(this.gtu, 2 * n));
}
function h3(i) {
  var t = O(i.x - this.long0), e = i.y;
  e = Hl(this.cbg, e);
  var n = Math.sin(e), s = Math.cos(e), r = Math.sin(t), o = Math.cos(t);
  e = Math.atan2(n, o * s), t = Math.atan2(r * s, Se(n, s * o)), t = r3(Math.tan(t));
  var a = Gf(this.gtu, 2 * e, 2 * t);
  e = e + a[0], t = t + a[1];
  var l, h;
  return Math.abs(t) <= 2.623395162778 ? (l = this.a * (this.Qn * t) + this.x0, h = this.a * (this.Qn * e + this.Zb) + this.y0) : (l = 1 / 0, h = 1 / 0), i.x = l, i.y = h, i;
}
function c3(i) {
  var t = (i.x - this.x0) * (1 / this.a), e = (i.y - this.y0) * (1 / this.a);
  e = (e - this.Zb) / this.Qn, t = t / this.Qn;
  var n, s;
  if (Math.abs(t) <= 2.623395162778) {
    var r = Gf(this.utg, 2 * e, 2 * t);
    e = e + r[0], t = t + r[1], t = Math.atan(kf(t));
    var o = Math.sin(e), a = Math.cos(e), l = Math.sin(t), h = Math.cos(t);
    e = Math.atan2(o * h, Se(l, h * a)), t = Math.atan2(l, h * a), n = O(t + this.long0), s = Hl(this.cgb, e);
  } else
    n = 1 / 0, s = 1 / 0;
  return i.x = n, i.y = s, i;
}
var u3 = ["Extended_Transverse_Mercator", "Extended Transverse Mercator", "etmerc", "Transverse_Mercator", "Transverse Mercator", "tmerc"];
const Or = {
  init: l3,
  forward: h3,
  inverse: c3,
  names: u3
};
function d3(i, t) {
  if (i === void 0) {
    if (i = Math.floor((O(t) + Math.PI) * 30 / Math.PI) + 1, i < 0)
      return 0;
    if (i > 60)
      return 60;
  }
  return i;
}
var f3 = "etmerc";
function g3() {
  var i = d3(this.zone, this.long0);
  if (i === void 0)
    throw new Error("unknown utm zone");
  this.lat0 = 0, this.long0 = (6 * Math.abs(i) - 183) * Bt, this.x0 = 5e5, this.y0 = this.utmSouth ? 1e7 : 0, this.k0 = 0.9996, Or.init.apply(this), this.forward = Or.forward, this.inverse = Or.inverse;
}
var m3 = ["Universal Transverse Mercator System", "utm"];
const p3 = {
  init: g3,
  names: m3,
  dependsOn: f3
};
function Xl(i, t) {
  return Math.pow((1 - i) / (1 + i), t);
}
var _3 = 20;
function y3() {
  var i = Math.sin(this.lat0), t = Math.cos(this.lat0);
  t *= t, this.rc = Math.sqrt(1 - this.es) / (1 - this.es * i * i), this.C = Math.sqrt(1 + this.es * t * t / (1 - this.es)), this.phic0 = Math.asin(i / this.C), this.ratexp = 0.5 * this.C * this.e, this.K = Math.tan(0.5 * this.phic0 + ht) / (Math.pow(Math.tan(0.5 * this.lat0 + ht), this.C) * Xl(this.e * i, this.ratexp));
}
function v3(i) {
  var t = i.x, e = i.y;
  return i.y = 2 * Math.atan(this.K * Math.pow(Math.tan(0.5 * e + ht), this.C) * Xl(this.e * Math.sin(e), this.ratexp)) - R, i.x = this.C * t, i;
}
function x3(i) {
  for (var t = 1e-14, e = i.x / this.C, n = i.y, s = Math.pow(Math.tan(0.5 * n + ht) / this.K, 1 / this.C), r = _3; r > 0 && (n = 2 * Math.atan(s * Xl(this.e * Math.sin(i.y), -0.5 * this.e)) - R, !(Math.abs(n - i.y) < t)); --r)
    i.y = n;
  return r ? (i.x = e, i.y = n, i) : null;
}
var C3 = ["gauss"];
const Yl = {
  init: y3,
  forward: v3,
  inverse: x3,
  names: C3
};
function M3() {
  Yl.init.apply(this), this.rc && (this.sinc0 = Math.sin(this.phic0), this.cosc0 = Math.cos(this.phic0), this.R2 = 2 * this.rc, this.title || (this.title = "Oblique Stereographic Alternative"));
}
function E3(i) {
  var t, e, n, s;
  return i.x = O(i.x - this.long0), Yl.forward.apply(this, [i]), t = Math.sin(i.y), e = Math.cos(i.y), n = Math.cos(i.x), s = this.k0 * this.R2 / (1 + this.sinc0 * t + this.cosc0 * e * n), i.x = s * e * Math.sin(i.x), i.y = s * (this.cosc0 * t - this.sinc0 * e * n), i.x = this.a * i.x + this.x0, i.y = this.a * i.y + this.y0, i;
}
function w3(i) {
  var t, e, n, s, r;
  if (i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, i.x /= this.k0, i.y /= this.k0, r = Math.sqrt(i.x * i.x + i.y * i.y)) {
    var o = 2 * Math.atan2(r, this.R2);
    t = Math.sin(o), e = Math.cos(o), s = Math.asin(e * this.sinc0 + i.y * t * this.cosc0 / r), n = Math.atan2(i.x * t, r * this.cosc0 * e - i.y * this.sinc0 * t);
  } else
    s = this.phic0, n = 0;
  return i.x = n, i.y = s, Yl.inverse.apply(this, [i]), i.x = O(i.x + this.long0), i;
}
var S3 = ["Stereographic_North_Pole", "Oblique_Stereographic", "Polar_Stereographic", "sterea", "Oblique Stereographic Alternative", "Double_Stereographic"];
const R3 = {
  init: M3,
  forward: E3,
  inverse: w3,
  names: S3
};
function b3(i, t, e) {
  return t *= e, Math.tan(0.5 * (R + i)) * Math.pow((1 - t) / (1 + t), 0.5 * e);
}
function L3() {
  this.coslat0 = Math.cos(this.lat0), this.sinlat0 = Math.sin(this.lat0), this.sphere ? this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= I && (this.k0 = 0.5 * (1 + Qs(this.lat0) * Math.sin(this.lat_ts))) : (Math.abs(this.coslat0) <= I && (this.lat0 > 0 ? this.con = 1 : this.con = -1), this.cons = Math.sqrt(Math.pow(1 + this.e, 1 + this.e) * Math.pow(1 - this.e, 1 - this.e)), this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= I && (this.k0 = 0.5 * this.cons * $e(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) / be(this.e, this.con * this.lat_ts, this.con * Math.sin(this.lat_ts))), this.ms1 = $e(this.e, this.sinlat0, this.coslat0), this.X0 = 2 * Math.atan(this.ssfn_(this.lat0, this.sinlat0, this.e)) - R, this.cosX0 = Math.cos(this.X0), this.sinX0 = Math.sin(this.X0));
}
function T3(i) {
  var t = i.x, e = i.y, n = Math.sin(e), s = Math.cos(e), r, o, a, l, h, c, u = O(t - this.long0);
  return Math.abs(Math.abs(t - this.long0) - Math.PI) <= I && Math.abs(e + this.lat0) <= I ? (i.x = NaN, i.y = NaN, i) : this.sphere ? (r = 2 * this.k0 / (1 + this.sinlat0 * n + this.coslat0 * s * Math.cos(u)), i.x = this.a * r * s * Math.sin(u) + this.x0, i.y = this.a * r * (this.coslat0 * n - this.sinlat0 * s * Math.cos(u)) + this.y0, i) : (o = 2 * Math.atan(this.ssfn_(e, n, this.e)) - R, l = Math.cos(o), a = Math.sin(o), Math.abs(this.coslat0) <= I ? (h = be(this.e, e * this.con, this.con * n), c = 2 * this.a * this.k0 * h / this.cons, i.x = this.x0 + c * Math.sin(t - this.long0), i.y = this.y0 - this.con * c * Math.cos(t - this.long0), i) : (Math.abs(this.sinlat0) < I ? (r = 2 * this.a * this.k0 / (1 + l * Math.cos(u)), i.y = r * a) : (r = 2 * this.a * this.k0 * this.ms1 / (this.cosX0 * (1 + this.sinX0 * a + this.cosX0 * l * Math.cos(u))), i.y = r * (this.cosX0 * a - this.sinX0 * l * Math.cos(u)) + this.y0), i.x = r * l * Math.sin(u) + this.x0, i));
}
function I3(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e, n, s, r, o = Math.sqrt(i.x * i.x + i.y * i.y);
  if (this.sphere) {
    var a = 2 * Math.atan(o / (2 * this.a * this.k0));
    return t = this.long0, e = this.lat0, o <= I ? (i.x = t, i.y = e, i) : (e = Math.asin(Math.cos(a) * this.sinlat0 + i.y * Math.sin(a) * this.coslat0 / o), Math.abs(this.coslat0) < I ? this.lat0 > 0 ? t = O(this.long0 + Math.atan2(i.x, -1 * i.y)) : t = O(this.long0 + Math.atan2(i.x, i.y)) : t = O(this.long0 + Math.atan2(i.x * Math.sin(a), o * this.coslat0 * Math.cos(a) - i.y * this.sinlat0 * Math.sin(a))), i.x = t, i.y = e, i);
  } else if (Math.abs(this.coslat0) <= I) {
    if (o <= I)
      return e = this.lat0, t = this.long0, i.x = t, i.y = e, i;
    i.x *= this.con, i.y *= this.con, n = o * this.cons / (2 * this.a * this.k0), e = this.con * Gs(this.e, n), t = this.con * O(this.con * this.long0 + Math.atan2(i.x, -1 * i.y));
  } else
    s = 2 * Math.atan(o * this.cosX0 / (2 * this.a * this.k0 * this.ms1)), t = this.long0, o <= I ? r = this.X0 : (r = Math.asin(Math.cos(s) * this.sinX0 + i.y * Math.sin(s) * this.cosX0 / o), t = O(this.long0 + Math.atan2(i.x * Math.sin(s), o * this.cosX0 * Math.cos(s) - i.y * this.sinX0 * Math.sin(s)))), e = -1 * Gs(this.e, Math.tan(0.5 * (R + r)));
  return i.x = t, i.y = e, i;
}
var P3 = ["stere", "Stereographic_South_Pole", "Polar Stereographic (variant B)"];
const A3 = {
  init: L3,
  forward: T3,
  inverse: I3,
  names: P3,
  ssfn_: b3
};
function O3() {
  var i = this.lat0;
  this.lambda0 = this.long0;
  var t = Math.sin(i), e = this.a, n = this.rf, s = 1 / n, r = 2 * s - Math.pow(s, 2), o = this.e = Math.sqrt(r);
  this.R = this.k0 * e * Math.sqrt(1 - r) / (1 - r * Math.pow(t, 2)), this.alpha = Math.sqrt(1 + r / (1 - r) * Math.pow(Math.cos(i), 4)), this.b0 = Math.asin(t / this.alpha);
  var a = Math.log(Math.tan(Math.PI / 4 + this.b0 / 2)), l = Math.log(Math.tan(Math.PI / 4 + i / 2)), h = Math.log((1 + o * t) / (1 - o * t));
  this.K = a - this.alpha * l + this.alpha * o / 2 * h;
}
function N3(i) {
  var t = Math.log(Math.tan(Math.PI / 4 - i.y / 2)), e = this.e / 2 * Math.log((1 + this.e * Math.sin(i.y)) / (1 - this.e * Math.sin(i.y))), n = -this.alpha * (t + e) + this.K, s = 2 * (Math.atan(Math.exp(n)) - Math.PI / 4), r = this.alpha * (i.x - this.lambda0), o = Math.atan(Math.sin(r) / (Math.sin(this.b0) * Math.tan(s) + Math.cos(this.b0) * Math.cos(r))), a = Math.asin(Math.cos(this.b0) * Math.sin(s) - Math.sin(this.b0) * Math.cos(s) * Math.cos(r));
  return i.y = this.R / 2 * Math.log((1 + Math.sin(a)) / (1 - Math.sin(a))) + this.y0, i.x = this.R * o + this.x0, i;
}
function F3(i) {
  for (var t = i.x - this.x0, e = i.y - this.y0, n = t / this.R, s = 2 * (Math.atan(Math.exp(e / this.R)) - Math.PI / 4), r = Math.asin(Math.cos(this.b0) * Math.sin(s) + Math.sin(this.b0) * Math.cos(s) * Math.cos(n)), o = Math.atan(Math.sin(n) / (Math.cos(this.b0) * Math.cos(n) - Math.sin(this.b0) * Math.tan(s))), a = this.lambda0 + o / this.alpha, l = 0, h = r, c = -1e3, u = 0; Math.abs(h - c) > 1e-7; ) {
    if (++u > 20)
      return;
    l = 1 / this.alpha * (Math.log(Math.tan(Math.PI / 4 + r / 2)) - this.K) + this.e * Math.log(Math.tan(Math.PI / 4 + Math.asin(this.e * Math.sin(h)) / 2)), c = h, h = 2 * Math.atan(Math.exp(l)) - Math.PI / 2;
  }
  return i.x = a, i.y = h, i;
}
var D3 = ["somerc"];
const k3 = {
  init: O3,
  forward: N3,
  inverse: F3,
  names: D3
};
var wn = 1e-7;
function G3(i) {
  var t = ["Hotine_Oblique_Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin"], e = typeof i.PROJECTION == "object" ? Object.keys(i.PROJECTION)[0] : i.PROJECTION;
  return "no_uoff" in i || "no_off" in i || t.indexOf(e) !== -1;
}
function $3() {
  var i, t, e, n, s, r, o, a, l, h, c = 0, u, d = 0, f = 0, g = 0, m = 0, p = 0, _ = 0;
  this.no_off = G3(this), this.no_rot = "no_rot" in this;
  var y = !1;
  "alpha" in this && (y = !0);
  var v = !1;
  if ("rectified_grid_angle" in this && (v = !0), y && (_ = this.alpha), v && (c = this.rectified_grid_angle * Bt), y || v)
    d = this.longc;
  else if (f = this.long1, m = this.lat1, g = this.long2, p = this.lat2, Math.abs(m - p) <= wn || (i = Math.abs(m)) <= wn || Math.abs(i - R) <= wn || Math.abs(Math.abs(this.lat0) - R) <= wn || Math.abs(Math.abs(p) - R) <= wn)
    throw new Error();
  var x = 1 - this.es;
  t = Math.sqrt(x), Math.abs(this.lat0) > I ? (a = Math.sin(this.lat0), e = Math.cos(this.lat0), i = 1 - this.es * a * a, this.B = e * e, this.B = Math.sqrt(1 + this.es * this.B * this.B / x), this.A = this.B * this.k0 * t / i, n = this.B * t / (e * Math.sqrt(i)), s = n * n - 1, s <= 0 ? s = 0 : (s = Math.sqrt(s), this.lat0 < 0 && (s = -s)), this.E = s += n, this.E *= Math.pow(be(this.e, this.lat0, a), this.B)) : (this.B = 1 / t, this.A = this.k0, this.E = n = s = 1), y || v ? (y ? (u = Math.asin(Math.sin(_) / n), v || (c = _)) : (u = c, _ = Math.asin(n * Math.sin(u))), this.lam0 = d - Math.asin(0.5 * (s - 1 / s) * Math.tan(u)) / this.B) : (r = Math.pow(be(this.e, m, Math.sin(m)), this.B), o = Math.pow(be(this.e, p, Math.sin(p)), this.B), s = this.E / r, l = (o - r) / (o + r), h = this.E * this.E, h = (h - o * r) / (h + o * r), i = f - g, i < -Math.pi ? g -= Ds : i > Math.pi && (g += Ds), this.lam0 = O(0.5 * (f + g) - Math.atan(h * Math.tan(0.5 * this.B * (f - g)) / l) / this.B), u = Math.atan(2 * Math.sin(this.B * O(f - this.lam0)) / (s - 1 / s)), c = _ = Math.asin(n * Math.sin(u))), this.singam = Math.sin(u), this.cosgam = Math.cos(u), this.sinrot = Math.sin(c), this.cosrot = Math.cos(c), this.rB = 1 / this.B, this.ArB = this.A * this.rB, this.BrA = 1 / this.ArB, this.A * this.B, this.no_off ? this.u_0 = 0 : (this.u_0 = Math.abs(this.ArB * Math.atan(Math.sqrt(n * n - 1) / Math.cos(_))), this.lat0 < 0 && (this.u_0 = -this.u_0)), s = 0.5 * u, this.v_pole_n = this.ArB * Math.log(Math.tan(ht - s)), this.v_pole_s = this.ArB * Math.log(Math.tan(ht + s));
}
function B3(i) {
  var t = {}, e, n, s, r, o, a, l, h;
  if (i.x = i.x - this.lam0, Math.abs(Math.abs(i.y) - R) > I) {
    if (o = this.E / Math.pow(be(this.e, i.y, Math.sin(i.y)), this.B), a = 1 / o, e = 0.5 * (o - a), n = 0.5 * (o + a), r = Math.sin(this.B * i.x), s = (e * this.singam - r * this.cosgam) / n, Math.abs(Math.abs(s) - 1) < I)
      throw new Error();
    h = 0.5 * this.ArB * Math.log((1 - s) / (1 + s)), a = Math.cos(this.B * i.x), Math.abs(a) < wn ? l = this.A * i.x : l = this.ArB * Math.atan2(e * this.cosgam + r * this.singam, a);
  } else
    h = i.y > 0 ? this.v_pole_n : this.v_pole_s, l = this.ArB * i.y;
  return this.no_rot ? (t.x = l, t.y = h) : (l -= this.u_0, t.x = h * this.cosrot + l * this.sinrot, t.y = l * this.cosrot - h * this.sinrot), t.x = this.a * t.x + this.x0, t.y = this.a * t.y + this.y0, t;
}
function z3(i) {
  var t, e, n, s, r, o, a, l = {};
  if (i.x = (i.x - this.x0) * (1 / this.a), i.y = (i.y - this.y0) * (1 / this.a), this.no_rot ? (e = i.y, t = i.x) : (e = i.x * this.cosrot - i.y * this.sinrot, t = i.y * this.cosrot + i.x * this.sinrot + this.u_0), n = Math.exp(-this.BrA * e), s = 0.5 * (n - 1 / n), r = 0.5 * (n + 1 / n), o = Math.sin(this.BrA * t), a = (o * this.cosgam + s * this.singam) / r, Math.abs(Math.abs(a) - 1) < I)
    l.x = 0, l.y = a < 0 ? -R : R;
  else {
    if (l.y = this.E / Math.sqrt((1 + a) / (1 - a)), l.y = Gs(this.e, Math.pow(l.y, 1 / this.B)), l.y === 1 / 0)
      throw new Error();
    l.x = -this.rB * Math.atan2(s * this.cosgam - o * this.singam, Math.cos(this.BrA * t));
  }
  return l.x += this.lam0, l;
}
var Z3 = ["Hotine_Oblique_Mercator", "Hotine Oblique Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin", "Hotine_Oblique_Mercator_Two_Point_Natural_Origin", "Hotine_Oblique_Mercator_Azimuth_Center", "Oblique_Mercator", "omerc"];
const V3 = {
  init: $3,
  forward: B3,
  inverse: z3,
  names: Z3
};
function U3() {
  if (this.lat2 || (this.lat2 = this.lat1), this.k0 || (this.k0 = 1), this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, !(Math.abs(this.lat1 + this.lat2) < I)) {
    var i = this.b / this.a;
    this.e = Math.sqrt(1 - i * i);
    var t = Math.sin(this.lat1), e = Math.cos(this.lat1), n = $e(this.e, t, e), s = be(this.e, this.lat1, t), r = Math.sin(this.lat2), o = Math.cos(this.lat2), a = $e(this.e, r, o), l = be(this.e, this.lat2, r), h = be(this.e, this.lat0, Math.sin(this.lat0));
    Math.abs(this.lat1 - this.lat2) > I ? this.ns = Math.log(n / a) / Math.log(s / l) : this.ns = t, isNaN(this.ns) && (this.ns = t), this.f0 = n / (this.ns * Math.pow(s, this.ns)), this.rh = this.a * this.f0 * Math.pow(h, this.ns), this.title || (this.title = "Lambert Conformal Conic");
  }
}
function W3(i) {
  var t = i.x, e = i.y;
  Math.abs(2 * Math.abs(e) - Math.PI) <= I && (e = Qs(e) * (R - 2 * I));
  var n = Math.abs(Math.abs(e) - R), s, r;
  if (n > I)
    s = be(this.e, e, Math.sin(e)), r = this.a * this.f0 * Math.pow(s, this.ns);
  else {
    if (n = e * this.ns, n <= 0)
      return null;
    r = 0;
  }
  var o = this.ns * O(t - this.long0);
  return i.x = this.k0 * (r * Math.sin(o)) + this.x0, i.y = this.k0 * (this.rh - r * Math.cos(o)) + this.y0, i;
}
function H3(i) {
  var t, e, n, s, r, o = (i.x - this.x0) / this.k0, a = this.rh - (i.y - this.y0) / this.k0;
  this.ns > 0 ? (t = Math.sqrt(o * o + a * a), e = 1) : (t = -Math.sqrt(o * o + a * a), e = -1);
  var l = 0;
  if (t !== 0 && (l = Math.atan2(e * o, e * a)), t !== 0 || this.ns > 0) {
    if (e = 1 / this.ns, n = Math.pow(t / (this.a * this.f0), e), s = Gs(this.e, n), s === -9999)
      return null;
  } else
    s = -R;
  return r = O(l / this.ns + this.long0), i.x = r, i.y = s, i;
}
var X3 = [
  "Lambert Tangential Conformal Conic Projection",
  "Lambert_Conformal_Conic",
  "Lambert_Conformal_Conic_1SP",
  "Lambert_Conformal_Conic_2SP",
  "lcc",
  "Lambert Conic Conformal (1SP)",
  "Lambert Conic Conformal (2SP)"
];
const Y3 = {
  init: U3,
  forward: W3,
  inverse: H3,
  names: X3
};
function j3() {
  this.a = 6377397155e-3, this.es = 0.006674372230614, this.e = Math.sqrt(this.es), this.lat0 || (this.lat0 = 0.863937979737193), this.long0 || (this.long0 = 0.7417649320975901 - 0.308341501185665), this.k0 || (this.k0 = 0.9999), this.s45 = 0.785398163397448, this.s90 = 2 * this.s45, this.fi0 = this.lat0, this.e2 = this.es, this.e = Math.sqrt(this.e2), this.alfa = Math.sqrt(1 + this.e2 * Math.pow(Math.cos(this.fi0), 4) / (1 - this.e2)), this.uq = 1.04216856380474, this.u0 = Math.asin(Math.sin(this.fi0) / this.alfa), this.g = Math.pow((1 + this.e * Math.sin(this.fi0)) / (1 - this.e * Math.sin(this.fi0)), this.alfa * this.e / 2), this.k = Math.tan(this.u0 / 2 + this.s45) / Math.pow(Math.tan(this.fi0 / 2 + this.s45), this.alfa) * this.g, this.k1 = this.k0, this.n0 = this.a * Math.sqrt(1 - this.e2) / (1 - this.e2 * Math.pow(Math.sin(this.fi0), 2)), this.s0 = 1.37008346281555, this.n = Math.sin(this.s0), this.ro0 = this.k1 * this.n0 / Math.tan(this.s0), this.ad = this.s90 - this.uq;
}
function K3(i) {
  var t, e, n, s, r, o, a, l = i.x, h = i.y, c = O(l - this.long0);
  return t = Math.pow((1 + this.e * Math.sin(h)) / (1 - this.e * Math.sin(h)), this.alfa * this.e / 2), e = 2 * (Math.atan(this.k * Math.pow(Math.tan(h / 2 + this.s45), this.alfa) / t) - this.s45), n = -c * this.alfa, s = Math.asin(Math.cos(this.ad) * Math.sin(e) + Math.sin(this.ad) * Math.cos(e) * Math.cos(n)), r = Math.asin(Math.cos(e) * Math.sin(n) / Math.cos(s)), o = this.n * r, a = this.ro0 * Math.pow(Math.tan(this.s0 / 2 + this.s45), this.n) / Math.pow(Math.tan(s / 2 + this.s45), this.n), i.y = a * Math.cos(o) / 1, i.x = a * Math.sin(o) / 1, this.czech || (i.y *= -1, i.x *= -1), i;
}
function q3(i) {
  var t, e, n, s, r, o, a, l, h = i.x;
  i.x = i.y, i.y = h, this.czech || (i.y *= -1, i.x *= -1), o = Math.sqrt(i.x * i.x + i.y * i.y), r = Math.atan2(i.y, i.x), s = r / Math.sin(this.s0), n = 2 * (Math.atan(Math.pow(this.ro0 / o, 1 / this.n) * Math.tan(this.s0 / 2 + this.s45)) - this.s45), t = Math.asin(Math.cos(this.ad) * Math.sin(n) - Math.sin(this.ad) * Math.cos(n) * Math.cos(s)), e = Math.asin(Math.cos(n) * Math.sin(s) / Math.cos(t)), i.x = this.long0 - e / this.alfa, a = t, l = 0;
  var c = 0;
  do
    i.y = 2 * (Math.atan(Math.pow(this.k, -1 / this.alfa) * Math.pow(Math.tan(t / 2 + this.s45), 1 / this.alfa) * Math.pow((1 + this.e * Math.sin(a)) / (1 - this.e * Math.sin(a)), this.e / 2)) - this.s45), Math.abs(a - i.y) < 1e-10 && (l = 1), a = i.y, c += 1;
  while (l === 0 && c < 15);
  return c >= 15 ? null : i;
}
var J3 = ["Krovak", "krovak"];
const Q3 = {
  init: j3,
  forward: K3,
  inverse: q3,
  names: J3
};
function jt(i, t, e, n, s) {
  return i * s - t * Math.sin(2 * s) + e * Math.sin(4 * s) - n * Math.sin(6 * s);
}
function tr(i) {
  return 1 - 0.25 * i * (1 + i / 16 * (3 + 1.25 * i));
}
function er(i) {
  return 0.375 * i * (1 + 0.25 * i * (1 + 0.46875 * i));
}
function ir(i) {
  return 0.05859375 * i * i * (1 + 0.75 * i);
}
function nr(i) {
  return i * i * i * (35 / 3072);
}
function Hn(i, t, e) {
  var n = t * e;
  return i / Math.sqrt(1 - n * n);
}
function Qn(i) {
  return Math.abs(i) < R ? i : i - Qs(i) * Math.PI;
}
function so(i, t, e, n, s) {
  var r, o;
  r = i / t;
  for (var a = 0; a < 15; a++)
    if (o = (i - (t * r - e * Math.sin(2 * r) + n * Math.sin(4 * r) - s * Math.sin(6 * r))) / (t - 2 * e * Math.cos(2 * r) + 4 * n * Math.cos(4 * r) - 6 * s * Math.cos(6 * r)), r += o, Math.abs(o) <= 1e-10)
      return r;
  return NaN;
}
function tC() {
  this.sphere || (this.e0 = tr(this.es), this.e1 = er(this.es), this.e2 = ir(this.es), this.e3 = nr(this.es), this.ml0 = this.a * jt(this.e0, this.e1, this.e2, this.e3, this.lat0));
}
function eC(i) {
  var t, e, n = i.x, s = i.y;
  if (n = O(n - this.long0), this.sphere)
    t = this.a * Math.asin(Math.cos(s) * Math.sin(n)), e = this.a * (Math.atan2(Math.tan(s), Math.cos(n)) - this.lat0);
  else {
    var r = Math.sin(s), o = Math.cos(s), a = Hn(this.a, this.e, r), l = Math.tan(s) * Math.tan(s), h = n * Math.cos(s), c = h * h, u = this.es * o * o / (1 - this.es), d = this.a * jt(this.e0, this.e1, this.e2, this.e3, s);
    t = a * h * (1 - c * l * (1 / 6 - (8 - l + 8 * u) * c / 120)), e = d - this.ml0 + a * r / o * c * (0.5 + (5 - l + 6 * u) * c / 24);
  }
  return i.x = t + this.x0, i.y = e + this.y0, i;
}
function iC(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = i.x / this.a, e = i.y / this.a, n, s;
  if (this.sphere) {
    var r = e + this.lat0;
    n = Math.asin(Math.sin(r) * Math.cos(t)), s = Math.atan2(Math.tan(t), Math.cos(r));
  } else {
    var o = this.ml0 / this.a + e, a = so(o, this.e0, this.e1, this.e2, this.e3);
    if (Math.abs(Math.abs(a) - R) <= I)
      return i.x = this.long0, i.y = R, e < 0 && (i.y *= -1), i;
    var l = Hn(this.a, this.e, Math.sin(a)), h = l * l * l / this.a / this.a * (1 - this.es), c = Math.pow(Math.tan(a), 2), u = t * this.a / l, d = u * u;
    n = a - l * Math.tan(a) / h * u * u * (0.5 - (1 + 3 * c) * u * u / 24), s = u * (1 - d * (c / 3 + (1 + 3 * c) * c * d / 15)) / Math.cos(a);
  }
  return i.x = O(s + this.long0), i.y = Qn(n), i;
}
var nC = ["Cassini", "Cassini_Soldner", "cass"];
const sC = {
  init: tC,
  forward: eC,
  inverse: iC,
  names: nC
};
function Mi(i, t) {
  var e;
  return i > 1e-7 ? (e = i * t, (1 - i * i) * (t / (1 - e * e) - 0.5 / i * Math.log((1 - e) / (1 + e)))) : 2 * t;
}
var rC = 1, oC = 2, aC = 3, lC = 4;
function hC() {
  var i = Math.abs(this.lat0);
  if (Math.abs(i - R) < I ? this.mode = this.lat0 < 0 ? this.S_POLE : this.N_POLE : Math.abs(i) < I ? this.mode = this.EQUIT : this.mode = this.OBLIQ, this.es > 0) {
    var t;
    switch (this.qp = Mi(this.e, 1), this.mmf = 0.5 / (1 - this.es), this.apa = yC(this.es), this.mode) {
      case this.N_POLE:
        this.dd = 1;
        break;
      case this.S_POLE:
        this.dd = 1;
        break;
      case this.EQUIT:
        this.rq = Math.sqrt(0.5 * this.qp), this.dd = 1 / this.rq, this.xmf = 1, this.ymf = 0.5 * this.qp;
        break;
      case this.OBLIQ:
        this.rq = Math.sqrt(0.5 * this.qp), t = Math.sin(this.lat0), this.sinb1 = Mi(this.e, t) / this.qp, this.cosb1 = Math.sqrt(1 - this.sinb1 * this.sinb1), this.dd = Math.cos(this.lat0) / (Math.sqrt(1 - this.es * t * t) * this.rq * this.cosb1), this.ymf = (this.xmf = this.rq) / this.dd, this.xmf *= this.dd;
        break;
    }
  } else
    this.mode === this.OBLIQ && (this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0));
}
function cC(i) {
  var t, e, n, s, r, o, a, l, h, c, u = i.x, d = i.y;
  if (u = O(u - this.long0), this.sphere) {
    if (r = Math.sin(d), c = Math.cos(d), n = Math.cos(u), this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (e = this.mode === this.EQUIT ? 1 + c * n : 1 + this.sinph0 * r + this.cosph0 * c * n, e <= I)
        return null;
      e = Math.sqrt(2 / e), t = e * c * Math.sin(u), e *= this.mode === this.EQUIT ? r : this.cosph0 * r - this.sinph0 * c * n;
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (n = -n), Math.abs(d + this.lat0) < I)
        return null;
      e = ht - d * 0.5, e = 2 * (this.mode === this.S_POLE ? Math.cos(e) : Math.sin(e)), t = e * Math.sin(u), e *= n;
    }
  } else {
    switch (a = 0, l = 0, h = 0, n = Math.cos(u), s = Math.sin(u), r = Math.sin(d), o = Mi(this.e, r), (this.mode === this.OBLIQ || this.mode === this.EQUIT) && (a = o / this.qp, l = Math.sqrt(1 - a * a)), this.mode) {
      case this.OBLIQ:
        h = 1 + this.sinb1 * a + this.cosb1 * l * n;
        break;
      case this.EQUIT:
        h = 1 + l * n;
        break;
      case this.N_POLE:
        h = R + d, o = this.qp - o;
        break;
      case this.S_POLE:
        h = d - R, o = this.qp + o;
        break;
    }
    if (Math.abs(h) < I)
      return null;
    switch (this.mode) {
      case this.OBLIQ:
      case this.EQUIT:
        h = Math.sqrt(2 / h), this.mode === this.OBLIQ ? e = this.ymf * h * (this.cosb1 * a - this.sinb1 * l * n) : e = (h = Math.sqrt(2 / (1 + l * n))) * a * this.ymf, t = this.xmf * h * l * s;
        break;
      case this.N_POLE:
      case this.S_POLE:
        o >= 0 ? (t = (h = Math.sqrt(o)) * s, e = n * (this.mode === this.S_POLE ? h : -h)) : t = e = 0;
        break;
    }
  }
  return i.x = this.a * t + this.x0, i.y = this.a * e + this.y0, i;
}
function uC(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = i.x / this.a, e = i.y / this.a, n, s, r, o, a, l, h;
  if (this.sphere) {
    var c = 0, u, d = 0;
    if (u = Math.sqrt(t * t + e * e), s = u * 0.5, s > 1)
      return null;
    switch (s = 2 * Math.asin(s), (this.mode === this.OBLIQ || this.mode === this.EQUIT) && (d = Math.sin(s), c = Math.cos(s)), this.mode) {
      case this.EQUIT:
        s = Math.abs(u) <= I ? 0 : Math.asin(e * d / u), t *= d, e = c * u;
        break;
      case this.OBLIQ:
        s = Math.abs(u) <= I ? this.lat0 : Math.asin(c * this.sinph0 + e * d * this.cosph0 / u), t *= d * this.cosph0, e = (c - Math.sin(s) * this.sinph0) * u;
        break;
      case this.N_POLE:
        e = -e, s = R - s;
        break;
      case this.S_POLE:
        s -= R;
        break;
    }
    n = e === 0 && (this.mode === this.EQUIT || this.mode === this.OBLIQ) ? 0 : Math.atan2(t, e);
  } else {
    if (h = 0, this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (t /= this.dd, e *= this.dd, l = Math.sqrt(t * t + e * e), l < I)
        return i.x = this.long0, i.y = this.lat0, i;
      o = 2 * Math.asin(0.5 * l / this.rq), r = Math.cos(o), t *= o = Math.sin(o), this.mode === this.OBLIQ ? (h = r * this.sinb1 + e * o * this.cosb1 / l, a = this.qp * h, e = l * this.cosb1 * r - e * this.sinb1 * o) : (h = e * o / l, a = this.qp * h, e = l * r);
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (e = -e), a = t * t + e * e, !a)
        return i.x = this.long0, i.y = this.lat0, i;
      h = 1 - a / this.qp, this.mode === this.S_POLE && (h = -h);
    }
    n = Math.atan2(t, e), s = vC(Math.asin(h), this.apa);
  }
  return i.x = O(this.long0 + n), i.y = s, i;
}
var dC = 0.3333333333333333, fC = 0.17222222222222222, gC = 0.10257936507936508, mC = 0.06388888888888888, pC = 0.0664021164021164, _C = 0.016415012942191543;
function yC(i) {
  var t, e = [];
  return e[0] = i * dC, t = i * i, e[0] += t * fC, e[1] = t * mC, t *= i, e[0] += t * gC, e[1] += t * pC, e[2] = t * _C, e;
}
function vC(i, t) {
  var e = i + i;
  return i + t[0] * Math.sin(e) + t[1] * Math.sin(e + e) + t[2] * Math.sin(e + e + e);
}
var xC = ["Lambert Azimuthal Equal Area", "Lambert_Azimuthal_Equal_Area", "laea"];
const CC = {
  init: hC,
  forward: cC,
  inverse: uC,
  names: xC,
  S_POLE: rC,
  N_POLE: oC,
  EQUIT: aC,
  OBLIQ: lC
};
function Li(i) {
  return Math.abs(i) > 1 && (i = i > 1 ? 1 : -1), Math.asin(i);
}
function MC() {
  Math.abs(this.lat1 + this.lat2) < I || (this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e3 = Math.sqrt(this.es), this.sin_po = Math.sin(this.lat1), this.cos_po = Math.cos(this.lat1), this.t1 = this.sin_po, this.con = this.sin_po, this.ms1 = $e(this.e3, this.sin_po, this.cos_po), this.qs1 = Mi(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat2), this.cos_po = Math.cos(this.lat2), this.t2 = this.sin_po, this.ms2 = $e(this.e3, this.sin_po, this.cos_po), this.qs2 = Mi(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat0), this.cos_po = Math.cos(this.lat0), this.t3 = this.sin_po, this.qs0 = Mi(this.e3, this.sin_po, this.cos_po), Math.abs(this.lat1 - this.lat2) > I ? this.ns0 = (this.ms1 * this.ms1 - this.ms2 * this.ms2) / (this.qs2 - this.qs1) : this.ns0 = this.con, this.c = this.ms1 * this.ms1 + this.ns0 * this.qs1, this.rh = this.a * Math.sqrt(this.c - this.ns0 * this.qs0) / this.ns0);
}
function EC(i) {
  var t = i.x, e = i.y;
  this.sin_phi = Math.sin(e), this.cos_phi = Math.cos(e);
  var n = Mi(this.e3, this.sin_phi, this.cos_phi), s = this.a * Math.sqrt(this.c - this.ns0 * n) / this.ns0, r = this.ns0 * O(t - this.long0), o = s * Math.sin(r) + this.x0, a = this.rh - s * Math.cos(r) + this.y0;
  return i.x = o, i.y = a, i;
}
function wC(i) {
  var t, e, n, s, r, o;
  return i.x -= this.x0, i.y = this.rh - i.y + this.y0, this.ns0 >= 0 ? (t = Math.sqrt(i.x * i.x + i.y * i.y), n = 1) : (t = -Math.sqrt(i.x * i.x + i.y * i.y), n = -1), s = 0, t !== 0 && (s = Math.atan2(n * i.x, n * i.y)), n = t * this.ns0 / this.a, this.sphere ? o = Math.asin((this.c - n * n) / (2 * this.ns0)) : (e = (this.c - n * n) / this.ns0, o = this.phi1z(this.e3, e)), r = O(s / this.ns0 + this.long0), i.x = r, i.y = o, i;
}
function SC(i, t) {
  var e, n, s, r, o, a = Li(0.5 * t);
  if (i < I)
    return a;
  for (var l = i * i, h = 1; h <= 25; h++)
    if (e = Math.sin(a), n = Math.cos(a), s = i * e, r = 1 - s * s, o = 0.5 * r * r / n * (t / (1 - l) - e / r + 0.5 / i * Math.log((1 - s) / (1 + s))), a = a + o, Math.abs(o) <= 1e-7)
      return a;
  return null;
}
var RC = ["Albers_Conic_Equal_Area", "Albers", "aea"];
const bC = {
  init: MC,
  forward: EC,
  inverse: wC,
  names: RC,
  phi1z: SC
};
function LC() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0), this.infinity_dist = 1e3 * this.a, this.rc = 1;
}
function TC(i) {
  var t, e, n, s, r, o, a, l, h = i.x, c = i.y;
  return n = O(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(n), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, o > 0 || Math.abs(o) <= I ? (a = this.x0 + this.a * r * e * Math.sin(n) / o, l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s) / o) : (a = this.x0 + this.infinity_dist * e * Math.sin(n), l = this.y0 + this.infinity_dist * (this.cos_p14 * t - this.sin_p14 * e * s)), i.x = a, i.y = l, i;
}
function IC(i) {
  var t, e, n, s, r, o;
  return i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, i.x /= this.k0, i.y /= this.k0, (t = Math.sqrt(i.x * i.x + i.y * i.y)) ? (s = Math.atan2(t, this.rc), e = Math.sin(s), n = Math.cos(s), o = Li(n * this.sin_p14 + i.y * e * this.cos_p14 / t), r = Math.atan2(i.x * e, t * this.cos_p14 * n - i.y * this.sin_p14 * e), r = O(this.long0 + r)) : (o = this.phic0, r = 0), i.x = r, i.y = o, i;
}
var PC = ["gnom"];
const AC = {
  init: LC,
  forward: TC,
  inverse: IC,
  names: PC
};
function OC(i, t) {
  var e = 1 - (1 - i * i) / (2 * i) * Math.log((1 - i) / (1 + i));
  if (Math.abs(Math.abs(t) - e) < 1e-6)
    return t < 0 ? -1 * R : R;
  for (var n = Math.asin(0.5 * t), s, r, o, a, l = 0; l < 30; l++)
    if (r = Math.sin(n), o = Math.cos(n), a = i * r, s = Math.pow(1 - a * a, 2) / (2 * o) * (t / (1 - i * i) - r / (1 - a * a) + 0.5 / i * Math.log((1 - a) / (1 + a))), n += s, Math.abs(s) <= 1e-10)
      return n;
  return NaN;
}
function NC() {
  this.sphere || (this.k0 = $e(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)));
}
function FC(i) {
  var t = i.x, e = i.y, n, s, r = O(t - this.long0);
  if (this.sphere)
    n = this.x0 + this.a * r * Math.cos(this.lat_ts), s = this.y0 + this.a * Math.sin(e) / Math.cos(this.lat_ts);
  else {
    var o = Mi(this.e, Math.sin(e));
    n = this.x0 + this.a * this.k0 * r, s = this.y0 + this.a * o * 0.5 / this.k0;
  }
  return i.x = n, i.y = s, i;
}
function DC(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e;
  return this.sphere ? (t = O(this.long0 + i.x / this.a / Math.cos(this.lat_ts)), e = Math.asin(i.y / this.a * Math.cos(this.lat_ts))) : (e = OC(this.e, 2 * i.y * this.k0 / this.a), t = O(this.long0 + i.x / (this.a * this.k0))), i.x = t, i.y = e, i;
}
var kC = ["cea"];
const GC = {
  init: NC,
  forward: FC,
  inverse: DC,
  names: kC
};
function $C() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Equidistant Cylindrical (Plate Carre)", this.rc = Math.cos(this.lat_ts);
}
function BC(i) {
  var t = i.x, e = i.y, n = O(t - this.long0), s = Qn(e - this.lat0);
  return i.x = this.x0 + this.a * n * this.rc, i.y = this.y0 + this.a * s, i;
}
function zC(i) {
  var t = i.x, e = i.y;
  return i.x = O(this.long0 + (t - this.x0) / (this.a * this.rc)), i.y = Qn(this.lat0 + (e - this.y0) / this.a), i;
}
var ZC = ["Equirectangular", "Equidistant_Cylindrical", "eqc"];
const VC = {
  init: $C,
  forward: BC,
  inverse: zC,
  names: ZC
};
var tu = 20;
function UC() {
  this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = tr(this.es), this.e1 = er(this.es), this.e2 = ir(this.es), this.e3 = nr(this.es), this.ml0 = this.a * jt(this.e0, this.e1, this.e2, this.e3, this.lat0);
}
function WC(i) {
  var t = i.x, e = i.y, n, s, r, o = O(t - this.long0);
  if (r = o * Math.sin(e), this.sphere)
    Math.abs(e) <= I ? (n = this.a * o, s = -1 * this.a * this.lat0) : (n = this.a * Math.sin(r) / Math.tan(e), s = this.a * (Qn(e - this.lat0) + (1 - Math.cos(r)) / Math.tan(e)));
  else if (Math.abs(e) <= I)
    n = this.a * o, s = -1 * this.ml0;
  else {
    var a = Hn(this.a, this.e, Math.sin(e)) / Math.tan(e);
    n = a * Math.sin(r), s = this.a * jt(this.e0, this.e1, this.e2, this.e3, e) - this.ml0 + a * (1 - Math.cos(r));
  }
  return i.x = n + this.x0, i.y = s + this.y0, i;
}
function HC(i) {
  var t, e, n, s, r, o, a, l, h;
  if (n = i.x - this.x0, s = i.y - this.y0, this.sphere)
    if (Math.abs(s + this.a * this.lat0) <= I)
      t = O(n / this.a + this.long0), e = 0;
    else {
      o = this.lat0 + s / this.a, a = n * n / this.a / this.a + o * o, l = o;
      var c;
      for (r = tu; r; --r)
        if (c = Math.tan(l), h = -1 * (o * (l * c + 1) - l - 0.5 * (l * l + a) * c) / ((l - o) / c - 1), l += h, Math.abs(h) <= I) {
          e = l;
          break;
        }
      t = O(this.long0 + Math.asin(n * Math.tan(l) / this.a) / Math.sin(e));
    }
  else if (Math.abs(s + this.ml0) <= I)
    e = 0, t = O(this.long0 + n / this.a);
  else {
    o = (this.ml0 + s) / this.a, a = n * n / this.a / this.a + o * o, l = o;
    var u, d, f, g, m;
    for (r = tu; r; --r)
      if (m = this.e * Math.sin(l), u = Math.sqrt(1 - m * m) * Math.tan(l), d = this.a * jt(this.e0, this.e1, this.e2, this.e3, l), f = this.e0 - 2 * this.e1 * Math.cos(2 * l) + 4 * this.e2 * Math.cos(4 * l) - 6 * this.e3 * Math.cos(6 * l), g = d / this.a, h = (o * (u * g + 1) - g - 0.5 * u * (g * g + a)) / (this.es * Math.sin(2 * l) * (g * g + a - 2 * o * g) / (4 * u) + (o - g) * (u * f - 2 / Math.sin(2 * l)) - f), l -= h, Math.abs(h) <= I) {
        e = l;
        break;
      }
    u = Math.sqrt(1 - this.es * Math.pow(Math.sin(e), 2)) * Math.tan(e), t = O(this.long0 + Math.asin(n * u / this.a) / Math.sin(e));
  }
  return i.x = t, i.y = e, i;
}
var XC = ["Polyconic", "poly"];
const YC = {
  init: UC,
  forward: WC,
  inverse: HC,
  names: XC
};
function jC() {
  this.A = [], this.A[1] = 0.6399175073, this.A[2] = -0.1358797613, this.A[3] = 0.063294409, this.A[4] = -0.02526853, this.A[5] = 0.0117879, this.A[6] = -55161e-7, this.A[7] = 26906e-7, this.A[8] = -1333e-6, this.A[9] = 67e-5, this.A[10] = -34e-5, this.B_re = [], this.B_im = [], this.B_re[1] = 0.7557853228, this.B_im[1] = 0, this.B_re[2] = 0.249204646, this.B_im[2] = 3371507e-9, this.B_re[3] = -1541739e-9, this.B_im[3] = 0.04105856, this.B_re[4] = -0.10162907, this.B_im[4] = 0.01727609, this.B_re[5] = -0.26623489, this.B_im[5] = -0.36249218, this.B_re[6] = -0.6870983, this.B_im[6] = -1.1651967, this.C_re = [], this.C_im = [], this.C_re[1] = 1.3231270439, this.C_im[1] = 0, this.C_re[2] = -0.577245789, this.C_im[2] = -7809598e-9, this.C_re[3] = 0.508307513, this.C_im[3] = -0.112208952, this.C_re[4] = -0.15094762, this.C_im[4] = 0.18200602, this.C_re[5] = 1.01418179, this.C_im[5] = 1.64497696, this.C_re[6] = 1.9660549, this.C_im[6] = 2.5127645, this.D = [], this.D[1] = 1.5627014243, this.D[2] = 0.5185406398, this.D[3] = -0.03333098, this.D[4] = -0.1052906, this.D[5] = -0.0368594, this.D[6] = 7317e-6, this.D[7] = 0.0122, this.D[8] = 394e-5, this.D[9] = -13e-4;
}
function KC(i) {
  var t, e = i.x, n = i.y, s = n - this.lat0, r = e - this.long0, o = s / ys * 1e-5, a = r, l = 1, h = 0;
  for (t = 1; t <= 10; t++)
    l = l * o, h = h + this.A[t] * l;
  var c = h, u = a, d = 1, f = 0, g, m, p = 0, _ = 0;
  for (t = 1; t <= 6; t++)
    g = d * c - f * u, m = f * c + d * u, d = g, f = m, p = p + this.B_re[t] * d - this.B_im[t] * f, _ = _ + this.B_im[t] * d + this.B_re[t] * f;
  return i.x = _ * this.a + this.x0, i.y = p * this.a + this.y0, i;
}
function qC(i) {
  var t, e = i.x, n = i.y, s = e - this.x0, r = n - this.y0, o = r / this.a, a = s / this.a, l = 1, h = 0, c, u, d = 0, f = 0;
  for (t = 1; t <= 6; t++)
    c = l * o - h * a, u = h * o + l * a, l = c, h = u, d = d + this.C_re[t] * l - this.C_im[t] * h, f = f + this.C_im[t] * l + this.C_re[t] * h;
  for (var g = 0; g < this.iterations; g++) {
    var m = d, p = f, _, y, v = o, x = a;
    for (t = 2; t <= 6; t++)
      _ = m * d - p * f, y = p * d + m * f, m = _, p = y, v = v + (t - 1) * (this.B_re[t] * m - this.B_im[t] * p), x = x + (t - 1) * (this.B_im[t] * m + this.B_re[t] * p);
    m = 1, p = 0;
    var C = this.B_re[1], w = this.B_im[1];
    for (t = 2; t <= 6; t++)
      _ = m * d - p * f, y = p * d + m * f, m = _, p = y, C = C + t * (this.B_re[t] * m - this.B_im[t] * p), w = w + t * (this.B_im[t] * m + this.B_re[t] * p);
    var S = C * C + w * w;
    d = (v * C + x * w) / S, f = (x * C - v * w) / S;
  }
  var b = d, A = f, G = 1, V = 0;
  for (t = 1; t <= 9; t++)
    G = G * b, V = V + this.D[t] * G;
  var T = this.lat0 + V * ys * 1e5, $ = this.long0 + A;
  return i.x = $, i.y = T, i;
}
var JC = ["New_Zealand_Map_Grid", "nzmg"];
const QC = {
  init: jC,
  forward: KC,
  inverse: qC,
  names: JC
};
function tM() {
}
function eM(i) {
  var t = i.x, e = i.y, n = O(t - this.long0), s = this.x0 + this.a * n, r = this.y0 + this.a * Math.log(Math.tan(Math.PI / 4 + e / 2.5)) * 1.25;
  return i.x = s, i.y = r, i;
}
function iM(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = O(this.long0 + i.x / this.a), e = 2.5 * (Math.atan(Math.exp(0.8 * i.y / this.a)) - Math.PI / 4);
  return i.x = t, i.y = e, i;
}
var nM = ["Miller_Cylindrical", "mill"];
const sM = {
  init: tM,
  forward: eM,
  inverse: iM,
  names: nM
};
var rM = 20;
function oM() {
  this.sphere ? (this.n = 1, this.m = 0, this.es = 0, this.C_y = Math.sqrt((this.m + 1) / this.n), this.C_x = this.C_y / (this.m + 1)) : this.en = Ff(this.es);
}
function aM(i) {
  var t, e, n = i.x, s = i.y;
  if (n = O(n - this.long0), this.sphere) {
    if (!this.m)
      s = this.n !== 1 ? Math.asin(this.n * Math.sin(s)) : s;
    else
      for (var r = this.n * Math.sin(s), o = rM; o; --o) {
        var a = (this.m * s + Math.sin(s) - r) / (this.m + Math.cos(s));
        if (s -= a, Math.abs(a) < I)
          break;
      }
    t = this.a * this.C_x * n * (this.m + Math.cos(s)), e = this.a * this.C_y * s;
  } else {
    var l = Math.sin(s), h = Math.cos(s);
    e = this.a * Po(s, l, h, this.en), t = this.a * n * h / Math.sqrt(1 - this.es * l * l);
  }
  return i.x = t, i.y = e, i;
}
function lM(i) {
  var t, e, n, s;
  return i.x -= this.x0, n = i.x / this.a, i.y -= this.y0, t = i.y / this.a, this.sphere ? (t /= this.C_y, n = n / (this.C_x * (this.m + Math.cos(t))), this.m ? t = Li((this.m * t + Math.sin(t)) / this.n) : this.n !== 1 && (t = Li(Math.sin(t) / this.n)), n = O(n + this.long0), t = Qn(t)) : (t = Df(i.y / this.a, this.es, this.en), s = Math.abs(t), s < R ? (s = Math.sin(t), e = this.long0 + i.x * Math.sqrt(1 - this.es * s * s) / (this.a * Math.cos(t)), n = O(e)) : s - I < R && (n = this.long0)), i.x = n, i.y = t, i;
}
var hM = ["Sinusoidal", "sinu"];
const cM = {
  init: oM,
  forward: aM,
  inverse: lM,
  names: hM
};
function uM() {
}
function dM(i) {
  for (var t = i.x, e = i.y, n = O(t - this.long0), s = e, r = Math.PI * Math.sin(e); ; ) {
    var o = -(s + Math.sin(s) - r) / (1 + Math.cos(s));
    if (s += o, Math.abs(o) < I)
      break;
  }
  s /= 2, Math.PI / 2 - Math.abs(e) < I && (n = 0);
  var a = 0.900316316158 * this.a * n * Math.cos(s) + this.x0, l = 1.4142135623731 * this.a * Math.sin(s) + this.y0;
  return i.x = a, i.y = l, i;
}
function fM(i) {
  var t, e;
  i.x -= this.x0, i.y -= this.y0, e = i.y / (1.4142135623731 * this.a), Math.abs(e) > 0.999999999999 && (e = 0.999999999999), t = Math.asin(e);
  var n = O(this.long0 + i.x / (0.900316316158 * this.a * Math.cos(t)));
  n < -Math.PI && (n = -Math.PI), n > Math.PI && (n = Math.PI), e = (2 * t + Math.sin(2 * t)) / Math.PI, Math.abs(e) > 1 && (e = 1);
  var s = Math.asin(e);
  return i.x = n, i.y = s, i;
}
var gM = ["Mollweide", "moll"];
const mM = {
  init: uM,
  forward: dM,
  inverse: fM,
  names: gM
};
function pM() {
  Math.abs(this.lat1 + this.lat2) < I || (this.lat2 = this.lat2 || this.lat1, this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = tr(this.es), this.e1 = er(this.es), this.e2 = ir(this.es), this.e3 = nr(this.es), this.sinphi = Math.sin(this.lat1), this.cosphi = Math.cos(this.lat1), this.ms1 = $e(this.e, this.sinphi, this.cosphi), this.ml1 = jt(this.e0, this.e1, this.e2, this.e3, this.lat1), Math.abs(this.lat1 - this.lat2) < I ? this.ns = this.sinphi : (this.sinphi = Math.sin(this.lat2), this.cosphi = Math.cos(this.lat2), this.ms2 = $e(this.e, this.sinphi, this.cosphi), this.ml2 = jt(this.e0, this.e1, this.e2, this.e3, this.lat2), this.ns = (this.ms1 - this.ms2) / (this.ml2 - this.ml1)), this.g = this.ml1 + this.ms1 / this.ns, this.ml0 = jt(this.e0, this.e1, this.e2, this.e3, this.lat0), this.rh = this.a * (this.g - this.ml0));
}
function _M(i) {
  var t = i.x, e = i.y, n;
  if (this.sphere)
    n = this.a * (this.g - e);
  else {
    var s = jt(this.e0, this.e1, this.e2, this.e3, e);
    n = this.a * (this.g - s);
  }
  var r = this.ns * O(t - this.long0), o = this.x0 + n * Math.sin(r), a = this.y0 + this.rh - n * Math.cos(r);
  return i.x = o, i.y = a, i;
}
function yM(i) {
  i.x -= this.x0, i.y = this.rh - i.y + this.y0;
  var t, e, n, s;
  this.ns >= 0 ? (e = Math.sqrt(i.x * i.x + i.y * i.y), t = 1) : (e = -Math.sqrt(i.x * i.x + i.y * i.y), t = -1);
  var r = 0;
  if (e !== 0 && (r = Math.atan2(t * i.x, t * i.y)), this.sphere)
    return s = O(this.long0 + r / this.ns), n = Qn(this.g - e / this.a), i.x = s, i.y = n, i;
  var o = this.g - e / this.a;
  return n = so(o, this.e0, this.e1, this.e2, this.e3), s = O(this.long0 + r / this.ns), i.x = s, i.y = n, i;
}
var vM = ["Equidistant_Conic", "eqdc"];
const xM = {
  init: pM,
  forward: _M,
  inverse: yM,
  names: vM
};
function CM() {
  this.R = this.a;
}
function MM(i) {
  var t = i.x, e = i.y, n = O(t - this.long0), s, r;
  Math.abs(e) <= I && (s = this.x0 + this.R * n, r = this.y0);
  var o = Li(2 * Math.abs(e / Math.PI));
  (Math.abs(n) <= I || Math.abs(Math.abs(e) - R) <= I) && (s = this.x0, e >= 0 ? r = this.y0 + Math.PI * this.R * Math.tan(0.5 * o) : r = this.y0 + Math.PI * this.R * -Math.tan(0.5 * o));
  var a = 0.5 * Math.abs(Math.PI / n - n / Math.PI), l = a * a, h = Math.sin(o), c = Math.cos(o), u = c / (h + c - 1), d = u * u, f = u * (2 / h - 1), g = f * f, m = Math.PI * this.R * (a * (u - g) + Math.sqrt(l * (u - g) * (u - g) - (g + l) * (d - g))) / (g + l);
  n < 0 && (m = -m), s = this.x0 + m;
  var p = l + u;
  return m = Math.PI * this.R * (f * p - a * Math.sqrt((g + l) * (l + 1) - p * p)) / (g + l), e >= 0 ? r = this.y0 + m : r = this.y0 - m, i.x = s, i.y = r, i;
}
function EM(i) {
  var t, e, n, s, r, o, a, l, h, c, u, d, f;
  return i.x -= this.x0, i.y -= this.y0, u = Math.PI * this.R, n = i.x / u, s = i.y / u, r = n * n + s * s, o = -Math.abs(s) * (1 + r), a = o - 2 * s * s + n * n, l = -2 * o + 1 + 2 * s * s + r * r, f = s * s / l + (2 * a * a * a / l / l / l - 9 * o * a / l / l) / 27, h = (o - a * a / 3 / l) / l, c = 2 * Math.sqrt(-h / 3), u = 3 * f / h / c, Math.abs(u) > 1 && (u >= 0 ? u = 1 : u = -1), d = Math.acos(u) / 3, i.y >= 0 ? e = (-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI : e = -(-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI, Math.abs(n) < I ? t = this.long0 : t = O(this.long0 + Math.PI * (r - 1 + Math.sqrt(1 + 2 * (n * n - s * s) + r * r)) / 2 / n), i.x = t, i.y = e, i;
}
var wM = ["Van_der_Grinten_I", "VanDerGrinten", "vandg"];
const SM = {
  init: CM,
  forward: MM,
  inverse: EM,
  names: wM
};
function RM() {
  this.sin_p12 = Math.sin(this.lat0), this.cos_p12 = Math.cos(this.lat0);
}
function bM(i) {
  var t = i.x, e = i.y, n = Math.sin(i.y), s = Math.cos(i.y), r = O(t - this.long0), o, a, l, h, c, u, d, f, g, m, p, _, y, v, x, C, w, S, b, A, G, V, T;
  return this.sphere ? Math.abs(this.sin_p12 - 1) <= I ? (i.x = this.x0 + this.a * (R - e) * Math.sin(r), i.y = this.y0 - this.a * (R - e) * Math.cos(r), i) : Math.abs(this.sin_p12 + 1) <= I ? (i.x = this.x0 + this.a * (R + e) * Math.sin(r), i.y = this.y0 + this.a * (R + e) * Math.cos(r), i) : (S = this.sin_p12 * n + this.cos_p12 * s * Math.cos(r), C = Math.acos(S), w = C ? C / Math.sin(C) : 1, i.x = this.x0 + this.a * w * s * Math.sin(r), i.y = this.y0 + this.a * w * (this.cos_p12 * n - this.sin_p12 * s * Math.cos(r)), i) : (o = tr(this.es), a = er(this.es), l = ir(this.es), h = nr(this.es), Math.abs(this.sin_p12 - 1) <= I ? (c = this.a * jt(o, a, l, h, R), u = this.a * jt(o, a, l, h, e), i.x = this.x0 + (c - u) * Math.sin(r), i.y = this.y0 - (c - u) * Math.cos(r), i) : Math.abs(this.sin_p12 + 1) <= I ? (c = this.a * jt(o, a, l, h, R), u = this.a * jt(o, a, l, h, e), i.x = this.x0 + (c + u) * Math.sin(r), i.y = this.y0 + (c + u) * Math.cos(r), i) : (d = n / s, f = Hn(this.a, this.e, this.sin_p12), g = Hn(this.a, this.e, n), m = Math.atan((1 - this.es) * d + this.es * f * this.sin_p12 / (g * s)), p = Math.atan2(Math.sin(r), this.cos_p12 * Math.tan(m) - this.sin_p12 * Math.cos(r)), p === 0 ? b = Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : Math.abs(Math.abs(p) - Math.PI) <= I ? b = -Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : b = Math.asin(Math.sin(r) * Math.cos(m) / Math.sin(p)), _ = this.e * this.sin_p12 / Math.sqrt(1 - this.es), y = this.e * this.cos_p12 * Math.cos(p) / Math.sqrt(1 - this.es), v = _ * y, x = y * y, A = b * b, G = A * b, V = G * b, T = V * b, C = f * b * (1 - A * x * (1 - x) / 6 + G / 8 * v * (1 - 2 * x) + V / 120 * (x * (4 - 7 * x) - 3 * _ * _ * (1 - 7 * x)) - T / 48 * v), i.x = this.x0 + C * Math.sin(p), i.y = this.y0 + C * Math.cos(p), i));
}
function LM(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p, _, y, v, x, C, w, S, b;
  return this.sphere ? (t = Math.sqrt(i.x * i.x + i.y * i.y), t > 2 * R * this.a ? void 0 : (e = t / this.a, n = Math.sin(e), s = Math.cos(e), r = this.long0, Math.abs(t) <= I ? o = this.lat0 : (o = Li(s * this.sin_p12 + i.y * n * this.cos_p12 / t), a = Math.abs(this.lat0) - R, Math.abs(a) <= I ? this.lat0 >= 0 ? r = O(this.long0 + Math.atan2(i.x, -i.y)) : r = O(this.long0 - Math.atan2(-i.x, i.y)) : r = O(this.long0 + Math.atan2(i.x * n, t * this.cos_p12 * s - i.y * this.sin_p12 * n))), i.x = r, i.y = o, i)) : (l = tr(this.es), h = er(this.es), c = ir(this.es), u = nr(this.es), Math.abs(this.sin_p12 - 1) <= I ? (d = this.a * jt(l, h, c, u, R), t = Math.sqrt(i.x * i.x + i.y * i.y), f = d - t, o = so(f / this.a, l, h, c, u), r = O(this.long0 + Math.atan2(i.x, -1 * i.y)), i.x = r, i.y = o, i) : Math.abs(this.sin_p12 + 1) <= I ? (d = this.a * jt(l, h, c, u, R), t = Math.sqrt(i.x * i.x + i.y * i.y), f = t - d, o = so(f / this.a, l, h, c, u), r = O(this.long0 + Math.atan2(i.x, i.y)), i.x = r, i.y = o, i) : (t = Math.sqrt(i.x * i.x + i.y * i.y), p = Math.atan2(i.x, i.y), g = Hn(this.a, this.e, this.sin_p12), _ = Math.cos(p), y = this.e * this.cos_p12 * _, v = -y * y / (1 - this.es), x = 3 * this.es * (1 - v) * this.sin_p12 * this.cos_p12 * _ / (1 - this.es), C = t / g, w = C - v * (1 + v) * Math.pow(C, 3) / 6 - x * (1 + 3 * v) * Math.pow(C, 4) / 24, S = 1 - v * w * w / 2 - C * w * w * w / 6, m = Math.asin(this.sin_p12 * Math.cos(w) + this.cos_p12 * Math.sin(w) * _), r = O(this.long0 + Math.asin(Math.sin(p) * Math.sin(w) / Math.cos(m))), b = Math.sin(m), o = Math.atan2((b - this.es * S * this.sin_p12) * Math.tan(m), b * (1 - this.es)), i.x = r, i.y = o, i));
}
var TM = ["Azimuthal_Equidistant", "aeqd"];
const IM = {
  init: RM,
  forward: bM,
  inverse: LM,
  names: TM
};
function PM() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0);
}
function AM(i) {
  var t, e, n, s, r, o, a, l, h = i.x, c = i.y;
  return n = O(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(n), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, (o > 0 || Math.abs(o) <= I) && (a = this.a * r * e * Math.sin(n), l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s)), i.x = a, i.y = l, i;
}
function OM(i) {
  var t, e, n, s, r, o, a;
  return i.x -= this.x0, i.y -= this.y0, t = Math.sqrt(i.x * i.x + i.y * i.y), e = Li(t / this.a), n = Math.sin(e), s = Math.cos(e), o = this.long0, Math.abs(t) <= I ? (a = this.lat0, i.x = o, i.y = a, i) : (a = Li(s * this.sin_p14 + i.y * n * this.cos_p14 / t), r = Math.abs(this.lat0) - R, Math.abs(r) <= I ? (this.lat0 >= 0 ? o = O(this.long0 + Math.atan2(i.x, -i.y)) : o = O(this.long0 - Math.atan2(-i.x, i.y)), i.x = o, i.y = a, i) : (o = O(this.long0 + Math.atan2(i.x * n, t * this.cos_p14 * s - i.y * this.sin_p14 * n)), i.x = o, i.y = a, i));
}
var NM = ["ortho"];
const FM = {
  init: PM,
  forward: AM,
  inverse: OM,
  names: NM
};
var xt = {
  FRONT: 1,
  RIGHT: 2,
  BACK: 3,
  LEFT: 4,
  TOP: 5,
  BOTTOM: 6
}, ct = {
  AREA_0: 1,
  AREA_1: 2,
  AREA_2: 3,
  AREA_3: 4
};
function DM() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Quadrilateralized Spherical Cube", this.lat0 >= R - ht / 2 ? this.face = xt.TOP : this.lat0 <= -(R - ht / 2) ? this.face = xt.BOTTOM : Math.abs(this.long0) <= ht ? this.face = xt.FRONT : Math.abs(this.long0) <= R + ht ? this.face = this.long0 > 0 ? xt.RIGHT : xt.LEFT : this.face = xt.BACK, this.es !== 0 && (this.one_minus_f = 1 - (this.a - this.b) / this.a, this.one_minus_f_squared = this.one_minus_f * this.one_minus_f);
}
function kM(i) {
  var t = { x: 0, y: 0 }, e, n, s, r, o, a, l = { value: 0 };
  if (i.x -= this.long0, this.es !== 0 ? e = Math.atan(this.one_minus_f_squared * Math.tan(i.y)) : e = i.y, n = i.x, this.face === xt.TOP)
    r = R - e, n >= ht && n <= R + ht ? (l.value = ct.AREA_0, s = n - R) : n > R + ht || n <= -(R + ht) ? (l.value = ct.AREA_1, s = n > 0 ? n - Rt : n + Rt) : n > -(R + ht) && n <= -ht ? (l.value = ct.AREA_2, s = n + R) : (l.value = ct.AREA_3, s = n);
  else if (this.face === xt.BOTTOM)
    r = R + e, n >= ht && n <= R + ht ? (l.value = ct.AREA_0, s = -n + R) : n < ht && n >= -ht ? (l.value = ct.AREA_1, s = -n) : n < -ht && n >= -(R + ht) ? (l.value = ct.AREA_2, s = -n - R) : (l.value = ct.AREA_3, s = n > 0 ? -n + Rt : -n - Rt);
  else {
    var h, c, u, d, f, g, m;
    this.face === xt.RIGHT ? n = Nn(n, +R) : this.face === xt.BACK ? n = Nn(n, +Rt) : this.face === xt.LEFT && (n = Nn(n, -R)), d = Math.sin(e), f = Math.cos(e), g = Math.sin(n), m = Math.cos(n), h = f * m, c = f * g, u = d, this.face === xt.FRONT ? (r = Math.acos(h), s = Lr(r, u, c, l)) : this.face === xt.RIGHT ? (r = Math.acos(c), s = Lr(r, u, -h, l)) : this.face === xt.BACK ? (r = Math.acos(-h), s = Lr(r, u, -c, l)) : this.face === xt.LEFT ? (r = Math.acos(-c), s = Lr(r, u, h, l)) : (r = s = 0, l.value = ct.AREA_0);
  }
  return a = Math.atan(12 / Rt * (s + Math.acos(Math.sin(s) * Math.cos(ht)) - R)), o = Math.sqrt((1 - Math.cos(r)) / (Math.cos(a) * Math.cos(a)) / (1 - Math.cos(Math.atan(1 / Math.cos(s))))), l.value === ct.AREA_1 ? a += R : l.value === ct.AREA_2 ? a += Rt : l.value === ct.AREA_3 && (a += 1.5 * Rt), t.x = o * Math.cos(a), t.y = o * Math.sin(a), t.x = t.x * this.a + this.x0, t.y = t.y * this.a + this.y0, i.x = t.x, i.y = t.y, i;
}
function GM(i) {
  var t = { lam: 0, phi: 0 }, e, n, s, r, o, a, l, h, c, u = { value: 0 };
  if (i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, n = Math.atan(Math.sqrt(i.x * i.x + i.y * i.y)), e = Math.atan2(i.y, i.x), i.x >= 0 && i.x >= Math.abs(i.y) ? u.value = ct.AREA_0 : i.y >= 0 && i.y >= Math.abs(i.x) ? (u.value = ct.AREA_1, e -= R) : i.x < 0 && -i.x >= Math.abs(i.y) ? (u.value = ct.AREA_2, e = e < 0 ? e + Rt : e - Rt) : (u.value = ct.AREA_3, e += R), c = Rt / 12 * Math.tan(e), o = Math.sin(c) / (Math.cos(c) - 1 / Math.sqrt(2)), a = Math.atan(o), s = Math.cos(e), r = Math.tan(n), l = 1 - s * s * r * r * (1 - Math.cos(Math.atan(1 / Math.cos(a)))), l < -1 ? l = -1 : l > 1 && (l = 1), this.face === xt.TOP)
    h = Math.acos(l), t.phi = R - h, u.value === ct.AREA_0 ? t.lam = a + R : u.value === ct.AREA_1 ? t.lam = a < 0 ? a + Rt : a - Rt : u.value === ct.AREA_2 ? t.lam = a - R : t.lam = a;
  else if (this.face === xt.BOTTOM)
    h = Math.acos(l), t.phi = h - R, u.value === ct.AREA_0 ? t.lam = -a + R : u.value === ct.AREA_1 ? t.lam = -a : u.value === ct.AREA_2 ? t.lam = -a - R : t.lam = a < 0 ? -a - Rt : -a + Rt;
  else {
    var d, f, g;
    d = l, c = d * d, c >= 1 ? g = 0 : g = Math.sqrt(1 - c) * Math.sin(a), c += g * g, c >= 1 ? f = 0 : f = Math.sqrt(1 - c), u.value === ct.AREA_1 ? (c = f, f = -g, g = c) : u.value === ct.AREA_2 ? (f = -f, g = -g) : u.value === ct.AREA_3 && (c = f, f = g, g = -c), this.face === xt.RIGHT ? (c = d, d = -f, f = c) : this.face === xt.BACK ? (d = -d, f = -f) : this.face === xt.LEFT && (c = d, d = f, f = -c), t.phi = Math.acos(-g) - R, t.lam = Math.atan2(f, d), this.face === xt.RIGHT ? t.lam = Nn(t.lam, -R) : this.face === xt.BACK ? t.lam = Nn(t.lam, -Rt) : this.face === xt.LEFT && (t.lam = Nn(t.lam, +R));
  }
  if (this.es !== 0) {
    var m, p, _;
    m = t.phi < 0 ? 1 : 0, p = Math.tan(t.phi), _ = this.b / Math.sqrt(p * p + this.one_minus_f_squared), t.phi = Math.atan(Math.sqrt(this.a * this.a - _ * _) / (this.one_minus_f * _)), m && (t.phi = -t.phi);
  }
  return t.lam += this.long0, i.x = t.lam, i.y = t.phi, i;
}
function Lr(i, t, e, n) {
  var s;
  return i < I ? (n.value = ct.AREA_0, s = 0) : (s = Math.atan2(t, e), Math.abs(s) <= ht ? n.value = ct.AREA_0 : s > ht && s <= R + ht ? (n.value = ct.AREA_1, s -= R) : s > R + ht || s <= -(R + ht) ? (n.value = ct.AREA_2, s = s >= 0 ? s - Rt : s + Rt) : (n.value = ct.AREA_3, s += R)), s;
}
function Nn(i, t) {
  var e = i + t;
  return e < -Rt ? e += Ds : e > +Rt && (e -= Ds), e;
}
var $M = ["Quadrilateralized Spherical Cube", "Quadrilateralized_Spherical_Cube", "qsc"];
const BM = {
  init: DM,
  forward: kM,
  inverse: GM,
  names: $M
};
var Ua = [
  [1, 22199e-21, -715515e-10, 31103e-10],
  [0.9986, -482243e-9, -24897e-9, -13309e-10],
  [0.9954, -83103e-8, -448605e-10, -986701e-12],
  [0.99, -135364e-8, -59661e-9, 36777e-10],
  [0.9822, -167442e-8, -449547e-11, -572411e-11],
  [0.973, -214868e-8, -903571e-10, 18736e-12],
  [0.96, -305085e-8, -900761e-10, 164917e-11],
  [0.9427, -382792e-8, -653386e-10, -26154e-10],
  [0.9216, -467746e-8, -10457e-8, 481243e-11],
  [0.8962, -536223e-8, -323831e-10, -543432e-11],
  [0.8679, -609363e-8, -113898e-9, 332484e-11],
  [0.835, -698325e-8, -640253e-10, 934959e-12],
  [0.7986, -755338e-8, -500009e-10, 935324e-12],
  [0.7597, -798324e-8, -35971e-9, -227626e-11],
  [0.7186, -851367e-8, -701149e-10, -86303e-10],
  [0.6732, -986209e-8, -199569e-9, 191974e-10],
  [0.6213, -0.010418, 883923e-10, 624051e-11],
  [0.5722, -906601e-8, 182e-6, 624051e-11],
  [0.5322, -677797e-8, 275608e-9, 624051e-11]
], fs = [
  [-520417e-23, 0.0124, 121431e-23, -845284e-16],
  [0.062, 0.0124, -126793e-14, 422642e-15],
  [0.124, 0.0124, 507171e-14, -160604e-14],
  [0.186, 0.0123999, -190189e-13, 600152e-14],
  [0.248, 0.0124002, 710039e-13, -224e-10],
  [0.31, 0.0123992, -264997e-12, 835986e-13],
  [0.372, 0.0124029, 988983e-12, -311994e-12],
  [0.434, 0.0123893, -369093e-11, -435621e-12],
  [0.4958, 0.0123198, -102252e-10, -345523e-12],
  [0.5571, 0.0121916, -154081e-10, -582288e-12],
  [0.6176, 0.0119938, -241424e-10, -525327e-12],
  [0.6769, 0.011713, -320223e-10, -516405e-12],
  [0.7346, 0.0113541, -397684e-10, -609052e-12],
  [0.7903, 0.0109107, -489042e-10, -104739e-11],
  [0.8435, 0.0103431, -64615e-9, -140374e-14],
  [0.8936, 969686e-8, -64636e-9, -8547e-9],
  [0.9394, 840947e-8, -192841e-9, -42106e-10],
  [0.9761, 616527e-8, -256e-6, -42106e-10],
  [1, 328947e-8, -319159e-9, -42106e-10]
], $f = 0.8487, Bf = 1.3523, zf = Ne / 5, zM = 1 / zf, In = 18, ro = function(i, t) {
  return i[0] + t * (i[1] + t * (i[2] + t * i[3]));
}, ZM = function(i, t) {
  return i[1] + t * (2 * i[2] + t * 3 * i[3]);
};
function VM(i, t, e, n) {
  for (var s = t; n; --n) {
    var r = i(s);
    if (s -= r, Math.abs(r) < e)
      break;
  }
  return s;
}
function UM() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.long0 = this.long0 || 0, this.es = 0, this.title = this.title || "Robinson";
}
function WM(i) {
  var t = O(i.x - this.long0), e = Math.abs(i.y), n = Math.floor(e * zf);
  n < 0 ? n = 0 : n >= In && (n = In - 1), e = Ne * (e - zM * n);
  var s = {
    x: ro(Ua[n], e) * t,
    y: ro(fs[n], e)
  };
  return i.y < 0 && (s.y = -s.y), s.x = s.x * this.a * $f + this.x0, s.y = s.y * this.a * Bf + this.y0, s;
}
function HM(i) {
  var t = {
    x: (i.x - this.x0) / (this.a * $f),
    y: Math.abs(i.y - this.y0) / (this.a * Bf)
  };
  if (t.y >= 1)
    t.x /= Ua[In][0], t.y = i.y < 0 ? -R : R;
  else {
    var e = Math.floor(t.y * In);
    for (e < 0 ? e = 0 : e >= In && (e = In - 1); ; )
      if (fs[e][0] > t.y)
        --e;
      else if (fs[e + 1][0] <= t.y)
        ++e;
      else
        break;
    var n = fs[e], s = 5 * (t.y - n[0]) / (fs[e + 1][0] - n[0]);
    s = VM(function(r) {
      return (ro(n, r) - t.y) / ZM(n, r);
    }, s, I, 100), t.x /= ro(Ua[e], s), t.y = (5 * e + s) * Bt, i.y < 0 && (t.y = -t.y);
  }
  return t.x = O(t.x + this.long0), t;
}
var XM = ["Robinson", "robin"];
const YM = {
  init: UM,
  forward: WM,
  inverse: HM,
  names: XM
};
function jM() {
  this.name = "geocent";
}
function KM(i) {
  var t = Rf(i, this.es, this.a);
  return t;
}
function qM(i) {
  var t = bf(i, this.es, this.a, this.b);
  return t;
}
var JM = ["Geocentric", "geocentric", "geocent", "Geocent"];
const QM = {
  init: jM,
  forward: KM,
  inverse: qM,
  names: JM
};
var Vt = {
  N_POLE: 0,
  S_POLE: 1,
  EQUIT: 2,
  OBLIQ: 3
}, ls = {
  h: { def: 1e5, num: !0 },
  azi: { def: 0, num: !0, degrees: !0 },
  tilt: { def: 0, num: !0, degrees: !0 },
  long0: { def: 0, num: !0 },
  lat0: { def: 0, num: !0 }
};
function tE() {
  if (Object.keys(ls).forEach(function(e) {
    if (typeof this[e] > "u")
      this[e] = ls[e].def;
    else {
      if (ls[e].num && isNaN(this[e]))
        throw new Error("Invalid parameter value, must be numeric " + e + " = " + this[e]);
      ls[e].num && (this[e] = parseFloat(this[e]));
    }
    ls[e].degrees && (this[e] = this[e] * Bt);
  }.bind(this)), Math.abs(Math.abs(this.lat0) - R) < I ? this.mode = this.lat0 < 0 ? Vt.S_POLE : Vt.N_POLE : Math.abs(this.lat0) < I ? this.mode = Vt.EQUIT : (this.mode = Vt.OBLIQ, this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0)), this.pn1 = this.h / this.a, this.pn1 <= 0 || this.pn1 > 1e10)
    throw new Error("Invalid height");
  this.p = 1 + this.pn1, this.rp = 1 / this.p, this.h1 = 1 / this.pn1, this.pfact = (this.p + 1) * this.h1, this.es = 0;
  var i = this.tilt, t = this.azi;
  this.cg = Math.cos(t), this.sg = Math.sin(t), this.cw = Math.cos(i), this.sw = Math.sin(i);
}
function eE(i) {
  i.x -= this.long0;
  var t = Math.sin(i.y), e = Math.cos(i.y), n = Math.cos(i.x), s, r;
  switch (this.mode) {
    case Vt.OBLIQ:
      r = this.sinph0 * t + this.cosph0 * e * n;
      break;
    case Vt.EQUIT:
      r = e * n;
      break;
    case Vt.S_POLE:
      r = -t;
      break;
    case Vt.N_POLE:
      r = t;
      break;
  }
  switch (r = this.pn1 / (this.p - r), s = r * e * Math.sin(i.x), this.mode) {
    case Vt.OBLIQ:
      r *= this.cosph0 * t - this.sinph0 * e * n;
      break;
    case Vt.EQUIT:
      r *= t;
      break;
    case Vt.N_POLE:
      r *= -(e * n);
      break;
    case Vt.S_POLE:
      r *= e * n;
      break;
  }
  var o, a;
  return o = r * this.cg + s * this.sg, a = 1 / (o * this.sw * this.h1 + this.cw), s = (s * this.cg - r * this.sg) * this.cw * a, r = o * a, i.x = s * this.a, i.y = r * this.a, i;
}
function iE(i) {
  i.x /= this.a, i.y /= this.a;
  var t = { x: i.x, y: i.y }, e, n, s;
  s = 1 / (this.pn1 - i.y * this.sw), e = this.pn1 * i.x * s, n = this.pn1 * i.y * this.cw * s, i.x = e * this.cg + n * this.sg, i.y = n * this.cg - e * this.sg;
  var r = Se(i.x, i.y);
  if (Math.abs(r) < I)
    t.x = 0, t.y = i.y;
  else {
    var o, a;
    switch (a = 1 - r * r * this.pfact, a = (this.p - Math.sqrt(a)) / (this.pn1 / r + r / this.pn1), o = Math.sqrt(1 - a * a), this.mode) {
      case Vt.OBLIQ:
        t.y = Math.asin(o * this.sinph0 + i.y * a * this.cosph0 / r), i.y = (o - this.sinph0 * Math.sin(t.y)) * r, i.x *= a * this.cosph0;
        break;
      case Vt.EQUIT:
        t.y = Math.asin(i.y * a / r), i.y = o * r, i.x *= a;
        break;
      case Vt.N_POLE:
        t.y = Math.asin(o), i.y = -i.y;
        break;
      case Vt.S_POLE:
        t.y = -Math.asin(o);
        break;
    }
    t.x = Math.atan2(i.x, i.y);
  }
  return i.x = t.x + this.long0, i.y = t.y, i;
}
var nE = ["Tilted_Perspective", "tpers"];
const sE = {
  init: tE,
  forward: eE,
  inverse: iE,
  names: nE
};
function rE() {
  if (this.flip_axis = this.sweep === "x" ? 1 : 0, this.h = Number(this.h), this.radius_g_1 = this.h / this.a, this.radius_g_1 <= 0 || this.radius_g_1 > 1e10)
    throw new Error();
  if (this.radius_g = 1 + this.radius_g_1, this.C = this.radius_g * this.radius_g - 1, this.es !== 0) {
    var i = 1 - this.es, t = 1 / i;
    this.radius_p = Math.sqrt(i), this.radius_p2 = i, this.radius_p_inv2 = t, this.shape = "ellipse";
  } else
    this.radius_p = 1, this.radius_p2 = 1, this.radius_p_inv2 = 1, this.shape = "sphere";
  this.title || (this.title = "Geostationary Satellite View");
}
function oE(i) {
  var t = i.x, e = i.y, n, s, r, o;
  if (t = t - this.long0, this.shape === "ellipse") {
    e = Math.atan(this.radius_p2 * Math.tan(e));
    var a = this.radius_p / Se(this.radius_p * Math.cos(e), Math.sin(e));
    if (s = a * Math.cos(t) * Math.cos(e), r = a * Math.sin(t) * Math.cos(e), o = a * Math.sin(e), (this.radius_g - s) * s - r * r - o * o * this.radius_p_inv2 < 0)
      return i.x = Number.NaN, i.y = Number.NaN, i;
    n = this.radius_g - s, this.flip_axis ? (i.x = this.radius_g_1 * Math.atan(r / Se(o, n)), i.y = this.radius_g_1 * Math.atan(o / n)) : (i.x = this.radius_g_1 * Math.atan(r / n), i.y = this.radius_g_1 * Math.atan(o / Se(r, n)));
  } else
    this.shape === "sphere" && (n = Math.cos(e), s = Math.cos(t) * n, r = Math.sin(t) * n, o = Math.sin(e), n = this.radius_g - s, this.flip_axis ? (i.x = this.radius_g_1 * Math.atan(r / Se(o, n)), i.y = this.radius_g_1 * Math.atan(o / n)) : (i.x = this.radius_g_1 * Math.atan(r / n), i.y = this.radius_g_1 * Math.atan(o / Se(r, n))));
  return i.x = i.x * this.a, i.y = i.y * this.a, i;
}
function aE(i) {
  var t = -1, e = 0, n = 0, s, r, o, a;
  if (i.x = i.x / this.a, i.y = i.y / this.a, this.shape === "ellipse") {
    this.flip_axis ? (n = Math.tan(i.y / this.radius_g_1), e = Math.tan(i.x / this.radius_g_1) * Se(1, n)) : (e = Math.tan(i.x / this.radius_g_1), n = Math.tan(i.y / this.radius_g_1) * Se(1, e));
    var l = n / this.radius_p;
    if (s = e * e + l * l + t * t, r = 2 * this.radius_g * t, o = r * r - 4 * s * this.C, o < 0)
      return i.x = Number.NaN, i.y = Number.NaN, i;
    a = (-r - Math.sqrt(o)) / (2 * s), t = this.radius_g + a * t, e *= a, n *= a, i.x = Math.atan2(e, t), i.y = Math.atan(n * Math.cos(i.x) / t), i.y = Math.atan(this.radius_p_inv2 * Math.tan(i.y));
  } else if (this.shape === "sphere") {
    if (this.flip_axis ? (n = Math.tan(i.y / this.radius_g_1), e = Math.tan(i.x / this.radius_g_1) * Math.sqrt(1 + n * n)) : (e = Math.tan(i.x / this.radius_g_1), n = Math.tan(i.y / this.radius_g_1) * Math.sqrt(1 + e * e)), s = e * e + n * n + t * t, r = 2 * this.radius_g * t, o = r * r - 4 * s * this.C, o < 0)
      return i.x = Number.NaN, i.y = Number.NaN, i;
    a = (-r - Math.sqrt(o)) / (2 * s), t = this.radius_g + a * t, e *= a, n *= a, i.x = Math.atan2(e, t), i.y = Math.atan(n * Math.cos(i.x) / t);
  }
  return i.x = i.x + this.long0, i;
}
var lE = ["Geostationary Satellite View", "Geostationary_Satellite", "geos"];
const hE = {
  init: rE,
  forward: oE,
  inverse: aE,
  names: lE
};
function cE(i) {
  i.Proj.projections.add(Ar), i.Proj.projections.add(Or), i.Proj.projections.add(p3), i.Proj.projections.add(R3), i.Proj.projections.add(A3), i.Proj.projections.add(k3), i.Proj.projections.add(V3), i.Proj.projections.add(Y3), i.Proj.projections.add(Q3), i.Proj.projections.add(sC), i.Proj.projections.add(CC), i.Proj.projections.add(bC), i.Proj.projections.add(AC), i.Proj.projections.add(GC), i.Proj.projections.add(VC), i.Proj.projections.add(YC), i.Proj.projections.add(QC), i.Proj.projections.add(sM), i.Proj.projections.add(cM), i.Proj.projections.add(mM), i.Proj.projections.add(xM), i.Proj.projections.add(SM), i.Proj.projections.add(IM), i.Proj.projections.add(FM), i.Proj.projections.add(BM), i.Proj.projections.add(YM), i.Proj.projections.add(QM), i.Proj.projections.add(sE), i.Proj.projections.add(hE);
}
se.defaultDatum = "WGS84";
se.Proj = De;
se.WGS84 = new se.Proj("WGS84");
se.Point = Wn;
se.toPoint = Lf;
se.defs = Xt;
se.nadgrid = yx;
se.transform = no;
se.mgrs = Nx;
se.version = "__VERSION__";
cE(se);
function uE(i) {
  const t = Object.keys(i.defs), e = t.length;
  let n, s;
  for (n = 0; n < e; ++n) {
    const r = t[n];
    if (!J(r)) {
      const o = i.defs(r);
      let a = o.units;
      !a && o.projName === "longlat" && (a = "degrees"), Hu(
        new nl({
          code: r,
          axisOrientation: o.axis,
          metersPerUnit: o.to_meter,
          units: a
        })
      );
    }
  }
  for (n = 0; n < e; ++n) {
    const r = t[n], o = J(r);
    for (s = 0; s < e; ++s) {
      const a = t[s], l = J(a);
      if (!Vu(r, a))
        if (i.defs[r] === i.defs[a])
          _a([o, l]);
        else {
          const h = i(r, a);
          Rg(
            o,
            l,
            bh(o, l, h.forward),
            bh(l, o, h.inverse)
          );
        }
    }
  }
}
class eu {
  constructor(t, e, n) {
    this.control = new nf(), this.store = M(), this.states = n, this.renderUtils = e;
    const s = this.store.getMap();
    this.vectorSource = new Kn(), this.setupMapForCreation(s, this.vectorSource), this.states.readonly || (window.addEventListener("authorize-created", (r) => {
      this.createElement(this.vectorSource, r);
    }), window.addEventListener("refused-created", () => {
      this.store.removeLastSelectedFeature();
    }), window.addEventListener("remove-created-icon", () => {
      this.deleteElement(this.vectorSource);
    }), window.addEventListener("recenter-selected-element", () => {
      var a;
      const r = this.store.getCurrentItemId(), o = (a = this.store.getSelectedFeature(r)) == null ? void 0 : a.get("geom").getCoordinates();
      s.getView().setCenter(o);
    }), this.addLongClickEvent(t, s), s.on("click", (r) => {
      s.forEachFeatureAtPixel(r.pixel, (o) => {
        var a, l;
        o && ((a = o.getGeometry()) == null ? void 0 : a.getType()) === "Point" && o.get("id") && (this.store.unselectFeatures(), this.store.setCurrentItemId(o.get("id")), (l = this.store.getSelectedFeature(o.get("id"))) == null || l.set("isSelected", !0), it.sendEvent("open-select-create-box", o.get("geom").getCoordinates()), this.control.show());
      });
    }));
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementCreateTargetMode(this.vectorSource, t);
  }
  setupMapForCreation(t, e) {
    this.renderUtils.setupAndLoadLayer(e), this.states.readonly || (this.control.disable(), t.addControl(this.control));
  }
  createElement(t, e) {
    if (this.store.getSelectedFeatures().length > this.store.getMaxElement()) {
      this.store.removeSelectedFeature(e.detail);
      return;
    }
    this.store.setCurrentItemId(e.detail);
    const s = this.store.getSelectedFeature(this.store.getCurrentItemId());
    s && (this.store.getMaxElement() === 1 ? (t.getFeatures().forEach((r) => t.removeFeature(r)), this.control.hide()) : t.getFeatures().forEach((r) => {
      r.get("id") !== this.store.getCurrentItemId() && r.set("isSelected", void 0);
    }), t.addFeature(s), this.control.show(), it.sendEvent("open-select-create-box", s.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select")), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
  }
  deleteElement(t) {
    const e = this.store.getSelectedFeature(this.store.getCurrentItemId());
    e && (t.removeFeature(e), this.control.hide(), this.store.removeSelectedFeature(this.store.getCurrentItemId()), it.sendEvent("rule-validation", void 0), sf.setCustomStyleWithouInfoBox()), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
  }
  addLongClickEvent(t, e) {
    let s, r = [0, 0];
    t.addEventListener("mousedown", (o) => {
      r = [o.pageX, o.pageY], this.clearCreationTimeout(s), s = setTimeout(() => {
        this.requestElementCreation(o.pageX, o.pageY, e, t);
      }, 800);
    }), t.addEventListener("mousemove", (o) => {
      this.moveAnalyzer(r, o.pageX, o.pageY) && this.clearCreationTimeout(s);
    }), t.addEventListener("mouseup", () => {
      this.clearCreationTimeout(s);
    }), t.addEventListener("touchstart", (o) => {
      r = [o.changedTouches[0].pageX, o.changedTouches[0].pageY], this.clearCreationTimeout(s), s = setTimeout(() => {
        this.requestElementCreation(o.changedTouches[0].pageX, o.changedTouches[0].pageY, e, t);
      }, 800);
    }), t.addEventListener("touchmove", (o) => {
      this.moveAnalyzer(r, o.changedTouches[0].pageX, o.changedTouches[0].pageY) && this.clearCreationTimeout(s);
    }), t.addEventListener("touchend", () => {
      this.clearCreationTimeout(s);
    });
  }
  requestElementCreation(t, e, n, s) {
    if (!this.states.readonly) {
      const r = s.getBoundingClientRect(), o = n.getCoordinateFromPixel([t - r.left - document.documentElement.scrollLeft, e - r.top - document.documentElement.scrollTop]), a = new si(o), l = new on({
        geom: a,
        id: Number(`${Math.round(o[0])}${Math.round(o[1])}`),
        isSelected: !0
      });
      l.setGeometryName("geom"), this.store.getMaxElement() === 1 && this.store.removeSelectedFeature(this.store.getCurrentItemId()), (this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement()) && (this.store.addSelectedFeature(l, l.get("id"), "create"), it.sendEvent("icon-created", l.get("id")));
    }
  }
  moveAnalyzer(t, e, n) {
    return Math.abs(e - t[0]) > 10 || Math.abs(n - t[1]) > 10;
  }
  clearCreationTimeout(t) {
    clearTimeout(t), t = void 0;
  }
}
const Zf = `@media only screen and (min-width: 351px) and (max-width: 995px){.search-container{left:calc((100% - 334px)/2);width:100%;max-width:332px}}@media only screen and (max-width: 350px){.search-container{left:10px;width:calc(100% - 20px);max-width:332px}}@media only screen and (min-width: 996px){.search-container{left:calc((100% - (var(--search-width) + 30px)) / 2);width:calc(var(--search-width) + 30px)}}.search-container{position:absolute;top:var(--top-distance);z-index:0}.search-input-container{border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color);margin-bottom:1px}.search-input{width:calc(100% - 13px);height:44px;border:none;outline:none;padding:0 0 0 11px;font-size:14px;background-color:var(--information-box-background-color);color:var(--suggestion-box-text-color);font-family:sans-serif}.search-svg-container{width:29px;height:44px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-radius:var(--icon-border-radius)}ul>:first-child{border-top-right-radius:var(--icon-border-radius);border-top-left-radius:var(--icon-border-radius)}li{height:40px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--suggestion-box-text-color);font-family:sans-serif;cursor:pointer}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var dE = Object.defineProperty, fE = Object.getOwnPropertyDescriptor, Pi = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? fE(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && dE(t, e, s), s;
};
let $s = class extends Pt {
  constructor() {
    super(), this._results = [], M().getMap().addEventListener("click", () => {
      this._results = [];
    });
  }
  updated(i) {
    if (i.has("locations"))
      if (this.locations && this.locations.results && this.locations.results.length > 0) {
        const t = this.locations.results.length > 5 ? 5 : this.locations.results.length;
        this._results = [];
        for (let e = 0; e < t; e++) {
          let n = "";
          if (this.locations.results[e].attrs.origin == "address") {
            if (this.locations.results[e].attrs.label.trim().startsWith("<b>"))
              continue;
            n = this.locations.results[e].attrs.label.replace("<b>", " - ").replace("</b>", "");
          } else
            this.locations.results[e].attrs.origin == "parcel" && (n = "Parcelle: " + this.locations.results[e].attrs.label.replace("<b>", "").replace("</b>", "").split("(CH")[0]);
          this._results.push({ coordinate: [this.locations.results[e].attrs.lon, this.locations.results[e].attrs.lat], address: n });
        }
      } else
        this._results = [];
  }
  selectAddress(i, t) {
    M().getMap().getView().setCenter(bg([i[0], i[1]], "EPSG:2056")), this._results = [], it.sendEvent("address_selected", t);
  }
  render() {
    return Lt`
                <ul>
                  ${this._results.map(
      (i) => Lt`<li tabindex="0" @click=${() => this.selectAddress(i.coordinate, i.address)}>${i.address}</li>`
    )}
                </ul>
              `;
  }
};
$s.styles = [yt(Zf)];
Pi([
  Ti({ type: Object })
], $s.prototype, "locations", 2);
Pi([
  Dt()
], $s.prototype, "_results", 2);
$s = Pi([
  qt("location-list")
], $s);
let en = class extends Pt {
  constructor() {
    super(), this.results = {}, this._hasSearch = !1, this._hasSelected = !1, window.addEventListener("address_selected", (i) => {
      this.inputElement.value = i.detail, this._hasSearch = !1, this._hasSelected = !0;
    });
  }
  firstUpdated() {
    this.inputElement.oninput = () => {
      if (this.inputElement.value.length > 1) {
        this._hasSearch = !0;
        const i = M().getOptions();
        let t = `${i.search.requestWithoutCustomValue}&searchText=${this.inputElement.value}`;
        i.search.bboxRestiction !== "" && (t += `&bbox=${i.search.bboxRestiction}`), fetch(t).then((e) => e.json()).then((e) => {
          this.results = e;
        });
      } else
        this._hasSearch = !1, this.results = {};
    };
  }
  clear() {
    this.inputElement.value = "", this.results = {}, this._hasSearch = !1, this._hasSelected = !1;
  }
  render() {
    return Lt`<div class="search-container">
                    <div class="search-input-container">
                        <input id="search" type="text" class="search-input">
                        <div class="search-svg-container">
                        ${Wd(
      this._hasSearch || this._hasSelected ? Lt`<div class="cross-div" @click="${this.clear}">
                                        ${Le(rt.cross)}
                                    </div>` : Lt`${Le(rt.search)}`
    )}
                        </div>
                    </div>
                    <location-list locations='${JSON.stringify(this.results)}'/>
                </div>`;
  }
};
en.styles = [yt(Zf)];
Pi([
  pu("#search")
], en.prototype, "inputElement", 2);
Pi([
  Dt()
], en.prototype, "results", 2);
Pi([
  Dt()
], en.prototype, "_hasSearch", 2);
Pi([
  Dt()
], en.prototype, "_hasSelected", 2);
en = Pi([
  qt("search-location")
], en);
class gE extends kt {
  constructor() {
    const t = document.createElement("search-location");
    super({ element: t }), this.div = t, Wt.setResizeEvent(this.div, "--search-width");
  }
}
class mE {
  constructor() {
    const t = new Ut({
      fill: new Yt({
        color: "#ffffff00"
      }),
      stroke: new Re({
        color: "#dddddd",
        width: 5
      })
    }), e = new Ys({
      source: new Kn({
        url: () => M().getOptions().border.url,
        format: new Ia()
      }),
      zIndex: 9999,
      style: t,
      opacity: 0.9
    });
    e.on("change", () => {
      var s;
      const n = (s = e.getSource()) == null ? void 0 : s.getExtent();
      if (n) {
        const r = M().getOptions();
        M().getMap().setView(new ti({
          extent: n,
          projection: "EPSG:2056",
          center: r.defaultCenter,
          zoom: r.zoom,
          minZoom: r.minZoom,
          maxZoom: r.maxZoom,
          enableRotation: r.interaction.enableRotation,
          constrainOnlyCenter: !0
        }));
      }
      M().setBorderConstraint(e), it.sendEvent("border-contraint-enabled", void 0);
    }), M().getMap().addLayer(e);
  }
}
class pE {
  constructor() {
    var e;
    this.vectorLayer = new Ys(), this.vectorSource = new Kn();
    const t = M().getGeolocation();
    if (t) {
      const n = new on();
      n.setStyle(
        new Ut({
          image: new ei({
            radius: 6,
            fill: new Yt({
              color: "#3399CC"
            }),
            stroke: new Re({
              color: "#fff",
              width: 2
            })
          })
        })
      ), t.on("change:position", function() {
        const s = t.getPosition();
        n.setGeometry(
          s ? new si(s) : void 0
        );
      }), (e = this.vectorSource) == null || e.addFeature(n), this.vectorLayer.setSource(this.vectorSource), M().getMap().addLayer(this.vectorLayer);
    }
  }
  removeMarker() {
    M().getMap().removeLayer(this.vectorLayer);
  }
}
const _E = `.loader-element{position:absolute;top:calc(50% - 52px);background-color:var(--information-box-background-color);box-shadow:#0003 0 1px 4px;padding:15px;border-radius:10px;border:1px solid var(--information-box-background-color);z-index:10;max-width:302px;width:100%;left:calc(50% - 167px)}.loader-text{display:flex;justify-content:center;margin-top:10px;color:var(--information-box-title-color)}.loader-container{display:flex;justify-content:center}.loader{width:48px;height:48px;border:4px solid #008c6f;border-bottom-color:transparent;border-radius:50%;display:inline-block;box-sizing:border-box;animation:rotation 1s linear infinite}@keyframes rotation{0%{transform:rotate(0)}to{transform:rotate(360deg)}}
`;
var yE = Object.defineProperty, vE = Object.getOwnPropertyDescriptor, Vf = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? vE(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && yE(t, e, s), s;
};
let oo = class extends Pt {
  constructor(i) {
    super(), this.message = "", this.message = i;
  }
  render() {
    return Lt`
      <div class="loader-element" style="pointer-events: auto;">
        <div class="loader-container">
          <span class="loader"></span>
        </div>
        <div class="loader-text">${this.message}</div>
      </div>
    `;
  }
};
oo.styles = [yt(_E)];
Vf([
  Dt()
], oo.prototype, "message", 2);
oo = Vf([
  qt("loader-box")
], oo);
class xE extends kt {
  constructor(t) {
    const e = document.createElement("loader-box");
    e.message = t, super({
      element: e
    });
  }
  disable() {
    this.element.classList.add("disabled");
  }
  show() {
    this.element.classList.remove("fade-out"), this.element.classList.remove("disabled"), this.element.classList.add("fade-in");
  }
  hide() {
    this.element.classList.remove("fade-in"), this.element.classList.add("fade-out");
  }
}
class CE {
  removeLoaderBox() {
    this.loaderBox.hide();
  }
  chromeBasePermissionAnalyzer() {
    const t = M().getGeolocation();
    navigator.permissions.query({ name: "geolocation" }).then((e) => {
      e.state === "denied" && (t == null || t.setTracking(!1), this.denied()), e.state === "prompt" && this.openInfo(), e.state === "granted" && this.granted(), e.onchange = () => {
        var n;
        e.state === "denied" && (t == null || t.setTracking(!1), this.denied()), e.state === "prompt" && (this.openInfo(), t == null || t.setTracking(!0), (n = this.marker) == null || n.removeMarker()), e.state === "granted" && (t == null || t.setTracking(!0), this.granted());
      };
    });
  }
  granted() {
    this.removeLoaderBox(), M().getMap().removeOverlay(this.overlay), this.marker = new pE();
  }
  denied() {
    var t;
    this.removeLoaderBox(), M().getMap().removeOverlay(this.overlay), (t = this.marker) == null || t.removeMarker();
  }
  geolocationSuccess() {
    this.granted();
  }
  geolocationError() {
    this.denied();
  }
  getLocation() {
    navigator.geolocation ? navigator.geolocation.getCurrentPosition(this.geolocationSuccess.bind(this), this.geolocationError.bind(this)) : this.denied();
  }
  openInfo() {
    M().getMap().addOverlay(this.overlay), this.loaderBox.show(), this.getLocation();
  }
  checkGeolocation() {
    const t = M().getGeolocation();
    navigator.userAgent.match(/Chrome\/\d+/) !== null ? this.chromeBasePermissionAnalyzer() : (navigator.permissions.query({ name: "geolocation" }).then((e) => {
      e.state === "denied" && this.denied(), e.state === "prompt" && this.openInfo(), e.state === "granted" && this.granted();
    }), t == null || t.on("error", () => {
      this.denied();
    }), t == null || t.on("change:position", () => {
      this.granted();
    }));
  }
  constructor() {
    const t = M().getGeolocation();
    t == null || t.setTracking(!0);
    const e = document.createElement("div");
    e.classList.add("map-overlay");
    const n = M().getMap().getView().calculateExtent(M().getMap().getSize());
    this.overlay = new p2({ element: e, position: Ii(n), className: "ol-overlay-container ol-selectable overlay-index" }), this.loaderBox = new xE("Chargement des donn\xE9es GPS"), M().getMap().addControl(this.loaderBox), this.checkGeolocation();
  }
}
class iu {
  static getStates(t) {
    const e = {
      readonly: !1,
      currentSelections: []
    };
    return t && (t.readonly && (e.readonly = t.readonly), t.currentSelections && t.currentSelections.length > 0 && (e.currentSelections = t.currentSelections)), e;
  }
}
class ME {
  constructor(t) {
    this.vectorSource = new Kn(), this.renderUtils = t, this.renderUtils.setupAndLoadLayer(this.vectorSource);
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementCreateTargetMode(this.vectorSource, t);
  }
}
class nu {
  static setupCircles(t, e) {
    let n = [];
    return t.get("isSelected") ? n = [
      new Ut({
        zIndex: 1,
        image: new ei({
          radius: 2 * e,
          stroke: new Re({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Yt({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Ut({
        zIndex: 2,
        image: new ei({
          radius: e > 8 ? 4 : 0.2 * e,
          stroke: new Re({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Yt({
            color: "#DC2626"
          })
        })
      })
    ] : n = [
      new Ut({
        zIndex: 1,
        image: new ei({
          radius: 2 * e,
          stroke: new Re({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Yt({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Ut({
        zIndex: 2,
        image: new ei({
          radius: e > 8 ? 4 : 0.2 * e,
          stroke: new Re({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Yt({
            color: "#DC2626"
          })
        })
      })
    ], n;
  }
}
class EE {
  constructor() {
    this.vectorIsLoaded = !1;
  }
  getDefaultZoomFactor() {
    let t = M().getMap().getView().getZoom() || 1;
    return t > 1 && (t = t / 2), t;
  }
  setChangeResolution(t, e) {
    var a;
    const n = M().getOptions(), s = ((a = n.notifications.find((l) => l.rule.type === "ZOOM_CONSTRAINT")) == null ? void 0 : a.rule.minZoom) || n.zoom, r = t.getView().getZoom(), o = t.getView().getResolution();
    r && o && r > s && e.setStyle(function(l) {
      return nu.setupCircles(l, r / o);
    });
  }
  setupAndLoadLayer(t) {
    const e = new Ys({
      source: t,
      visible: !0
    });
    e.setStyle((n) => nu.setupCircles(n, this.getDefaultZoomFactor())), M().getMap().addLayer(e), Wt.registerBorderConstaintMapEvent("change:resolution", () => this.setChangeResolution(M().getMap(), e));
  }
  generateFeaturePointFromCoordinate(t) {
    const e = t, n = new si(e), s = new on({
      geom: n,
      id: Number(`${Math.round(e[0])}${Math.round(e[1])}`),
      isSelected: !1
    });
    return s.setGeometryName("geom"), s;
  }
  displayCurrentElementCreateTargetMode(t, e) {
    t.getFeatures().forEach((n) => t.removeFeature(n)), e.currentSelections.length > 0 && e.currentSelections.forEach((n) => {
      const s = this.generateFeaturePointFromCoordinate(n);
      e.readonly || M().addSelectedFeature(s, s.get("id"), "create"), t.addFeature(s);
    });
  }
  loadSelectMode(t, e) {
    const n = [];
    return e.currentSelections && e.currentSelections.length > 0 && (t.getFeatures().forEach((s) => {
      s.get("isClick") && s.set("isClick", !1);
    }), e.currentSelections.forEach((s) => {
      t.getFeatures().forEach((r) => {
        const o = r.get("geom").getCoordinates();
        o[0].toFixed(2) == s[0] && o[1].toFixed(2) == s[1] && (n.push(s), r.set("isClick", !0), e.readonly || M().addSelectedFeature(r, r.get("objectid"), "select"));
      });
    })), n;
  }
  displayCurrentElementSelectMode(t, e) {
    this.vectorIsLoaded ? this.loadSelectMode(t, e) : t.on("featuresloadend", () => {
      this.loadSelectMode(t, e), this.vectorIsLoaded = !0;
    });
  }
  loadMixMode(t, e, n) {
    const s = this.loadSelectMode(t, n), r = {
      readonly: n.readonly,
      currentSelections: n.currentSelections.filter((o) => !s.includes(o))
    };
    this.displayCurrentElementCreateTargetMode(e, r);
  }
  displayMixMode(t, e, n) {
    this.vectorIsLoaded ? this.loadMixMode(t, e, n) : t.on("featuresloadend", () => {
      this.loadMixMode(t, e, n), this.vectorIsLoaded = !0;
    });
  }
}
var wE = Object.defineProperty, SE = Object.getOwnPropertyDescriptor, an = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? SE(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && wE(t, e, s), s;
};
let ri = class extends Pt {
  constructor() {
    super(), this.modeControllers = [], this.renderUtils = new EE(), this.options = {}, this.states = {};
  }
  connectedCallback() {
    super.connectedCallback();
  }
  setupTheme(i) {
    i.darkMode ? M().setTheme("dark") : i.lightMode || window.matchMedia("(prefers-color-scheme: light)").matches ? M().setTheme("light") : window.matchMedia("(prefers-color-scheme: dark)").matches ? M().setTheme("dark") : M().setTheme("light");
  }
  setupCustomDisplay(i) {
    i.mode.type === "target" ? (M().setCustomDisplay(i.geolocationInformation.displayBox), this.setupTargetBoxSize(i.geolocationInformation)) : i.search.displaySearch ? (M().setTargetBoxSize("small"), M().setCustomDisplay(!0)) : (M().setTargetBoxSize("no-box"), M().setCustomDisplay(!1));
  }
  setupTargetBoxSize(i) {
    i.currentLocation && i.reverseLocation ? M().setTargetBoxSize("large") : i.currentLocation || i.reverseLocation ? M().setTargetBoxSize("medium") : M().setTargetBoxSize("small");
  }
  firstUpdated() {
    new Ky(this.options);
    const i = iu.getStates(this.states), t = M().getOptions(), e = i.readonly;
    this.setupTheme(t), this.setupCustomDisplay(t), se.defs("EPSG:2056", "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"), uE(se), this.view = new ti({
      projection: "EPSG:2056",
      center: t.defaultCenter,
      zoom: t.zoom,
      minZoom: t.minZoom,
      maxZoom: t.maxZoom,
      enableRotation: t.interaction.enableRotation
    }), M().setMap(new J1({
      target: this.mapElement,
      controls: [],
      layers: [],
      view: this.view
    })), Mv.setupIcon(i), t.interaction.enableGeolocation && !e && (M().setGeolocation(new im({
      trackingOptions: {
        enableHighAccuracy: !0
      },
      projection: this.view.getProjection()
    })), new CE()), t.search.displaySearch && t.mode.type !== "target" && !e && M().getMap().addControl(new gE()), t.mode.type === "target" && (this.modeControllers.push(new ME(this.renderUtils)), e || (M().getMap().addControl(new Lv()), t.geolocationInformation.displayBox && M().getMap().addControl(
      new Av()
    ))), t.wmts.length > 0 && new zy(), t.interaction.displayScaleLine && M().getMap().addControl(new T2({ units: "metric" })), t.border.url !== "" && new mE(), t.inclusionArea.url !== "" && new Jy(), t.mode.type === "select" && t.wfs.url != "" && this.modeControllers.push(new Oc(this.renderUtils, i)), t.mode.type === "create" && this.modeControllers.push(new eu(this.mapElement, this.renderUtils, i)), t.mode.type === "mix" && t.wfs.url != "" && (this.modeControllers.push(new Oc(this.renderUtils, i)), this.modeControllers.push(new eu(this.mapElement, this.renderUtils, i))), e || new Hy(), Wt.setCursorEvent();
  }
  updated(i) {
    if (i.has("states") && this.states) {
      const t = iu.getStates(this.states);
      switch (M().getOptions().mode.type) {
        case "target":
          this.modeControllers[0].renderCurrentSelection(t);
          break;
        case "select":
          this.modeControllers[0].renderCurrentSelection(t);
          break;
        case "create":
          this.modeControllers[0].renderCurrentSelection(t);
          break;
        case "mix":
          this.renderUtils.displayMixMode(this.modeControllers[0].vectorSource, this.modeControllers[1].vectorSource, t);
          break;
      }
    }
  }
  render() {
    return Lt`
    <div id="map" class="${M().getTargetBoxSize()} ${M().getTheme()}">
    </div>
    `;
  }
};
ri.styles = [yt(Zy), yt(Vy), yt(Lo), yt(_f), yt(Xy), yt(Yy), yt(jy)];
an([
  pu("#map")
], ri.prototype, "mapElement", 2);
an([
  Dt()
], ri.prototype, "view", 2);
an([
  Dt()
], ri.prototype, "modeControllers", 2);
an([
  Dt()
], ri.prototype, "renderUtils", 2);
an([
  Ti({ type: Object, attribute: "options" })
], ri.prototype, "options", 2);
an([
  Ti({ type: Object, attribute: "states" })
], ri.prototype, "states", 2);
ri = an([
  qt("openlayers-element")
], ri);
export {
  ri as OpenLayersElement
};
