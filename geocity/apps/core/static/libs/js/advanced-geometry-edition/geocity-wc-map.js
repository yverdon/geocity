/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Wr = window, ul = Wr.ShadowRoot && (Wr.ShadyCSS === void 0 || Wr.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, Pu = Symbol(), Sh = /* @__PURE__ */ new WeakMap();
class yg {
  constructor(t, e, i) {
    if (this._$cssResult$ = !0, i !== Pu)
      throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (ul && t === void 0) {
      const i = e !== void 0 && e.length === 1;
      i && (t = Sh.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), i && Sh.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
}
const Mt = (n) => new yg(typeof n == "string" ? n : n + "", void 0, Pu), vg = (n, t) => {
  ul ? n.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet) : t.forEach((e) => {
    const i = document.createElement("style"), s = Wr.litNonce;
    s !== void 0 && i.setAttribute("nonce", s), i.textContent = e.cssText, n.appendChild(i);
  });
}, Rh = ul ? (n) => n : (n) => n instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const i of t.cssRules)
    e += i.cssText;
  return Mt(e);
})(n) : n;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var Jo;
const qr = window, Th = qr.trustedTypes, xg = Th ? Th.emptyScript : "", bh = qr.reactiveElementPolyfillSupport, Ta = { toAttribute(n, t) {
  switch (t) {
    case Boolean:
      n = n ? xg : null;
      break;
    case Object:
    case Array:
      n = n == null ? n : JSON.stringify(n);
  }
  return n;
}, fromAttribute(n, t) {
  let e = n;
  switch (t) {
    case Boolean:
      e = n !== null;
      break;
    case Number:
      e = n === null ? null : Number(n);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(n);
      } catch {
        e = null;
      }
  }
  return e;
} }, Au = (n, t) => t !== n && (t == t || n == n), Qo = { attribute: !0, type: String, converter: Ta, reflect: !1, hasChanged: Au };
class Sn extends HTMLElement {
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
    return this.elementProperties.forEach((e, i) => {
      const s = this._$Ep(i, e);
      s !== void 0 && (this._$Ev.set(s, i), t.push(s));
    }), t;
  }
  static createProperty(t, e = Qo) {
    if (e.state && (e.attribute = !1), this.finalize(), this.elementProperties.set(t, e), !e.noAccessor && !this.prototype.hasOwnProperty(t)) {
      const i = typeof t == "symbol" ? Symbol() : "__" + t, s = this.getPropertyDescriptor(t, i, e);
      s !== void 0 && Object.defineProperty(this.prototype, t, s);
    }
  }
  static getPropertyDescriptor(t, e, i) {
    return { get() {
      return this[e];
    }, set(s) {
      const r = this[t];
      this[e] = s, this.requestUpdate(t, r, i);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) || Qo;
  }
  static finalize() {
    if (this.hasOwnProperty("finalized"))
      return !1;
    this.finalized = !0;
    const t = Object.getPrototypeOf(this);
    if (t.finalize(), t.h !== void 0 && (this.h = [...t.h]), this.elementProperties = new Map(t.elementProperties), this._$Ev = /* @__PURE__ */ new Map(), this.hasOwnProperty("properties")) {
      const e = this.properties, i = [...Object.getOwnPropertyNames(e), ...Object.getOwnPropertySymbols(e)];
      for (const s of i)
        this.createProperty(s, e[s]);
    }
    return this.elementStyles = this.finalizeStyles(this.styles), !0;
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const i = new Set(t.flat(1 / 0).reverse());
      for (const s of i)
        e.unshift(Rh(s));
    } else
      t !== void 0 && e.push(Rh(t));
    return e;
  }
  static _$Ep(t, e) {
    const i = e.attribute;
    return i === !1 ? void 0 : typeof i == "string" ? i : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  u() {
    var t;
    this._$E_ = new Promise((e) => this.enableUpdating = e), this._$AL = /* @__PURE__ */ new Map(), this._$Eg(), this.requestUpdate(), (t = this.constructor.h) === null || t === void 0 || t.forEach((e) => e(this));
  }
  addController(t) {
    var e, i;
    ((e = this._$ES) !== null && e !== void 0 ? e : this._$ES = []).push(t), this.renderRoot !== void 0 && this.isConnected && ((i = t.hostConnected) === null || i === void 0 || i.call(t));
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
    return vg(e, this.constructor.elementStyles), e;
  }
  connectedCallback() {
    var t;
    this.renderRoot === void 0 && (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), (t = this._$ES) === null || t === void 0 || t.forEach((e) => {
      var i;
      return (i = e.hostConnected) === null || i === void 0 ? void 0 : i.call(e);
    });
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    var t;
    (t = this._$ES) === null || t === void 0 || t.forEach((e) => {
      var i;
      return (i = e.hostDisconnected) === null || i === void 0 ? void 0 : i.call(e);
    });
  }
  attributeChangedCallback(t, e, i) {
    this._$AK(t, i);
  }
  _$EO(t, e, i = Qo) {
    var s;
    const r = this.constructor._$Ep(t, i);
    if (r !== void 0 && i.reflect === !0) {
      const o = (((s = i.converter) === null || s === void 0 ? void 0 : s.toAttribute) !== void 0 ? i.converter : Ta).toAttribute(e, i.type);
      this._$El = t, o == null ? this.removeAttribute(r) : this.setAttribute(r, o), this._$El = null;
    }
  }
  _$AK(t, e) {
    var i;
    const s = this.constructor, r = s._$Ev.get(t);
    if (r !== void 0 && this._$El !== r) {
      const o = s.getPropertyOptions(r), a = typeof o.converter == "function" ? { fromAttribute: o.converter } : ((i = o.converter) === null || i === void 0 ? void 0 : i.fromAttribute) !== void 0 ? o.converter : Ta;
      this._$El = r, this[r] = a.fromAttribute(e, o.type), this._$El = null;
    }
  }
  requestUpdate(t, e, i) {
    let s = !0;
    t !== void 0 && (((i = i || this.constructor.getPropertyOptions(t)).hasChanged || Au)(this[t], e) ? (this._$AL.has(t) || this._$AL.set(t, e), i.reflect === !0 && this._$El !== t && (this._$EC === void 0 && (this._$EC = /* @__PURE__ */ new Map()), this._$EC.set(t, i))) : s = !1), !this.isUpdatePending && s && (this._$E_ = this._$Ej());
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
    const i = this._$AL;
    try {
      e = this.shouldUpdate(i), e ? (this.willUpdate(i), (t = this._$ES) === null || t === void 0 || t.forEach((s) => {
        var r;
        return (r = s.hostUpdate) === null || r === void 0 ? void 0 : r.call(s);
      }), this.update(i)) : this._$Ek();
    } catch (s) {
      throw e = !1, this._$Ek(), s;
    }
    e && this._$AE(i);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    var e;
    (e = this._$ES) === null || e === void 0 || e.forEach((i) => {
      var s;
      return (s = i.hostUpdated) === null || s === void 0 ? void 0 : s.call(i);
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
    this._$EC !== void 0 && (this._$EC.forEach((e, i) => this._$EO(i, this[i], e)), this._$EC = void 0), this._$Ek();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
}
Sn.finalized = !0, Sn.elementProperties = /* @__PURE__ */ new Map(), Sn.elementStyles = [], Sn.shadowRootOptions = { mode: "open" }, bh == null || bh({ ReactiveElement: Sn }), ((Jo = qr.reactiveElementVersions) !== null && Jo !== void 0 ? Jo : qr.reactiveElementVersions = []).push("1.5.0");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var ta;
const Kr = window, Vn = Kr.trustedTypes, Lh = Vn ? Vn.createPolicy("lit-html", { createHTML: (n) => n }) : void 0, ni = `lit$${(Math.random() + "").slice(9)}$`, dl = "?" + ni, Cg = `<${dl}>`, Un = document, Ps = (n = "") => Un.createComment(n), As = (n) => n === null || typeof n != "object" && typeof n != "function", Ou = Array.isArray, Fu = (n) => Ou(n) || typeof (n == null ? void 0 : n[Symbol.iterator]) == "function", fs = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, Ih = /-->/g, Ph = />/g, $i = RegExp(`>|[ 	
\f\r](?:([^\\s"'>=/]+)([ 	
\f\r]*=[ 	
\f\r]*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Ah = /'/g, Oh = /"/g, Nu = /^(?:script|style|textarea|title)$/i, Mg = (n) => (t, ...e) => ({ _$litType$: n, strings: t, values: e }), Lt = Mg(1), bi = Symbol.for("lit-noChange"), bt = Symbol.for("lit-nothing"), Fh = /* @__PURE__ */ new WeakMap(), $n = Un.createTreeWalker(Un, 129, null, !1), Du = (n, t) => {
  const e = n.length - 1, i = [];
  let s, r = t === 2 ? "<svg>" : "", o = fs;
  for (let l = 0; l < e; l++) {
    const h = n[l];
    let c, u, d = -1, f = 0;
    for (; f < h.length && (o.lastIndex = f, u = o.exec(h), u !== null); )
      f = o.lastIndex, o === fs ? u[1] === "!--" ? o = Ih : u[1] !== void 0 ? o = Ph : u[2] !== void 0 ? (Nu.test(u[2]) && (s = RegExp("</" + u[2], "g")), o = $i) : u[3] !== void 0 && (o = $i) : o === $i ? u[0] === ">" ? (o = s != null ? s : fs, d = -1) : u[1] === void 0 ? d = -2 : (d = o.lastIndex - u[2].length, c = u[1], o = u[3] === void 0 ? $i : u[3] === '"' ? Oh : Ah) : o === Oh || o === Ah ? o = $i : o === Ih || o === Ph ? o = fs : (o = $i, s = void 0);
    const g = o === $i && n[l + 1].startsWith("/>") ? " " : "";
    r += o === fs ? h + Cg : d >= 0 ? (i.push(c), h.slice(0, d) + "$lit$" + h.slice(d) + ni + g) : h + ni + (d === -2 ? (i.push(void 0), l) : g);
  }
  const a = r + (n[e] || "<?>") + (t === 2 ? "</svg>" : "");
  if (!Array.isArray(n) || !n.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return [Lh !== void 0 ? Lh.createHTML(a) : a, i];
};
class Os {
  constructor({ strings: t, _$litType$: e }, i) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, l = this.parts, [h, c] = Du(t, e);
    if (this.el = Os.createElement(h, i), $n.currentNode = this.el.content, e === 2) {
      const u = this.el.content, d = u.firstChild;
      d.remove(), u.append(...d.childNodes);
    }
    for (; (s = $n.nextNode()) !== null && l.length < a; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) {
          const u = [];
          for (const d of s.getAttributeNames())
            if (d.endsWith("$lit$") || d.startsWith(ni)) {
              const f = c[o++];
              if (u.push(d), f !== void 0) {
                const g = s.getAttribute(f.toLowerCase() + "$lit$").split(ni), m = /([.?@])?(.*)/.exec(f);
                l.push({ type: 1, index: r, name: m[2], strings: g, ctor: m[1] === "." ? Gu : m[1] === "?" ? $u : m[1] === "@" ? Bu : qs });
              } else
                l.push({ type: 6, index: r });
            }
          for (const d of u)
            s.removeAttribute(d);
        }
        if (Nu.test(s.tagName)) {
          const u = s.textContent.split(ni), d = u.length - 1;
          if (d > 0) {
            s.textContent = Vn ? Vn.emptyScript : "";
            for (let f = 0; f < d; f++)
              s.append(u[f], Ps()), $n.nextNode(), l.push({ type: 2, index: ++r });
            s.append(u[d], Ps());
          }
        }
      } else if (s.nodeType === 8)
        if (s.data === dl)
          l.push({ type: 2, index: r });
        else {
          let u = -1;
          for (; (u = s.data.indexOf(ni, u + 1)) !== -1; )
            l.push({ type: 7, index: r }), u += ni.length - 1;
        }
      r++;
    }
  }
  static createElement(t, e) {
    const i = Un.createElement("template");
    return i.innerHTML = t, i;
  }
}
function Qi(n, t, e = n, i) {
  var s, r, o, a;
  if (t === bi)
    return t;
  let l = i !== void 0 ? (s = e._$Co) === null || s === void 0 ? void 0 : s[i] : e._$Cl;
  const h = As(t) ? void 0 : t._$litDirective$;
  return (l == null ? void 0 : l.constructor) !== h && ((r = l == null ? void 0 : l._$AO) === null || r === void 0 || r.call(l, !1), h === void 0 ? l = void 0 : (l = new h(n), l._$AT(n, e, i)), i !== void 0 ? ((o = (a = e)._$Co) !== null && o !== void 0 ? o : a._$Co = [])[i] = l : e._$Cl = l), l !== void 0 && (t = Qi(n, l._$AS(n, t.values), l, i)), t;
}
class ku {
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
    const { el: { content: i }, parts: s } = this._$AD, r = ((e = t == null ? void 0 : t.creationScope) !== null && e !== void 0 ? e : Un).importNode(i, !0);
    $n.currentNode = r;
    let o = $n.nextNode(), a = 0, l = 0, h = s[0];
    for (; h !== void 0; ) {
      if (a === h.index) {
        let c;
        h.type === 2 ? c = new ns(o, o.nextSibling, this, t) : h.type === 1 ? c = new h.ctor(o, h.name, h.strings, this, t) : h.type === 6 && (c = new zu(o, this, t)), this.u.push(c), h = s[++l];
      }
      a !== (h == null ? void 0 : h.index) && (o = $n.nextNode(), a++);
    }
    return r;
  }
  p(t) {
    let e = 0;
    for (const i of this.u)
      i !== void 0 && (i.strings !== void 0 ? (i._$AI(t, i, e), e += i.strings.length - 2) : i._$AI(t[e])), e++;
  }
}
class ns {
  constructor(t, e, i, s) {
    var r;
    this.type = 2, this._$AH = bt, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = i, this.options = s, this._$Cm = (r = s == null ? void 0 : s.isConnected) === null || r === void 0 || r;
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
    t = Qi(this, t, e), As(t) ? t === bt || t == null || t === "" ? (this._$AH !== bt && this._$AR(), this._$AH = bt) : t !== this._$AH && t !== bi && this.g(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : Fu(t) ? this.k(t) : this.g(t);
  }
  O(t, e = this._$AB) {
    return this._$AA.parentNode.insertBefore(t, e);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  g(t) {
    this._$AH !== bt && As(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Un.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var e;
    const { values: i, _$litType$: s } = t, r = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = Os.createElement(s.h, this.options)), s);
    if (((e = this._$AH) === null || e === void 0 ? void 0 : e._$AD) === r)
      this._$AH.p(i);
    else {
      const o = new ku(r, this), a = o.v(this.options);
      o.p(i), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = Fh.get(t.strings);
    return e === void 0 && Fh.set(t.strings, e = new Os(t)), e;
  }
  k(t) {
    Ou(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let i, s = 0;
    for (const r of t)
      s === e.length ? e.push(i = new ns(this.O(Ps()), this.O(Ps()), this, this.options)) : i = e[s], i._$AI(r), s++;
    s < e.length && (this._$AR(i && i._$AB.nextSibling, s), e.length = s);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    var i;
    for ((i = this._$AP) === null || i === void 0 || i.call(this, !1, !0, e); t && t !== this._$AB; ) {
      const s = t.nextSibling;
      t.remove(), t = s;
    }
  }
  setConnected(t) {
    var e;
    this._$AM === void 0 && (this._$Cm = t, (e = this._$AP) === null || e === void 0 || e.call(this, t));
  }
}
class qs {
  constructor(t, e, i, s, r) {
    this.type = 1, this._$AH = bt, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = bt;
  }
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t, e = this, i, s) {
    const r = this.strings;
    let o = !1;
    if (r === void 0)
      t = Qi(this, t, e, 0), o = !As(t) || t !== this._$AH && t !== bi, o && (this._$AH = t);
    else {
      const a = t;
      let l, h;
      for (t = r[0], l = 0; l < r.length - 1; l++)
        h = Qi(this, a[i + l], e, l), h === bi && (h = this._$AH[l]), o || (o = !As(h) || h !== this._$AH[l]), h === bt ? t = bt : t !== bt && (t += (h != null ? h : "") + r[l + 1]), this._$AH[l] = h;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === bt ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t != null ? t : "");
  }
}
class Gu extends qs {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === bt ? void 0 : t;
  }
}
const Eg = Vn ? Vn.emptyScript : "";
class $u extends qs {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    t && t !== bt ? this.element.setAttribute(this.name, Eg) : this.element.removeAttribute(this.name);
  }
}
class Bu extends qs {
  constructor(t, e, i, s, r) {
    super(t, e, i, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    var i;
    if ((t = (i = Qi(this, t, e, 0)) !== null && i !== void 0 ? i : bt) === bi)
      return;
    const s = this._$AH, r = t === bt && s !== bt || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, o = t !== bt && (s === bt || r);
    r && this.element.removeEventListener(this.name, this, s), o && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e, i;
    typeof this._$AH == "function" ? this._$AH.call((i = (e = this.options) === null || e === void 0 ? void 0 : e.host) !== null && i !== void 0 ? i : this.element, t) : this._$AH.handleEvent(t);
  }
}
class zu {
  constructor(t, e, i) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    Qi(this, t);
  }
}
const wg = { P: "$lit$", A: ni, M: dl, C: 1, L: Du, R: ku, D: Fu, V: Qi, I: ns, H: qs, N: $u, U: Bu, B: Gu, F: zu }, Nh = Kr.litHtmlPolyfillSupport;
Nh == null || Nh(Os, ns), ((ta = Kr.litHtmlVersions) !== null && ta !== void 0 ? ta : Kr.litHtmlVersions = []).push("2.5.0");
const Zu = (n, t, e) => {
  var i, s;
  const r = (i = e == null ? void 0 : e.renderBefore) !== null && i !== void 0 ? i : t;
  let o = r._$litPart$;
  if (o === void 0) {
    const a = (s = e == null ? void 0 : e.renderBefore) !== null && s !== void 0 ? s : null;
    r._$litPart$ = o = new ns(t.insertBefore(Ps(), a), a, void 0, e != null ? e : {});
  }
  return o._$AI(n), o;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var ea, ia;
class kt extends Sn {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    var t, e;
    const i = super.createRenderRoot();
    return (t = (e = this.renderOptions).renderBefore) !== null && t !== void 0 || (e.renderBefore = i.firstChild), i;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = Zu(e, this.renderRoot, this.renderOptions);
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
    return bi;
  }
}
kt.finalized = !0, kt._$litElement$ = !0, (ea = globalThis.litElementHydrateSupport) === null || ea === void 0 || ea.call(globalThis, { LitElement: kt });
const Dh = globalThis.litElementPolyfillSupport;
Dh == null || Dh({ LitElement: kt });
((ia = globalThis.litElementVersions) !== null && ia !== void 0 ? ia : globalThis.litElementVersions = []).push("3.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const oe = (n) => (t) => typeof t == "function" ? ((e, i) => (customElements.define(e, i), i))(n, t) : ((e, i) => {
  const { kind: s, elements: r } = i;
  return { kind: s, elements: r, finisher(o) {
    customElements.define(e, o);
  } };
})(n, t);
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Sg = (n, t) => t.kind === "method" && t.descriptor && !("value" in t.descriptor) ? { ...t, finisher(e) {
  e.createProperty(t.key, n);
} } : { kind: "field", key: Symbol(), placement: "own", descriptor: {}, originalKey: t.key, initializer() {
  typeof t.initializer == "function" && (this[t.key] = t.initializer.call(this));
}, finisher(e) {
  e.createProperty(t.key, n);
} };
function cn(n) {
  return (t, e) => e !== void 0 ? ((i, s, r) => {
    s.constructor.createProperty(r, i);
  })(n, t, e) : Sg(n, t);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function ae(n) {
  return cn({ ...n, state: !0 });
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Rg = ({ finisher: n, descriptor: t }) => (e, i) => {
  var s;
  if (i === void 0) {
    const r = (s = e.originalKey) !== null && s !== void 0 ? s : e.key, o = t != null ? { kind: "method", placement: "prototype", key: r, descriptor: t(e.key) } : { ...e, key: r };
    return n != null && (o.finisher = function(a) {
      n(a, r);
    }), o;
  }
  {
    const r = e.constructor;
    t !== void 0 && Object.defineProperty(e, i, t(i)), n == null || n(r, i);
  }
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function Vu(n, t) {
  return Rg({ descriptor: (e) => {
    const i = { get() {
      var s, r;
      return (r = (s = this.renderRoot) === null || s === void 0 ? void 0 : s.querySelector(n)) !== null && r !== void 0 ? r : null;
    }, enumerable: !0, configurable: !0 };
    if (t) {
      const s = typeof e == "symbol" ? Symbol() : "__" + e;
      i.get = function() {
        var r, o;
        return this[s] === void 0 && (this[s] = (o = (r = this.renderRoot) === null || r === void 0 ? void 0 : r.querySelector(n)) !== null && o !== void 0 ? o : null), this[s];
      };
    }
    return i;
  } });
}
/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var na;
((na = window.HTMLSlotElement) === null || na === void 0 ? void 0 : na.prototype.assignedElements) != null;
class Tg {
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
const Re = Tg, Wn = {
  PROPERTYCHANGE: "propertychange"
};
class bg {
  constructor() {
    this.disposed = !1;
  }
  dispose() {
    this.disposed || (this.disposed = !0, this.disposeInternal());
  }
  disposeInternal() {
  }
}
const fl = bg;
function Lg(n, t, e) {
  let i, s;
  e = e || tn;
  let r = 0, o = n.length, a = !1;
  for (; r < o; )
    i = r + (o - r >> 1), s = +e(n[i], t), s < 0 ? r = i + 1 : (o = i, a = !s);
  return a ? r : ~r;
}
function tn(n, t) {
  return n > t ? 1 : n < t ? -1 : 0;
}
function gl(n, t, e) {
  const i = n.length;
  if (n[0] <= t)
    return 0;
  if (t <= n[i - 1])
    return i - 1;
  {
    let s;
    if (e > 0) {
      for (s = 1; s < i; ++s)
        if (n[s] < t)
          return s - 1;
    } else if (e < 0) {
      for (s = 1; s < i; ++s)
        if (n[s] <= t)
          return s;
    } else
      for (s = 1; s < i; ++s) {
        if (n[s] == t)
          return s;
        if (n[s] < t)
          return typeof e == "function" ? e(t, n[s - 1], n[s]) > 0 ? s - 1 : s : n[s - 1] - t < t - n[s] ? s - 1 : s;
      }
    return i - 1;
  }
}
function Ig(n, t, e) {
  for (; t < e; ) {
    const i = n[t];
    n[t] = n[e], n[e] = i, ++t, --e;
  }
}
function Qt(n, t) {
  const e = Array.isArray(t) ? t : [t], i = e.length;
  for (let s = 0; s < i; s++)
    n[n.length] = e[s];
}
function Ni(n, t) {
  const e = n.length;
  if (e !== t.length)
    return !1;
  for (let i = 0; i < e; i++)
    if (n[i] !== t[i])
      return !1;
  return !0;
}
function Pg(n, t, e) {
  const i = t || tn;
  return n.every(function(s, r) {
    if (r === 0)
      return !0;
    const o = i(n[r - 1], s);
    return !(o > 0 || e && o === 0);
  });
}
function en() {
  return !0;
}
function un() {
  return !1;
}
function nn() {
}
function Ag(n) {
  let t = !1, e, i, s;
  return function() {
    const r = Array.prototype.slice.call(arguments);
    return (!t || this !== s || !Ni(r, i)) && (t = !0, s = this, i = r, e = n.apply(this, arguments)), e;
  };
}
function Ks(n) {
  for (const t in n)
    delete n[t];
}
function Hn(n) {
  let t;
  for (t in n)
    return !1;
  return !t;
}
class Og extends fl {
  constructor(t) {
    super(), this.eventTarget_ = t, this.pendingRemovals_ = null, this.dispatching_ = null, this.listeners_ = null;
  }
  addEventListener(t, e) {
    if (!t || !e)
      return;
    const i = this.listeners_ || (this.listeners_ = {}), s = i[t] || (i[t] = []);
    s.includes(e) || s.push(e);
  }
  dispatchEvent(t) {
    const e = typeof t == "string", i = e ? t : t.type, s = this.listeners_ && this.listeners_[i];
    if (!s)
      return;
    const r = e ? new Re(t) : t;
    r.target || (r.target = this.eventTarget_ || this);
    const o = this.dispatching_ || (this.dispatching_ = {}), a = this.pendingRemovals_ || (this.pendingRemovals_ = {});
    i in o || (o[i] = 0, a[i] = 0), ++o[i];
    let l;
    for (let h = 0, c = s.length; h < c; ++h)
      if ("handleEvent" in s[h] ? l = s[h].handleEvent(r) : l = s[h].call(this, r), l === !1 || r.propagationStopped) {
        l = !1;
        break;
      }
    if (--o[i] === 0) {
      let h = a[i];
      for (delete a[i]; h--; )
        this.removeEventListener(i, nn);
      delete o[i];
    }
    return l;
  }
  disposeInternal() {
    this.listeners_ && Ks(this.listeners_);
  }
  getListeners(t) {
    return this.listeners_ && this.listeners_[t] || void 0;
  }
  hasListener(t) {
    return this.listeners_ ? t ? t in this.listeners_ : Object.keys(this.listeners_).length > 0 : !1;
  }
  removeEventListener(t, e) {
    const i = this.listeners_ && this.listeners_[t];
    if (i) {
      const s = i.indexOf(e);
      s !== -1 && (this.pendingRemovals_ && t in this.pendingRemovals_ ? (i[s] = nn, ++this.pendingRemovals_[t]) : (i.splice(s, 1), i.length === 0 && delete this.listeners_[t]));
    }
  }
}
const So = Og, U = {
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
function et(n, t, e, i, s) {
  if (i && i !== n && (e = e.bind(i)), s) {
    const o = e;
    e = function() {
      n.removeEventListener(t, e), o.apply(this, arguments);
    };
  }
  const r = {
    target: n,
    type: t,
    listener: e
  };
  return n.addEventListener(t, e), r;
}
function Jr(n, t, e, i) {
  return et(n, t, e, i, !0);
}
function mt(n) {
  n && n.target && (n.target.removeEventListener(n.type, n.listener), Ks(n));
}
class Ro extends So {
  constructor() {
    super(), this.on = this.onInternal, this.once = this.onceInternal, this.un = this.unInternal, this.revision_ = 0;
  }
  changed() {
    ++this.revision_, this.dispatchEvent(U.CHANGE);
  }
  getRevision() {
    return this.revision_;
  }
  onInternal(t, e) {
    if (Array.isArray(t)) {
      const i = t.length, s = new Array(i);
      for (let r = 0; r < i; ++r)
        s[r] = et(this, t[r], e);
      return s;
    } else
      return et(this, t, e);
  }
  onceInternal(t, e) {
    let i;
    if (Array.isArray(t)) {
      const s = t.length;
      i = new Array(s);
      for (let r = 0; r < s; ++r)
        i[r] = Jr(this, t[r], e);
    } else
      i = Jr(this, t, e);
    return e.ol_key = i, i;
  }
  unInternal(t, e) {
    const i = e.ol_key;
    if (i)
      Fg(i);
    else if (Array.isArray(t))
      for (let s = 0, r = t.length; s < r; ++s)
        this.removeEventListener(t[s], e);
    else
      this.removeEventListener(t, e);
  }
}
Ro.prototype.on;
Ro.prototype.once;
Ro.prototype.un;
function Fg(n) {
  if (Array.isArray(n))
    for (let t = 0, e = n.length; t < e; ++t)
      mt(n[t]);
  else
    mt(n);
}
const Uu = Ro;
function H() {
  throw new Error("Unimplemented abstract method.");
}
let Ng = 0;
function q(n) {
  return n.ol_uid || (n.ol_uid = String(++Ng));
}
class kh extends Re {
  constructor(t, e, i) {
    super(t), this.key = e, this.oldValue = i;
  }
}
class Dg extends Uu {
  constructor(t) {
    super(), this.on, this.once, this.un, q(this), this.values_ = null, t !== void 0 && this.setProperties(t);
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
    let i;
    i = `change:${t}`, this.hasListener(i) && this.dispatchEvent(new kh(i, t, e)), i = Wn.PROPERTYCHANGE, this.hasListener(i) && this.dispatchEvent(new kh(i, t, e));
  }
  addChangeListener(t, e) {
    this.addEventListener(`change:${t}`, e);
  }
  removeChangeListener(t, e) {
    this.removeEventListener(`change:${t}`, e);
  }
  set(t, e, i) {
    const s = this.values_ || (this.values_ = {});
    if (i)
      s[t] = e;
    else {
      const r = s[t];
      s[t] = e, r !== e && this.notify(t, r);
    }
  }
  setProperties(t, e) {
    for (const i in t)
      this.set(i, t[i], e);
  }
  applyProperties(t) {
    !t.values_ || Object.assign(this.values_ || (this.values_ = {}), t.values_);
  }
  unset(t, e) {
    if (this.values_ && t in this.values_) {
      const i = this.values_[t];
      delete this.values_[t], Hn(this.values_) && (this.values_ = null), e || this.notify(t, i);
    }
  }
}
const Oe = Dg, kg = {
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
class Gg extends Error {
  constructor(t) {
    const e = kg[t];
    super(e), this.code = t, this.name = "AssertionError", this.message = e;
  }
}
const Wu = Gg, Dt = {
  ADD: "add",
  REMOVE: "remove"
}, Gh = {
  LENGTH: "length"
};
class Er extends Re {
  constructor(t, e, i) {
    super(t), this.element = e, this.index = i;
  }
}
class $g extends Oe {
  constructor(t, e) {
    if (super(), this.on, this.once, this.un, e = e || {}, this.unique_ = !!e.unique, this.array_ = t || [], this.unique_)
      for (let i = 0, s = this.array_.length; i < s; ++i)
        this.assertUnique_(this.array_[i], i);
    this.updateLength_();
  }
  clear() {
    for (; this.getLength() > 0; )
      this.pop();
  }
  extend(t) {
    for (let e = 0, i = t.length; e < i; ++e)
      this.push(t[e]);
    return this;
  }
  forEach(t) {
    const e = this.array_;
    for (let i = 0, s = e.length; i < s; ++i)
      t(e[i], i, e);
  }
  getArray() {
    return this.array_;
  }
  item(t) {
    return this.array_[t];
  }
  getLength() {
    return this.get(Gh.LENGTH);
  }
  insertAt(t, e) {
    if (t < 0 || t > this.getLength())
      throw new Error("Index out of bounds: " + t);
    this.unique_ && this.assertUnique_(e), this.array_.splice(t, 0, e), this.updateLength_(), this.dispatchEvent(
      new Er(Dt.ADD, e, t)
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
    for (let i = 0, s = e.length; i < s; ++i)
      if (e[i] === t)
        return this.removeAt(i);
  }
  removeAt(t) {
    if (t < 0 || t >= this.getLength())
      return;
    const e = this.array_[t];
    return this.array_.splice(t, 1), this.updateLength_(), this.dispatchEvent(
      new Er(Dt.REMOVE, e, t)
    ), e;
  }
  setAt(t, e) {
    const i = this.getLength();
    if (t >= i) {
      this.insertAt(t, e);
      return;
    }
    if (t < 0)
      throw new Error("Index out of bounds: " + t);
    this.unique_ && this.assertUnique_(e, t);
    const s = this.array_[t];
    this.array_[t] = e, this.dispatchEvent(
      new Er(Dt.REMOVE, s, t)
    ), this.dispatchEvent(
      new Er(Dt.ADD, e, t)
    );
  }
  updateLength_() {
    this.set(Gh.LENGTH, this.array_.length);
  }
  assertUnique_(t, e) {
    for (let i = 0, s = this.array_.length; i < s; ++i)
      if (this.array_[i] === t && i !== e)
        throw new Wu(58);
  }
}
const Ee = $g, Li = typeof navigator < "u" && typeof navigator.userAgent < "u" ? navigator.userAgent.toLowerCase() : "", Bg = Li.includes("firefox"), zg = Li.includes("safari") && !Li.includes("chrom");
zg && (Li.includes("version/15.4") || /cpu (os|iphone os) 15_4 like mac os x/.test(Li));
const Zg = Li.includes("webkit") && !Li.includes("edge"), Vg = Li.includes("macintosh"), Hu = typeof devicePixelRatio < "u" ? devicePixelRatio : 1, ml = typeof WorkerGlobalScope < "u" && typeof OffscreenCanvas < "u" && self instanceof WorkerGlobalScope, Ug = typeof Image < "u" && Image.prototype.decode, Xu = function() {
  let n = !1;
  try {
    const t = Object.defineProperty({}, "passive", {
      get: function() {
        n = !0;
      }
    });
    window.addEventListener("_", null, t), window.removeEventListener("_", null, t);
  } catch {
  }
  return n;
}();
function Y(n, t) {
  if (!n)
    throw new Wu(t);
}
new Array(6);
function $e() {
  return [1, 0, 0, 1, 0, 0];
}
function Wg(n, t, e, i, s, r, o) {
  return n[0] = t, n[1] = e, n[2] = i, n[3] = s, n[4] = r, n[5] = o, n;
}
function Hg(n, t) {
  return n[0] = t[0], n[1] = t[1], n[2] = t[2], n[3] = t[3], n[4] = t[4], n[5] = t[5], n;
}
function Nt(n, t) {
  const e = t[0], i = t[1];
  return t[0] = n[0] * e + n[2] * i + n[4], t[1] = n[1] * e + n[3] * i + n[5], t;
}
function Xg(n, t, e) {
  return Wg(n, t, 0, 0, e, 0, 0);
}
function Ii(n, t, e, i, s, r, o, a) {
  const l = Math.sin(r), h = Math.cos(r);
  return n[0] = i * h, n[1] = s * l, n[2] = -i * l, n[3] = s * h, n[4] = o * i * h - a * i * l + t, n[5] = o * s * l + a * s * h + e, n;
}
function _l(n, t) {
  const e = Yg(t);
  Y(e !== 0, 32);
  const i = t[0], s = t[1], r = t[2], o = t[3], a = t[4], l = t[5];
  return n[0] = o / e, n[1] = -s / e, n[2] = -r / e, n[3] = i / e, n[4] = (r * l - o * a) / e, n[5] = -(i * l - s * a) / e, n;
}
function Yg(n) {
  return n[0] * n[3] - n[1] * n[2];
}
let $h;
function Yu(n) {
  const t = "matrix(" + n.join(", ") + ")";
  if (ml)
    return t;
  const e = $h || ($h = document.createElement("div"));
  return e.style.transform = t, e.style.transform;
}
const Ft = {
  UNKNOWN: 0,
  INTERSECTING: 1,
  ABOVE: 2,
  RIGHT: 4,
  BELOW: 8,
  LEFT: 16
};
function Ut(n) {
  const t = se();
  for (let e = 0, i = n.length; e < i; ++e)
    Ss(t, n[e]);
  return t;
}
function jg(n, t, e) {
  const i = Math.min.apply(null, n), s = Math.min.apply(null, t), r = Math.max.apply(null, n), o = Math.max.apply(null, t);
  return _e(i, s, r, o, e);
}
function Js(n, t, e) {
  return e ? (e[0] = n[0] - t, e[1] = n[1] - t, e[2] = n[2] + t, e[3] = n[3] + t, e) : [
    n[0] - t,
    n[1] - t,
    n[2] + t,
    n[3] + t
  ];
}
function ju(n, t) {
  return t ? (t[0] = n[0], t[1] = n[1], t[2] = n[2], t[3] = n[3], t) : n.slice();
}
function dn(n, t, e) {
  let i, s;
  return t < n[0] ? i = n[0] - t : n[2] < t ? i = t - n[2] : i = 0, e < n[1] ? s = n[1] - e : n[3] < e ? s = e - n[3] : s = 0, i * i + s * s;
}
function To(n, t) {
  return pl(n, t[0], t[1]);
}
function Vi(n, t) {
  return n[0] <= t[0] && t[2] <= n[2] && n[1] <= t[1] && t[3] <= n[3];
}
function pl(n, t, e) {
  return n[0] <= t && t <= n[2] && n[1] <= e && e <= n[3];
}
function ba(n, t) {
  const e = n[0], i = n[1], s = n[2], r = n[3], o = t[0], a = t[1];
  let l = Ft.UNKNOWN;
  return o < e ? l = l | Ft.LEFT : o > s && (l = l | Ft.RIGHT), a < i ? l = l | Ft.BELOW : a > r && (l = l | Ft.ABOVE), l === Ft.UNKNOWN && (l = Ft.INTERSECTING), l;
}
function se() {
  return [1 / 0, 1 / 0, -1 / 0, -1 / 0];
}
function _e(n, t, e, i, s) {
  return s ? (s[0] = n, s[1] = t, s[2] = e, s[3] = i, s) : [n, t, e, i];
}
function Qs(n) {
  return _e(1 / 0, 1 / 0, -1 / 0, -1 / 0, n);
}
function ws(n, t) {
  const e = n[0], i = n[1];
  return _e(e, i, e, i, t);
}
function qu(n, t, e, i, s) {
  const r = Qs(s);
  return Ju(r, n, t, e, i);
}
function Fs(n, t) {
  return n[0] == t[0] && n[2] == t[2] && n[1] == t[1] && n[3] == t[3];
}
function Ku(n, t) {
  return t[0] < n[0] && (n[0] = t[0]), t[2] > n[2] && (n[2] = t[2]), t[1] < n[1] && (n[1] = t[1]), t[3] > n[3] && (n[3] = t[3]), n;
}
function Ss(n, t) {
  t[0] < n[0] && (n[0] = t[0]), t[0] > n[2] && (n[2] = t[0]), t[1] < n[1] && (n[1] = t[1]), t[1] > n[3] && (n[3] = t[1]);
}
function Ju(n, t, e, i, s) {
  for (; e < i; e += s)
    qg(n, t[e], t[e + 1]);
  return n;
}
function qg(n, t, e) {
  n[0] = Math.min(n[0], t), n[1] = Math.min(n[1], e), n[2] = Math.max(n[2], t), n[3] = Math.max(n[3], e);
}
function yl(n, t) {
  let e;
  return e = t(bo(n)), e || (e = t(Lo(n)), e) || (e = t(Io(n)), e) || (e = t(fn(n)), e) ? e : !1;
}
function La(n) {
  let t = 0;
  return vl(n) || (t = pt(n) * ze(n)), t;
}
function bo(n) {
  return [n[0], n[1]];
}
function Lo(n) {
  return [n[2], n[1]];
}
function Pi(n) {
  return [(n[0] + n[2]) / 2, (n[1] + n[3]) / 2];
}
function Kg(n, t) {
  let e;
  return t === "bottom-left" ? e = bo(n) : t === "bottom-right" ? e = Lo(n) : t === "top-left" ? e = fn(n) : t === "top-right" ? e = Io(n) : Y(!1, 13), e;
}
function Ia(n, t, e, i, s) {
  const [r, o, a, l, h, c, u, d] = Pa(
    n,
    t,
    e,
    i
  );
  return _e(
    Math.min(r, a, h, u),
    Math.min(o, l, c, d),
    Math.max(r, a, h, u),
    Math.max(o, l, c, d),
    s
  );
}
function Pa(n, t, e, i) {
  const s = t * i[0] / 2, r = t * i[1] / 2, o = Math.cos(e), a = Math.sin(e), l = s * o, h = s * a, c = r * o, u = r * a, d = n[0], f = n[1];
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
function ze(n) {
  return n[3] - n[1];
}
function Rs(n, t, e) {
  const i = e || se();
  return Kt(n, t) ? (n[0] > t[0] ? i[0] = n[0] : i[0] = t[0], n[1] > t[1] ? i[1] = n[1] : i[1] = t[1], n[2] < t[2] ? i[2] = n[2] : i[2] = t[2], n[3] < t[3] ? i[3] = n[3] : i[3] = t[3]) : Qs(i), i;
}
function fn(n) {
  return [n[0], n[3]];
}
function Io(n) {
  return [n[2], n[3]];
}
function pt(n) {
  return n[2] - n[0];
}
function Kt(n, t) {
  return n[0] <= t[2] && n[2] >= t[0] && n[1] <= t[3] && n[3] >= t[1];
}
function vl(n) {
  return n[2] < n[0] || n[3] < n[1];
}
function Jg(n, t) {
  return t ? (t[0] = n[0], t[1] = n[1], t[2] = n[2], t[3] = n[3], t) : n;
}
function Qg(n, t, e) {
  let i = !1;
  const s = ba(n, t), r = ba(n, e);
  if (s === Ft.INTERSECTING || r === Ft.INTERSECTING)
    i = !0;
  else {
    const o = n[0], a = n[1], l = n[2], h = n[3], c = t[0], u = t[1], d = e[0], f = e[1], g = (f - u) / (d - c);
    let m, _;
    !!(r & Ft.ABOVE) && !(s & Ft.ABOVE) && (m = d - (f - h) / g, i = m >= o && m <= l), !i && !!(r & Ft.RIGHT) && !(s & Ft.RIGHT) && (_ = f - (d - l) * g, i = _ >= a && _ <= h), !i && !!(r & Ft.BELOW) && !(s & Ft.BELOW) && (m = d - (f - a) / g, i = m >= o && m <= l), !i && !!(r & Ft.LEFT) && !(s & Ft.LEFT) && (_ = f - (d - o) * g, i = _ >= a && _ <= h);
  }
  return i;
}
function t0(n, t, e, i) {
  let s = [];
  if (i > 1) {
    const a = n[2] - n[0], l = n[3] - n[1];
    for (let h = 0; h < i; ++h)
      s.push(
        n[0] + a * h / i,
        n[1],
        n[2],
        n[1] + l * h / i,
        n[2] - a * h / i,
        n[3],
        n[0],
        n[3] - l * h / i
      );
  } else
    s = [
      n[0],
      n[1],
      n[2],
      n[1],
      n[2],
      n[3],
      n[0],
      n[3]
    ];
  t(s, s, 2);
  const r = [], o = [];
  for (let a = 0, l = s.length; a < l; a += 2)
    r.push(s[a]), o.push(s[a + 1]);
  return jg(r, o, e);
}
function Qu(n, t) {
  const e = t.getExtent(), i = Pi(n);
  if (t.canWrapX() && (i[0] < e[0] || i[0] >= e[2])) {
    const s = pt(e), o = Math.floor(
      (i[0] - e[0]) / s
    ) * s;
    n[0] -= o, n[2] -= o;
  }
  return n;
}
function e0(n, t) {
  if (t.canWrapX()) {
    const e = t.getExtent();
    if (!isFinite(n[0]) || !isFinite(n[2]))
      return [[e[0], n[1], e[2], n[3]]];
    Qu(n, t);
    const i = pt(e);
    if (pt(n) > i)
      return [[e[0], n[1], e[2], n[3]]];
    if (n[0] < e[0])
      return [
        [n[0] + i, n[1], e[2], n[3]],
        [e[0], n[1], n[2], n[3]]
      ];
    if (n[2] > e[2])
      return [
        [n[0], n[1], e[2], n[3]],
        [e[0], n[1], n[2] - i, n[3]]
      ];
  }
  return [n];
}
function Et(n, t, e) {
  return Math.min(Math.max(n, t), e);
}
function i0(n, t, e, i, s, r) {
  const o = s - e, a = r - i;
  if (o !== 0 || a !== 0) {
    const l = ((n - e) * o + (t - i) * a) / (o * o + a * a);
    l > 1 ? (e = s, i = r) : l > 0 && (e += o * l, i += a * l);
  }
  return ri(n, t, e, i);
}
function ri(n, t, e, i) {
  const s = e - n, r = i - t;
  return s * s + r * r;
}
function n0(n) {
  const t = n.length;
  for (let i = 0; i < t; i++) {
    let s = i, r = Math.abs(n[i][i]);
    for (let a = i + 1; a < t; a++) {
      const l = Math.abs(n[a][i]);
      l > r && (r = l, s = a);
    }
    if (r === 0)
      return null;
    const o = n[s];
    n[s] = n[i], n[i] = o;
    for (let a = i + 1; a < t; a++) {
      const l = -n[a][i] / n[i][i];
      for (let h = i; h < t + 1; h++)
        i == h ? n[a][h] = 0 : n[a][h] += l * n[i][h];
    }
  }
  const e = new Array(t);
  for (let i = t - 1; i >= 0; i--) {
    e[i] = n[i][t] / n[i][i];
    for (let s = i - 1; s >= 0; s--)
      n[s][t] -= n[s][i] * e[i];
  }
  return e;
}
function Bh(n) {
  return n * 180 / Math.PI;
}
function ji(n) {
  return n * Math.PI / 180;
}
function qi(n, t) {
  const e = n % t;
  return e * t < 0 ? e + t : e;
}
function ii(n, t, e) {
  return n + e * (t - n);
}
function xl(n, t) {
  const e = Math.pow(10, t);
  return Math.round(n * e) / e;
}
function wr(n, t) {
  return Math.floor(xl(n, t));
}
function Sr(n, t) {
  return Math.ceil(xl(n, t));
}
const s0 = /^#([a-f0-9]{3}|[a-f0-9]{4}(?:[a-f0-9]{2}){0,2})$/i, r0 = /^([a-z]*)$|^hsla?\(.*\)$/i;
function td(n) {
  return typeof n == "string" ? n : ed(n);
}
function o0(n) {
  const t = document.createElement("div");
  if (t.style.color = n, t.style.color !== "") {
    document.body.appendChild(t);
    const e = getComputedStyle(t).color;
    return document.body.removeChild(t), e;
  } else
    return "";
}
const a0 = function() {
  const t = {};
  let e = 0;
  return function(i) {
    let s;
    if (t.hasOwnProperty(i))
      s = t[i];
    else {
      if (e >= 1024) {
        let r = 0;
        for (const o in t)
          (r++ & 3) === 0 && (delete t[o], --e);
      }
      s = l0(i), t[i] = s, ++e;
    }
    return s;
  };
}();
function Qr(n) {
  return Array.isArray(n) ? n : a0(n);
}
function l0(n) {
  let t, e, i, s, r;
  if (r0.exec(n) && (n = o0(n)), s0.exec(n)) {
    const o = n.length - 1;
    let a;
    o <= 4 ? a = 1 : a = 2;
    const l = o === 4 || o === 8;
    t = parseInt(n.substr(1 + 0 * a, a), 16), e = parseInt(n.substr(1 + 1 * a, a), 16), i = parseInt(n.substr(1 + 2 * a, a), 16), l ? s = parseInt(n.substr(1 + 3 * a, a), 16) : s = 255, a == 1 && (t = (t << 4) + t, e = (e << 4) + e, i = (i << 4) + i, l && (s = (s << 4) + s)), r = [t, e, i, s / 255];
  } else
    n.startsWith("rgba(") ? (r = n.slice(5, -1).split(",").map(Number), zh(r)) : n.startsWith("rgb(") ? (r = n.slice(4, -1).split(",").map(Number), r.push(1), zh(r)) : Y(!1, 14);
  return r;
}
function zh(n) {
  return n[0] = Et(n[0] + 0.5 | 0, 0, 255), n[1] = Et(n[1] + 0.5 | 0, 0, 255), n[2] = Et(n[2] + 0.5 | 0, 0, 255), n[3] = Et(n[3], 0, 1), n;
}
function ed(n) {
  let t = n[0];
  t != (t | 0) && (t = t + 0.5 | 0);
  let e = n[1];
  e != (e | 0) && (e = e + 0.5 | 0);
  let i = n[2];
  i != (i | 0) && (i = i + 0.5 | 0);
  const s = n[3] === void 0 ? 1 : Math.round(n[3] * 100) / 100;
  return "rgba(" + t + "," + e + "," + i + "," + s + ")";
}
class h0 {
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
        const i = this.cache_[e];
        (t++ & 3) === 0 && !i.hasListener() && (delete this.cache_[e], --this.cacheSize_);
      }
    }
  }
  get(t, e, i) {
    const s = Zh(t, e, i);
    return s in this.cache_ ? this.cache_[s] : null;
  }
  set(t, e, i, s) {
    const r = Zh(t, e, i);
    this.cache_[r] = s, ++this.cacheSize_;
  }
  setSize(t) {
    this.maxCacheSize_ = t, this.expire();
  }
}
function Zh(n, t, e) {
  const i = e ? td(e) : "null";
  return t + ":" + n + ":" + i;
}
const to = new h0(), ft = {
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
class c0 extends Oe {
  constructor(t) {
    super(), this.on, this.once, this.un, this.background_ = t.background;
    const e = Object.assign({}, t);
    typeof t.properties == "object" && (delete e.properties, Object.assign(e, t.properties)), e[ft.OPACITY] = t.opacity !== void 0 ? t.opacity : 1, Y(typeof e[ft.OPACITY] == "number", 64), e[ft.VISIBLE] = t.visible !== void 0 ? t.visible : !0, e[ft.Z_INDEX] = t.zIndex, e[ft.MAX_RESOLUTION] = t.maxResolution !== void 0 ? t.maxResolution : 1 / 0, e[ft.MIN_RESOLUTION] = t.minResolution !== void 0 ? t.minResolution : 0, e[ft.MIN_ZOOM] = t.minZoom !== void 0 ? t.minZoom : -1 / 0, e[ft.MAX_ZOOM] = t.maxZoom !== void 0 ? t.maxZoom : 1 / 0, this.className_ = e.className !== void 0 ? e.className : "ol-layer", delete e.className, this.setProperties(e), this.state_ = null;
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
    }, i = this.getZIndex();
    return e.opacity = Et(Math.round(this.getOpacity() * 100) / 100, 0, 1), e.visible = this.getVisible(), e.extent = this.getExtent(), e.zIndex = i === void 0 && !e.managed ? 1 / 0 : i, e.maxResolution = this.getMaxResolution(), e.minResolution = Math.max(this.getMinResolution(), 0), e.minZoom = this.getMinZoom(), e.maxZoom = this.getMaxZoom(), this.state_ = e, e;
  }
  getLayersArray(t) {
    return H();
  }
  getLayerStatesArray(t) {
    return H();
  }
  getExtent() {
    return this.get(ft.EXTENT);
  }
  getMaxResolution() {
    return this.get(ft.MAX_RESOLUTION);
  }
  getMinResolution() {
    return this.get(ft.MIN_RESOLUTION);
  }
  getMinZoom() {
    return this.get(ft.MIN_ZOOM);
  }
  getMaxZoom() {
    return this.get(ft.MAX_ZOOM);
  }
  getOpacity() {
    return this.get(ft.OPACITY);
  }
  getSourceState() {
    return H();
  }
  getVisible() {
    return this.get(ft.VISIBLE);
  }
  getZIndex() {
    return this.get(ft.Z_INDEX);
  }
  setBackground(t) {
    this.background_ = t, this.changed();
  }
  setExtent(t) {
    this.set(ft.EXTENT, t);
  }
  setMaxResolution(t) {
    this.set(ft.MAX_RESOLUTION, t);
  }
  setMinResolution(t) {
    this.set(ft.MIN_RESOLUTION, t);
  }
  setMaxZoom(t) {
    this.set(ft.MAX_ZOOM, t);
  }
  setMinZoom(t) {
    this.set(ft.MIN_ZOOM, t);
  }
  setOpacity(t) {
    Y(typeof t == "number", 64), this.set(ft.OPACITY, t);
  }
  setVisible(t) {
    this.set(ft.VISIBLE, t);
  }
  setZIndex(t) {
    this.set(ft.Z_INDEX, t);
  }
  disposeInternal() {
    this.state_ && (this.state_.layer = null, this.state_ = null), super.disposeInternal();
  }
}
const id = c0, Ri = {
  PRERENDER: "prerender",
  POSTRENDER: "postrender",
  PRECOMPOSE: "precompose",
  POSTCOMPOSE: "postcompose",
  RENDERCOMPLETE: "rendercomplete"
};
class u0 extends id {
  constructor(t) {
    const e = Object.assign({}, t);
    delete e.source, super(e), this.on, this.once, this.un, this.mapPrecomposeKey_ = null, this.mapRenderKey_ = null, this.sourceChangeKey_ = null, this.renderer_ = null, this.rendered = !1, t.render && (this.render = t.render), t.map && this.setMap(t.map), this.addChangeListener(
      ft.SOURCE,
      this.handleSourcePropertyChange_
    );
    const i = t.source ? t.source : null;
    this.setSource(i);
  }
  getLayersArray(t) {
    return t = t || [], t.push(this), t;
  }
  getLayerStatesArray(t) {
    return t = t || [], t.push(this.getLayerState()), t;
  }
  getSource() {
    return this.get(ft.SOURCE) || null;
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
    this.sourceChangeKey_ && (mt(this.sourceChangeKey_), this.sourceChangeKey_ = null);
    const t = this.getSource();
    t && (this.sourceChangeKey_ = et(
      t,
      U.CHANGE,
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
    const i = this.getRenderer();
    if (i.prepareFrame(t))
      return this.rendered = !0, i.renderFrame(t, e);
  }
  unrender() {
    this.rendered = !1;
  }
  setMapInternal(t) {
    t || this.unrender(), this.set(ft.MAP, t);
  }
  getMapInternal() {
    return this.get(ft.MAP);
  }
  setMap(t) {
    this.mapPrecomposeKey_ && (mt(this.mapPrecomposeKey_), this.mapPrecomposeKey_ = null), t || this.changed(), this.mapRenderKey_ && (mt(this.mapRenderKey_), this.mapRenderKey_ = null), t && (this.mapPrecomposeKey_ = et(
      t,
      Ri.PRECOMPOSE,
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
    ), this.mapRenderKey_ = et(this, U.CHANGE, t.render, t), this.changed());
  }
  setSource(t) {
    this.set(ft.SOURCE, t);
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
function Cl(n, t) {
  if (!n.visible)
    return !1;
  const e = t.resolution;
  if (e < n.minResolution || e >= n.maxResolution)
    return !1;
  const i = t.zoom;
  return i > n.minZoom && i <= n.maxZoom;
}
const Po = u0;
function nd(n, t) {
  return n[0] += +t[0], n[1] += +t[1], n;
}
function d0(n, t) {
  const e = t.getRadius(), i = t.getCenter(), s = i[0], r = i[1], o = n[0], a = n[1];
  let l = o - s;
  const h = a - r;
  l === 0 && h === 0 && (l = 1);
  const c = Math.sqrt(l * l + h * h), u = s + e * l / c, d = r + e * h / c;
  return [u, d];
}
function Ml(n, t) {
  const e = n[0], i = n[1], s = t[0], r = t[1], o = s[0], a = s[1], l = r[0], h = r[1], c = l - o, u = h - a, d = c === 0 && u === 0 ? 0 : (c * (e - o) + u * (i - a)) / (c * c + u * u || 0);
  let f, g;
  return d <= 0 ? (f = o, g = a) : d >= 1 ? (f = l, g = h) : (f = o + d * c, g = a + d * u), [f, g];
}
function Le(n, t) {
  let e = !0;
  for (let i = n.length - 1; i >= 0; --i)
    if (n[i] != t[i]) {
      e = !1;
      break;
    }
  return e;
}
function El(n, t) {
  const e = Math.cos(t), i = Math.sin(t), s = n[0] * e - n[1] * i, r = n[1] * e + n[0] * i;
  return n[0] = s, n[1] = r, n;
}
function sd(n, t) {
  return n[0] *= t, n[1] *= t, n;
}
function oi(n, t) {
  const e = n[0] - t[0], i = n[1] - t[1];
  return e * e + i * i;
}
function eo(n, t) {
  return Math.sqrt(oi(n, t));
}
function f0(n, t) {
  return oi(n, Ml(n, t));
}
function rd(n, t) {
  if (t.canWrapX()) {
    const e = pt(t.getExtent()), i = od(n, t, e);
    i && (n[0] -= i * e);
  }
  return n;
}
function od(n, t, e) {
  const i = t.getExtent();
  let s = 0;
  return t.canWrapX() && (n[0] < i[0] || n[0] > i[2]) && (e = e || pt(i), s = Math.floor(
    (n[0] - i[0]) / e
  )), s;
}
class g0 extends fl {
  constructor(t) {
    super(), this.map_ = t;
  }
  dispatchRenderEvent(t, e) {
    H();
  }
  calculateMatrices2D(t) {
    const e = t.viewState, i = t.coordinateToPixelTransform, s = t.pixelToCoordinateTransform;
    Ii(
      i,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / e.resolution,
      -1 / e.resolution,
      -e.rotation,
      -e.center[0],
      -e.center[1]
    ), _l(s, i);
  }
  forEachFeatureAtCoordinate(t, e, i, s, r, o, a, l) {
    let h;
    const c = e.viewState;
    function u(x, C, E, R) {
      return r.call(o, C, x ? E : null, R);
    }
    const d = c.projection, f = rd(t.slice(), d), g = [[0, 0]];
    if (d.canWrapX() && s) {
      const x = d.getExtent(), C = pt(x);
      g.push([-C, 0], [C, 0]);
    }
    const m = e.layerStatesArray, _ = m.length, y = [], p = [];
    for (let x = 0; x < g.length; x++)
      for (let C = _ - 1; C >= 0; --C) {
        const E = m[C], R = E.layer;
        if (R.hasRenderer() && Cl(E, c) && a.call(l, R)) {
          const b = R.getRenderer(), F = R.getSource();
          if (b && F) {
            const G = F.getWrapX() ? f : t, V = u.bind(
              null,
              E.managed
            );
            p[0] = G[0] + g[x][0], p[1] = G[1] + g[x][1], h = b.forEachFeatureAtCoordinate(
              p,
              e,
              i,
              V,
              y
            );
          }
          if (h)
            return h;
        }
      }
    if (y.length === 0)
      return;
    const v = 1 / y.length;
    return y.forEach((x, C) => x.distanceSq += C * v), y.sort((x, C) => x.distanceSq - C.distanceSq), y.some((x) => h = x.callback(x.feature, x.layer, x.geometry)), h;
  }
  hasFeatureAtCoordinate(t, e, i, s, r, o) {
    return this.forEachFeatureAtCoordinate(
      t,
      e,
      i,
      s,
      en,
      this,
      r,
      o
    ) !== void 0;
  }
  getMap() {
    return this.map_;
  }
  renderFrame(t) {
    H();
  }
  scheduleExpireIconCache(t) {
    to.canExpireCache() && t.postRenderFunctions.push(m0);
  }
}
function m0(n, t) {
  to.expire();
}
const _0 = g0;
class p0 extends Re {
  constructor(t, e, i, s) {
    super(t), this.inversePixelTransform = e, this.frameState = i, this.context = s;
  }
}
const ad = p0, Rr = "ol-hidden", ss = "ol-unselectable", Vh = "ol-unsupported", Ao = "ol-control", Uh = "ol-collapsed", y0 = new RegExp(
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
), Wh = [
  "style",
  "variant",
  "weight",
  "size",
  "lineHeight",
  "family"
], ld = function(n) {
  const t = n.match(y0);
  if (!t)
    return null;
  const e = {
    lineHeight: "normal",
    size: "1.2em",
    style: "normal",
    weight: "normal",
    variant: "normal"
  };
  for (let i = 0, s = Wh.length; i < s; ++i) {
    const r = t[i + 1];
    r !== void 0 && (e[Wh[i]] = r);
  }
  return e.families = e.family.split(/,\s?/), e;
};
function pe(n, t, e, i) {
  let s;
  return e && e.length ? s = e.shift() : ml ? s = new OffscreenCanvas(n || 300, t || 300) : s = document.createElement("canvas"), n && (s.width = n), t && (s.height = t), s.getContext("2d", i);
}
function hd(n) {
  const t = n.canvas;
  t.width = 1, t.height = 1, n.clearRect(0, 0, 1, 1);
}
function io(n, t) {
  const e = t.parentNode;
  e && e.replaceChild(n, t);
}
function Aa(n) {
  return n && n.parentNode ? n.parentNode.removeChild(n) : null;
}
function v0(n) {
  for (; n.lastChild; )
    n.removeChild(n.lastChild);
}
function x0(n, t) {
  const e = n.childNodes;
  for (let i = 0; ; ++i) {
    const s = e[i], r = t[i];
    if (!s && !r)
      break;
    if (s !== r) {
      if (!s) {
        n.appendChild(r);
        continue;
      }
      if (!r) {
        n.removeChild(s), --i;
        continue;
      }
      n.insertBefore(r, s);
    }
  }
}
const cd = "10px sans-serif", ai = "#000", no = "round", Ns = [], Ds = 0, Xn = "round", ks = 10, Gs = "#000", $s = "center", so = "middle", Ui = [0, 0, 0, 0], Bs = 1, ti = new Oe();
let Rn = null, Oa;
const Fa = {}, C0 = function() {
  const t = "32px ", e = ["monospace", "serif"], i = e.length, s = "wmytzilWMYTZIL@#/&?$%10\uF013";
  let r, o;
  function a(h, c, u) {
    let d = !0;
    for (let f = 0; f < i; ++f) {
      const g = e[f];
      if (o = ro(
        h + " " + c + " " + t + g,
        s
      ), u != g) {
        const m = ro(
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
    const c = ti.getKeys();
    for (let u = 0, d = c.length; u < d; ++u) {
      const f = c[u];
      ti.get(f) < 100 && (a.apply(this, f.split(`
`)) ? (Ks(Fa), Rn = null, Oa = void 0, ti.set(f, 100)) : (ti.set(f, ti.get(f) + 1, !0), h = !1));
    }
    h && (clearInterval(r), r = void 0);
  }
  return function(h) {
    const c = ld(h);
    if (!c)
      return;
    const u = c.families;
    for (let d = 0, f = u.length; d < f; ++d) {
      const g = u[d], m = c.style + `
` + c.weight + `
` + g;
      ti.get(m) === void 0 && (ti.set(m, 100, !0), a(c.style, c.weight, g) || (ti.set(m, 0, !0), r === void 0 && (r = setInterval(l, 32))));
    }
  };
}(), M0 = function() {
  let n;
  return function(t) {
    let e = Fa[t];
    if (e == null) {
      if (ml) {
        const i = ld(t), s = ud(t, "\u017Dg");
        e = (isNaN(Number(i.lineHeight)) ? 1.2 : Number(i.lineHeight)) * (s.actualBoundingBoxAscent + s.actualBoundingBoxDescent);
      } else
        n || (n = document.createElement("div"), n.innerHTML = "M", n.style.minHeight = "0", n.style.maxHeight = "none", n.style.height = "auto", n.style.padding = "0", n.style.border = "none", n.style.position = "absolute", n.style.display = "block", n.style.left = "-99999px"), n.style.font = t, document.body.appendChild(n), e = n.offsetHeight, document.body.removeChild(n);
      Fa[t] = e;
    }
    return e;
  };
}();
function ud(n, t) {
  return Rn || (Rn = pe(1, 1)), n != Oa && (Rn.font = n, Oa = Rn.font), Rn.measureText(t);
}
function ro(n, t) {
  return ud(n, t).width;
}
function Hh(n, t, e) {
  if (t in e)
    return e[t];
  const i = t.split(`
`).reduce((s, r) => Math.max(s, ro(n, r)), 0);
  return e[t] = i, i;
}
function E0(n, t) {
  const e = [], i = [], s = [];
  let r = 0, o = 0, a = 0, l = 0;
  for (let h = 0, c = t.length; h <= c; h += 2) {
    const u = t[h];
    if (u === `
` || h === c) {
      r = Math.max(r, o), s.push(o), o = 0, a += l;
      continue;
    }
    const d = t[h + 1] || n.font, f = ro(d, u);
    e.push(f), o += f;
    const g = M0(d);
    i.push(g), l = Math.max(l, g);
  }
  return { width: r, height: a, widths: e, heights: i, lineWidths: s };
}
function w0(n, t, e, i, s, r, o, a, l, h, c) {
  n.save(), e !== 1 && (n.globalAlpha *= e), t && n.setTransform.apply(n, t), i.contextInstructions ? (n.translate(l, h), n.scale(c[0], c[1]), S0(i, n)) : c[0] < 0 || c[1] < 0 ? (n.translate(l, h), n.scale(c[0], c[1]), n.drawImage(
    i,
    s,
    r,
    o,
    a,
    0,
    0,
    o,
    a
  )) : n.drawImage(
    i,
    s,
    r,
    o,
    a,
    l,
    h,
    o * c[0],
    a * c[1]
  ), n.restore();
}
function S0(n, t) {
  const e = n.contextInstructions;
  for (let i = 0, s = e.length; i < s; i += 2)
    Array.isArray(e[i + 1]) ? t[e[i]].apply(
      t,
      e[i + 1]
    ) : t[e[i]] = e[i + 1];
}
class R0 extends _0 {
  constructor(t) {
    super(t), this.fontChangeListenerKey_ = et(
      ti,
      Wn.PROPERTYCHANGE,
      t.redrawText.bind(t)
    ), this.element_ = document.createElement("div");
    const e = this.element_.style;
    e.position = "absolute", e.width = "100%", e.height = "100%", e.zIndex = "0", this.element_.className = ss + " ol-layers";
    const i = t.getViewport();
    i.insertBefore(this.element_, i.firstChild || null), this.children_ = [], this.renderedVisible_ = !0;
  }
  dispatchRenderEvent(t, e) {
    const i = this.getMap();
    if (i.hasListener(t)) {
      const s = new ad(t, void 0, e);
      i.dispatchEvent(s);
    }
  }
  disposeInternal() {
    mt(this.fontChangeListenerKey_), this.element_.parentNode.removeChild(this.element_), super.disposeInternal();
  }
  renderFrame(t) {
    if (!t) {
      this.renderedVisible_ && (this.element_.style.display = "none", this.renderedVisible_ = !1);
      return;
    }
    this.calculateMatrices2D(t), this.dispatchRenderEvent(Ri.PRECOMPOSE, t);
    const e = t.layerStatesArray.sort(function(o, a) {
      return o.zIndex - a.zIndex;
    }), i = t.viewState;
    this.children_.length = 0;
    const s = [];
    let r = null;
    for (let o = 0, a = e.length; o < a; ++o) {
      const l = e[o];
      t.layerIndex = o;
      const h = l.layer, c = h.getSourceState();
      if (!Cl(l, i) || c != "ready" && c != "undefined") {
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
    x0(this.element_, this.children_), this.dispatchRenderEvent(Ri.POSTCOMPOSE, t), this.renderedVisible_ || (this.element_.style.display = "", this.renderedVisible_ = !0), this.scheduleExpireIconCache(t);
  }
}
const T0 = R0;
class Ci extends Re {
  constructor(t, e) {
    super(t), this.layer = e;
  }
}
const sa = {
  LAYERS: "layers"
};
class wl extends id {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.layers;
    let i = t.layers;
    super(e), this.on, this.once, this.un, this.layersListenerKeys_ = [], this.listenerKeys_ = {}, this.addChangeListener(sa.LAYERS, this.handleLayersChanged_), i ? Array.isArray(i) ? i = new Ee(i.slice(), { unique: !0 }) : Y(typeof i.getArray == "function", 43) : i = new Ee(void 0, { unique: !0 }), this.setLayers(i);
  }
  handleLayerChange_() {
    this.changed();
  }
  handleLayersChanged_() {
    this.layersListenerKeys_.forEach(mt), this.layersListenerKeys_.length = 0;
    const t = this.getLayers();
    this.layersListenerKeys_.push(
      et(t, Dt.ADD, this.handleLayersAdd_, this),
      et(t, Dt.REMOVE, this.handleLayersRemove_, this)
    );
    for (const i in this.listenerKeys_)
      this.listenerKeys_[i].forEach(mt);
    Ks(this.listenerKeys_);
    const e = t.getArray();
    for (let i = 0, s = e.length; i < s; i++) {
      const r = e[i];
      this.registerLayerListeners_(r), this.dispatchEvent(new Ci("addlayer", r));
    }
    this.changed();
  }
  registerLayerListeners_(t) {
    const e = [
      et(
        t,
        Wn.PROPERTYCHANGE,
        this.handleLayerChange_,
        this
      ),
      et(t, U.CHANGE, this.handleLayerChange_, this)
    ];
    t instanceof wl && e.push(
      et(t, "addlayer", this.handleLayerGroupAdd_, this),
      et(t, "removelayer", this.handleLayerGroupRemove_, this)
    ), this.listenerKeys_[q(t)] = e;
  }
  handleLayerGroupAdd_(t) {
    this.dispatchEvent(new Ci("addlayer", t.layer));
  }
  handleLayerGroupRemove_(t) {
    this.dispatchEvent(new Ci("removelayer", t.layer));
  }
  handleLayersAdd_(t) {
    const e = t.element;
    this.registerLayerListeners_(e), this.dispatchEvent(new Ci("addlayer", e)), this.changed();
  }
  handleLayersRemove_(t) {
    const e = t.element, i = q(e);
    this.listenerKeys_[i].forEach(mt), delete this.listenerKeys_[i], this.dispatchEvent(new Ci("removelayer", e)), this.changed();
  }
  getLayers() {
    return this.get(sa.LAYERS);
  }
  setLayers(t) {
    const e = this.getLayers();
    if (e) {
      const i = e.getArray();
      for (let s = 0, r = i.length; s < r; ++s)
        this.dispatchEvent(new Ci("removelayer", i[s]));
    }
    this.set(sa.LAYERS, t);
  }
  getLayersArray(t) {
    return t = t !== void 0 ? t : [], this.getLayers().forEach(function(e) {
      e.getLayersArray(t);
    }), t;
  }
  getLayerStatesArray(t) {
    const e = t !== void 0 ? t : [], i = e.length;
    this.getLayers().forEach(function(o) {
      o.getLayerStatesArray(e);
    });
    const s = this.getLayerState();
    let r = s.zIndex;
    !t && s.zIndex === void 0 && (r = 0);
    for (let o = i, a = e.length; o < a; o++) {
      const l = e[o];
      l.opacity *= s.opacity, l.visible = l.visible && s.visible, l.maxResolution = Math.min(
        l.maxResolution,
        s.maxResolution
      ), l.minResolution = Math.max(
        l.minResolution,
        s.minResolution
      ), l.minZoom = Math.max(l.minZoom, s.minZoom), l.maxZoom = Math.min(l.maxZoom, s.maxZoom), s.extent !== void 0 && (l.extent !== void 0 ? l.extent = Rs(
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
const Oo = wl;
class b0 extends Re {
  constructor(t, e, i) {
    super(t), this.map = e, this.frameState = i !== void 0 ? i : null;
  }
}
const Tn = b0;
class L0 extends Tn {
  constructor(t, e, i, s, r, o) {
    super(t, e, r), this.originalEvent = i, this.pixel_ = null, this.coordinate_ = null, this.dragging = s !== void 0 ? s : !1, this.activePointers = o;
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
const ei = L0, nt = {
  SINGLECLICK: "singleclick",
  CLICK: U.CLICK,
  DBLCLICK: U.DBLCLICK,
  POINTERDRAG: "pointerdrag",
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
}, Na = {
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
};
class I0 extends So {
  constructor(t, e) {
    super(t), this.map_ = t, this.clickTimeoutId_, this.emulateClicks_ = !1, this.dragging_ = !1, this.dragListenerKeys_ = [], this.moveTolerance_ = e === void 0 ? 1 : e, this.down_ = null;
    const i = this.map_.getViewport();
    this.activePointers_ = [], this.trackedTouches_ = {}, this.element_ = i, this.pointerdownListenerKey_ = et(
      i,
      Na.POINTERDOWN,
      this.handlePointerDown_,
      this
    ), this.originalPointerMoveEvent_, this.relayedListenerKey_ = et(
      i,
      Na.POINTERMOVE,
      this.relayMoveEvent_,
      this
    ), this.boundHandleTouchMove_ = this.handleTouchMove_.bind(this), this.element_.addEventListener(
      U.TOUCHMOVE,
      this.boundHandleTouchMove_,
      Xu ? { passive: !1 } : !1
    );
  }
  emulateClick_(t) {
    let e = new ei(
      nt.CLICK,
      this.map_,
      t
    );
    this.dispatchEvent(e), this.clickTimeoutId_ !== void 0 ? (clearTimeout(this.clickTimeoutId_), this.clickTimeoutId_ = void 0, e = new ei(
      nt.DBLCLICK,
      this.map_,
      t
    ), this.dispatchEvent(e)) : this.clickTimeoutId_ = setTimeout(
      function() {
        this.clickTimeoutId_ = void 0;
        const i = new ei(
          nt.SINGLECLICK,
          this.map_,
          t
        );
        this.dispatchEvent(i);
      }.bind(this),
      250
    );
  }
  updateActivePointers_(t) {
    const e = t, i = e.pointerId;
    if (e.type == nt.POINTERUP || e.type == nt.POINTERCANCEL) {
      delete this.trackedTouches_[i];
      for (const s in this.trackedTouches_)
        if (this.trackedTouches_[s].target !== e.target) {
          delete this.trackedTouches_[s];
          break;
        }
    } else
      (e.type == nt.POINTERDOWN || e.type == nt.POINTERMOVE) && (this.trackedTouches_[i] = e);
    this.activePointers_ = Object.values(this.trackedTouches_);
  }
  handlePointerUp_(t) {
    this.updateActivePointers_(t);
    const e = new ei(
      nt.POINTERUP,
      this.map_,
      t,
      void 0,
      void 0,
      this.activePointers_
    );
    this.dispatchEvent(e), this.emulateClicks_ && !e.defaultPrevented && !this.dragging_ && this.isMouseActionButton_(t) && this.emulateClick_(this.down_), this.activePointers_.length === 0 && (this.dragListenerKeys_.forEach(mt), this.dragListenerKeys_.length = 0, this.dragging_ = !1, this.down_ = null);
  }
  isMouseActionButton_(t) {
    return t.button === 0;
  }
  handlePointerDown_(t) {
    this.emulateClicks_ = this.activePointers_.length === 0, this.updateActivePointers_(t);
    const e = new ei(
      nt.POINTERDOWN,
      this.map_,
      t,
      void 0,
      void 0,
      this.activePointers_
    );
    this.dispatchEvent(e), this.down_ = {};
    for (const i in t) {
      const s = t[i];
      this.down_[i] = typeof s == "function" ? nn : s;
    }
    if (this.dragListenerKeys_.length === 0) {
      const i = this.map_.getOwnerDocument();
      this.dragListenerKeys_.push(
        et(
          i,
          nt.POINTERMOVE,
          this.handlePointerMove_,
          this
        ),
        et(i, nt.POINTERUP, this.handlePointerUp_, this),
        et(
          this.element_,
          nt.POINTERCANCEL,
          this.handlePointerUp_,
          this
        )
      ), this.element_.getRootNode && this.element_.getRootNode() !== i && this.dragListenerKeys_.push(
        et(
          this.element_.getRootNode(),
          nt.POINTERUP,
          this.handlePointerUp_,
          this
        )
      );
    }
  }
  handlePointerMove_(t) {
    if (this.isMoving_(t)) {
      this.updateActivePointers_(t), this.dragging_ = !0;
      const e = new ei(
        nt.POINTERDRAG,
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
      new ei(
        nt.POINTERMOVE,
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
    this.relayedListenerKey_ && (mt(this.relayedListenerKey_), this.relayedListenerKey_ = null), this.element_.removeEventListener(
      U.TOUCHMOVE,
      this.boundHandleTouchMove_
    ), this.pointerdownListenerKey_ && (mt(this.pointerdownListenerKey_), this.pointerdownListenerKey_ = null), this.dragListenerKeys_.forEach(mt), this.dragListenerKeys_.length = 0, this.element_ = null, super.disposeInternal();
  }
}
const P0 = I0, vi = {
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
}, oo = 1 / 0;
class A0 {
  constructor(t, e) {
    this.priorityFunction_ = t, this.keyFunction_ = e, this.elements_ = [], this.priorities_ = [], this.queuedElements_ = {};
  }
  clear() {
    this.elements_.length = 0, this.priorities_.length = 0, Ks(this.queuedElements_);
  }
  dequeue() {
    const t = this.elements_, e = this.priorities_, i = t[0];
    t.length == 1 ? (t.length = 0, e.length = 0) : (t[0] = t.pop(), e[0] = e.pop(), this.siftUp_(0));
    const s = this.keyFunction_(i);
    return delete this.queuedElements_[s], i;
  }
  enqueue(t) {
    Y(!(this.keyFunction_(t) in this.queuedElements_), 31);
    const e = this.priorityFunction_(t);
    return e != oo ? (this.elements_.push(t), this.priorities_.push(e), this.queuedElements_[this.keyFunction_(t)] = !0, this.siftDown_(0, this.elements_.length - 1), !0) : !1;
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
    const e = this.elements_, i = this.priorities_, s = e.length, r = e[t], o = i[t], a = t;
    for (; t < s >> 1; ) {
      const l = this.getLeftChildIndex_(t), h = this.getRightChildIndex_(t), c = h < s && i[h] < i[l] ? h : l;
      e[t] = e[c], i[t] = i[c], t = c;
    }
    e[t] = r, i[t] = o, this.siftDown_(a, t);
  }
  siftDown_(t, e) {
    const i = this.elements_, s = this.priorities_, r = i[e], o = s[e];
    for (; e > t; ) {
      const a = this.getParentIndex_(e);
      if (s[a] > o)
        i[e] = i[a], s[e] = s[a], e = a;
      else
        break;
    }
    i[e] = r, s[e] = o;
  }
  reprioritize() {
    const t = this.priorityFunction_, e = this.elements_, i = this.priorities_;
    let s = 0;
    const r = e.length;
    let o, a, l;
    for (a = 0; a < r; ++a)
      o = e[a], l = t(o), l == oo ? delete this.queuedElements_[this.keyFunction_(o)] : (i[s] = l, e[s++] = o);
    e.length = s, i.length = s, this.heapify_();
  }
}
const O0 = A0, z = {
  IDLE: 0,
  LOADING: 1,
  LOADED: 2,
  ERROR: 3,
  EMPTY: 4
};
class F0 extends O0 {
  constructor(t, e) {
    super(
      function(i) {
        return t.apply(null, i);
      },
      function(i) {
        return i[0].getKey();
      }
    ), this.boundHandleTileChange_ = this.handleTileChange.bind(this), this.tileChangeCallback_ = e, this.tilesLoading_ = 0, this.tilesLoadingKeys_ = {};
  }
  enqueue(t) {
    const e = super.enqueue(t);
    return e && t[0].addEventListener(U.CHANGE, this.boundHandleTileChange_), e;
  }
  getTilesLoading() {
    return this.tilesLoading_;
  }
  handleTileChange(t) {
    const e = t.target, i = e.getState();
    if (i === z.LOADED || i === z.ERROR || i === z.EMPTY) {
      i !== z.ERROR && e.removeEventListener(U.CHANGE, this.boundHandleTileChange_);
      const s = e.getKey();
      s in this.tilesLoadingKeys_ && (delete this.tilesLoadingKeys_[s], --this.tilesLoading_), this.tileChangeCallback_();
    }
  }
  loadMoreTiles(t, e) {
    let i = 0, s, r, o;
    for (; this.tilesLoading_ < t && i < e && this.getCount() > 0; )
      r = this.dequeue()[0], o = r.getKey(), s = r.getState(), s === z.IDLE && !(o in this.tilesLoadingKeys_) && (this.tilesLoadingKeys_[o] = !0, ++this.tilesLoading_, ++i, r.load());
  }
}
const N0 = F0;
function D0(n, t, e, i, s) {
  if (!n || !(e in n.wantedTiles) || !n.wantedTiles[e][t.getKey()])
    return oo;
  const r = n.viewState.center, o = i[0] - r[0], a = i[1] - r[1];
  return 65536 * Math.log(s) + Math.sqrt(o * o + a * a) / s;
}
const Wt = {
  ANIMATING: 0,
  INTERACTING: 1
}, be = {
  CENTER: "center",
  RESOLUTION: "resolution",
  ROTATION: "rotation"
}, k0 = 42, Sl = 256, Yn = {
  radians: 6370997 / (2 * Math.PI),
  degrees: 2 * Math.PI * 6370997 / 360,
  ft: 0.3048,
  m: 1,
  "us-ft": 1200 / 3937
};
class G0 {
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
    return this.metersPerUnit_ || Yn[this.units_];
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
const Rl = G0, tr = 6378137, Pn = Math.PI * tr, $0 = [-Pn, -Pn, Pn, Pn], B0 = [-180, -85, 180, 85], Tr = tr * Math.log(Math.tan(Math.PI / 2));
class Cn extends Rl {
  constructor(t) {
    super({
      code: t,
      units: "m",
      extent: $0,
      global: !0,
      worldExtent: B0,
      getPointResolution: function(e, i) {
        return e / Math.cosh(i[1] / tr);
      }
    });
  }
}
const Xh = [
  new Cn("EPSG:3857"),
  new Cn("EPSG:102100"),
  new Cn("EPSG:102113"),
  new Cn("EPSG:900913"),
  new Cn("http://www.opengis.net/def/crs/EPSG/0/3857"),
  new Cn("http://www.opengis.net/gml/srs/epsg.xml#3857")
];
function z0(n, t, e) {
  const i = n.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = n.slice() : t = new Array(i));
  for (let s = 0; s < i; s += e) {
    t[s] = Pn * n[s] / 180;
    let r = tr * Math.log(Math.tan(Math.PI * (+n[s + 1] + 90) / 360));
    r > Tr ? r = Tr : r < -Tr && (r = -Tr), t[s + 1] = r;
  }
  return t;
}
function Z0(n, t, e) {
  const i = n.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = n.slice() : t = new Array(i));
  for (let s = 0; s < i; s += e)
    t[s] = 180 * n[s] / Pn, t[s + 1] = 360 * Math.atan(Math.exp(n[s + 1] / tr)) / Math.PI - 90;
  return t;
}
const V0 = 6378137, Yh = [-180, -90, 180, 90], U0 = Math.PI * V0 / 180;
class Bi extends Rl {
  constructor(t, e) {
    super({
      code: t,
      units: "degrees",
      extent: Yh,
      axisOrientation: e,
      global: !0,
      metersPerUnit: U0,
      worldExtent: Yh
    });
  }
}
const jh = [
  new Bi("CRS:84"),
  new Bi("EPSG:4326", "neu"),
  new Bi("urn:ogc:def:crs:OGC:1.3:CRS84"),
  new Bi("urn:ogc:def:crs:OGC:2:84"),
  new Bi("http://www.opengis.net/def/crs/OGC/1.3/CRS84"),
  new Bi("http://www.opengis.net/gml/srs/epsg.xml#4326", "neu"),
  new Bi("http://www.opengis.net/def/crs/EPSG/0/4326", "neu")
];
let Da = {};
function W0(n) {
  return Da[n] || Da[n.replace(/urn:(x-)?ogc:def:crs:EPSG:(.*:)?(\w+)$/, "EPSG:$3")] || null;
}
function H0(n, t) {
  Da[n] = t;
}
let Bn = {};
function jn(n, t, e) {
  const i = n.getCode(), s = t.getCode();
  i in Bn || (Bn[i] = {}), Bn[i][s] = e;
}
function dd(n, t) {
  let e;
  return n in Bn && t in Bn[n] && (e = Bn[n][t]), e;
}
const fd = 63710088e-1;
function qh(n, t, e) {
  e = e || fd;
  const i = ji(n[1]), s = ji(t[1]), r = (s - i) / 2, o = ji(t[0] - n[0]) / 2, a = Math.sin(r) * Math.sin(r) + Math.sin(o) * Math.sin(o) * Math.cos(i) * Math.cos(s);
  return 2 * e * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
function X0(n, t, e, i) {
  i = i || fd;
  const s = ji(n[1]), r = ji(n[0]), o = t / i, a = Math.asin(
    Math.sin(s) * Math.cos(o) + Math.cos(s) * Math.sin(o) * Math.cos(e)
  ), l = r + Math.atan2(
    Math.sin(e) * Math.sin(o) * Math.cos(s),
    Math.cos(o) - Math.sin(s) * Math.sin(a)
  );
  return [Bh(l), Bh(a)];
}
let ka = !0;
function gd(n) {
  ka = !(n === void 0 ? !0 : n);
}
function Tl(n, t, e) {
  if (t !== void 0) {
    for (let i = 0, s = n.length; i < s; ++i)
      t[i] = n[i];
    t = t;
  } else
    t = n.slice();
  return t;
}
function bl(n, t, e) {
  if (t !== void 0 && n !== t) {
    for (let i = 0, s = n.length; i < s; ++i)
      t[i] = n[i];
    n = t;
  }
  return n;
}
function md(n) {
  H0(n.getCode(), n), jn(n, n, Tl);
}
function Y0(n) {
  n.forEach(md);
}
function Q(n) {
  return typeof n == "string" ? W0(n) : n || null;
}
function ao(n, t, e, i) {
  n = Q(n);
  let s;
  const r = n.getPointResolutionFunc();
  if (r) {
    if (s = r(t, e), i && i !== n.getUnits()) {
      const o = n.getMetersPerUnit();
      o && (s = s * o / Yn[i]);
    }
  } else {
    const o = n.getUnits();
    if (o == "degrees" && !i || i == "degrees")
      s = t;
    else {
      const a = Fo(
        n,
        Q("EPSG:4326")
      );
      if (a === bl && o !== "degrees")
        s = t * n.getMetersPerUnit();
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
        const c = qh(h.slice(0, 2), h.slice(2, 4)), u = qh(h.slice(4, 6), h.slice(6, 8));
        s = (c + u) / 2;
      }
      const l = i ? Yn[i] : n.getMetersPerUnit();
      l !== void 0 && (s /= l);
    }
  }
  return s;
}
function Ga(n) {
  Y0(n), n.forEach(function(t) {
    n.forEach(function(e) {
      t !== e && jn(t, e, Tl);
    });
  });
}
function j0(n, t, e, i) {
  n.forEach(function(s) {
    t.forEach(function(r) {
      jn(s, r, e), jn(r, s, i);
    });
  });
}
function Ll(n, t) {
  return n ? typeof n == "string" ? Q(n) : n : Q(t);
}
function Kh(n) {
  return function(t, e, i) {
    const s = t.length;
    i = i !== void 0 ? i : 2, e = e !== void 0 ? e : new Array(s);
    for (let r = 0; r < s; r += i) {
      const o = n(t.slice(r, r + i)), a = o.length;
      for (let l = 0, h = i; l < h; ++l)
        e[r + l] = l >= a ? t[r + l] : o[l];
    }
    return e;
  };
}
function q0(n, t, e, i) {
  const s = Q(n), r = Q(t);
  jn(
    s,
    r,
    Kh(e)
  ), jn(
    r,
    s,
    Kh(i)
  );
}
function K0(n, t) {
  return gd(), _d(
    n,
    "EPSG:4326",
    t !== void 0 ? t : "EPSG:3857"
  );
}
function Ne(n, t) {
  if (n === t)
    return !0;
  const e = n.getUnits() === t.getUnits();
  return (n.getCode() === t.getCode() || Fo(n, t) === Tl) && e;
}
function Fo(n, t) {
  const e = n.getCode(), i = t.getCode();
  let s = dd(e, i);
  return s || (s = bl), s;
}
function zs(n, t) {
  const e = Q(n), i = Q(t);
  return Fo(e, i);
}
function _d(n, t, e) {
  return zs(t, e)(n, void 0, n.length);
}
function pd(n, t, e, i) {
  const s = zs(t, e);
  return t0(n, s, void 0, i);
}
function qn(n, t) {
  return n;
}
function vt(n, t) {
  return ka && !Le(n, [0, 0]) && n[0] >= -180 && n[0] <= 180 && n[1] >= -90 && n[1] <= 90 && (ka = !1, console.warn(
    "Call useGeographic() from ol/proj once to work with [longitude, latitude] coordinates."
  )), n;
}
function Il(n, t) {
  return n;
}
function Mi(n, t) {
  return n;
}
function Jh(n, t, e) {
  return function(i) {
    let s, r;
    if (n.canWrapX()) {
      const o = n.getExtent(), a = pt(o);
      i = i.slice(0), r = od(i, n, a), r && (i[0] = i[0] - r * a), i[0] = Et(i[0], o[0], o[2]), i[1] = Et(i[1], o[1], o[3]), s = e(i);
    } else
      s = e(i);
    return r && t.canWrapX() && (s[0] += r * pt(t.getExtent())), s;
  };
}
function J0() {
  Ga(Xh), Ga(jh), j0(
    jh,
    Xh,
    z0,
    Z0
  );
}
J0();
function Qh(n, t, e) {
  return function(i, s, r, o, a) {
    if (!i)
      return;
    if (!s && !t)
      return i;
    const l = t ? 0 : r[0] * s, h = t ? 0 : r[1] * s, c = a ? a[0] : 0, u = a ? a[1] : 0;
    let d = n[0] + l / 2 + c, f = n[2] - l / 2 + c, g = n[1] + h / 2 + u, m = n[3] - h / 2 + u;
    d > f && (d = (f + d) / 2, f = d), g > m && (g = (m + g) / 2, m = g);
    let _ = Et(i[0], d, f), y = Et(i[1], g, m);
    if (o && e && s) {
      const p = 30 * s;
      _ += -p * Math.log(1 + Math.max(0, d - i[0]) / p) + p * Math.log(1 + Math.max(0, i[0] - f) / p), y += -p * Math.log(1 + Math.max(0, g - i[1]) / p) + p * Math.log(1 + Math.max(0, i[1] - m) / p);
    }
    return [_, y];
  };
}
function Q0(n) {
  return n;
}
function Pl(n, t, e, i) {
  const s = pt(t) / e[0], r = ze(t) / e[1];
  return i ? Math.min(n, Math.max(s, r)) : Math.min(n, Math.min(s, r));
}
function Al(n, t, e) {
  let i = Math.min(n, t);
  const s = 50;
  return i *= Math.log(1 + s * Math.max(0, n / t - 1)) / s + 1, e && (i = Math.max(i, e), i /= Math.log(1 + s * Math.max(0, e / n - 1)) / s + 1), Et(i, e / 2, t * 2);
}
function t1(n, t, e, i) {
  return t = t !== void 0 ? t : !0, function(s, r, o, a) {
    if (s !== void 0) {
      const l = n[0], h = n[n.length - 1], c = e ? Pl(
        l,
        e,
        o,
        i
      ) : l;
      if (a)
        return t ? Al(
          s,
          c,
          h
        ) : Et(s, h, c);
      const u = Math.min(c, s), d = Math.floor(gl(n, u, r));
      return n[d] > c && d < n.length - 1 ? n[d + 1] : n[d];
    } else
      return;
  };
}
function e1(n, t, e, i, s, r) {
  return i = i !== void 0 ? i : !0, e = e !== void 0 ? e : 0, function(o, a, l, h) {
    if (o !== void 0) {
      const c = s ? Pl(
        t,
        s,
        l,
        r
      ) : t;
      if (h)
        return i ? Al(
          o,
          c,
          e
        ) : Et(o, e, c);
      const u = 1e-9, d = Math.ceil(
        Math.log(t / c) / Math.log(n) - u
      ), f = -a * (0.5 - u) + 0.5, g = Math.min(c, o), m = Math.floor(
        Math.log(t / g) / Math.log(n) + f
      ), _ = Math.max(d, m), y = t / Math.pow(n, _);
      return Et(y, e, c);
    } else
      return;
  };
}
function tc(n, t, e, i, s) {
  return e = e !== void 0 ? e : !0, function(r, o, a, l) {
    if (r !== void 0) {
      const h = i ? Pl(
        n,
        i,
        a,
        s
      ) : n;
      return !e || !l ? Et(r, t, h) : Al(
        r,
        h,
        t
      );
    } else
      return;
  };
}
function Ol(n) {
  if (n !== void 0)
    return 0;
}
function ec(n) {
  if (n !== void 0)
    return n;
}
function i1(n) {
  const t = 2 * Math.PI / n;
  return function(e, i) {
    if (i)
      return e;
    if (e !== void 0)
      return e = Math.floor(e / t + 0.5) * t, e;
  };
}
function n1(n) {
  return n = n || ji(5), function(t, e) {
    if (e)
      return t;
    if (t !== void 0)
      return Math.abs(t) <= n ? 0 : t;
  };
}
function yd(n) {
  return Math.pow(n, 3);
}
function rs(n) {
  return 1 - yd(1 - n);
}
function s1(n) {
  return 3 * n * n - 2 * n * n * n;
}
function r1(n) {
  return n;
}
function Ki(n, t, e, i, s, r) {
  r = r || [];
  let o = 0;
  for (let a = t; a < e; a += i) {
    const l = n[a], h = n[a + 1];
    r[o++] = s[0] * l + s[2] * h + s[4], r[o++] = s[1] * l + s[3] * h + s[5];
  }
  return r && r.length != o && (r.length = o), r;
}
function Fl(n, t, e, i, s, r, o) {
  o = o || [];
  const a = Math.cos(s), l = Math.sin(s), h = r[0], c = r[1];
  let u = 0;
  for (let d = t; d < e; d += i) {
    const f = n[d] - h, g = n[d + 1] - c;
    o[u++] = h + f * a - g * l, o[u++] = c + f * l + g * a;
    for (let m = d + 2; m < d + i; ++m)
      o[u++] = n[m];
  }
  return o && o.length != u && (o.length = u), o;
}
function o1(n, t, e, i, s, r, o, a) {
  a = a || [];
  const l = o[0], h = o[1];
  let c = 0;
  for (let u = t; u < e; u += i) {
    const d = n[u] - l, f = n[u + 1] - h;
    a[c++] = l + s * d, a[c++] = h + r * f;
    for (let g = u + 2; g < u + i; ++g)
      a[c++] = n[g];
  }
  return a && a.length != c && (a.length = c), a;
}
function vd(n, t, e, i, s, r, o) {
  o = o || [];
  let a = 0;
  for (let l = t; l < e; l += i) {
    o[a++] = n[l] + s, o[a++] = n[l + 1] + r;
    for (let h = l + 2; h < l + i; ++h)
      o[a++] = n[h];
  }
  return o && o.length != a && (o.length = a), o;
}
const ic = $e();
class a1 extends Oe {
  constructor() {
    super(), this.extent_ = se(), this.extentRevision_ = -1, this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = 0, this.simplifyTransformedInternal = Ag(function(t, e, i) {
      if (!i)
        return this.getSimplifiedGeometry(e);
      const s = this.clone();
      return s.applyTransform(i), s.getSimplifiedGeometry(e);
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
    return H();
  }
  closestPointXY(t, e, i, s) {
    return H();
  }
  containsXY(t, e) {
    const i = this.getClosestPoint([t, e]);
    return i[0] === t && i[1] === e;
  }
  getClosestPoint(t, e) {
    return e = e || [NaN, NaN], this.closestPointXY(t[0], t[1], e, 1 / 0), e;
  }
  intersectsCoordinate(t) {
    return this.containsXY(t[0], t[1]);
  }
  computeExtent(t) {
    return H();
  }
  getExtent(t) {
    if (this.extentRevision_ != this.getRevision()) {
      const e = this.computeExtent(this.extent_);
      (isNaN(e[0]) || isNaN(e[1])) && Qs(e), this.extentRevision_ = this.getRevision();
    }
    return Jg(this.extent_, t);
  }
  rotate(t, e) {
    H();
  }
  scale(t, e, i) {
    H();
  }
  simplify(t) {
    return this.getSimplifiedGeometry(t * t);
  }
  getSimplifiedGeometry(t) {
    return H();
  }
  getType() {
    return H();
  }
  applyTransform(t) {
    H();
  }
  intersectsExtent(t) {
    return H();
  }
  translate(t, e) {
    H();
  }
  transform(t, e) {
    const i = Q(t), s = i.getUnits() == "tile-pixels" ? function(r, o, a) {
      const l = i.getExtent(), h = i.getWorldExtent(), c = ze(h) / ze(l);
      return Ii(
        ic,
        h[0],
        h[3],
        c,
        -c,
        0,
        0,
        0
      ), Ki(
        r,
        0,
        r.length,
        a,
        ic,
        o
      ), zs(i, e)(
        r,
        o,
        a
      );
    } : zs(i, e);
    return this.applyTransform(s), this;
  }
}
const xd = a1;
class l1 extends xd {
  constructor() {
    super(), this.layout = "XY", this.stride = 2, this.flatCoordinates = null;
  }
  computeExtent(t) {
    return qu(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinates() {
    return H();
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
    this.stride = lo(t), this.layout = t, this.flatCoordinates = e;
  }
  setCoordinates(t, e) {
    H();
  }
  setLayout(t, e, i) {
    let s;
    if (t)
      s = lo(t);
    else {
      for (let r = 0; r < i; ++r)
        if (e.length === 0) {
          this.layout = "XY", this.stride = 2;
          return;
        } else
          e = e[0];
      s = e.length, t = h1(s);
    }
    this.layout = t, this.stride = s;
  }
  applyTransform(t) {
    this.flatCoordinates && (t(this.flatCoordinates, this.flatCoordinates, this.stride), this.changed());
  }
  rotate(t, e) {
    const i = this.getFlatCoordinates();
    if (i) {
      const s = this.getStride();
      Fl(
        i,
        0,
        i.length,
        s,
        t,
        e,
        i
      ), this.changed();
    }
  }
  scale(t, e, i) {
    e === void 0 && (e = t), i || (i = Pi(this.getExtent()));
    const s = this.getFlatCoordinates();
    if (s) {
      const r = this.getStride();
      o1(
        s,
        0,
        s.length,
        r,
        t,
        e,
        i,
        s
      ), this.changed();
    }
  }
  translate(t, e) {
    const i = this.getFlatCoordinates();
    if (i) {
      const s = this.getStride();
      vd(
        i,
        0,
        i.length,
        s,
        t,
        e,
        i
      ), this.changed();
    }
  }
}
function h1(n) {
  let t;
  return n == 2 ? t = "XY" : n == 3 ? t = "XYZ" : n == 4 && (t = "XYZM"), t;
}
function lo(n) {
  let t;
  return n == "XY" ? t = 2 : n == "XYZ" || n == "XYM" ? t = 3 : n == "XYZM" && (t = 4), t;
}
function c1(n, t, e) {
  const i = n.getFlatCoordinates();
  if (i) {
    const s = n.getStride();
    return Ki(
      i,
      0,
      i.length,
      s,
      t,
      e
    );
  } else
    return null;
}
const Di = l1;
function nc(n, t, e, i, s, r, o) {
  const a = n[t], l = n[t + 1], h = n[e] - a, c = n[e + 1] - l;
  let u;
  if (h === 0 && c === 0)
    u = t;
  else {
    const d = ((s - a) * h + (r - l) * c) / (h * h + c * c);
    if (d > 1)
      u = e;
    else if (d > 0) {
      for (let f = 0; f < i; ++f)
        o[f] = ii(
          n[t + f],
          n[e + f],
          d
        );
      o.length = i;
      return;
    } else
      u = t;
  }
  for (let d = 0; d < i; ++d)
    o[d] = n[u + d];
  o.length = i;
}
function Nl(n, t, e, i, s) {
  let r = n[t], o = n[t + 1];
  for (t += i; t < e; t += i) {
    const a = n[t], l = n[t + 1], h = ri(r, o, a, l);
    h > s && (s = h), r = a, o = l;
  }
  return s;
}
function Dl(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s = Nl(n, t, a, i, s), t = a;
  }
  return s;
}
function u1(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s = Dl(n, t, a, i, s), t = a[a.length - 1];
  }
  return s;
}
function kl(n, t, e, i, s, r, o, a, l, h, c) {
  if (t == e)
    return h;
  let u, d;
  if (s === 0)
    if (d = ri(
      o,
      a,
      n[t],
      n[t + 1]
    ), d < h) {
      for (u = 0; u < i; ++u)
        l[u] = n[t + u];
      return l.length = i, d;
    } else
      return h;
  c = c || [NaN, NaN];
  let f = t + i;
  for (; f < e; )
    if (nc(
      n,
      f - i,
      f,
      i,
      o,
      a,
      c
    ), d = ri(o, a, c[0], c[1]), d < h) {
      for (h = d, u = 0; u < i; ++u)
        l[u] = c[u];
      l.length = i, f += i;
    } else
      f += i * Math.max(
        (Math.sqrt(d) - Math.sqrt(h)) / s | 0,
        1
      );
  if (r && (nc(
    n,
    e - i,
    t,
    i,
    o,
    a,
    c
  ), d = ri(o, a, c[0], c[1]), d < h)) {
    for (h = d, u = 0; u < i; ++u)
      l[u] = c[u];
    l.length = i;
  }
  return h;
}
function Gl(n, t, e, i, s, r, o, a, l, h, c) {
  c = c || [NaN, NaN];
  for (let u = 0, d = e.length; u < d; ++u) {
    const f = e[u];
    h = kl(
      n,
      t,
      f,
      i,
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
function d1(n, t, e, i, s, r, o, a, l, h, c) {
  c = c || [NaN, NaN];
  for (let u = 0, d = e.length; u < d; ++u) {
    const f = e[u];
    h = Gl(
      n,
      t,
      f,
      i,
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
function Cd(n, t, e, i) {
  for (let s = 0, r = e.length; s < r; ++s)
    n[t++] = e[s];
  return t;
}
function No(n, t, e, i) {
  for (let s = 0, r = e.length; s < r; ++s) {
    const o = e[s];
    for (let a = 0; a < i; ++a)
      n[t++] = o[a];
  }
  return t;
}
function $l(n, t, e, i, s) {
  s = s || [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = No(
      n,
      t,
      e[o],
      i
    );
    s[r++] = l, t = l;
  }
  return s.length = r, s;
}
function f1(n, t, e, i, s) {
  s = s || [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = $l(
      n,
      t,
      e[o],
      i,
      s[r]
    );
    l.length === 0 && (l[0] = t), s[r++] = l, t = l[l.length - 1];
  }
  return s.length = r, s;
}
function Bl(n, t, e, i, s, r, o) {
  const a = (e - t) / i;
  if (a < 3) {
    for (; t < e; t += i)
      r[o++] = n[t], r[o++] = n[t + 1];
    return o;
  }
  const l = new Array(a);
  l[0] = 1, l[a - 1] = 1;
  const h = [t, e - i];
  let c = 0;
  for (; h.length > 0; ) {
    const u = h.pop(), d = h.pop();
    let f = 0;
    const g = n[d], m = n[d + 1], _ = n[u], y = n[u + 1];
    for (let p = d + i; p < u; p += i) {
      const v = n[p], x = n[p + 1], C = i0(v, x, g, m, _, y);
      C > f && (c = p, f = C);
    }
    f > s && (l[(c - t) / i] = 1, d + i < c && h.push(d, c), c + i < u && h.push(c, u));
  }
  for (let u = 0; u < a; ++u)
    l[u] && (r[o++] = n[t + u * i], r[o++] = n[t + u * i + 1]);
  return o;
}
function g1(n, t, e, i, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    o = Bl(
      n,
      t,
      c,
      i,
      s,
      r,
      o
    ), a.push(o), t = c;
  }
  return o;
}
function Zi(n, t) {
  return t * Math.round(n / t);
}
function m1(n, t, e, i, s, r, o) {
  if (t == e)
    return o;
  let a = Zi(n[t], s), l = Zi(n[t + 1], s);
  t += i, r[o++] = a, r[o++] = l;
  let h, c;
  do
    if (h = Zi(n[t], s), c = Zi(n[t + 1], s), t += i, t == e)
      return r[o++] = h, r[o++] = c, o;
  while (h == a && c == l);
  for (; t < e; ) {
    const u = Zi(n[t], s), d = Zi(n[t + 1], s);
    if (t += i, u == h && d == c)
      continue;
    const f = h - a, g = c - l, m = u - a, _ = d - l;
    if (f * _ == g * m && (f < 0 && m < f || f == m || f > 0 && m > f) && (g < 0 && _ < g || g == _ || g > 0 && _ > g)) {
      h = u, c = d;
      continue;
    }
    r[o++] = h, r[o++] = c, a = h, l = c, h = u, c = d;
  }
  return r[o++] = h, r[o++] = c, o;
}
function Md(n, t, e, i, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    o = m1(
      n,
      t,
      c,
      i,
      s,
      r,
      o
    ), a.push(o), t = c;
  }
  return o;
}
function _1(n, t, e, i, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l], u = [];
    o = Md(
      n,
      t,
      c,
      i,
      s,
      r,
      o,
      u
    ), a.push(u), t = c[c.length - 1];
  }
  return o;
}
function Ei(n, t, e, i, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = t; o < e; o += i)
    s[r++] = n.slice(o, o + i);
  return s.length = r, s;
}
function Zs(n, t, e, i, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = Ei(
      n,
      t,
      l,
      i,
      s[r]
    ), t = l;
  }
  return s.length = r, s;
}
function $a(n, t, e, i, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = l.length === 1 && l[0] === t ? [] : Zs(
      n,
      t,
      l,
      i,
      s[r]
    ), t = l[l.length - 1];
  }
  return s.length = r, s;
}
function Ed(n, t, e, i) {
  let s = 0, r = n[e - i], o = n[e - i + 1];
  for (; t < e; t += i) {
    const a = n[t], l = n[t + 1];
    s += o * a - r * l, r = a, o = l;
  }
  return s / 2;
}
function wd(n, t, e, i) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += Ed(n, t, a, i), t = a;
  }
  return s;
}
function p1(n, t, e, i) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += wd(n, t, a, i), t = a[a.length - 1];
  }
  return s;
}
class ho extends Di {
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
    return new ho(this.flatCoordinates.slice(), this.layout);
  }
  closestPointXY(t, e, i, s) {
    return s < dn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Nl(
        this.flatCoordinates,
        0,
        this.flatCoordinates.length,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), kl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      i,
      s
    ));
  }
  getArea() {
    return Ed(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinates() {
    return Ei(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getSimplifiedGeometryInternal(t) {
    const e = [];
    return e.length = Bl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e,
      0
    ), new ho(e, "XY");
  }
  getType() {
    return "LinearRing";
  }
  intersectsExtent(t) {
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = No(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const Ba = ho;
class zl extends Di {
  constructor(t, e) {
    super(), this.setCoordinates(t, e);
  }
  clone() {
    const t = new zl(this.flatCoordinates.slice(), this.layout);
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    const r = this.flatCoordinates, o = ri(
      t,
      e,
      r[0],
      r[1]
    );
    if (o < s) {
      const a = this.stride;
      for (let l = 0; l < a; ++l)
        i[l] = r[l];
      return i.length = a, o;
    } else
      return s;
  }
  getCoordinates() {
    return this.flatCoordinates ? this.flatCoordinates.slice() : [];
  }
  computeExtent(t) {
    return ws(this.flatCoordinates, t);
  }
  getType() {
    return "Point";
  }
  intersectsExtent(t) {
    return pl(t, this.flatCoordinates[0], this.flatCoordinates[1]);
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 0), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Cd(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const Se = zl;
function y1(n, t, e, i, s) {
  return !yl(
    s,
    function(o) {
      return !Wi(
        n,
        t,
        e,
        i,
        o[0],
        o[1]
      );
    }
  );
}
function Wi(n, t, e, i, s, r) {
  let o = 0, a = n[e - i], l = n[e - i + 1];
  for (; t < e; t += i) {
    const h = n[t], c = n[t + 1];
    l <= r ? c > r && (h - a) * (r - l) - (s - a) * (c - l) > 0 && o++ : c <= r && (h - a) * (r - l) - (s - a) * (c - l) < 0 && o--, a = h, l = c;
  }
  return o !== 0;
}
function Zl(n, t, e, i, s, r) {
  if (e.length === 0 || !Wi(n, t, e[0], i, s, r))
    return !1;
  for (let o = 1, a = e.length; o < a; ++o)
    if (Wi(n, e[o - 1], e[o], i, s, r))
      return !1;
  return !0;
}
function v1(n, t, e, i, s, r) {
  if (e.length === 0)
    return !1;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    if (Zl(n, t, l, i, s, r))
      return !0;
    t = l[l.length - 1];
  }
  return !1;
}
function Sd(n, t, e, i, s, r, o) {
  let a, l, h, c, u, d, f;
  const g = s[r + 1], m = [];
  for (let p = 0, v = e.length; p < v; ++p) {
    const x = e[p];
    for (c = n[x - i], d = n[x - i + 1], a = t; a < x; a += i)
      u = n[a], f = n[a + 1], (g <= d && f <= g || d <= g && g <= f) && (h = (g - d) / (f - d) * (u - c) + c, m.push(h)), c = u, d = f;
  }
  let _ = NaN, y = -1 / 0;
  for (m.sort(tn), c = m[0], a = 1, l = m.length; a < l; ++a) {
    u = m[a];
    const p = Math.abs(u - c);
    p > y && (h = (c + u) / 2, Zl(n, t, e, i, h, g) && (_ = h, y = p)), c = u;
  }
  return isNaN(_) && (_ = s[r]), o ? (o.push(_, g, y), o) : [_, g, y];
}
function x1(n, t, e, i, s) {
  let r = [];
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = Sd(
      n,
      t,
      l,
      i,
      s,
      2 * o,
      r
    ), t = l[l.length - 1];
  }
  return r;
}
function Rd(n, t, e, i, s) {
  let r;
  for (t += i; t < e; t += i)
    if (r = s(
      n.slice(t - i, t),
      n.slice(t, t + i)
    ), r)
      return r;
  return !1;
}
function Do(n, t, e, i, s) {
  const r = Ju(
    se(),
    n,
    t,
    e,
    i
  );
  return Kt(s, r) ? Vi(s, r) || r[0] >= s[0] && r[2] <= s[2] || r[1] >= s[1] && r[3] <= s[3] ? !0 : Rd(
    n,
    t,
    e,
    i,
    function(o, a) {
      return Qg(s, o, a);
    }
  ) : !1;
}
function C1(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    if (Do(n, t, e[r], i, s))
      return !0;
    t = e[r];
  }
  return !1;
}
function Td(n, t, e, i, s) {
  return !!(Do(n, t, e, i, s) || Wi(
    n,
    t,
    e,
    i,
    s[0],
    s[1]
  ) || Wi(
    n,
    t,
    e,
    i,
    s[0],
    s[3]
  ) || Wi(
    n,
    t,
    e,
    i,
    s[2],
    s[1]
  ) || Wi(
    n,
    t,
    e,
    i,
    s[2],
    s[3]
  ));
}
function bd(n, t, e, i, s) {
  if (!Td(n, t, e[0], i, s))
    return !1;
  if (e.length === 1)
    return !0;
  for (let r = 1, o = e.length; r < o; ++r)
    if (y1(
      n,
      e[r - 1],
      e[r],
      i,
      s
    ) && !Do(
      n,
      e[r - 1],
      e[r],
      i,
      s
    ))
      return !1;
  return !0;
}
function M1(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (bd(n, t, a, i, s))
      return !0;
    t = a[a.length - 1];
  }
  return !1;
}
function E1(n, t, e, i) {
  for (; t < e - i; ) {
    for (let s = 0; s < i; ++s) {
      const r = n[t + s];
      n[t + s] = n[e - i + s], n[e - i + s] = r;
    }
    t += i, e -= i;
  }
}
function Ld(n, t, e, i) {
  let s = 0, r = n[e - i], o = n[e - i + 1];
  for (; t < e; t += i) {
    const a = n[t], l = n[t + 1];
    s += (a - r) * (l + o), r = a, o = l;
  }
  return s === 0 ? void 0 : s > 0;
}
function Id(n, t, e, i, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = Ld(
      n,
      t,
      a,
      i
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
function w1(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (!Id(n, t, a, i, s))
      return !1;
    a.length && (t = a[a.length - 1]);
  }
  return !0;
}
function za(n, t, e, i, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = Ld(
      n,
      t,
      a,
      i
    );
    (r === 0 ? s && l || !s && !l : s && !l || !s && l) && E1(n, t, a, i), t = a;
  }
  return t;
}
function sc(n, t, e, i, s) {
  for (let r = 0, o = e.length; r < o; ++r)
    t = za(
      n,
      t,
      e[r],
      i,
      s
    );
  return t;
}
class sn extends Di {
  constructor(t, e, i) {
    super(), this.ends_ = [], this.flatInteriorPointRevision_ = -1, this.flatInteriorPoint_ = null, this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, this.orientedRevision_ = -1, this.orientedFlatCoordinates_ = null, e !== void 0 && i ? (this.setFlatCoordinates(
      e,
      t
    ), this.ends_ = i) : this.setCoordinates(
      t,
      e
    );
  }
  appendLinearRing(t) {
    this.flatCoordinates ? Qt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new sn(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    return s < dn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Dl(
        this.flatCoordinates,
        0,
        this.ends_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), Gl(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      i,
      s
    ));
  }
  containsXY(t, e) {
    return Zl(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return wd(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), za(e, 0, this.ends_, this.stride, t)) : e = this.flatCoordinates, Zs(e, 0, this.ends_, this.stride);
  }
  getEnds() {
    return this.ends_;
  }
  getFlatInteriorPoint() {
    if (this.flatInteriorPointRevision_ != this.getRevision()) {
      const t = Pi(this.getExtent());
      this.flatInteriorPoint_ = Sd(
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
    return new Se(this.getFlatInteriorPoint(), "XYM");
  }
  getLinearRingCount() {
    return this.ends_.length;
  }
  getLinearRing(t) {
    return t < 0 || this.ends_.length <= t ? null : new Ba(
      this.flatCoordinates.slice(
        t === 0 ? 0 : this.ends_[t - 1],
        this.ends_[t]
      ),
      this.layout
    );
  }
  getLinearRings() {
    const t = this.layout, e = this.flatCoordinates, i = this.ends_, s = [];
    let r = 0;
    for (let o = 0, a = i.length; o < a; ++o) {
      const l = i[o], h = new Ba(
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
      Id(t, 0, this.ends_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = za(
        this.orientedFlatCoordinates_,
        0,
        this.ends_,
        this.stride
      )), this.orientedRevision_ = this.getRevision();
    }
    return this.orientedFlatCoordinates_;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], i = [];
    return e.length = Md(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      Math.sqrt(t),
      e,
      0,
      i
    ), new sn(e, "XY", i);
  }
  getType() {
    return "Polygon";
  }
  intersectsExtent(t) {
    return bd(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 2), this.flatCoordinates || (this.flatCoordinates = []);
    const i = $l(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.ends_
    );
    this.flatCoordinates.length = i.length === 0 ? 0 : i[i.length - 1], this.changed();
  }
}
const Ai = sn;
function S1(n, t, e, i) {
  e = e || 32;
  const s = [];
  for (let r = 0; r < e; ++r)
    Qt(
      s,
      X0(n, t, 2 * Math.PI * r / e, i)
    );
  return s.push(s[0], s[1]), new sn(s, "XY", [s.length]);
}
function rc(n) {
  const t = n[0], e = n[1], i = n[2], s = n[3], r = [
    t,
    e,
    t,
    s,
    i,
    s,
    i,
    e,
    t,
    e
  ];
  return new sn(r, "XY", [r.length]);
}
function R1(n, t, e) {
  t = t || 32;
  const i = n.getStride(), s = n.getLayout(), r = n.getCenter(), o = i * (t + 1), a = new Array(o);
  for (let c = 0; c < o; c += i) {
    a[c] = 0, a[c + 1] = 0;
    for (let u = 2; u < i; u++)
      a[c + u] = r[u];
  }
  const l = [a.length], h = new sn(a, s, l);
  return T1(h, r, n.getRadius(), e), h;
}
function T1(n, t, e, i) {
  const s = n.getFlatCoordinates(), r = n.getStride(), o = s.length / r - 1, a = i || 0;
  for (let l = 0; l <= o; ++l) {
    const h = l * r, c = a + qi(l, o) * 2 * Math.PI / o;
    s[h] = t[0] + e * Math.cos(c), s[h + 1] = t[1] + e * Math.sin(c);
  }
  n.changed();
}
const ra = 0;
class b1 extends Oe {
  constructor(t) {
    super(), this.on, this.once, this.un, t = Object.assign({}, t), this.hints_ = [0, 0], this.animations_ = [], this.updateAnimationKey_, this.projection_ = Ll(t.projection, "EPSG:3857"), this.viewportSize_ = [100, 100], this.targetCenter_ = null, this.targetResolution_, this.targetRotation_, this.nextCenter_ = null, this.nextResolution_, this.nextRotation_, this.cancelAnchor_ = void 0, t.projection && gd(), t.center && (t.center = vt(t.center, this.projection_)), t.extent && (t.extent = Mi(t.extent, this.projection_)), this.applyOptions_(t);
  }
  applyOptions_(t) {
    const e = Object.assign({}, t);
    for (const a in be)
      delete e[a];
    this.setProperties(e, !0);
    const i = I1(t);
    this.maxResolution_ = i.maxResolution, this.minResolution_ = i.minResolution, this.zoomFactor_ = i.zoomFactor, this.resolutions_ = t.resolutions, this.padding_ = t.padding, this.minZoom_ = i.minZoom;
    const s = L1(t), r = i.constraint, o = P1(t);
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
    const i = this.getCenter();
    if (i) {
      const s = t || [0, 0, 0, 0];
      e = e || [0, 0, 0, 0];
      const r = this.getResolution(), o = r / 2 * (s[3] - e[3] + e[1] - s[1]), a = r / 2 * (s[0] - e[0] + e[2] - s[2]);
      this.setCenterInternal([i[0] + o, i[1] - a]);
    }
  }
  getUpdatedOptions_(t) {
    const e = this.getProperties();
    return e.resolution !== void 0 ? e.resolution = this.getResolution() : e.zoom = this.getZoom(), e.center = this.getCenterInternal(), e.rotation = this.getRotation(), Object.assign({}, e, t);
  }
  animate(t) {
    this.isDef() && !this.getAnimating() && this.resolveConstraints(0);
    const e = new Array(arguments.length);
    for (let i = 0; i < e.length; ++i) {
      let s = arguments[i];
      s.center && (s = Object.assign({}, s), s.center = vt(
        s.center,
        this.getProjection()
      )), s.anchor && (s = Object.assign({}, s), s.anchor = vt(
        s.anchor,
        this.getProjection()
      )), e[i] = s;
    }
    this.animateInternal.apply(this, e);
  }
  animateInternal(t) {
    let e = arguments.length, i;
    e > 1 && typeof arguments[e - 1] == "function" && (i = arguments[e - 1], --e);
    let s = 0;
    for (; s < e && !this.isDef(); ++s) {
      const c = arguments[s];
      c.center && this.setCenterInternal(c.center), c.zoom !== void 0 ? this.setZoom(c.zoom) : c.resolution && this.setResolution(c.resolution), c.rotation !== void 0 && this.setRotation(c.rotation);
    }
    if (s === e) {
      i && br(i, !0);
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
        easing: c.easing || s1,
        callback: i
      };
      if (c.center && (u.sourceCenter = o, u.targetCenter = c.center.slice(), o = u.targetCenter), c.zoom !== void 0 ? (u.sourceResolution = a, u.targetResolution = this.getResolutionForZoom(c.zoom), a = u.targetResolution) : c.resolution && (u.sourceResolution = a, u.targetResolution = c.resolution, a = u.targetResolution), c.rotation !== void 0) {
        u.sourceRotation = l;
        const d = qi(c.rotation - l + Math.PI, 2 * Math.PI) - Math.PI;
        u.targetRotation = l + d, l = u.targetRotation;
      }
      A1(u) ? u.complete = !0 : r += u.duration, h.push(u);
    }
    this.animations_.push(h), this.setHint(Wt.ANIMATING, 1), this.updateAnimations_();
  }
  getAnimating() {
    return this.hints_[Wt.ANIMATING] > 0;
  }
  getInteracting() {
    return this.hints_[Wt.INTERACTING] > 0;
  }
  cancelAnimations() {
    this.setHint(Wt.ANIMATING, -this.hints_[Wt.ANIMATING]);
    let t;
    for (let e = 0, i = this.animations_.length; e < i; ++e) {
      const s = this.animations_[e];
      if (s[0].callback && br(s[0].callback, !1), !t)
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
    for (let i = this.animations_.length - 1; i >= 0; --i) {
      const s = this.animations_[i];
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
          const _ = d + u * (g - d), y = f + u * (m - f);
          this.targetCenter_ = [_, y];
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
          const d = u === 1 ? qi(l.targetRotation + Math.PI, 2 * Math.PI) - Math.PI : l.sourceRotation + u * (l.targetRotation - l.sourceRotation);
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
        this.animations_[i] = null, this.setHint(Wt.ANIMATING, -1), this.nextCenter_ = null, this.nextResolution_ = NaN, this.nextRotation_ = NaN;
        const o = s[0].callback;
        o && br(o, !0);
      }
    }
    this.animations_ = this.animations_.filter(Boolean), e && this.updateAnimationKey_ === void 0 && (this.updateAnimationKey_ = requestAnimationFrame(
      this.updateAnimations_.bind(this)
    ));
  }
  calculateCenterRotate(t, e) {
    let i;
    const s = this.getCenterInternal();
    return s !== void 0 && (i = [s[0] - e[0], s[1] - e[1]], El(i, t - this.getRotation()), nd(i, e)), i;
  }
  calculateCenterZoom(t, e) {
    let i;
    const s = this.getCenterInternal(), r = this.getResolution();
    if (s !== void 0 && r !== void 0) {
      const o = e[0] - t * (e[0] - s[0]) / r, a = e[1] - t * (e[1] - s[1]) / r;
      i = [o, a];
    }
    return i;
  }
  getViewportSize_(t) {
    const e = this.viewportSize_;
    if (t) {
      const i = e[0], s = e[1];
      return [
        Math.abs(i * Math.cos(t)) + Math.abs(s * Math.sin(t)),
        Math.abs(i * Math.sin(t)) + Math.abs(s * Math.cos(t))
      ];
    } else
      return e;
  }
  setViewportSize(t) {
    this.viewportSize_ = Array.isArray(t) ? t.slice() : [100, 100], this.getAnimating() || this.resolveConstraints(0);
  }
  getCenter() {
    const t = this.getCenterInternal();
    return t && qn(t, this.getProjection());
  }
  getCenterInternal() {
    return this.get(be.CENTER);
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
    return Il(e, this.getProjection());
  }
  calculateExtentInternal(t) {
    t = t || this.getViewportSizeMinusPadding_();
    const e = this.getCenterInternal();
    Y(e, 1);
    const i = this.getResolution();
    Y(i !== void 0, 2);
    const s = this.getRotation();
    return Y(s !== void 0, 3), Ia(e, i, s, t);
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
    return this.get(be.RESOLUTION);
  }
  getResolutions() {
    return this.resolutions_;
  }
  getResolutionForExtent(t, e) {
    return this.getResolutionForExtentInternal(
      Mi(t, this.getProjection()),
      e
    );
  }
  getResolutionForExtentInternal(t, e) {
    e = e || this.getViewportSizeMinusPadding_();
    const i = pt(t) / e[0], s = ze(t) / e[1];
    return Math.max(i, s);
  }
  getResolutionForValueFunction(t) {
    t = t || 2;
    const e = this.getConstrainedResolution(this.maxResolution_), i = this.minResolution_, s = Math.log(e / i) / Math.log(t);
    return function(r) {
      return e / Math.pow(t, r * s);
    };
  }
  getRotation() {
    return this.get(be.ROTATION);
  }
  getValueForResolutionFunction(t) {
    const e = Math.log(t || 2), i = this.getConstrainedResolution(this.maxResolution_), s = this.minResolution_, r = Math.log(i / s) / e;
    return function(o) {
      return Math.log(i / o) / e / r;
    };
  }
  getViewportSizeMinusPadding_(t) {
    let e = this.getViewportSize_(t);
    const i = this.padding_;
    return i && (e = [
      e[0] - i[1] - i[3],
      e[1] - i[0] - i[2]
    ]), e;
  }
  getState() {
    const t = this.getProjection(), e = this.getResolution(), i = this.getRotation();
    let s = this.getCenterInternal();
    const r = this.padding_;
    if (r) {
      const o = this.getViewportSizeMinusPadding_();
      s = oa(
        s,
        this.getViewportSize_(),
        [o[0] / 2 + r[3], o[1] / 2 + r[0]],
        e,
        i
      );
    }
    return {
      center: s.slice(0),
      projection: t !== void 0 ? t : null,
      resolution: e,
      nextCenter: this.nextCenter_,
      nextResolution: this.nextResolution_,
      nextRotation: this.nextRotation_,
      rotation: i,
      zoom: this.getZoom()
    };
  }
  getZoom() {
    let t;
    const e = this.getResolution();
    return e !== void 0 && (t = this.getZoomForResolution(e)), t;
  }
  getZoomForResolution(t) {
    let e = this.minZoom_ || 0, i, s;
    if (this.resolutions_) {
      const r = gl(this.resolutions_, t, 1);
      e = r, i = this.resolutions_[r], r == this.resolutions_.length - 1 ? s = 2 : s = i / this.resolutions_[r + 1];
    } else
      i = this.maxResolution_, s = this.zoomFactor_;
    return e + Math.log(i / t) / Math.log(s);
  }
  getResolutionForZoom(t) {
    if (this.resolutions_) {
      if (this.resolutions_.length <= 1)
        return 0;
      const e = Et(
        Math.floor(t),
        0,
        this.resolutions_.length - 2
      ), i = this.resolutions_[e] / this.resolutions_[e + 1];
      return this.resolutions_[e] / Math.pow(i, Et(t - e, 0, 1));
    } else
      return this.maxResolution_ / Math.pow(this.zoomFactor_, t - this.minZoom_);
  }
  fit(t, e) {
    let i;
    if (Y(
      Array.isArray(t) || typeof t.getSimplifiedGeometry == "function",
      24
    ), Array.isArray(t)) {
      Y(!vl(t), 25);
      const s = Mi(t, this.getProjection());
      i = rc(s);
    } else if (t.getType() === "Circle") {
      const s = Mi(
        t.getExtent(),
        this.getProjection()
      );
      i = rc(s), i.rotate(this.getRotation(), Pi(s));
    } else
      i = t;
    this.fitInternal(i, e);
  }
  rotatedExtentForGeometry(t) {
    const e = this.getRotation(), i = Math.cos(e), s = Math.sin(-e), r = t.getFlatCoordinates(), o = t.getStride();
    let a = 1 / 0, l = 1 / 0, h = -1 / 0, c = -1 / 0;
    for (let u = 0, d = r.length; u < d; u += o) {
      const f = r[u] * i - r[u + 1] * s, g = r[u] * s + r[u + 1] * i;
      a = Math.min(a, f), l = Math.min(l, g), h = Math.max(h, f), c = Math.max(c, g);
    }
    return [a, l, h, c];
  }
  fitInternal(t, e) {
    e = e || {};
    let i = e.size;
    i || (i = this.getViewportSizeMinusPadding_());
    const s = e.padding !== void 0 ? e.padding : [0, 0, 0, 0], r = e.nearest !== void 0 ? e.nearest : !1;
    let o;
    e.minResolution !== void 0 ? o = e.minResolution : e.maxZoom !== void 0 ? o = this.getResolutionForZoom(e.maxZoom) : o = 0;
    const a = this.rotatedExtentForGeometry(t);
    let l = this.getResolutionForExtentInternal(a, [
      i[0] - s[1] - s[3],
      i[1] - s[0] - s[2]
    ]);
    l = isNaN(l) ? o : Math.max(l, o), l = this.getConstrainedResolution(l, r ? 0 : 1);
    const h = this.getRotation(), c = Math.sin(h), u = Math.cos(h), d = Pi(a);
    d[0] += (s[1] - s[3]) / 2 * l, d[1] += (s[0] - s[2]) / 2 * l;
    const f = d[0] * u - d[1] * c, g = d[1] * u + d[0] * c, m = this.getConstrainedCenter([f, g], l), _ = e.callback ? e.callback : nn;
    e.duration !== void 0 ? this.animateInternal(
      {
        resolution: l,
        center: m,
        duration: e.duration,
        easing: e.easing
      },
      _
    ) : (this.targetResolution_ = l, this.targetCenter_ = m, this.applyTargetState_(!1, !0), br(_, !0));
  }
  centerOn(t, e, i) {
    this.centerOnInternal(
      vt(t, this.getProjection()),
      e,
      i
    );
  }
  centerOnInternal(t, e, i) {
    this.setCenterInternal(
      oa(
        t,
        e,
        i,
        this.getResolution(),
        this.getRotation()
      )
    );
  }
  calculateCenterShift(t, e, i, s) {
    let r;
    const o = this.padding_;
    if (o && t) {
      const a = this.getViewportSizeMinusPadding_(-i), l = oa(
        t,
        s,
        [a[0] / 2 + o[3], a[1] / 2 + o[0]],
        e,
        i
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
    const e = qn(this.targetCenter_, this.getProjection());
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
    e = e && vt(e, this.getProjection()), this.adjustResolutionInternal(t, e);
  }
  adjustResolutionInternal(t, e) {
    const i = this.getAnimating() || this.getInteracting(), s = this.getViewportSize_(this.getRotation()), r = this.constraints_.resolution(
      this.targetResolution_ * t,
      0,
      s,
      i
    );
    e && (this.targetCenter_ = this.calculateCenterZoom(r, e)), this.targetResolution_ *= t, this.applyTargetState_();
  }
  adjustZoom(t, e) {
    this.adjustResolution(Math.pow(this.zoomFactor_, -t), e);
  }
  adjustRotation(t, e) {
    e && (e = vt(e, this.getProjection())), this.adjustRotationInternal(t, e);
  }
  adjustRotationInternal(t, e) {
    const i = this.getAnimating() || this.getInteracting(), s = this.constraints_.rotation(
      this.targetRotation_ + t,
      i
    );
    e && (this.targetCenter_ = this.calculateCenterRotate(s, e)), this.targetRotation_ += t, this.applyTargetState_();
  }
  setCenter(t) {
    this.setCenterInternal(
      t && vt(t, this.getProjection())
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
    const i = this.getAnimating() || this.getInteracting() || e, s = this.constraints_.rotation(
      this.targetRotation_,
      i
    ), r = this.getViewportSize_(s), o = this.constraints_.resolution(
      this.targetResolution_,
      0,
      r,
      i
    ), a = this.constraints_.center(
      this.targetCenter_,
      o,
      r,
      i,
      this.calculateCenterShift(
        this.targetCenter_,
        o,
        s,
        r
      )
    );
    this.get(be.ROTATION) !== s && this.set(be.ROTATION, s), this.get(be.RESOLUTION) !== o && (this.set(be.RESOLUTION, o), this.set("zoom", this.getZoom(), !0)), (!a || !this.get(be.CENTER) || !Le(this.get(be.CENTER), a)) && this.set(be.CENTER, a), this.getAnimating() && !t && this.cancelAnimations(), this.cancelAnchor_ = void 0;
  }
  resolveConstraints(t, e, i) {
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
    i = i || (t === 0 ? this.cancelAnchor_ : void 0), this.cancelAnchor_ = void 0, (this.getResolution() !== a || this.getRotation() !== r || !this.getCenterInternal() || !Le(this.getCenterInternal(), l)) && (this.getAnimating() && this.cancelAnimations(), this.animateInternal({
      rotation: r,
      center: l,
      resolution: a,
      duration: t,
      easing: rs,
      anchor: i
    }));
  }
  beginInteraction() {
    this.resolveConstraints(0), this.setHint(Wt.INTERACTING, 1);
  }
  endInteraction(t, e, i) {
    i = i && vt(i, this.getProjection()), this.endInteractionInternal(t, e, i);
  }
  endInteractionInternal(t, e, i) {
    this.setHint(Wt.INTERACTING, -1), this.resolveConstraints(t, e, i);
  }
  getConstrainedCenter(t, e) {
    const i = this.getViewportSize_(this.getRotation());
    return this.constraints_.center(
      t,
      e || this.getResolution(),
      i
    );
  }
  getConstrainedZoom(t, e) {
    const i = this.getResolutionForZoom(t);
    return this.getZoomForResolution(
      this.getConstrainedResolution(i, e)
    );
  }
  getConstrainedResolution(t, e) {
    e = e || 0;
    const i = this.getViewportSize_(this.getRotation());
    return this.constraints_.resolution(t, e, i);
  }
}
function br(n, t) {
  setTimeout(function() {
    n(t);
  }, 0);
}
function L1(n) {
  if (n.extent !== void 0) {
    const e = n.smoothExtentConstraint !== void 0 ? n.smoothExtentConstraint : !0;
    return Qh(n.extent, n.constrainOnlyCenter, e);
  }
  const t = Ll(n.projection, "EPSG:3857");
  if (n.multiWorld !== !0 && t.isGlobal()) {
    const e = t.getExtent().slice();
    return e[0] = -1 / 0, e[2] = 1 / 0, Qh(e, !1, !1);
  }
  return Q0;
}
function I1(n) {
  let t, e, i, o = n.minZoom !== void 0 ? n.minZoom : ra, a = n.maxZoom !== void 0 ? n.maxZoom : 28;
  const l = n.zoomFactor !== void 0 ? n.zoomFactor : 2, h = n.multiWorld !== void 0 ? n.multiWorld : !1, c = n.smoothResolutionConstraint !== void 0 ? n.smoothResolutionConstraint : !0, u = n.showFullExtent !== void 0 ? n.showFullExtent : !1, d = Ll(n.projection, "EPSG:3857"), f = d.getExtent();
  let g = n.constrainOnlyCenter, m = n.extent;
  if (!h && !m && d.isGlobal() && (g = !1, m = f), n.resolutions !== void 0) {
    const _ = n.resolutions;
    e = _[o], i = _[a] !== void 0 ? _[a] : _[_.length - 1], n.constrainResolution ? t = t1(
      _,
      c,
      !g && m,
      u
    ) : t = tc(
      e,
      i,
      c,
      !g && m,
      u
    );
  } else {
    const y = (f ? Math.max(pt(f), ze(f)) : 360 * Yn.degrees / d.getMetersPerUnit()) / Sl / Math.pow(2, ra), p = y / Math.pow(2, 28 - ra);
    e = n.maxResolution, e !== void 0 ? o = 0 : e = y / Math.pow(l, o), i = n.minResolution, i === void 0 && (n.maxZoom !== void 0 ? n.maxResolution !== void 0 ? i = e / Math.pow(l, a) : i = y / Math.pow(l, a) : i = p), a = o + Math.floor(
      Math.log(e / i) / Math.log(l)
    ), i = e / Math.pow(l, a - o), n.constrainResolution ? t = e1(
      l,
      e,
      i,
      c,
      !g && m,
      u
    ) : t = tc(
      e,
      i,
      c,
      !g && m,
      u
    );
  }
  return {
    constraint: t,
    maxResolution: e,
    minResolution: i,
    minZoom: o,
    zoomFactor: l
  };
}
function P1(n) {
  if (n.enableRotation !== void 0 ? n.enableRotation : !0) {
    const e = n.constrainRotation;
    return e === void 0 || e === !0 ? n1() : e === !1 ? ec : typeof e == "number" ? i1(e) : ec;
  } else
    return Ol;
}
function A1(n) {
  return !(n.sourceCenter && n.targetCenter && !Le(n.sourceCenter, n.targetCenter) || n.sourceResolution !== n.targetResolution || n.sourceRotation !== n.targetRotation);
}
function oa(n, t, e, i, s) {
  const r = Math.cos(-s);
  let o = Math.sin(-s), a = n[0] * r - n[1] * o, l = n[1] * r + n[0] * o;
  a += (t[0] / 2 - e[0]) * i, l += (e[1] - t[1] / 2) * i, o = -o;
  const h = a * r - l * o, c = l * r + a * o;
  return [h, c];
}
const si = b1;
class O1 extends Oe {
  constructor(t) {
    super();
    const e = t.element;
    e && !t.target && !e.style.pointerEvents && (e.style.pointerEvents = "auto"), this.element = e || null, this.target_ = null, this.map_ = null, this.listenerKeys = [], t.render && (this.render = t.render), t.target && this.setTarget(t.target);
  }
  disposeInternal() {
    Aa(this.element), super.disposeInternal();
  }
  getMap() {
    return this.map_;
  }
  setMap(t) {
    this.map_ && Aa(this.element);
    for (let e = 0, i = this.listenerKeys.length; e < i; ++e)
      mt(this.listenerKeys[e]);
    this.listenerKeys.length = 0, this.map_ = t, t && ((this.target_ ? this.target_ : t.getOverlayContainerStopEvent()).appendChild(this.element), this.render !== nn && this.listenerKeys.push(
      et(t, vi.POSTRENDER, this.render, this)
    ), t.render());
  }
  render(t) {
  }
  setTarget(t) {
    this.target_ = typeof t == "string" ? document.getElementById(t) : t;
  }
}
const Gt = O1;
class F1 extends Gt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      render: t.render,
      target: t.target
    }), this.ulElement_ = document.createElement("ul"), this.collapsed_ = t.collapsed !== void 0 ? t.collapsed : !0, this.userCollapsed_ = this.collapsed_, this.overrideCollapsible_ = t.collapsible !== void 0, this.collapsible_ = t.collapsible !== void 0 ? t.collapsible : !0, this.collapsible_ || (this.collapsed_ = !1);
    const e = t.className !== void 0 ? t.className : "ol-attribution", i = t.tipLabel !== void 0 ? t.tipLabel : "Attributions", s = t.expandClassName !== void 0 ? t.expandClassName : e + "-expand", r = t.collapseLabel !== void 0 ? t.collapseLabel : "\u203A", o = t.collapseClassName !== void 0 ? t.collapseClassName : e + "-collapse";
    typeof r == "string" ? (this.collapseLabel_ = document.createElement("span"), this.collapseLabel_.textContent = r, this.collapseLabel_.className = o) : this.collapseLabel_ = r;
    const a = t.label !== void 0 ? t.label : "i";
    typeof a == "string" ? (this.label_ = document.createElement("span"), this.label_.textContent = a, this.label_.className = s) : this.label_ = a;
    const l = this.collapsible_ && !this.collapsed_ ? this.collapseLabel_ : this.label_;
    this.toggleButton_ = document.createElement("button"), this.toggleButton_.setAttribute("type", "button"), this.toggleButton_.setAttribute("aria-expanded", String(!this.collapsed_)), this.toggleButton_.title = i, this.toggleButton_.appendChild(l), this.toggleButton_.addEventListener(
      U.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const h = e + " " + ss + " " + Ao + (this.collapsed_ && this.collapsible_ ? " " + Uh : "") + (this.collapsible_ ? "" : " ol-uncollapsible"), c = this.element;
    c.className = h, c.appendChild(this.toggleButton_), c.appendChild(this.ulElement_), this.renderedAttributions_ = [], this.renderedVisible_ = !0;
  }
  collectSourceAttributions_(t) {
    const e = {}, i = [];
    let s = !0;
    const r = t.layerStatesArray;
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      if (!Cl(l, t.viewState))
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
            u[d] in e || (i.push(u[d]), e[u[d]] = !0);
        else
          u in e || (i.push(u), e[u] = !0);
    }
    return this.overrideCollapsible_ || this.setCollapsible(s), i;
  }
  updateElement_(t) {
    if (!t) {
      this.renderedVisible_ && (this.element.style.display = "none", this.renderedVisible_ = !1);
      return;
    }
    const e = this.collectSourceAttributions_(t), i = e.length > 0;
    if (this.renderedVisible_ != i && (this.element.style.display = i ? "" : "none", this.renderedVisible_ = i), !Ni(e, this.renderedAttributions_)) {
      v0(this.ulElement_);
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
    this.element.classList.toggle(Uh), this.collapsed_ ? io(this.collapseLabel_, this.label_) : io(this.label_, this.collapseLabel_), this.collapsed_ = !this.collapsed_, this.toggleButton_.setAttribute("aria-expanded", String(!this.collapsed_));
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
const N1 = F1;
class D1 extends Gt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      render: t.render,
      target: t.target
    });
    const e = t.className !== void 0 ? t.className : "ol-rotate", i = t.label !== void 0 ? t.label : "\u21E7", s = t.compassClassName !== void 0 ? t.compassClassName : "ol-compass";
    this.label_ = null, typeof i == "string" ? (this.label_ = document.createElement("span"), this.label_.className = s, this.label_.textContent = i) : (this.label_ = i, this.label_.classList.add(s));
    const r = t.tipLabel ? t.tipLabel : "Reset rotation", o = document.createElement("button");
    o.className = e + "-reset", o.setAttribute("type", "button"), o.title = r, o.appendChild(this.label_), o.addEventListener(
      U.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const a = e + " " + ss + " " + Ao, l = this.element;
    l.className = a, l.appendChild(o), this.callResetNorth_ = t.resetNorth ? t.resetNorth : void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.autoHide_ = t.autoHide !== void 0 ? t.autoHide : !0, this.rotation_ = void 0, this.autoHide_ && this.element.classList.add(Rr);
  }
  handleClick_(t) {
    t.preventDefault(), this.callResetNorth_ !== void 0 ? this.callResetNorth_() : this.resetNorth_();
  }
  resetNorth_() {
    const e = this.getMap().getView();
    if (!e)
      return;
    const i = e.getRotation();
    i !== void 0 && (this.duration_ > 0 && i % (2 * Math.PI) !== 0 ? e.animate({
      rotation: 0,
      duration: this.duration_,
      easing: rs
    }) : e.setRotation(0));
  }
  render(t) {
    const e = t.frameState;
    if (!e)
      return;
    const i = e.viewState.rotation;
    if (i != this.rotation_) {
      const s = "rotate(" + i + "rad)";
      if (this.autoHide_) {
        const r = this.element.classList.contains(Rr);
        !r && i === 0 ? this.element.classList.add(Rr) : r && i !== 0 && this.element.classList.remove(Rr);
      }
      this.label_.style.transform = s;
    }
    this.rotation_ = i;
  }
}
const k1 = D1;
class G1 extends Gt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      target: t.target
    });
    const e = t.className !== void 0 ? t.className : "ol-zoom", i = t.delta !== void 0 ? t.delta : 1, s = t.zoomInClassName !== void 0 ? t.zoomInClassName : e + "-in", r = t.zoomOutClassName !== void 0 ? t.zoomOutClassName : e + "-out", o = t.zoomInLabel !== void 0 ? t.zoomInLabel : "+", a = t.zoomOutLabel !== void 0 ? t.zoomOutLabel : "\u2013", l = t.zoomInTipLabel !== void 0 ? t.zoomInTipLabel : "Zoom in", h = t.zoomOutTipLabel !== void 0 ? t.zoomOutTipLabel : "Zoom out", c = document.createElement("button");
    c.className = s, c.setAttribute("type", "button"), c.title = l, c.appendChild(
      typeof o == "string" ? document.createTextNode(o) : o
    ), c.addEventListener(
      U.CLICK,
      this.handleClick_.bind(this, i),
      !1
    );
    const u = document.createElement("button");
    u.className = r, u.setAttribute("type", "button"), u.title = h, u.appendChild(
      typeof a == "string" ? document.createTextNode(a) : a
    ), u.addEventListener(
      U.CLICK,
      this.handleClick_.bind(this, -i),
      !1
    );
    const d = e + " " + ss + " " + Ao, f = this.element;
    f.className = d, f.appendChild(c), f.appendChild(u), this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleClick_(t, e) {
    e.preventDefault(), this.zoomByDelta_(t);
  }
  zoomByDelta_(t) {
    const i = this.getMap().getView();
    if (!i)
      return;
    const s = i.getZoom();
    if (s !== void 0) {
      const r = i.getConstrainedZoom(s + t);
      this.duration_ > 0 ? (i.getAnimating() && i.cancelAnimations(), i.animate({
        zoom: r,
        duration: this.duration_,
        easing: rs
      })) : i.setZoom(r);
    }
  }
}
const Pd = G1;
function $1(n) {
  n = n || {};
  const t = new Ee();
  return (n.zoom !== void 0 ? n.zoom : !0) && t.push(new Pd(n.zoomOptions)), (n.rotate !== void 0 ? n.rotate : !0) && t.push(new k1(n.rotateOptions)), (n.attribution !== void 0 ? n.attribution : !0) && t.push(new N1(n.attributionOptions)), t;
}
const Za = {
  ACTIVE: "active"
};
class B1 extends Oe {
  constructor(t) {
    super(), this.on, this.once, this.un, t && t.handleEvent && (this.handleEvent = t.handleEvent), this.map_ = null, this.setActive(!0);
  }
  getActive() {
    return this.get(Za.ACTIVE);
  }
  getMap() {
    return this.map_;
  }
  handleEvent(t) {
    return !0;
  }
  setActive(t) {
    this.set(Za.ACTIVE, t);
  }
  setMap(t) {
    this.map_ = t;
  }
}
function z1(n, t, e) {
  const i = n.getCenterInternal();
  if (i) {
    const s = [i[0] + t[0], i[1] + t[1]];
    n.animateInternal({
      duration: e !== void 0 ? e : 250,
      easing: r1,
      center: n.getConstrainedCenter(s)
    });
  }
}
function Vl(n, t, e, i) {
  const s = n.getZoom();
  if (s === void 0)
    return;
  const r = n.getConstrainedZoom(s + t), o = n.getResolutionForZoom(r);
  n.getAnimating() && n.cancelAnimations(), n.animate({
    resolution: o,
    anchor: e,
    duration: i !== void 0 ? i : 250,
    easing: rs
  });
}
const er = B1;
class Z1 extends er {
  constructor(t) {
    super(), t = t || {}, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == nt.DBLCLICK) {
      const i = t.originalEvent, s = t.map, r = t.coordinate, o = i.shiftKey ? -this.delta_ : this.delta_, a = s.getView();
      Vl(a, o, r, this.duration_), i.preventDefault(), e = !0;
    }
    return !e;
  }
}
const V1 = Z1;
class U1 extends er {
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
      if (t.type == nt.POINTERDRAG)
        this.handleDragEvent(t), t.originalEvent.preventDefault();
      else if (t.type == nt.POINTERUP) {
        const i = this.handleUpEvent(t);
        this.handlingDownUpSequence = i && this.targetPointers.length > 0;
      }
    } else if (t.type == nt.POINTERDOWN) {
      const i = this.handleDownEvent(t);
      this.handlingDownUpSequence = i, e = this.stopDown(i);
    } else
      t.type == nt.POINTERMOVE && this.handleMoveEvent(t);
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
function Ul(n) {
  const t = n.length;
  let e = 0, i = 0;
  for (let s = 0; s < t; s++)
    e += n[s].clientX, i += n[s].clientY;
  return [e / t, i / t];
}
const ki = U1;
function Va(n) {
  const t = arguments;
  return function(e) {
    let i = !0;
    for (let s = 0, r = t.length; s < r && (i = i && t[s](e), !!i); ++s)
      ;
    return i;
  };
}
const W1 = function(n) {
  const t = n.originalEvent;
  return t.altKey && !(t.metaKey || t.ctrlKey) && !t.shiftKey;
}, H1 = function(n) {
  const t = n.originalEvent;
  return t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, X1 = function(n) {
  const t = n.map.getTargetElement(), e = n.map.getOwnerDocument().activeElement;
  return t.contains(e);
}, Ad = function(n) {
  return n.map.getTargetElement().hasAttribute("tabindex") ? X1(n) : !0;
}, co = en, Od = function(n) {
  const t = n.originalEvent;
  return t.button == 0 && !(Zg && Vg && t.ctrlKey);
}, Y1 = un, j1 = function(n) {
  return n.type == nt.SINGLECLICK;
}, Wl = function(n) {
  const t = n.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && !t.shiftKey;
}, Fd = function(n) {
  const t = n.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, Nd = function(n) {
  const t = n.originalEvent, e = t.target.tagName;
  return e !== "INPUT" && e !== "SELECT" && e !== "TEXTAREA" && !t.target.isContentEditable;
}, aa = function(n) {
  const t = n.originalEvent;
  return Y(t !== void 0, 56), t.pointerType == "mouse";
}, Dd = function(n) {
  const t = n.originalEvent;
  return Y(t !== void 0, 56), t.isPrimary && t.button === 0;
};
class q1 extends ki {
  constructor(t) {
    super({
      stopDown: un
    }), t = t || {}, this.kinetic_ = t.kinetic, this.lastCentroid = null, this.lastPointersCount_, this.panning_ = !1;
    const e = t.condition ? t.condition : Va(Wl, Dd);
    this.condition_ = t.onFocusOnly ? Va(Ad, e) : e, this.noKinetic_ = !1;
  }
  handleDragEvent(t) {
    this.panning_ || (this.panning_ = !0, this.getMap().getView().beginInteraction());
    const e = this.targetPointers, i = Ul(e);
    if (e.length == this.lastPointersCount_) {
      if (this.kinetic_ && this.kinetic_.update(i[0], i[1]), this.lastCentroid) {
        const s = [
          this.lastCentroid[0] - i[0],
          i[1] - this.lastCentroid[1]
        ], o = t.map.getView();
        sd(s, o.getResolution()), El(s, o.getRotation()), o.adjustCenterInternal(s);
      }
    } else
      this.kinetic_ && this.kinetic_.begin();
    this.lastCentroid = i, this.lastPointersCount_ = e.length, t.originalEvent.preventDefault();
  }
  handleUpEvent(t) {
    const e = t.map, i = e.getView();
    if (this.targetPointers.length === 0) {
      if (!this.noKinetic_ && this.kinetic_ && this.kinetic_.end()) {
        const s = this.kinetic_.getDistance(), r = this.kinetic_.getAngle(), o = i.getCenterInternal(), a = e.getPixelFromCoordinateInternal(o), l = e.getCoordinateFromPixelInternal([
          a[0] - s * Math.cos(r),
          a[1] - s * Math.sin(r)
        ]);
        i.animateInternal({
          center: i.getConstrainedCenter(l),
          duration: 500,
          easing: rs
        });
      }
      return this.panning_ && (this.panning_ = !1, i.endInteraction()), !1;
    } else
      return this.kinetic_ && this.kinetic_.begin(), this.lastCentroid = null, !0;
  }
  handleDownEvent(t) {
    if (this.targetPointers.length > 0 && this.condition_(t)) {
      const i = t.map.getView();
      return this.lastCentroid = null, i.getAnimating() && i.cancelAnimations(), this.kinetic_ && this.kinetic_.begin(), this.noKinetic_ = this.targetPointers.length > 1, !0;
    } else
      return !1;
  }
}
const K1 = q1;
class J1 extends ki {
  constructor(t) {
    t = t || {}, super({
      stopDown: un
    }), this.condition_ = t.condition ? t.condition : H1, this.lastAngle_ = void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleDragEvent(t) {
    if (!aa(t))
      return;
    const e = t.map, i = e.getView();
    if (i.getConstraints().rotation === Ol)
      return;
    const s = e.getSize(), r = t.pixel, o = Math.atan2(s[1] / 2 - r[1], r[0] - s[0] / 2);
    if (this.lastAngle_ !== void 0) {
      const a = o - this.lastAngle_;
      i.adjustRotationInternal(-a);
    }
    this.lastAngle_ = o;
  }
  handleUpEvent(t) {
    return aa(t) ? (t.map.getView().endInteraction(this.duration_), !1) : !0;
  }
  handleDownEvent(t) {
    return aa(t) && Od(t) && this.condition_(t) ? (t.map.getView().beginInteraction(), this.lastAngle_ = void 0, !0) : !1;
  }
}
const Q1 = J1;
class tm extends fl {
  constructor(t) {
    super(), this.geometry_ = null, this.element_ = document.createElement("div"), this.element_.style.position = "absolute", this.element_.style.pointerEvents = "auto", this.element_.className = "ol-box " + t, this.map_ = null, this.startPixel_ = null, this.endPixel_ = null;
  }
  disposeInternal() {
    this.setMap(null);
  }
  render_() {
    const t = this.startPixel_, e = this.endPixel_, i = "px", s = this.element_.style;
    s.left = Math.min(t[0], e[0]) + i, s.top = Math.min(t[1], e[1]) + i, s.width = Math.abs(e[0] - t[0]) + i, s.height = Math.abs(e[1] - t[1]) + i;
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
    s[4] = s[0].slice(), this.geometry_ ? this.geometry_.setCoordinates([s]) : this.geometry_ = new Ai([s]);
  }
  getGeometry() {
    return this.geometry_;
  }
}
const em = tm, Lr = {
  BOXSTART: "boxstart",
  BOXDRAG: "boxdrag",
  BOXEND: "boxend",
  BOXCANCEL: "boxcancel"
};
class la extends Re {
  constructor(t, e, i) {
    super(t), this.coordinate = e, this.mapBrowserEvent = i;
  }
}
class im extends ki {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.box_ = new em(t.className || "ol-dragbox"), this.minArea_ = t.minArea !== void 0 ? t.minArea : 64, t.onBoxEnd && (this.onBoxEnd = t.onBoxEnd), this.startPixel_ = null, this.condition_ = t.condition ? t.condition : Od, this.boxEndCondition_ = t.boxEndCondition ? t.boxEndCondition : this.defaultBoxEndCondition;
  }
  defaultBoxEndCondition(t, e, i) {
    const s = i[0] - e[0], r = i[1] - e[1];
    return s * s + r * r >= this.minArea_;
  }
  getGeometry() {
    return this.box_.getGeometry();
  }
  handleDragEvent(t) {
    this.box_.setPixels(this.startPixel_, t.pixel), this.dispatchEvent(
      new la(
        Lr.BOXDRAG,
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
      new la(
        e ? Lr.BOXEND : Lr.BOXCANCEL,
        t.coordinate,
        t
      )
    ), !1;
  }
  handleDownEvent(t) {
    return this.condition_(t) ? (this.startPixel_ = t.pixel, this.box_.setMap(t.map), this.box_.setPixels(this.startPixel_, this.startPixel_), this.dispatchEvent(
      new la(
        Lr.BOXSTART,
        t.coordinate,
        t
      )
    ), !0) : !1;
  }
  onBoxEnd(t) {
  }
}
const nm = im;
class sm extends nm {
  constructor(t) {
    t = t || {};
    const e = t.condition ? t.condition : Fd;
    super({
      condition: e,
      className: t.className || "ol-dragzoom",
      minArea: t.minArea
    }), this.duration_ = t.duration !== void 0 ? t.duration : 200, this.out_ = t.out !== void 0 ? t.out : !1;
  }
  onBoxEnd(t) {
    const i = this.getMap().getView();
    let s = this.getGeometry();
    if (this.out_) {
      const r = i.rotatedExtentForGeometry(s), o = i.getResolutionForExtentInternal(r), a = i.getResolution() / o;
      s = s.clone(), s.scale(a * a);
    }
    i.fitInternal(s, {
      duration: this.duration_,
      easing: rs
    });
  }
}
const rm = sm, zi = {
  LEFT: 37,
  UP: 38,
  RIGHT: 39,
  DOWN: 40
};
class om extends er {
  constructor(t) {
    super(), t = t || {}, this.defaultCondition_ = function(e) {
      return Wl(e) && Nd(e);
    }, this.condition_ = t.condition !== void 0 ? t.condition : this.defaultCondition_, this.duration_ = t.duration !== void 0 ? t.duration : 100, this.pixelDelta_ = t.pixelDelta !== void 0 ? t.pixelDelta : 128;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == U.KEYDOWN) {
      const i = t.originalEvent, s = i.keyCode;
      if (this.condition_(t) && (s == zi.DOWN || s == zi.LEFT || s == zi.RIGHT || s == zi.UP)) {
        const o = t.map.getView(), a = o.getResolution() * this.pixelDelta_;
        let l = 0, h = 0;
        s == zi.DOWN ? h = -a : s == zi.LEFT ? l = -a : s == zi.RIGHT ? l = a : h = a;
        const c = [l, h];
        El(c, o.getRotation()), z1(o, c, this.duration_), i.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const am = om;
class lm extends er {
  constructor(t) {
    super(), t = t || {}, this.condition_ = t.condition ? t.condition : Nd, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 100;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == U.KEYDOWN || t.type == U.KEYPRESS) {
      const i = t.originalEvent, s = i.charCode;
      if (this.condition_(t) && (s == "+".charCodeAt(0) || s == "-".charCodeAt(0))) {
        const r = t.map, o = s == "+".charCodeAt(0) ? this.delta_ : -this.delta_, a = r.getView();
        Vl(a, o, void 0, this.duration_), i.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const hm = lm;
class cm {
  constructor(t, e, i) {
    this.decay_ = t, this.minVelocity_ = e, this.delay_ = i, this.points_ = [], this.angle_ = 0, this.initialVelocity_ = 0;
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
    let i = e - 3;
    for (; i > 0 && this.points_[i + 2] > t; )
      i -= 3;
    const s = this.points_[e + 2] - this.points_[i + 2];
    if (s < 1e3 / 60)
      return !1;
    const r = this.points_[e] - this.points_[i], o = this.points_[e + 1] - this.points_[i + 1];
    return this.angle_ = Math.atan2(o, r), this.initialVelocity_ = Math.sqrt(r * r + o * o) / s, this.initialVelocity_ > this.minVelocity_;
  }
  getDistance() {
    return (this.minVelocity_ - this.initialVelocity_) / this.decay_;
  }
  getAngle() {
    return this.angle_;
  }
}
const um = cm;
class dm extends er {
  constructor(t) {
    t = t || {}, super(
      t
    ), this.totalDelta_ = 0, this.lastDelta_ = 0, this.maxDelta_ = t.maxDelta !== void 0 ? t.maxDelta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.timeout_ = t.timeout !== void 0 ? t.timeout : 80, this.useAnchor_ = t.useAnchor !== void 0 ? t.useAnchor : !0, this.constrainResolution_ = t.constrainResolution !== void 0 ? t.constrainResolution : !1;
    const e = t.condition ? t.condition : co;
    this.condition_ = t.onFocusOnly ? Va(Ad, e) : e, this.lastAnchor_ = null, this.startTime_ = void 0, this.timeoutId_, this.mode_ = void 0, this.trackpadEventGap_ = 400, this.trackpadTimeoutId_, this.deltaPerZoom_ = 300;
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
    if (!this.condition_(t) || t.type !== U.WHEEL)
      return !0;
    const i = t.map, s = t.originalEvent;
    s.preventDefault(), this.useAnchor_ && (this.lastAnchor_ = t.coordinate);
    let r;
    if (t.type == U.WHEEL && (r = s.deltaY, Bg && s.deltaMode === WheelEvent.DOM_DELTA_PIXEL && (r /= Hu), s.deltaMode === WheelEvent.DOM_DELTA_LINE && (r *= 40)), r === 0)
      return !1;
    this.lastDelta_ = r;
    const o = Date.now();
    this.startTime_ === void 0 && (this.startTime_ = o), (!this.mode_ || o - this.startTime_ > this.trackpadEventGap_) && (this.mode_ = Math.abs(r) < 4 ? "trackpad" : "wheel");
    const a = i.getView();
    if (this.mode_ === "trackpad" && !(a.getConstrainResolution() || this.constrainResolution_))
      return this.trackpadTimeoutId_ ? clearTimeout(this.trackpadTimeoutId_) : (a.getAnimating() && a.cancelAnimations(), a.beginInteraction()), this.trackpadTimeoutId_ = setTimeout(
        this.endInteraction_.bind(this),
        this.timeout_
      ), a.adjustZoom(-r / this.deltaPerZoom_, this.lastAnchor_), this.startTime_ = o, !1;
    this.totalDelta_ += r;
    const l = Math.max(this.timeout_ - (o - this.startTime_), 0);
    return clearTimeout(this.timeoutId_), this.timeoutId_ = setTimeout(
      this.handleWheelZoom_.bind(this, i),
      l
    ), !1;
  }
  handleWheelZoom_(t) {
    const e = t.getView();
    e.getAnimating() && e.cancelAnimations();
    let i = -Et(
      this.totalDelta_,
      -this.maxDelta_ * this.deltaPerZoom_,
      this.maxDelta_ * this.deltaPerZoom_
    ) / this.deltaPerZoom_;
    (e.getConstrainResolution() || this.constrainResolution_) && (i = i ? i > 0 ? 1 : -1 : 0), Vl(e, i, this.lastAnchor_, this.duration_), this.mode_ = void 0, this.totalDelta_ = 0, this.lastAnchor_ = null, this.startTime_ = void 0, this.timeoutId_ = void 0;
  }
  setMouseAnchor(t) {
    this.useAnchor_ = t, t || (this.lastAnchor_ = null);
  }
}
const fm = dm;
class gm extends ki {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = un), super(e), this.anchor_ = null, this.lastAngle_ = void 0, this.rotating_ = !1, this.rotationDelta_ = 0, this.threshold_ = t.threshold !== void 0 ? t.threshold : 0.3, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleDragEvent(t) {
    let e = 0;
    const i = this.targetPointers[0], s = this.targetPointers[1], r = Math.atan2(
      s.clientY - i.clientY,
      s.clientX - i.clientX
    );
    if (this.lastAngle_ !== void 0) {
      const c = r - this.lastAngle_;
      this.rotationDelta_ += c, !this.rotating_ && Math.abs(this.rotationDelta_) > this.threshold_ && (this.rotating_ = !0), e = c;
    }
    this.lastAngle_ = r;
    const o = t.map, a = o.getView();
    if (a.getConstraints().rotation === Ol)
      return;
    const l = o.getViewport().getBoundingClientRect(), h = Ul(this.targetPointers);
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
const mm = gm;
class _m extends ki {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = un), super(e), this.anchor_ = null, this.duration_ = t.duration !== void 0 ? t.duration : 400, this.lastDistance_ = void 0, this.lastScaleDelta_ = 1;
  }
  handleDragEvent(t) {
    let e = 1;
    const i = this.targetPointers[0], s = this.targetPointers[1], r = i.clientX - s.clientX, o = i.clientY - s.clientY, a = Math.sqrt(r * r + o * o);
    this.lastDistance_ !== void 0 && (e = this.lastDistance_ / a), this.lastDistance_ = a;
    const l = t.map, h = l.getView();
    e != 1 && (this.lastScaleDelta_ = e);
    const c = l.getViewport().getBoundingClientRect(), u = Ul(this.targetPointers);
    u[0] -= c.left, u[1] -= c.top, this.anchor_ = l.getCoordinateFromPixelInternal(u), l.render(), h.adjustResolutionInternal(e, this.anchor_);
  }
  handleUpEvent(t) {
    if (this.targetPointers.length < 2) {
      const i = t.map.getView(), s = this.lastScaleDelta_ > 1 ? 1 : -1;
      return i.endInteraction(this.duration_, s), !1;
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
const pm = _m;
function ym(n) {
  n = n || {};
  const t = new Ee(), e = new um(-5e-3, 0.05, 100);
  return (n.altShiftDragRotate !== void 0 ? n.altShiftDragRotate : !0) && t.push(new Q1()), (n.doubleClickZoom !== void 0 ? n.doubleClickZoom : !0) && t.push(
    new V1({
      delta: n.zoomDelta,
      duration: n.zoomDuration
    })
  ), (n.dragPan !== void 0 ? n.dragPan : !0) && t.push(
    new K1({
      onFocusOnly: n.onFocusOnly,
      kinetic: e
    })
  ), (n.pinchRotate !== void 0 ? n.pinchRotate : !0) && t.push(new mm()), (n.pinchZoom !== void 0 ? n.pinchZoom : !0) && t.push(
    new pm({
      duration: n.zoomDuration
    })
  ), (n.keyboard !== void 0 ? n.keyboard : !0) && (t.push(new am()), t.push(
    new hm({
      delta: n.zoomDelta,
      duration: n.zoomDuration
    })
  )), (n.mouseWheelZoom !== void 0 ? n.mouseWheelZoom : !0) && t.push(
    new fm({
      onFocusOnly: n.onFocusOnly,
      duration: n.zoomDuration
    })
  ), (n.shiftDragZoom !== void 0 ? n.shiftDragZoom : !0) && t.push(
    new rm({
      duration: n.zoomDuration
    })
  ), t;
}
function oc(n) {
  return n[0] > 0 && n[1] > 0;
}
function vm(n, t, e) {
  return e === void 0 && (e = [0, 0]), e[0] = n[0] * t + 0.5 | 0, e[1] = n[1] * t + 0.5 | 0, e;
}
function fe(n, t) {
  return Array.isArray(n) ? n : (t === void 0 ? t = [n, n] : (t[0] = n, t[1] = n), t);
}
function kd(n) {
  if (n instanceof Po) {
    n.setMapInternal(null);
    return;
  }
  n instanceof Oo && n.getLayers().forEach(kd);
}
function Gd(n, t) {
  if (n instanceof Po) {
    n.setMapInternal(t);
    return;
  }
  if (n instanceof Oo) {
    const e = n.getLayers().getArray();
    for (let i = 0, s = e.length; i < s; ++i)
      Gd(e[i], t);
  }
}
class xm extends Oe {
  constructor(t) {
    super(), t = t || {}, this.on, this.once, this.un;
    const e = Cm(t);
    this.renderComplete_, this.loaded_ = !0, this.boundHandleBrowserEvent_ = this.handleBrowserEvent.bind(this), this.maxTilesLoading_ = t.maxTilesLoading !== void 0 ? t.maxTilesLoading : 16, this.pixelRatio_ = t.pixelRatio !== void 0 ? t.pixelRatio : Hu, this.postRenderTimeoutHandle_, this.animationDelayKey_, this.animationDelay_ = this.animationDelay_.bind(this), this.coordinateToPixelTransform_ = $e(), this.pixelToCoordinateTransform_ = $e(), this.frameIndex_ = 0, this.frameState_ = null, this.previousExtent_ = null, this.viewPropertyListenerKey_ = null, this.viewChangeListenerKey_ = null, this.layerGroupPropertyListenerKeys_ = null, this.viewport_ = document.createElement("div"), this.viewport_.className = "ol-viewport" + ("ontouchstart" in window ? " ol-touch" : ""), this.viewport_.style.position = "relative", this.viewport_.style.overflow = "hidden", this.viewport_.style.width = "100%", this.viewport_.style.height = "100%", this.overlayContainer_ = document.createElement("div"), this.overlayContainer_.style.position = "absolute", this.overlayContainer_.style.zIndex = "0", this.overlayContainer_.style.width = "100%", this.overlayContainer_.style.height = "100%", this.overlayContainer_.style.pointerEvents = "none", this.overlayContainer_.className = "ol-overlaycontainer", this.viewport_.appendChild(this.overlayContainer_), this.overlayContainerStopEvent_ = document.createElement("div"), this.overlayContainerStopEvent_.style.position = "absolute", this.overlayContainerStopEvent_.style.zIndex = "0", this.overlayContainerStopEvent_.style.width = "100%", this.overlayContainerStopEvent_.style.height = "100%", this.overlayContainerStopEvent_.style.pointerEvents = "none", this.overlayContainerStopEvent_.className = "ol-overlaycontainer-stopevent", this.viewport_.appendChild(this.overlayContainerStopEvent_), this.mapBrowserEventHandler_ = null, this.moveTolerance_ = t.moveTolerance, this.keyboardEventTarget_ = e.keyboardEventTarget, this.targetChangeHandlerKeys_ = null, this.controls = e.controls || $1(), this.interactions = e.interactions || ym({
      onFocusOnly: !0
    }), this.overlays_ = e.overlays, this.overlayIdIndex_ = {}, this.renderer_ = null, this.postRenderFunctions_ = [], this.tileQueue_ = new N0(
      this.getTilePriority.bind(this),
      this.handleTileChange_.bind(this)
    ), this.addChangeListener(
      Ot.LAYERGROUP,
      this.handleLayerGroupChanged_
    ), this.addChangeListener(Ot.VIEW, this.handleViewChanged_), this.addChangeListener(Ot.SIZE, this.handleSizeChanged_), this.addChangeListener(Ot.TARGET, this.handleTargetChanged_), this.setProperties(e.values);
    const i = this;
    t.view && !(t.view instanceof si) && t.view.then(function(s) {
      i.setView(new si(s));
    }), this.controls.addEventListener(
      Dt.ADD,
      function(s) {
        s.element.setMap(this);
      }.bind(this)
    ), this.controls.addEventListener(
      Dt.REMOVE,
      function(s) {
        s.element.setMap(null);
      }.bind(this)
    ), this.interactions.addEventListener(
      Dt.ADD,
      function(s) {
        s.element.setMap(this);
      }.bind(this)
    ), this.interactions.addEventListener(
      Dt.REMOVE,
      function(s) {
        s.element.setMap(null);
      }.bind(this)
    ), this.overlays_.addEventListener(
      Dt.ADD,
      function(s) {
        this.addOverlayInternal_(s.element);
      }.bind(this)
    ), this.overlays_.addEventListener(
      Dt.REMOVE,
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
    Gd(t.layer, this);
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
  forEachFeatureAtPixel(t, e, i) {
    if (!this.frameState_ || !this.renderer_)
      return;
    const s = this.getCoordinateFromPixelInternal(t);
    i = i !== void 0 ? i : {};
    const r = i.hitTolerance !== void 0 ? i.hitTolerance : 0, o = i.layerFilter !== void 0 ? i.layerFilter : en, a = i.checkWrapped !== !1;
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
    const i = [];
    return this.forEachFeatureAtPixel(
      t,
      function(s) {
        i.push(s);
      },
      e
    ), i;
  }
  getAllLayers() {
    const t = [];
    function e(i) {
      i.forEach(function(s) {
        s instanceof Oo ? e(s.getLayers()) : t.push(s);
      });
    }
    return e(this.getLayers()), t;
  }
  hasFeatureAtPixel(t, e) {
    if (!this.frameState_ || !this.renderer_)
      return !1;
    const i = this.getCoordinateFromPixelInternal(t);
    e = e !== void 0 ? e : {};
    const s = e.layerFilter !== void 0 ? e.layerFilter : en, r = e.hitTolerance !== void 0 ? e.hitTolerance : 0, o = e.checkWrapped !== !1;
    return this.renderer_.hasFeatureAtCoordinate(
      i,
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
    const e = this.viewport_.getBoundingClientRect(), i = "changedTouches" in t ? t.changedTouches[0] : t;
    return [
      i.clientX - e.left,
      i.clientY - e.top
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
    return qn(
      this.getCoordinateFromPixelInternal(t),
      this.getView().getProjection()
    );
  }
  getCoordinateFromPixelInternal(t) {
    const e = this.frameState_;
    return e ? Nt(
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
    if (t instanceof Ee) {
      e.setLayers(t);
      return;
    }
    const i = e.getLayers();
    i.clear(), i.extend(t);
  }
  getLayers() {
    return this.getLayerGroup().getLayers();
  }
  getLoadingOrNotReady() {
    const t = this.getLayerGroup().getLayerStatesArray();
    for (let e = 0, i = t.length; e < i; ++e) {
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
    const e = vt(
      t,
      this.getView().getProjection()
    );
    return this.getPixelFromCoordinateInternal(e);
  }
  getPixelFromCoordinateInternal(t) {
    const e = this.frameState_;
    return e ? Nt(
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
  getTilePriority(t, e, i, s) {
    return D0(
      this.frameState_,
      t,
      e,
      i,
      s
    );
  }
  handleBrowserEvent(t, e) {
    e = e || t.type;
    const i = new ei(e, this, t);
    this.handleMapBrowserEvent(i);
  }
  handleMapBrowserEvent(t) {
    if (!this.frameState_)
      return;
    const e = t.originalEvent, i = e.type;
    if (i === Na.POINTERDOWN || i === U.WHEEL || i === U.KEYDOWN) {
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
        if (o[Wt.ANIMATING] || o[Wt.INTERACTING]) {
          const a = Date.now() - t.time > 8;
          s = a ? 0 : 8, r = a ? 0 : 2;
        }
      }
      e.getTilesLoading() < s && (e.reprioritize(), e.loadMoreTiles(s, r));
    }
    t && this.renderer_ && !t.animate && (this.renderComplete_ === !0 ? (this.hasListener(Ri.RENDERCOMPLETE) && this.renderer_.dispatchRenderEvent(
      Ri.RENDERCOMPLETE,
      t
    ), this.loaded_ === !1 && (this.loaded_ = !0, this.dispatchEvent(
      new Tn(vi.LOADEND, this, t)
    ))) : this.loaded_ === !0 && (this.loaded_ = !1, this.dispatchEvent(
      new Tn(vi.LOADSTART, this, t)
    )));
    const i = this.postRenderFunctions_;
    for (let s = 0, r = i.length; s < r; ++s)
      i[s](this, t);
    i.length = 0;
  }
  handleSizeChanged_() {
    this.getView() && !this.getView().getAnimating() && this.getView().resolveConstraints(0), this.render();
  }
  handleTargetChanged_() {
    if (this.mapBrowserEventHandler_) {
      for (let e = 0, i = this.targetChangeHandlerKeys_.length; e < i; ++e)
        mt(this.targetChangeHandlerKeys_[e]);
      this.targetChangeHandlerKeys_ = null, this.viewport_.removeEventListener(
        U.CONTEXTMENU,
        this.boundHandleBrowserEvent_
      ), this.viewport_.removeEventListener(
        U.WHEEL,
        this.boundHandleBrowserEvent_
      ), this.mapBrowserEventHandler_.dispose(), this.mapBrowserEventHandler_ = null, Aa(this.viewport_);
    }
    const t = this.getTargetElement();
    if (!t)
      this.renderer_ && (clearTimeout(this.postRenderTimeoutHandle_), this.postRenderTimeoutHandle_ = void 0, this.postRenderFunctions_.length = 0, this.renderer_.dispose(), this.renderer_ = null), this.animationDelayKey_ && (cancelAnimationFrame(this.animationDelayKey_), this.animationDelayKey_ = void 0);
    else {
      t.appendChild(this.viewport_), this.renderer_ || (this.renderer_ = new T0(this)), this.mapBrowserEventHandler_ = new P0(
        this,
        this.moveTolerance_
      );
      for (const s in nt)
        this.mapBrowserEventHandler_.addEventListener(
          nt[s],
          this.handleMapBrowserEvent.bind(this)
        );
      this.viewport_.addEventListener(
        U.CONTEXTMENU,
        this.boundHandleBrowserEvent_,
        !1
      ), this.viewport_.addEventListener(
        U.WHEEL,
        this.boundHandleBrowserEvent_,
        Xu ? { passive: !1 } : !1
      );
      const e = this.getOwnerDocument().defaultView, i = this.keyboardEventTarget_ ? this.keyboardEventTarget_ : t;
      this.targetChangeHandlerKeys_ = [
        et(
          i,
          U.KEYDOWN,
          this.handleBrowserEvent,
          this
        ),
        et(
          i,
          U.KEYPRESS,
          this.handleBrowserEvent,
          this
        ),
        et(e, U.RESIZE, this.updateSize, this)
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
    this.viewPropertyListenerKey_ && (mt(this.viewPropertyListenerKey_), this.viewPropertyListenerKey_ = null), this.viewChangeListenerKey_ && (mt(this.viewChangeListenerKey_), this.viewChangeListenerKey_ = null);
    const t = this.getView();
    t && (this.updateViewportSize_(), this.viewPropertyListenerKey_ = et(
      t,
      Wn.PROPERTYCHANGE,
      this.handleViewPropertyChanged_,
      this
    ), this.viewChangeListenerKey_ = et(
      t,
      U.CHANGE,
      this.handleViewPropertyChanged_,
      this
    ), t.resolveConstraints(0)), this.render();
  }
  handleLayerGroupChanged_() {
    this.layerGroupPropertyListenerKeys_ && (this.layerGroupPropertyListenerKeys_.forEach(mt), this.layerGroupPropertyListenerKeys_ = null);
    const t = this.getLayerGroup();
    t && (this.handleLayerAdd_(new Ci("addlayer", t)), this.layerGroupPropertyListenerKeys_ = [
      et(t, Wn.PROPERTYCHANGE, this.render, this),
      et(t, U.CHANGE, this.render, this),
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
    for (let e = 0, i = t.length; e < i; ++e) {
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
    kd(t.layer);
  }
  removeOverlay(t) {
    return this.getOverlays().remove(t);
  }
  renderFrame_(t) {
    const e = this.getSize(), i = this.getView(), s = this.frameState_;
    let r = null;
    if (e !== void 0 && oc(e) && i && i.isDef()) {
      const o = i.getHints(
        this.frameState_ ? this.frameState_.viewHints : void 0
      ), a = i.getState();
      if (r = {
        animate: !1,
        coordinateToPixelTransform: this.coordinateToPixelTransform_,
        declutterTree: null,
        extent: Ia(
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
        mapId: q(this),
        renderTargets: {}
      }, a.nextCenter && a.nextResolution) {
        const l = isNaN(a.nextRotation) ? a.rotation : a.nextRotation;
        r.nextExtent = Ia(
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
    ), s && (!this.previousExtent_ || !vl(this.previousExtent_) && !Fs(r.extent, this.previousExtent_)) && (this.dispatchEvent(
      new Tn(vi.MOVESTART, this, s)
    ), this.previousExtent_ = Qs(this.previousExtent_)), this.previousExtent_ && !r.viewHints[Wt.ANIMATING] && !r.viewHints[Wt.INTERACTING] && !Fs(r.extent, this.previousExtent_) && (this.dispatchEvent(
      new Tn(vi.MOVEEND, this, r)
    ), ju(r.extent, this.previousExtent_))), this.dispatchEvent(new Tn(vi.POSTRENDER, this, r)), this.renderComplete_ = this.hasListener(vi.LOADSTART) || this.hasListener(vi.LOADEND) || this.hasListener(Ri.RENDERCOMPLETE) ? !this.tileQueue_.getTilesLoading() && !this.tileQueue_.getCount() && !this.getLoadingOrNotReady() : void 0, this.postRenderTimeoutHandle_ || (this.postRenderTimeoutHandle_ = setTimeout(() => {
      this.postRenderTimeoutHandle_ = void 0, this.handlePostRender();
    }, 0));
  }
  setLayerGroup(t) {
    const e = this.getLayerGroup();
    e && this.handleLayerRemove_(new Ci("removelayer", e)), this.set(Ot.LAYERGROUP, t);
  }
  setSize(t) {
    this.set(Ot.SIZE, t);
  }
  setTarget(t) {
    this.set(Ot.TARGET, t);
  }
  setView(t) {
    if (!t || t instanceof si) {
      this.set(Ot.VIEW, t);
      return;
    }
    this.set(Ot.VIEW, new si());
    const e = this;
    t.then(function(i) {
      e.setView(new si(i));
    });
  }
  updateSize() {
    const t = this.getTargetElement();
    let e;
    if (t) {
      const i = getComputedStyle(t), s = t.offsetWidth - parseFloat(i.borderLeftWidth) - parseFloat(i.paddingLeft) - parseFloat(i.paddingRight) - parseFloat(i.borderRightWidth), r = t.offsetHeight - parseFloat(i.borderTopWidth) - parseFloat(i.paddingTop) - parseFloat(i.paddingBottom) - parseFloat(i.borderBottomWidth);
      !isNaN(s) && !isNaN(r) && (e = [s, r], !oc(e) && !!(t.offsetWidth || t.offsetHeight || t.getClientRects().length) && console.warn(
        "No map visible because the map container's width or height are 0."
      ));
    }
    this.setSize(e), this.updateViewportSize_();
  }
  updateViewportSize_() {
    const t = this.getView();
    if (t) {
      let e;
      const i = getComputedStyle(this.viewport_);
      i.width && i.height && (e = [
        parseInt(i.width, 10),
        parseInt(i.height, 10)
      ]), t.setViewportSize(e);
    }
  }
}
function Cm(n) {
  let t = null;
  n.keyboardEventTarget !== void 0 && (t = typeof n.keyboardEventTarget == "string" ? document.getElementById(n.keyboardEventTarget) : n.keyboardEventTarget);
  const e = {}, i = n.layers && typeof n.layers.getLayers == "function" ? n.layers : new Oo({
    layers: n.layers
  });
  e[Ot.LAYERGROUP] = i, e[Ot.TARGET] = n.target, e[Ot.VIEW] = n.view instanceof si ? n.view : new si();
  let s;
  n.controls !== void 0 && (Array.isArray(n.controls) ? s = new Ee(n.controls.slice()) : (Y(
    typeof n.controls.getArray == "function",
    47
  ), s = n.controls));
  let r;
  n.interactions !== void 0 && (Array.isArray(n.interactions) ? r = new Ee(n.interactions.slice()) : (Y(
    typeof n.interactions.getArray == "function",
    48
  ), r = n.interactions));
  let o;
  return n.overlays !== void 0 ? Array.isArray(n.overlays) ? o = new Ee(n.overlays.slice()) : (Y(
    typeof n.overlays.getArray == "function",
    49
  ), o = n.overlays) : o = new Ee(), {
    controls: s,
    interactions: r,
    keyboardEventTarget: t,
    overlays: o,
    values: e
  };
}
const Mm = xm;
class Hl extends Oe {
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
    const t = new Hl(this.hasProperties() ? this.getProperties() : null);
    t.setGeometryName(this.getGeometryName());
    const e = this.getGeometry();
    e && t.setGeometry(e.clone());
    const i = this.getStyle();
    return i && t.setStyle(i), t;
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
    this.geometryChangeKey_ && (mt(this.geometryChangeKey_), this.geometryChangeKey_ = null);
    const t = this.getGeometry();
    t && (this.geometryChangeKey_ = et(
      t,
      U.CHANGE,
      this.handleGeometryChange_,
      this
    )), this.changed();
  }
  setGeometry(t) {
    this.set(this.geometryName_, t);
  }
  setStyle(t) {
    this.style_ = t, this.styleFunction_ = t ? Em(t) : void 0, this.changed();
  }
  setId(t) {
    this.id_ = t, this.changed();
  }
  setGeometryName(t) {
    this.removeChangeListener(this.geometryName_, this.handleGeometryChanged_), this.geometryName_ = t, this.addChangeListener(this.geometryName_, this.handleGeometryChanged_), this.handleGeometryChanged_();
  }
}
function Em(n) {
  if (typeof n == "function")
    return n;
  {
    let t;
    return Array.isArray(n) ? t = n : (Y(typeof n.getZIndex == "function", 41), t = [n]), function() {
      return t;
    };
  }
}
const Ie = Hl, xt = {
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
class wm extends Re {
  constructor(t) {
    super(U.ERROR), this.code = t.code, this.message = t.message;
  }
}
class Sm extends Oe {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.position_ = null, this.transform_ = bl, this.watchId_ = void 0, this.addChangeListener(xt.PROJECTION, this.handleProjectionChanged_), this.addChangeListener(xt.TRACKING, this.handleTrackingChanged_), t.projection !== void 0 && this.setProjection(t.projection), t.trackingOptions !== void 0 && this.setTrackingOptions(t.trackingOptions), this.setTracking(t.tracking !== void 0 ? t.tracking : !1);
  }
  disposeInternal() {
    this.setTracking(!1), super.disposeInternal();
  }
  handleProjectionChanged_() {
    const t = this.getProjection();
    t && (this.transform_ = Fo(
      Q("EPSG:4326"),
      t
    ), this.position_ && this.set(xt.POSITION, this.transform_(this.position_)));
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
    this.set(xt.ACCURACY, e.accuracy), this.set(
      xt.ALTITUDE,
      e.altitude === null ? void 0 : e.altitude
    ), this.set(
      xt.ALTITUDE_ACCURACY,
      e.altitudeAccuracy === null ? void 0 : e.altitudeAccuracy
    ), this.set(
      xt.HEADING,
      e.heading === null ? void 0 : ji(e.heading)
    ), this.position_ ? (this.position_[0] = e.longitude, this.position_[1] = e.latitude) : this.position_ = [e.longitude, e.latitude];
    const i = this.transform_(this.position_);
    this.set(xt.POSITION, i), this.set(xt.SPEED, e.speed === null ? void 0 : e.speed);
    const s = S1(this.position_, e.accuracy);
    s.applyTransform(this.transform_), this.set(xt.ACCURACY_GEOMETRY, s), this.changed();
  }
  positionError_(t) {
    this.dispatchEvent(new wm(t));
  }
  getAccuracy() {
    return this.get(xt.ACCURACY);
  }
  getAccuracyGeometry() {
    return this.get(xt.ACCURACY_GEOMETRY) || null;
  }
  getAltitude() {
    return this.get(xt.ALTITUDE);
  }
  getAltitudeAccuracy() {
    return this.get(xt.ALTITUDE_ACCURACY);
  }
  getHeading() {
    return this.get(xt.HEADING);
  }
  getPosition() {
    return this.get(xt.POSITION);
  }
  getProjection() {
    return this.get(xt.PROJECTION);
  }
  getSpeed() {
    return this.get(xt.SPEED);
  }
  getTracking() {
    return this.get(xt.TRACKING);
  }
  getTrackingOptions() {
    return this.get(xt.TRACKING_OPTIONS);
  }
  setProjection(t) {
    this.set(xt.PROJECTION, Q(t));
  }
  setTracking(t) {
    this.set(xt.TRACKING, t);
  }
  setTrackingOptions(t) {
    this.set(xt.TRACKING_OPTIONS, t);
  }
}
const Rm = Sm;
class Xl {
  constructor(t) {
    t = t || {}, this.color_ = t.color !== void 0 ? t.color : null;
  }
  clone() {
    const t = this.getColor();
    return new Xl({
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
const Vt = Xl;
function $d(n, t, e, i, s, r, o) {
  let a, l;
  const h = (e - t) / i;
  if (h === 1)
    a = t;
  else if (h === 2)
    a = t, l = s;
  else if (h !== 0) {
    let c = n[t], u = n[t + 1], d = 0;
    const f = [0];
    for (let _ = t + i; _ < e; _ += i) {
      const y = n[_], p = n[_ + 1];
      d += Math.sqrt((y - c) * (y - c) + (p - u) * (p - u)), f.push(d), c = y, u = p;
    }
    const g = s * d, m = Lg(f, g);
    m < 0 ? (l = (g - f[-m - 2]) / (f[-m - 1] - f[-m - 2]), a = t + (-m - 2) * i) : a = t + m * i;
  }
  o = o > 1 ? o : 2, r = r || new Array(o);
  for (let c = 0; c < o; ++c)
    r[c] = a === void 0 ? NaN : l === void 0 ? n[a + c] : ii(n[a + c], n[a + i + c], l);
  return r;
}
function Ua(n, t, e, i, s, r) {
  if (e == t)
    return null;
  let o;
  if (s < n[t + i - 1])
    return r ? (o = n.slice(t, t + i), o[i - 1] = s, o) : null;
  if (n[e - 1] < s)
    return r ? (o = n.slice(e - i, e), o[i - 1] = s, o) : null;
  if (s == n[t + i - 1])
    return n.slice(t, t + i);
  let a = t / i, l = e / i;
  for (; a < l; ) {
    const d = a + l >> 1;
    s < n[(d + 1) * i - 1] ? l = d : a = d + 1;
  }
  const h = n[a * i - 1];
  if (s == h)
    return n.slice((a - 1) * i, (a - 1) * i + i);
  const c = n[(a + 1) * i - 1], u = (s - h) / (c - h);
  o = [];
  for (let d = 0; d < i - 1; ++d)
    o.push(
      ii(
        n[(a - 1) * i + d],
        n[a * i + d],
        u
      )
    );
  return o.push(s), o;
}
function Tm(n, t, e, i, s, r, o) {
  if (o)
    return Ua(
      n,
      t,
      e[e.length - 1],
      i,
      s,
      r
    );
  let a;
  if (s < n[i - 1])
    return r ? (a = n.slice(0, i), a[i - 1] = s, a) : null;
  if (n[n.length - 1] < s)
    return r ? (a = n.slice(n.length - i), a[i - 1] = s, a) : null;
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    if (t != c) {
      if (s < n[t + i - 1])
        return null;
      if (s <= n[c - 1])
        return Ua(
          n,
          t,
          c,
          i,
          s,
          !1
        );
      t = c;
    }
  }
  return null;
}
function Bd(n, t, e, i) {
  let s = n[t], r = n[t + 1], o = 0;
  for (let a = t + i; a < e; a += i) {
    const l = n[a], h = n[a + 1];
    o += Math.sqrt((l - s) * (l - s) + (h - r) * (h - r)), s = l, r = h;
  }
  return o;
}
class uo extends Di {
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
    this.flatCoordinates ? Qt(this.flatCoordinates, t) : this.flatCoordinates = t.slice(), this.changed();
  }
  clone() {
    const t = new uo(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    return s < dn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Nl(
        this.flatCoordinates,
        0,
        this.flatCoordinates.length,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), kl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      this.maxDelta_,
      !1,
      t,
      e,
      i,
      s
    ));
  }
  forEachSegment(t) {
    return Rd(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinateAtM(t, e) {
    return this.layout != "XYM" && this.layout != "XYZM" ? null : (e = e !== void 0 ? e : !1, Ua(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e
    ));
  }
  getCoordinates() {
    return Ei(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinateAt(t, e) {
    return $d(
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
    return Bd(
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
    return e.length = Bl(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e,
      0
    ), new uo(e, "XY");
  }
  getType() {
    return "LineString";
  }
  intersectsExtent(t) {
    return Do(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = No(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const li = uo;
class Yl {
  constructor(t) {
    t = t || {}, this.color_ = t.color !== void 0 ? t.color : null, this.lineCap_ = t.lineCap, this.lineDash_ = t.lineDash !== void 0 ? t.lineDash : null, this.lineDashOffset_ = t.lineDashOffset, this.lineJoin_ = t.lineJoin, this.miterLimit_ = t.miterLimit, this.width_ = t.width;
  }
  clone() {
    const t = this.getColor();
    return new Yl({
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
const Xt = Yl, Pt = {
  IDLE: 0,
  LOADING: 1,
  LOADED: 2,
  ERROR: 3,
  EMPTY: 4
};
class jl {
  constructor(t) {
    this.opacity_ = t.opacity, this.rotateWithView_ = t.rotateWithView, this.rotation_ = t.rotation, this.scale_ = t.scale, this.scaleArray_ = fe(t.scale), this.displacement_ = t.displacement, this.declutterMode_ = t.declutterMode;
  }
  clone() {
    const t = this.getScale();
    return new jl({
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
    return H();
  }
  getImage(t) {
    return H();
  }
  getHitDetectionImage() {
    return H();
  }
  getPixelRatio(t) {
    return 1;
  }
  getImageState() {
    return H();
  }
  getImageSize() {
    return H();
  }
  getOrigin() {
    return H();
  }
  getSize() {
    return H();
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
    this.scale_ = t, this.scaleArray_ = fe(t);
  }
  listenImageChange(t) {
    H();
  }
  load() {
    H();
  }
  unlistenImageChange(t) {
    H();
  }
}
const zd = jl;
function ke(n) {
  return Array.isArray(n) ? ed(n) : n;
}
class ql extends zd {
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
    const t = this.getScale(), e = new ql({
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
    const e = this.getDisplacement(), i = this.getScaleArray();
    return [
      t[0] / 2 - e[0] / i[0],
      t[1] / 2 + e[1] / i[1]
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
      const i = this.renderOptions_, s = pe(
        i.size * t,
        i.size * t
      );
      this.draw_(i, s, t), e = s.canvas, this.canvas_[t] = e;
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
    return Pt.LOADED;
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
  calculateLineJoinSize_(t, e, i) {
    if (e === 0 || this.points_ === 1 / 0 || t !== "bevel" && t !== "miter")
      return e;
    let s = this.radius_, r = this.radius2_ === void 0 ? s : this.radius2_;
    if (s < r) {
      const E = s;
      s = r, r = E;
    }
    const o = this.radius2_ === void 0 ? this.points_ : this.points_ * 2, a = 2 * Math.PI / o, l = r * Math.sin(a), h = Math.sqrt(r * r - l * l), c = s - h, u = Math.sqrt(l * l + c * c), d = u / l;
    if (t === "miter" && d <= i)
      return d * e;
    const f = e / 2 / d, g = e / 2 * (c / u), _ = Math.sqrt((s + f) * (s + f) + g * g) - s;
    if (this.radius2_ === void 0 || t === "bevel")
      return _ * 2;
    const y = s * Math.sin(a), p = Math.sqrt(s * s - y * y), v = r - p, C = Math.sqrt(y * y + v * v) / y;
    if (C <= i) {
      const E = C * e / 2 - r - s;
      return 2 * Math.max(_, E);
    }
    return _ * 2;
  }
  createRenderOptions() {
    let t = Xn, e = 0, i = null, s = 0, r, o = 0;
    this.stroke_ && (r = this.stroke_.getColor(), r === null && (r = Gs), r = ke(r), o = this.stroke_.getWidth(), o === void 0 && (o = Bs), i = this.stroke_.getLineDash(), s = this.stroke_.getLineDashOffset(), t = this.stroke_.getLineJoin(), t === void 0 && (t = Xn), e = this.stroke_.getMiterLimit(), e === void 0 && (e = ks));
    const a = this.calculateLineJoinSize_(t, o, e), l = Math.max(this.radius_, this.radius2_ || 0), h = Math.ceil(2 * l + a);
    return {
      strokeStyle: r,
      strokeWidth: o,
      size: h,
      lineDash: i,
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
  draw_(t, e, i) {
    if (e.scale(i, i), e.translate(t.size / 2, t.size / 2), this.createPath_(e), this.fill_) {
      let s = this.fill_.getColor();
      s === null && (s = ai), e.fillStyle = ke(s), e.fill();
    }
    this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
  createHitDetectionCanvas_(t) {
    if (this.fill_) {
      let e = this.fill_.getColor(), i = 0;
      if (typeof e == "string" && (e = Qr(e)), e === null ? i = 1 : Array.isArray(e) && (i = e.length === 4 ? e[3] : 1), i === 0) {
        const s = pe(
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
    const i = this.radius_;
    if (e === 1 / 0)
      t.arc(0, 0, i, 0, 2 * Math.PI);
    else {
      const s = this.radius2_ === void 0 ? i : this.radius2_;
      this.radius2_ !== void 0 && (e *= 2);
      const r = this.angle_ - Math.PI / 2, o = 2 * Math.PI / e;
      for (let a = 0; a < e; a++) {
        const l = r + a * o, h = a % 2 === 0 ? i : s;
        t.lineTo(h * Math.cos(l), h * Math.sin(l));
      }
      t.closePath();
    }
  }
  drawHitDetectionCanvas_(t, e) {
    e.translate(t.size / 2, t.size / 2), this.createPath_(e), e.fillStyle = ai, e.fill(), this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
}
const Zd = ql;
class Kl extends Zd {
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
    const t = this.getScale(), e = new Kl({
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
const we = Kl;
class wi {
  constructor(t) {
    t = t || {}, this.geometry_ = null, this.geometryFunction_ = ac, t.geometry !== void 0 && this.setGeometry(t.geometry), this.fill_ = t.fill !== void 0 ? t.fill : null, this.image_ = t.image !== void 0 ? t.image : null, this.renderer_ = t.renderer !== void 0 ? t.renderer : null, this.hitDetectionRenderer_ = t.hitDetectionRenderer !== void 0 ? t.hitDetectionRenderer : null, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.text_ = t.text !== void 0 ? t.text : null, this.zIndex_ = t.zIndex;
  }
  clone() {
    let t = this.getGeometry();
    return t && typeof t == "object" && (t = t.clone()), new wi({
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
    }) : this.geometryFunction_ = ac, this.geometry_ = t;
  }
  setZIndex(t) {
    this.zIndex_ = t;
  }
}
function bm(n) {
  let t;
  if (typeof n == "function")
    t = n;
  else {
    let e;
    Array.isArray(n) ? e = n : (Y(typeof n.getZIndex == "function", 41), e = [n]), t = function() {
      return e;
    };
  }
  return t;
}
let ha = null;
function Lm(n, t) {
  if (!ha) {
    const e = new Vt({
      color: "rgba(255,255,255,0.4)"
    }), i = new Xt({
      color: "#3399CC",
      width: 1.25
    });
    ha = [
      new wi({
        image: new we({
          fill: e,
          stroke: i,
          radius: 5
        }),
        fill: e,
        stroke: i
      })
    ];
  }
  return ha;
}
function Vd() {
  const n = {}, t = [255, 255, 255, 1], e = [0, 153, 255, 1], i = 3;
  return n.Polygon = [
    new wi({
      fill: new Vt({
        color: [255, 255, 255, 0.5]
      })
    })
  ], n.MultiPolygon = n.Polygon, n.LineString = [
    new wi({
      stroke: new Xt({
        color: t,
        width: i + 2
      })
    }),
    new wi({
      stroke: new Xt({
        color: e,
        width: i
      })
    })
  ], n.MultiLineString = n.LineString, n.Circle = n.Polygon.concat(n.LineString), n.Point = [
    new wi({
      image: new we({
        radius: i * 2,
        fill: new Vt({
          color: e
        }),
        stroke: new Xt({
          color: t,
          width: i / 2
        })
      }),
      zIndex: 1 / 0
    })
  ], n.MultiPoint = n.Point, n.GeometryCollection = n.Polygon.concat(
    n.LineString,
    n.Point
  ), n;
}
function ac(n) {
  return n.getGeometry();
}
const Zt = wi, Im = "#333";
class Jl {
  constructor(t) {
    t = t || {}, this.font_ = t.font, this.rotation_ = t.rotation, this.rotateWithView_ = t.rotateWithView, this.scale_ = t.scale, this.scaleArray_ = fe(t.scale !== void 0 ? t.scale : 1), this.text_ = t.text, this.textAlign_ = t.textAlign, this.justify_ = t.justify, this.textBaseline_ = t.textBaseline, this.fill_ = t.fill !== void 0 ? t.fill : new Vt({ color: Im }), this.maxAngle_ = t.maxAngle !== void 0 ? t.maxAngle : Math.PI / 4, this.placement_ = t.placement !== void 0 ? t.placement : "point", this.overflow_ = !!t.overflow, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.offsetX_ = t.offsetX !== void 0 ? t.offsetX : 0, this.offsetY_ = t.offsetY !== void 0 ? t.offsetY : 0, this.backgroundFill_ = t.backgroundFill ? t.backgroundFill : null, this.backgroundStroke_ = t.backgroundStroke ? t.backgroundStroke : null, this.padding_ = t.padding === void 0 ? null : t.padding;
  }
  clone() {
    const t = this.getScale();
    return new Jl({
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
    this.scale_ = t, this.scaleArray_ = fe(t !== void 0 ? t : 1);
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
const Wa = Jl;
function Pm(n, t, e, i, s) {
  Ud(n, t, e || 0, i || n.length - 1, s || Am);
}
function Ud(n, t, e, i, s) {
  for (; i > e; ) {
    if (i - e > 600) {
      var r = i - e + 1, o = t - e + 1, a = Math.log(r), l = 0.5 * Math.exp(2 * a / 3), h = 0.5 * Math.sqrt(a * l * (r - l) / r) * (o - r / 2 < 0 ? -1 : 1), c = Math.max(e, Math.floor(t - o * l / r + h)), u = Math.min(i, Math.floor(t + (r - o) * l / r + h));
      Ud(n, t, c, u, s);
    }
    var d = n[t], f = e, g = i;
    for (gs(n, e, t), s(n[i], d) > 0 && gs(n, e, i); f < g; ) {
      for (gs(n, f, g), f++, g--; s(n[f], d) < 0; )
        f++;
      for (; s(n[g], d) > 0; )
        g--;
    }
    s(n[e], d) === 0 ? gs(n, e, g) : (g++, gs(n, g, i)), g <= t && (e = g + 1), t <= g && (i = g - 1);
  }
}
function gs(n, t, e) {
  var i = n[t];
  n[t] = n[e], n[e] = i;
}
function Am(n, t) {
  return n < t ? -1 : n > t ? 1 : 0;
}
class Wd {
  constructor(t = 9) {
    this._maxEntries = Math.max(4, t), this._minEntries = Math.max(2, Math.ceil(this._maxEntries * 0.4)), this.clear();
  }
  all() {
    return this._all(this.data, []);
  }
  search(t) {
    let e = this.data;
    const i = [];
    if (!Pr(t, e))
      return i;
    const s = this.toBBox, r = [];
    for (; e; ) {
      for (let o = 0; o < e.children.length; o++) {
        const a = e.children[o], l = e.leaf ? s(a) : a;
        Pr(t, l) && (e.leaf ? i.push(a) : ua(t, l) ? this._all(a, i) : r.push(a));
      }
      e = r.pop();
    }
    return i;
  }
  collides(t) {
    let e = this.data;
    if (!Pr(t, e))
      return !1;
    const i = [];
    for (; e; ) {
      for (let s = 0; s < e.children.length; s++) {
        const r = e.children[s], o = e.leaf ? this.toBBox(r) : r;
        if (Pr(t, o)) {
          if (e.leaf || ua(t, o))
            return !0;
          i.push(r);
        }
      }
      e = i.pop();
    }
    return !1;
  }
  load(t) {
    if (!(t && t.length))
      return this;
    if (t.length < this._minEntries) {
      for (let i = 0; i < t.length; i++)
        this.insert(t[i]);
      return this;
    }
    let e = this._build(t.slice(), 0, t.length - 1, 0);
    if (!this.data.children.length)
      this.data = e;
    else if (this.data.height === e.height)
      this._splitRoot(this.data, e);
    else {
      if (this.data.height < e.height) {
        const i = this.data;
        this.data = e, e = i;
      }
      this._insert(e, this.data.height - e.height - 1, !0);
    }
    return this;
  }
  insert(t) {
    return t && this._insert(t, this.data.height - 1), this;
  }
  clear() {
    return this.data = bn([]), this;
  }
  remove(t, e) {
    if (!t)
      return this;
    let i = this.data;
    const s = this.toBBox(t), r = [], o = [];
    let a, l, h;
    for (; i || r.length; ) {
      if (i || (i = r.pop(), l = r[r.length - 1], a = o.pop(), h = !0), i.leaf) {
        const c = Om(t, i.children, e);
        if (c !== -1)
          return i.children.splice(c, 1), r.push(i), this._condense(r), this;
      }
      !h && !i.leaf && ua(i, s) ? (r.push(i), o.push(a), a = 0, l = i, i = i.children[0]) : l ? (a++, i = l.children[a], h = !1) : i = null;
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
    const i = [];
    for (; t; )
      t.leaf ? e.push(...t.children) : i.push(...t.children), t = i.pop();
    return e;
  }
  _build(t, e, i, s) {
    const r = i - e + 1;
    let o = this._maxEntries, a;
    if (r <= o)
      return a = bn(t.slice(e, i + 1)), Mn(a, this.toBBox), a;
    s || (s = Math.ceil(Math.log(r) / Math.log(o)), o = Math.ceil(r / Math.pow(o, s - 1))), a = bn([]), a.leaf = !1, a.height = s;
    const l = Math.ceil(r / o), h = l * Math.ceil(Math.sqrt(o));
    lc(t, e, i, h, this.compareMinX);
    for (let c = e; c <= i; c += h) {
      const u = Math.min(c + h - 1, i);
      lc(t, c, u, l, this.compareMinY);
      for (let d = c; d <= u; d += l) {
        const f = Math.min(d + l - 1, u);
        a.children.push(this._build(t, d, f, s - 1));
      }
    }
    return Mn(a, this.toBBox), a;
  }
  _chooseSubtree(t, e, i, s) {
    for (; s.push(e), !(e.leaf || s.length - 1 === i); ) {
      let r = 1 / 0, o = 1 / 0, a;
      for (let l = 0; l < e.children.length; l++) {
        const h = e.children[l], c = ca(h), u = Dm(t, h) - c;
        u < o ? (o = u, r = c < r ? c : r, a = h) : u === o && c < r && (r = c, a = h);
      }
      e = a || e.children[0];
    }
    return e;
  }
  _insert(t, e, i) {
    const s = i ? t : this.toBBox(t), r = [], o = this._chooseSubtree(s, this.data, e, r);
    for (o.children.push(t), xs(o, s); e >= 0 && r[e].children.length > this._maxEntries; )
      this._split(r, e), e--;
    this._adjustParentBBoxes(s, r, e);
  }
  _split(t, e) {
    const i = t[e], s = i.children.length, r = this._minEntries;
    this._chooseSplitAxis(i, r, s);
    const o = this._chooseSplitIndex(i, r, s), a = bn(i.children.splice(o, i.children.length - o));
    a.height = i.height, a.leaf = i.leaf, Mn(i, this.toBBox), Mn(a, this.toBBox), e ? t[e - 1].children.push(a) : this._splitRoot(i, a);
  }
  _splitRoot(t, e) {
    this.data = bn([t, e]), this.data.height = t.height + 1, this.data.leaf = !1, Mn(this.data, this.toBBox);
  }
  _chooseSplitIndex(t, e, i) {
    let s, r = 1 / 0, o = 1 / 0;
    for (let a = e; a <= i - e; a++) {
      const l = vs(t, 0, a, this.toBBox), h = vs(t, a, i, this.toBBox), c = km(l, h), u = ca(l) + ca(h);
      c < r ? (r = c, s = a, o = u < o ? u : o) : c === r && u < o && (o = u, s = a);
    }
    return s || i - e;
  }
  _chooseSplitAxis(t, e, i) {
    const s = t.leaf ? this.compareMinX : Fm, r = t.leaf ? this.compareMinY : Nm, o = this._allDistMargin(t, e, i, s), a = this._allDistMargin(t, e, i, r);
    o < a && t.children.sort(s);
  }
  _allDistMargin(t, e, i, s) {
    t.children.sort(s);
    const r = this.toBBox, o = vs(t, 0, e, r), a = vs(t, i - e, i, r);
    let l = Ir(o) + Ir(a);
    for (let h = e; h < i - e; h++) {
      const c = t.children[h];
      xs(o, t.leaf ? r(c) : c), l += Ir(o);
    }
    for (let h = i - e - 1; h >= e; h--) {
      const c = t.children[h];
      xs(a, t.leaf ? r(c) : c), l += Ir(a);
    }
    return l;
  }
  _adjustParentBBoxes(t, e, i) {
    for (let s = i; s >= 0; s--)
      xs(e[s], t);
  }
  _condense(t) {
    for (let e = t.length - 1, i; e >= 0; e--)
      t[e].children.length === 0 ? e > 0 ? (i = t[e - 1].children, i.splice(i.indexOf(t[e]), 1)) : this.clear() : Mn(t[e], this.toBBox);
  }
}
function Om(n, t, e) {
  if (!e)
    return t.indexOf(n);
  for (let i = 0; i < t.length; i++)
    if (e(n, t[i]))
      return i;
  return -1;
}
function Mn(n, t) {
  vs(n, 0, n.children.length, t, n);
}
function vs(n, t, e, i, s) {
  s || (s = bn(null)), s.minX = 1 / 0, s.minY = 1 / 0, s.maxX = -1 / 0, s.maxY = -1 / 0;
  for (let r = t; r < e; r++) {
    const o = n.children[r];
    xs(s, n.leaf ? i(o) : o);
  }
  return s;
}
function xs(n, t) {
  return n.minX = Math.min(n.minX, t.minX), n.minY = Math.min(n.minY, t.minY), n.maxX = Math.max(n.maxX, t.maxX), n.maxY = Math.max(n.maxY, t.maxY), n;
}
function Fm(n, t) {
  return n.minX - t.minX;
}
function Nm(n, t) {
  return n.minY - t.minY;
}
function ca(n) {
  return (n.maxX - n.minX) * (n.maxY - n.minY);
}
function Ir(n) {
  return n.maxX - n.minX + (n.maxY - n.minY);
}
function Dm(n, t) {
  return (Math.max(t.maxX, n.maxX) - Math.min(t.minX, n.minX)) * (Math.max(t.maxY, n.maxY) - Math.min(t.minY, n.minY));
}
function km(n, t) {
  const e = Math.max(n.minX, t.minX), i = Math.max(n.minY, t.minY), s = Math.min(n.maxX, t.maxX), r = Math.min(n.maxY, t.maxY);
  return Math.max(0, s - e) * Math.max(0, r - i);
}
function ua(n, t) {
  return n.minX <= t.minX && n.minY <= t.minY && t.maxX <= n.maxX && t.maxY <= n.maxY;
}
function Pr(n, t) {
  return t.minX <= n.maxX && t.minY <= n.maxY && t.maxX >= n.minX && t.maxY >= n.minY;
}
function bn(n) {
  return {
    children: n,
    height: 1,
    leaf: !0,
    minX: 1 / 0,
    minY: 1 / 0,
    maxX: -1 / 0,
    maxY: -1 / 0
  };
}
function lc(n, t, e, i, s) {
  const r = [t, e];
  for (; r.length; ) {
    if (e = r.pop(), t = r.pop(), e - t <= i)
      continue;
    const o = t + Math.ceil((e - t) / i / 2) * i;
    Pm(n, o, t, e, s), r.push(t, o, o, e);
  }
}
function Hd(n, t, e) {
  const i = n;
  let s = !0, r = !1, o = !1;
  const a = [
    Jr(i, U.LOAD, function() {
      o = !0, r || t();
    })
  ];
  return i.src && Ug ? (r = !0, i.decode().then(function() {
    s && t();
  }).catch(function(l) {
    s && (o ? t() : e());
  })) : a.push(Jr(i, U.ERROR, e)), function() {
    s = !1, a.forEach(mt);
  };
}
let ms = null;
class Gm extends So {
  constructor(t, e, i, s, r, o) {
    super(), this.hitDetectionImage_ = null, this.image_ = t, this.crossOrigin_ = s, this.canvas_ = {}, this.color_ = o, this.unlisten_ = null, this.imageState_ = r, this.size_ = i, this.src_ = e, this.tainted_;
  }
  initializeImage_() {
    this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_);
  }
  isTainted_() {
    if (this.tainted_ === void 0 && this.imageState_ === Pt.LOADED) {
      ms || (ms = pe(1, 1)), ms.drawImage(this.image_, 0, 0);
      try {
        ms.getImageData(0, 0, 1, 1), this.tainted_ = !1;
      } catch {
        ms = null, this.tainted_ = !0;
      }
    }
    return this.tainted_ === !0;
  }
  dispatchChangeEvent_() {
    this.dispatchEvent(U.CHANGE);
  }
  handleImageError_() {
    this.imageState_ = Pt.ERROR, this.unlistenImage_(), this.dispatchChangeEvent_();
  }
  handleImageLoad_() {
    this.imageState_ = Pt.LOADED, this.size_ ? (this.image_.width = this.size_[0], this.image_.height = this.size_[1]) : this.size_ = [this.image_.width, this.image_.height], this.unlistenImage_(), this.dispatchChangeEvent_();
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
        const t = this.size_[0], e = this.size_[1], i = pe(t, e);
        i.fillRect(0, 0, t, e), this.hitDetectionImage_ = i.canvas;
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
    if (this.imageState_ === Pt.IDLE) {
      this.image_ || this.initializeImage_(), this.imageState_ = Pt.LOADING;
      try {
        this.image_.src = this.src_;
      } catch {
        this.handleImageError_();
      }
      this.unlisten_ = Hd(
        this.image_,
        this.handleImageLoad_.bind(this),
        this.handleImageError_.bind(this)
      );
    }
  }
  replaceColor_(t) {
    if (!this.color_ || this.canvas_[t] || this.imageState_ !== Pt.LOADED)
      return;
    const e = this.image_, i = document.createElement("canvas");
    i.width = Math.ceil(e.width * t), i.height = Math.ceil(e.height * t);
    const s = i.getContext("2d");
    s.scale(t, t), s.drawImage(e, 0, 0), s.globalCompositeOperation = "multiply", s.fillStyle = td(this.color_), s.fillRect(0, 0, i.width / t, i.height / t), s.globalCompositeOperation = "destination-in", s.drawImage(e, 0, 0), this.canvas_[t] = i;
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function $m(n, t, e, i, s, r) {
  let o = to.get(t, i, r);
  return o || (o = new Gm(n, t, e, i, s, r), to.set(t, i, r, o)), o;
}
class Ql extends zd {
  constructor(t) {
    t = t || {};
    const e = t.opacity !== void 0 ? t.opacity : 1, i = t.rotation !== void 0 ? t.rotation : 0, s = t.scale !== void 0 ? t.scale : 1, r = t.rotateWithView !== void 0 ? t.rotateWithView : !1;
    super({
      opacity: e,
      rotation: i,
      scale: s,
      displacement: t.displacement !== void 0 ? t.displacement : [0, 0],
      rotateWithView: r,
      declutterMode: t.declutterMode
    }), this.anchor_ = t.anchor !== void 0 ? t.anchor : [0.5, 0.5], this.normalizedAnchor_ = null, this.anchorOrigin_ = t.anchorOrigin !== void 0 ? t.anchorOrigin : "top-left", this.anchorXUnits_ = t.anchorXUnits !== void 0 ? t.anchorXUnits : "fraction", this.anchorYUnits_ = t.anchorYUnits !== void 0 ? t.anchorYUnits : "fraction", this.crossOrigin_ = t.crossOrigin !== void 0 ? t.crossOrigin : null;
    const o = t.img !== void 0 ? t.img : null;
    this.imgSize_ = t.imgSize;
    let a = t.src;
    Y(!(a !== void 0 && o), 4), Y(!o || o && this.imgSize_, 5), (a === void 0 || a.length === 0) && o && (a = o.src || q(o)), Y(a !== void 0 && a.length > 0, 6);
    const l = t.src !== void 0 ? Pt.IDLE : Pt.LOADED;
    this.color_ = t.color !== void 0 ? Qr(t.color) : null, this.iconImage_ = $m(
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
    return new Ql({
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
    const e = this.getDisplacement(), i = this.getScaleArray();
    return [
      t[0] - e[0] / i[0],
      t[1] + e[1] / i[1]
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
      const e = this.getSize(), i = this.iconImage_.getSize();
      if (!e || !i)
        return null;
      t = t.slice(), (this.offsetOrigin_ == "top-right" || this.offsetOrigin_ == "bottom-right") && (t[0] = i[0] - e[0] - t[0]), (this.offsetOrigin_ == "bottom-left" || this.offsetOrigin_ == "bottom-right") && (t[1] = i[1] - e[1] - t[1]);
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
    this.iconImage_.addEventListener(U.CHANGE, t);
  }
  load() {
    this.iconImage_.load();
  }
  unlistenImageChange(t) {
    this.iconImage_.removeEventListener(U.CHANGE, t);
  }
}
const Ts = Ql;
function hc(n) {
  return new Zt({
    fill: Vs(n, ""),
    stroke: Us(n, ""),
    text: Bm(n),
    image: zm(n)
  });
}
function Vs(n, t) {
  const e = n[t + "fill-color"];
  if (!!e)
    return new Vt({ color: e });
}
function Us(n, t) {
  const e = n[t + "stroke-width"], i = n[t + "stroke-color"];
  if (!(!e && !i))
    return new Xt({
      width: e,
      color: i,
      lineCap: n[t + "stroke-line-cap"],
      lineJoin: n[t + "stroke-line-join"],
      lineDash: n[t + "stroke-line-dash"],
      lineDashOffset: n[t + "stroke-line-dash-offset"],
      miterLimit: n[t + "stroke-miter-limit"]
    });
}
function Bm(n) {
  const t = n["text-value"];
  return t ? new Wa({
    text: t,
    font: n["text-font"],
    maxAngle: n["text-max-angle"],
    offsetX: n["text-offset-x"],
    offsetY: n["text-offset-y"],
    overflow: n["text-overflow"],
    placement: n["text-placement"],
    scale: n["text-scale"],
    rotateWithView: n["text-rotate-with-view"],
    rotation: n["text-rotation"],
    textAlign: n["text-align"],
    justify: n["text-justify"],
    textBaseline: n["text-baseline"],
    padding: n["text-padding"],
    fill: Vs(n, "text-"),
    backgroundFill: Vs(n, "text-background-"),
    stroke: Us(n, "text-"),
    backgroundStroke: Us(n, "text-background-")
  }) : void 0;
}
function zm(n) {
  const t = n["icon-src"], e = n["icon-img"];
  if (t || e)
    return new Ts({
      src: t,
      img: e,
      imgSize: n["icon-img-size"],
      anchor: n["icon-anchor"],
      anchorOrigin: n["icon-anchor-origin"],
      anchorXUnits: n["icon-anchor-x-units"],
      anchorYUnits: n["icon-anchor-y-units"],
      color: n["icon-color"],
      crossOrigin: n["icon-cross-origin"],
      offset: n["icon-offset"],
      displacement: n["icon-displacement"],
      opacity: n["icon-opacity"],
      scale: n["icon-scale"],
      rotation: n["icon-rotation"],
      rotateWithView: n["icon-rotate-with-view"],
      size: n["icon-size"],
      declutterMode: n["icon-declutter-mode"]
    });
  const i = n["shape-points"];
  if (i) {
    const r = "shape-";
    return new Zd({
      points: i,
      fill: Vs(n, r),
      stroke: Us(n, r),
      radius: n["shape-radius"],
      radius1: n["shape-radius1"],
      radius2: n["shape-radius2"],
      angle: n["shape-angle"],
      displacement: n["shape-displacement"],
      rotation: n["shape-rotation"],
      rotateWithView: n["shape-rotate-with-view"],
      scale: n["shape-scale"],
      declutterMode: n["shape-declutter-mode"]
    });
  }
  const s = n["circle-radius"];
  if (s) {
    const r = "circle-";
    return new we({
      radius: s,
      fill: Vs(n, r),
      stroke: Us(n, r),
      displacement: n["circle-displacement"],
      scale: n["circle-scale"],
      rotation: n["circle-rotation"],
      rotateWithView: n["circle-rotate-with-view"],
      declutterMode: n["circle-declutter-mode"]
    });
  }
}
const cc = {
  RENDER_ORDER: "renderOrder"
};
class Zm extends Po {
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
    return this.get(cc.RENDER_ORDER);
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
    t.declutterTree || (t.declutterTree = new Wd(9)), this.getRenderer().renderDeclutter(t);
  }
  setRenderOrder(t) {
    this.set(cc.RENDER_ORDER, t);
  }
  setStyle(t) {
    let e;
    if (t === void 0)
      e = Lm;
    else if (t === null)
      e = null;
    else if (typeof t == "function")
      e = t;
    else if (t instanceof Zt)
      e = t;
    else if (Array.isArray(t)) {
      const i = t.length, s = new Array(i);
      for (let r = 0; r < i; ++r) {
        const o = t[r];
        o instanceof Zt ? s[r] = o : s[r] = hc(o);
      }
      e = s;
    } else
      e = hc(t);
    this.style_ = e, this.styleFunction_ = t === null ? void 0 : bm(this.style_), this.changed();
  }
}
const Vm = Zm, ir = {
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
}, Ar = [ir.FILL], Si = [ir.STROKE], Hi = [ir.BEGIN_PATH], uc = [ir.CLOSE_PATH], W = ir;
class Um {
  drawCustom(t, e, i, s) {
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
const Xd = Um;
class Wm extends Xd {
  constructor(t, e, i, s) {
    super(), this.tolerance = t, this.maxExtent = e, this.pixelRatio = s, this.maxLineWidth = 0, this.resolution = i, this.beginGeometryInstruction1_ = null, this.beginGeometryInstruction2_ = null, this.bufferedMaxExtent_ = null, this.instructions = [], this.coordinates = [], this.tmpCoordinate_ = [], this.hitDetectionInstructions = [], this.state = {};
  }
  applyPixelRatio(t) {
    const e = this.pixelRatio;
    return e == 1 ? t : t.map(function(i) {
      return i * e;
    });
  }
  appendFlatPointCoordinates(t, e) {
    const i = this.getBufferedMaxExtent(), s = this.tmpCoordinate_, r = this.coordinates;
    let o = r.length;
    for (let a = 0, l = t.length; a < l; a += e)
      s[0] = t[a], s[1] = t[a + 1], To(i, s) && (r[o++] = s[0], r[o++] = s[1]);
    return o;
  }
  appendFlatLineCoordinates(t, e, i, s, r, o) {
    const a = this.coordinates;
    let l = a.length;
    const h = this.getBufferedMaxExtent();
    o && (e += s);
    let c = t[e], u = t[e + 1];
    const d = this.tmpCoordinate_;
    let f = !0, g, m, _;
    for (g = e + s; g < i; g += s)
      d[0] = t[g], d[1] = t[g + 1], _ = ba(h, d), _ !== m ? (f && (a[l++] = c, a[l++] = u, f = !1), a[l++] = d[0], a[l++] = d[1]) : _ === Ft.INTERSECTING ? (a[l++] = d[0], a[l++] = d[1], f = !1) : f = !0, c = d[0], u = d[1], m = _;
    return (r && f || g === e + s) && (a[l++] = c, a[l++] = u), l;
  }
  drawCustomCoordinates_(t, e, i, s, r) {
    for (let o = 0, a = i.length; o < a; ++o) {
      const l = i[o], h = this.appendFlatLineCoordinates(
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
  drawCustom(t, e, i, s) {
    this.beginGeometry(t, e);
    const r = t.getType(), o = t.getStride(), a = this.coordinates.length;
    let l, h, c, u, d;
    switch (r) {
      case "MultiPolygon":
        l = t.getOrientedFlatCoordinates(), u = [];
        const f = t.getEndss();
        d = 0;
        for (let g = 0, m = f.length; g < m; ++g) {
          const _ = [];
          d = this.drawCustomCoordinates_(
            l,
            d,
            f[g],
            o,
            _
          ), u.push(_);
        }
        this.instructions.push([
          W.CUSTOM,
          a,
          u,
          t,
          i,
          $a
        ]), this.hitDetectionInstructions.push([
          W.CUSTOM,
          a,
          u,
          t,
          s || i,
          $a
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
          W.CUSTOM,
          a,
          c,
          t,
          i,
          Zs
        ]), this.hitDetectionInstructions.push([
          W.CUSTOM,
          a,
          c,
          t,
          s || i,
          Zs
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
          W.CUSTOM,
          a,
          h,
          t,
          i,
          Ei
        ]), this.hitDetectionInstructions.push([
          W.CUSTOM,
          a,
          h,
          t,
          s || i,
          Ei
        ]);
        break;
      case "MultiPoint":
        l = t.getFlatCoordinates(), h = this.appendFlatPointCoordinates(l, o), h > a && (this.instructions.push([
          W.CUSTOM,
          a,
          h,
          t,
          i,
          Ei
        ]), this.hitDetectionInstructions.push([
          W.CUSTOM,
          a,
          h,
          t,
          s || i,
          Ei
        ]));
        break;
      case "Point":
        l = t.getFlatCoordinates(), this.coordinates.push(l[0], l[1]), h = this.coordinates.length, this.instructions.push([
          W.CUSTOM,
          a,
          h,
          t,
          i
        ]), this.hitDetectionInstructions.push([
          W.CUSTOM,
          a,
          h,
          t,
          s || i
        ]);
        break;
    }
    this.endGeometry(e);
  }
  beginGeometry(t, e) {
    this.beginGeometryInstruction1_ = [
      W.BEGIN_GEOMETRY,
      e,
      0,
      t
    ], this.instructions.push(this.beginGeometryInstruction1_), this.beginGeometryInstruction2_ = [
      W.BEGIN_GEOMETRY,
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
    const i = t.length;
    let s, r, o = -1;
    for (e = 0; e < i; ++e)
      s = t[e], r = s[0], r == W.END_GEOMETRY ? o = e : r == W.BEGIN_GEOMETRY && (s[2] = e, Ig(this.hitDetectionInstructions, o, e), o = -1);
  }
  setFillStrokeStyle(t, e) {
    const i = this.state;
    if (t) {
      const s = t.getColor();
      i.fillStyle = ke(
        s || ai
      );
    } else
      i.fillStyle = void 0;
    if (e) {
      const s = e.getColor();
      i.strokeStyle = ke(
        s || Gs
      );
      const r = e.getLineCap();
      i.lineCap = r !== void 0 ? r : no;
      const o = e.getLineDash();
      i.lineDash = o ? o.slice() : Ns;
      const a = e.getLineDashOffset();
      i.lineDashOffset = a || Ds;
      const l = e.getLineJoin();
      i.lineJoin = l !== void 0 ? l : Xn;
      const h = e.getWidth();
      i.lineWidth = h !== void 0 ? h : Bs;
      const c = e.getMiterLimit();
      i.miterLimit = c !== void 0 ? c : ks, i.lineWidth > this.maxLineWidth && (this.maxLineWidth = i.lineWidth, this.bufferedMaxExtent_ = null);
    } else
      i.strokeStyle = void 0, i.lineCap = void 0, i.lineDash = null, i.lineDashOffset = void 0, i.lineJoin = void 0, i.lineWidth = void 0, i.miterLimit = void 0;
  }
  createFill(t) {
    const e = t.fillStyle, i = [W.SET_FILL_STYLE, e];
    return typeof e != "string" && i.push(!0), i;
  }
  applyStroke(t) {
    this.instructions.push(this.createStroke(t));
  }
  createStroke(t) {
    return [
      W.SET_STROKE_STYLE,
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
    const i = t.fillStyle;
    (typeof i != "string" || t.currentFillStyle != i) && (i !== void 0 && this.instructions.push(e.call(this, t)), t.currentFillStyle = i);
  }
  updateStrokeStyle(t, e) {
    const i = t.strokeStyle, s = t.lineCap, r = t.lineDash, o = t.lineDashOffset, a = t.lineJoin, l = t.lineWidth, h = t.miterLimit;
    (t.currentStrokeStyle != i || t.currentLineCap != s || r != t.currentLineDash && !Ni(t.currentLineDash, r) || t.currentLineDashOffset != o || t.currentLineJoin != a || t.currentLineWidth != l || t.currentMiterLimit != h) && (i !== void 0 && e.call(this, t), t.currentStrokeStyle = i, t.currentLineCap = s, t.currentLineDash = r, t.currentLineDashOffset = o, t.currentLineJoin = a, t.currentLineWidth = l, t.currentMiterLimit = h);
  }
  endGeometry(t) {
    this.beginGeometryInstruction1_[2] = this.instructions.length, this.beginGeometryInstruction1_ = null, this.beginGeometryInstruction2_[2] = this.hitDetectionInstructions.length, this.beginGeometryInstruction2_ = null;
    const e = [W.END_GEOMETRY, t];
    this.instructions.push(e), this.hitDetectionInstructions.push(e);
  }
  getBufferedMaxExtent() {
    if (!this.bufferedMaxExtent_ && (this.bufferedMaxExtent_ = ju(this.maxExtent), this.maxLineWidth > 0)) {
      const t = this.resolution * (this.maxLineWidth + 1) / 2;
      Js(this.bufferedMaxExtent_, t, this.bufferedMaxExtent_);
    }
    return this.bufferedMaxExtent_;
  }
}
const nr = Wm;
class Hm extends nr {
  constructor(t, e, i, s) {
    super(t, e, i, s), this.hitDetectionImage_ = null, this.image_ = null, this.imagePixelRatio_ = void 0, this.anchorX_ = void 0, this.anchorY_ = void 0, this.height_ = void 0, this.opacity_ = void 0, this.originX_ = void 0, this.originY_ = void 0, this.rotateWithView_ = void 0, this.rotation_ = void 0, this.scale_ = void 0, this.width_ = void 0, this.declutterMode_ = void 0, this.declutterImageWithText_ = void 0;
  }
  drawPoint(t, e) {
    if (!this.image_)
      return;
    this.beginGeometry(t, e);
    const i = t.getFlatCoordinates(), s = t.getStride(), r = this.coordinates.length, o = this.appendFlatPointCoordinates(i, s);
    this.instructions.push([
      W.DRAW_IMAGE,
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
      W.DRAW_IMAGE,
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
    const i = t.getFlatCoordinates(), s = t.getStride(), r = this.coordinates.length, o = this.appendFlatPointCoordinates(i, s);
    this.instructions.push([
      W.DRAW_IMAGE,
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
      W.DRAW_IMAGE,
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
    const i = t.getAnchor(), s = t.getSize(), r = t.getOrigin();
    this.imagePixelRatio_ = t.getPixelRatio(this.pixelRatio), this.anchorX_ = i[0], this.anchorY_ = i[1], this.hitDetectionImage_ = t.getHitDetectionImage(), this.image_ = t.getImage(this.pixelRatio), this.height_ = s[1], this.opacity_ = t.getOpacity(), this.originX_ = r[0], this.originY_ = r[1], this.rotateWithView_ = t.getRotateWithView(), this.rotation_ = t.getRotation(), this.scale_ = t.getScaleArray(), this.width_ = s[0], this.declutterMode_ = t.getDeclutterMode(), this.declutterImageWithText_ = e;
  }
}
const Xm = Hm;
class Ym extends nr {
  constructor(t, e, i, s) {
    super(t, e, i, s);
  }
  drawFlatCoordinates_(t, e, i, s) {
    const r = this.coordinates.length, o = this.appendFlatLineCoordinates(
      t,
      e,
      i,
      s,
      !1,
      !1
    ), a = [
      W.MOVE_TO_LINE_TO,
      r,
      o
    ];
    return this.instructions.push(a), this.hitDetectionInstructions.push(a), i;
  }
  drawLineString(t, e) {
    const i = this.state, s = i.strokeStyle, r = i.lineWidth;
    if (s === void 0 || r === void 0)
      return;
    this.updateStrokeStyle(i, this.applyStroke), this.beginGeometry(t, e), this.hitDetectionInstructions.push(
      [
        W.SET_STROKE_STYLE,
        i.strokeStyle,
        i.lineWidth,
        i.lineCap,
        i.lineJoin,
        i.miterLimit,
        Ns,
        Ds
      ],
      Hi
    );
    const o = t.getFlatCoordinates(), a = t.getStride();
    this.drawFlatCoordinates_(
      o,
      0,
      o.length,
      a
    ), this.hitDetectionInstructions.push(Si), this.endGeometry(e);
  }
  drawMultiLineString(t, e) {
    const i = this.state, s = i.strokeStyle, r = i.lineWidth;
    if (s === void 0 || r === void 0)
      return;
    this.updateStrokeStyle(i, this.applyStroke), this.beginGeometry(t, e), this.hitDetectionInstructions.push(
      [
        W.SET_STROKE_STYLE,
        i.strokeStyle,
        i.lineWidth,
        i.lineCap,
        i.lineJoin,
        i.miterLimit,
        i.lineDash,
        i.lineDashOffset
      ],
      Hi
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
    this.hitDetectionInstructions.push(Si), this.endGeometry(e);
  }
  finish() {
    const t = this.state;
    return t.lastStroke != null && t.lastStroke != this.coordinates.length && this.instructions.push(Si), this.reverseHitDetectionInstructions(), this.state = null, super.finish();
  }
  applyStroke(t) {
    t.lastStroke != null && t.lastStroke != this.coordinates.length && (this.instructions.push(Si), t.lastStroke = this.coordinates.length), t.lastStroke = 0, super.applyStroke(t), this.instructions.push(Hi);
  }
}
const jm = Ym;
class qm extends nr {
  constructor(t, e, i, s) {
    super(t, e, i, s);
  }
  drawFlatCoordinatess_(t, e, i, s) {
    const r = this.state, o = r.fillStyle !== void 0, a = r.strokeStyle !== void 0, l = i.length;
    this.instructions.push(Hi), this.hitDetectionInstructions.push(Hi);
    for (let h = 0; h < l; ++h) {
      const c = i[h], u = this.coordinates.length, d = this.appendFlatLineCoordinates(
        t,
        e,
        c,
        s,
        !0,
        !a
      ), f = [
        W.MOVE_TO_LINE_TO,
        u,
        d
      ];
      this.instructions.push(f), this.hitDetectionInstructions.push(f), a && (this.instructions.push(uc), this.hitDetectionInstructions.push(uc)), e = c;
    }
    return o && (this.instructions.push(Ar), this.hitDetectionInstructions.push(Ar)), a && (this.instructions.push(Si), this.hitDetectionInstructions.push(Si)), e;
  }
  drawCircle(t, e) {
    const i = this.state, s = i.fillStyle, r = i.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), i.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_FILL_STYLE,
      ai
    ]), i.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_STROKE_STYLE,
      i.strokeStyle,
      i.lineWidth,
      i.lineCap,
      i.lineJoin,
      i.miterLimit,
      i.lineDash,
      i.lineDashOffset
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
    const h = [W.CIRCLE, l];
    this.instructions.push(Hi, h), this.hitDetectionInstructions.push(Hi, h), i.fillStyle !== void 0 && (this.instructions.push(Ar), this.hitDetectionInstructions.push(Ar)), i.strokeStyle !== void 0 && (this.instructions.push(Si), this.hitDetectionInstructions.push(Si)), this.endGeometry(e);
  }
  drawPolygon(t, e) {
    const i = this.state, s = i.fillStyle, r = i.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), i.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_FILL_STYLE,
      ai
    ]), i.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_STROKE_STYLE,
      i.strokeStyle,
      i.lineWidth,
      i.lineCap,
      i.lineJoin,
      i.miterLimit,
      i.lineDash,
      i.lineDashOffset
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
    const i = this.state, s = i.fillStyle, r = i.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), i.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_FILL_STYLE,
      ai
    ]), i.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      W.SET_STROKE_STYLE,
      i.strokeStyle,
      i.lineWidth,
      i.lineCap,
      i.lineJoin,
      i.miterLimit,
      i.lineDash,
      i.lineDashOffset
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
      for (let i = 0, s = e.length; i < s; ++i)
        e[i] = Zi(e[i], t);
    }
    return super.finish();
  }
  setFillStrokeStyles_() {
    const t = this.state;
    t.fillStyle !== void 0 && this.updateFillStyle(t, this.createFill), t.strokeStyle !== void 0 && this.updateStrokeStyle(t, this.applyStroke);
  }
}
const dc = qm;
function Km(n, t, e, i, s) {
  let r = e, o = e, a = 0, l = 0, h = e, c, u, d, f, g, m, _, y, p, v;
  for (u = e; u < i; u += s) {
    const x = t[u], C = t[u + 1];
    g !== void 0 && (p = x - g, v = C - m, f = Math.sqrt(p * p + v * v), _ !== void 0 && (l += d, c = Math.acos((_ * p + y * v) / (d * f)), c > n && (l > a && (a = l, r = h, o = u), l = 0, h = u - s)), d = f, _ = p, y = v), g = x, m = C;
  }
  return l += f, l > a ? [h, u] : [r, o];
}
const bs = {
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
class Jm extends nr {
  constructor(t, e, i, s) {
    super(t, e, i, s), this.labels_ = null, this.text_ = "", this.textOffsetX_ = 0, this.textOffsetY_ = 0, this.textRotateWithView_ = void 0, this.textRotation_ = 0, this.textFillState_ = null, this.fillStates = {}, this.textStrokeState_ = null, this.strokeStates = {}, this.textState_ = {}, this.textStates = {}, this.textKey_ = "", this.fillKey_ = "", this.strokeKey_ = "", this.declutterImageWithText_ = void 0;
  }
  finish() {
    const t = super.finish();
    return t.textStates = this.textStates, t.fillStates = this.fillStates, t.strokeStates = this.strokeStates, t;
  }
  drawText(t, e) {
    const i = this.textFillState_, s = this.textStrokeState_, r = this.textState_;
    if (this.text_ === "" || !r || !i && !s)
      return;
    const o = this.coordinates;
    let a = o.length;
    const l = t.getType();
    let h = null, c = t.getStride();
    if (r.placement === "line" && (l == "LineString" || l == "MultiLineString" || l == "Polygon" || l == "MultiPolygon")) {
      if (!Kt(this.getBufferedMaxExtent(), t.getExtent()))
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
        for (let _ = 0, y = m.length; _ < y; ++_)
          u.push(m[_][0]);
      }
      this.beginGeometry(t, e);
      const d = r.textAlign;
      let f = 0, g;
      for (let m = 0, _ = u.length; m < _; ++m) {
        if (d == null) {
          const p = Km(
            r.maxAngle,
            h,
            f,
            u[m],
            c
          );
          f = p[0], g = p[1];
        } else
          g = u[m];
        for (let p = f; p < g; p += c)
          o.push(h[p], h[p + 1]);
        const y = o.length;
        f = u[m], this.drawChars_(a, y), a = y;
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
          const _ = t.getFlatInteriorPoints();
          h = [];
          for (let y = 0, p = _.length; y < p; y += 3)
            r.overflow || u.push(_[y + 2] / this.resolution), h.push(_[y], _[y + 1]);
          if (h.length === 0)
            return;
          c = 2;
          break;
      }
      const d = this.appendFlatPointCoordinates(h, c);
      if (d === a)
        return;
      if (u && (d - a) / 2 !== h.length / c) {
        let _ = a / 2;
        u = u.filter((y, p) => {
          const v = o[(_ + p) * 2] === h[p * c] && o[(_ + p) * 2 + 1] === h[p * c + 1];
          return v || --_, v;
        });
      }
      this.saveTextStates_(), (r.backgroundFill || r.backgroundStroke) && (this.setFillStrokeStyle(
        r.backgroundFill,
        r.backgroundStroke
      ), r.backgroundFill && (this.updateFillStyle(this.state, this.createFill), this.hitDetectionInstructions.push(this.createFill(this.state))), r.backgroundStroke && (this.updateStrokeStyle(this.state, this.applyStroke), this.hitDetectionInstructions.push(this.createStroke(this.state)))), this.beginGeometry(t, e);
      let f = r.padding;
      if (f != Ui && (r.scale[0] < 0 || r.scale[1] < 0)) {
        let _ = r.padding[0], y = r.padding[1], p = r.padding[2], v = r.padding[3];
        r.scale[0] < 0 && (y = -y, v = -v), r.scale[1] < 0 && (_ = -_, p = -p), f = [_, y, p, v];
      }
      const g = this.pixelRatio;
      this.instructions.push([
        W.DRAW_IMAGE,
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
        f == Ui ? Ui : f.map(function(_) {
          return _ * g;
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
        W.DRAW_IMAGE,
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
    const t = this.textStrokeState_, e = this.textState_, i = this.textFillState_, s = this.strokeKey_;
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
      textAlign: e.textAlign || $s,
      justify: e.justify,
      textBaseline: e.textBaseline || so,
      scale: e.scale
    });
    const o = this.fillKey_;
    i && (o in this.fillStates || (this.fillStates[o] = {
      fillStyle: i.fillStyle
    }));
  }
  drawChars_(t, e) {
    const i = this.textStrokeState_, s = this.textState_, r = this.strokeKey_, o = this.textKey_, a = this.fillKey_;
    this.saveTextStates_();
    const l = this.pixelRatio, h = bs[s.textBaseline], c = this.textOffsetY_ * l, u = this.text_, d = i ? i.lineWidth * Math.abs(s.scale[0]) / 2 : 0;
    this.instructions.push([
      W.DRAW_CHARS,
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
      W.DRAW_CHARS,
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
    let i, s, r;
    if (!t)
      this.text_ = "";
    else {
      const o = t.getFill();
      o ? (s = this.textFillState_, s || (s = {}, this.textFillState_ = s), s.fillStyle = ke(
        o.getColor() || ai
      )) : (s = null, this.textFillState_ = s);
      const a = t.getStroke();
      if (!a)
        r = null, this.textStrokeState_ = r;
      else {
        r = this.textStrokeState_, r || (r = {}, this.textStrokeState_ = r);
        const g = a.getLineDash(), m = a.getLineDashOffset(), _ = a.getWidth(), y = a.getMiterLimit();
        r.lineCap = a.getLineCap() || no, r.lineDash = g ? g.slice() : Ns, r.lineDashOffset = m === void 0 ? Ds : m, r.lineJoin = a.getLineJoin() || Xn, r.lineWidth = _ === void 0 ? Bs : _, r.miterLimit = y === void 0 ? ks : y, r.strokeStyle = ke(
          a.getColor() || Gs
        );
      }
      i = this.textState_;
      const l = t.getFont() || cd;
      C0(l);
      const h = t.getScaleArray();
      i.overflow = t.getOverflow(), i.font = l, i.maxAngle = t.getMaxAngle(), i.placement = t.getPlacement(), i.textAlign = t.getTextAlign(), i.justify = t.getJustify(), i.textBaseline = t.getTextBaseline() || so, i.backgroundFill = t.getBackgroundFill(), i.backgroundStroke = t.getBackgroundStroke(), i.padding = t.getPadding() || Ui, i.scale = h === void 0 ? [1, 1] : h;
      const c = t.getOffsetX(), u = t.getOffsetY(), d = t.getRotateWithView(), f = t.getRotation();
      this.text_ = t.getText() || "", this.textOffsetX_ = c === void 0 ? 0 : c, this.textOffsetY_ = u === void 0 ? 0 : u, this.textRotateWithView_ = d === void 0 ? !1 : d, this.textRotation_ = f === void 0 ? 0 : f, this.strokeKey_ = r ? (typeof r.strokeStyle == "string" ? r.strokeStyle : q(r.strokeStyle)) + r.lineCap + r.lineDashOffset + "|" + r.lineWidth + r.lineJoin + r.miterLimit + "[" + r.lineDash.join() + "]" : "", this.textKey_ = i.font + i.scale + (i.textAlign || "?") + (i.justify || "?") + (i.textBaseline || "?"), this.fillKey_ = s ? typeof s.fillStyle == "string" ? s.fillStyle : "|" + q(s.fillStyle) : "";
    }
    this.declutterImageWithText_ = e;
  }
}
const Qm = {
  Circle: dc,
  Default: nr,
  Image: Xm,
  LineString: jm,
  Polygon: dc,
  Text: Jm
};
class t_ {
  constructor(t, e, i, s) {
    this.tolerance_ = t, this.maxExtent_ = e, this.pixelRatio_ = s, this.resolution_ = i, this.buildersByZIndex_ = {};
  }
  finish() {
    const t = {};
    for (const e in this.buildersByZIndex_) {
      t[e] = t[e] || {};
      const i = this.buildersByZIndex_[e];
      for (const s in i) {
        const r = i[s].finish();
        t[e][s] = r;
      }
    }
    return t;
  }
  getBuilder(t, e) {
    const i = t !== void 0 ? t.toString() : "0";
    let s = this.buildersByZIndex_[i];
    s === void 0 && (s = {}, this.buildersByZIndex_[i] = s);
    let r = s[e];
    if (r === void 0) {
      const o = Qm[e];
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
const fc = t_;
class e_ extends Uu {
  constructor(t) {
    super(), this.ready = !0, this.boundHandleImageChange_ = this.handleImageChange_.bind(this), this.layer_ = t, this.declutterExecutorGroup = null;
  }
  getFeatures(t) {
    return H();
  }
  getData(t) {
    return null;
  }
  prepareFrame(t) {
    return H();
  }
  renderFrame(t, e) {
    return H();
  }
  loadedTileCallback(t, e, i) {
    t[e] || (t[e] = {}), t[e][i.tileCoord.toString()] = i;
  }
  createLoadedTileFinder(t, e, i) {
    return function(s, r) {
      const o = this.loadedTileCallback.bind(this, i, s);
      return t.forEachLoadedTile(e, s, r, o);
    }.bind(this);
  }
  forEachFeatureAtCoordinate(t, e, i, s, r) {
  }
  getLayer() {
    return this.layer_;
  }
  handleFontsChanged() {
  }
  handleImageChange_(t) {
    t.target.getState() === Pt.LOADED && this.renderIfReadyAndVisible();
  }
  loadImage(t) {
    let e = t.getState();
    return e != Pt.LOADED && e != Pt.ERROR && t.addEventListener(U.CHANGE, this.boundHandleImageChange_), e == Pt.IDLE && (t.load(), e = t.getState()), e == Pt.LOADED;
  }
  renderIfReadyAndVisible() {
    const t = this.getLayer();
    t && t.getVisible() && t.getSourceState() === "ready" && t.changed();
  }
  disposeInternal() {
    delete this.layer_, super.disposeInternal();
  }
}
const i_ = e_, gc = [];
let Ln = null;
function n_() {
  const n = document.createElement("canvas");
  n.width = 1, n.height = 1, Ln = n.getContext("2d");
}
class s_ extends i_ {
  constructor(t) {
    super(t), this.container = null, this.renderedResolution, this.tempTransform = $e(), this.pixelTransform = $e(), this.inversePixelTransform = $e(), this.context = null, this.containerReused = !1, this.pixelContext_ = null, this.frameState = null;
  }
  getImageData(t, e, i) {
    Ln || n_(), Ln.clearRect(0, 0, 1, 1);
    let s;
    try {
      Ln.drawImage(t, e, i, 1, 1, 0, 0, 1, 1), s = Ln.getImageData(0, 0, 1, 1).data;
    } catch {
      return Ln = null, null;
    }
    return s;
  }
  getBackground(t) {
    let i = this.getLayer().getBackground();
    return typeof i == "function" && (i = i(t.viewState.resolution)), i || void 0;
  }
  useContainer(t, e, i) {
    const s = this.getLayer().getClassName();
    let r, o;
    if (t && t.className === s && (!i || t && t.style.backgroundColor && Ni(
      Qr(t.style.backgroundColor),
      Qr(i)
    ))) {
      const a = t.firstElementChild;
      a instanceof HTMLCanvasElement && (o = a.getContext("2d"));
    }
    if (o && o.canvas.style.transform === e ? (this.container = t, this.context = o, this.containerReused = !0) : this.containerReused && (this.container = null, this.context = null, this.containerReused = !1), !this.container) {
      r = document.createElement("div"), r.className = s;
      let a = r.style;
      a.position = "absolute", a.width = "100%", a.height = "100%", o = pe();
      const l = o.canvas;
      r.appendChild(l), a = l.style, a.position = "absolute", a.left = "0", a.transformOrigin = "top left", this.container = r, this.context = o;
    }
    !this.containerReused && i && !this.container.style.backgroundColor && (this.container.style.backgroundColor = i);
  }
  clipUnrotated(t, e, i) {
    const s = fn(i), r = Io(i), o = Lo(i), a = bo(i);
    Nt(e.coordinateToPixelTransform, s), Nt(e.coordinateToPixelTransform, r), Nt(e.coordinateToPixelTransform, o), Nt(e.coordinateToPixelTransform, a);
    const l = this.inversePixelTransform;
    Nt(l, s), Nt(l, r), Nt(l, o), Nt(l, a), t.save(), t.beginPath(), t.moveTo(Math.round(s[0]), Math.round(s[1])), t.lineTo(Math.round(r[0]), Math.round(r[1])), t.lineTo(Math.round(o[0]), Math.round(o[1])), t.lineTo(Math.round(a[0]), Math.round(a[1])), t.clip();
  }
  dispatchRenderEvent_(t, e, i) {
    const s = this.getLayer();
    if (s.hasListener(t)) {
      const r = new ad(
        t,
        this.inversePixelTransform,
        i,
        e
      );
      s.dispatchEvent(r);
    }
  }
  preRender(t, e) {
    this.frameState = e, this.dispatchRenderEvent_(Ri.PRERENDER, t, e);
  }
  postRender(t, e) {
    this.dispatchRenderEvent_(Ri.POSTRENDER, t, e);
  }
  getRenderTransform(t, e, i, s, r, o, a) {
    const l = r / 2, h = o / 2, c = s / e, u = -c, d = -t[0] + a, f = -t[1];
    return Ii(
      this.tempTransform,
      l,
      h,
      c,
      u,
      -i,
      d,
      f
    );
  }
  disposeInternal() {
    delete this.frameState, super.disposeInternal();
  }
}
const Yd = s_;
function r_(n, t, e, i, s, r, o, a, l, h, c, u) {
  let d = n[t], f = n[t + 1], g = 0, m = 0, _ = 0, y = 0;
  function p() {
    g = d, m = f, t += i, d = n[t], f = n[t + 1], y += _, _ = Math.sqrt((d - g) * (d - g) + (f - m) * (f - m));
  }
  do
    p();
  while (t < e - i && y + _ < r);
  let v = _ === 0 ? 0 : (r - y) / _;
  const x = ii(g, d, v), C = ii(m, f, v), E = t - i, R = y, b = r + a * l(h, s, c);
  for (; t < e - i && y + _ < b; )
    p();
  v = _ === 0 ? 0 : (b - y) / _;
  const F = ii(g, d, v), G = ii(m, f, v);
  let V;
  if (u) {
    const k = [x, C, F, G];
    Fl(k, 0, 4, 2, u, k, k), V = k[0] > k[2];
  } else
    V = x > F;
  const L = Math.PI, $ = [], gt = E + i === t;
  t = E, _ = 0, y = R, d = n[t], f = n[t + 1];
  let N;
  if (gt) {
    p(), N = Math.atan2(f - m, d - g), V && (N += N > 0 ? -L : L);
    const k = (F + x) / 2, P = (G + C) / 2;
    return $[0] = [k, P, (b - r) / 2, N, s], $;
  }
  s = s.replace(/\n/g, " ");
  for (let k = 0, P = s.length; k < P; ) {
    p();
    let it = Math.atan2(f - m, d - g);
    if (V && (it += it > 0 ? -L : L), N !== void 0) {
      let ht = it - N;
      if (ht += ht > L ? -2 * L : ht < -L ? 2 * L : 0, Math.abs(ht) > o)
        return null;
    }
    N = it;
    const wt = k;
    let yt = 0;
    for (; k < P; ++k) {
      const ht = V ? P - k - 1 : k, _t = a * l(h, s[ht], c);
      if (t + i < e && y + _ < r + yt + _t / 2)
        break;
      yt += _t;
    }
    if (k === wt)
      continue;
    const At = V ? s.substring(P - wt, P - k) : s.substring(wt, k);
    v = _ === 0 ? 0 : (r + yt / 2 - y) / _;
    const T = ii(g, d, v), ce = ii(m, f, v);
    $.push([T, ce, yt / 2, it, At]), r += yt;
  }
  return $;
}
const En = se(), mi = [], Ke = [], Je = [], _i = [];
function mc(n) {
  return n[3].declutterBox;
}
const o_ = new RegExp(
  "[" + String.fromCharCode(1425) + "-" + String.fromCharCode(2303) + String.fromCharCode(64285) + "-" + String.fromCharCode(65023) + String.fromCharCode(65136) + "-" + String.fromCharCode(65276) + String.fromCharCode(67584) + "-" + String.fromCharCode(69631) + String.fromCharCode(124928) + "-" + String.fromCharCode(126975) + "]"
);
function _c(n, t) {
  return (t === "start" || t === "end") && !o_.test(n) && (t = t === "start" ? "left" : "right"), bs[t];
}
function a_(n, t, e) {
  return e > 0 && n.push(`
`, ""), n.push(t, ""), n;
}
class l_ {
  constructor(t, e, i, s) {
    this.overlaps = i, this.pixelRatio = e, this.resolution = t, this.alignFill_, this.instructions = s.instructions, this.coordinates = s.coordinates, this.coordinateCache_ = {}, this.renderedTransform_ = $e(), this.hitDetectionInstructions = s.hitDetectionInstructions, this.pixelCoordinates_ = null, this.viewRotation_ = 0, this.fillStates = s.fillStates || {}, this.strokeStates = s.strokeStates || {}, this.textStates = s.textStates || {}, this.widths_ = {}, this.labels_ = {};
  }
  createLabel(t, e, i, s) {
    const r = t + e + i + s;
    if (this.labels_[r])
      return this.labels_[r];
    const o = s ? this.strokeStates[s] : null, a = i ? this.fillStates[i] : null, l = this.textStates[e], h = this.pixelRatio, c = [
      l.scale[0] * h,
      l.scale[1] * h
    ], u = Array.isArray(t), d = l.justify ? bs[l.justify] : _c(
      Array.isArray(t) ? t[0] : t,
      l.textAlign || $s
    ), f = s && o.lineWidth ? o.lineWidth : 0, g = u ? t : t.split(`
`).reduce(a_, []), { width: m, height: _, widths: y, heights: p, lineWidths: v } = E0(
      l,
      g
    ), x = m + f, C = [], E = (x + 2) * c[0], R = (_ + f) * c[1], b = {
      width: E < 0 ? Math.floor(E) : Math.ceil(E),
      height: R < 0 ? Math.floor(R) : Math.ceil(R),
      contextInstructions: C
    };
    (c[0] != 1 || c[1] != 1) && C.push("scale", c), s && (C.push("strokeStyle", o.strokeStyle), C.push("lineWidth", f), C.push("lineCap", o.lineCap), C.push("lineJoin", o.lineJoin), C.push("miterLimit", o.miterLimit), C.push("setLineDash", [o.lineDash]), C.push("lineDashOffset", o.lineDashOffset)), i && C.push("fillStyle", a.fillStyle), C.push("textBaseline", "middle"), C.push("textAlign", "center");
    const F = 0.5 - d;
    let G = d * x + F * f;
    const V = [], L = [];
    let $ = 0, gt = 0, N = 0, k = 0, P;
    for (let it = 0, wt = g.length; it < wt; it += 2) {
      const yt = g[it];
      if (yt === `
`) {
        gt += $, $ = 0, G = d * x + F * f, ++k;
        continue;
      }
      const At = g[it + 1] || l.font;
      At !== P && (s && V.push("font", At), i && L.push("font", At), P = At), $ = Math.max($, p[N]);
      const T = [
        yt,
        G + F * y[N] + d * (y[N] - v[k]),
        0.5 * (f + $) + gt
      ];
      G += y[N], s && V.push("strokeText", T), i && L.push("fillText", T), ++N;
    }
    return Array.prototype.push.apply(C, V), Array.prototype.push.apply(C, L), this.labels_[r] = b, b;
  }
  replayTextBackground_(t, e, i, s, r, o, a) {
    t.beginPath(), t.moveTo.apply(t, e), t.lineTo.apply(t, i), t.lineTo.apply(t, s), t.lineTo.apply(t, r), t.lineTo.apply(t, e), o && (this.alignFill_ = o[2], this.fill_(t)), a && (this.setStrokeStyle_(
      t,
      a
    ), t.stroke());
  }
  calculateImageOrLabelDimensions_(t, e, i, s, r, o, a, l, h, c, u, d, f, g, m, _) {
    a *= d[0], l *= d[1];
    let y = i - a, p = s - l;
    const v = r + h > t ? t - h : r, x = o + c > e ? e - c : o, C = g[3] + v * d[0] + g[1], E = g[0] + x * d[1] + g[2], R = y - g[3], b = p - g[0];
    (m || u !== 0) && (mi[0] = R, _i[0] = R, mi[1] = b, Ke[1] = b, Ke[0] = R + C, Je[0] = Ke[0], Je[1] = b + E, _i[1] = Je[1]);
    let F;
    return u !== 0 ? (F = Ii(
      $e(),
      i,
      s,
      1,
      1,
      u,
      -i,
      -s
    ), Nt(F, mi), Nt(F, Ke), Nt(F, Je), Nt(F, _i), _e(
      Math.min(mi[0], Ke[0], Je[0], _i[0]),
      Math.min(mi[1], Ke[1], Je[1], _i[1]),
      Math.max(mi[0], Ke[0], Je[0], _i[0]),
      Math.max(mi[1], Ke[1], Je[1], _i[1]),
      En
    )) : _e(
      Math.min(R, R + C),
      Math.min(b, b + E),
      Math.max(R, R + C),
      Math.max(b, b + E),
      En
    ), f && (y = Math.round(y), p = Math.round(p)), {
      drawImageX: y,
      drawImageY: p,
      drawImageW: v,
      drawImageH: x,
      originX: h,
      originY: c,
      declutterBox: {
        minX: En[0],
        minY: En[1],
        maxX: En[2],
        maxY: En[3],
        value: _
      },
      canvasTransform: F,
      scale: d
    };
  }
  replayImageOrLabel_(t, e, i, s, r, o, a) {
    const l = !!(o || a), h = s.declutterBox, c = t.canvas, u = a ? a[2] * s.scale[0] / 2 : 0;
    return h.minX - u <= c.width / e && h.maxX + u >= 0 && h.minY - u <= c.height / e && h.maxY + u >= 0 && (l && this.replayTextBackground_(
      t,
      mi,
      Ke,
      Je,
      _i,
      o,
      a
    ), w0(
      t,
      s.canvasTransform,
      r,
      i,
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
      const e = Nt(this.renderedTransform_, [0, 0]), i = 512 * this.pixelRatio;
      t.save(), t.translate(e[0] % i, e[1] % i), t.rotate(this.viewRotation_);
    }
    t.fill(), this.alignFill_ && t.restore();
  }
  setStrokeStyle_(t, e) {
    t.strokeStyle = e[1], t.lineWidth = e[2], t.lineCap = e[3], t.lineJoin = e[4], t.miterLimit = e[5], t.lineDashOffset = e[7], t.setLineDash(e[6]);
  }
  drawLabelWithPointPlacement_(t, e, i, s) {
    const r = this.textStates[e], o = this.createLabel(t, e, s, i), a = this.strokeStates[i], l = this.pixelRatio, h = _c(
      Array.isArray(t) ? t[0] : t,
      r.textAlign || $s
    ), c = bs[r.textBaseline || so], u = a && a.lineWidth ? a.lineWidth : 0, d = o.width / l - 2 * r.scale[0], f = h * d + 2 * (0.5 - h) * u, g = c * o.height / l + 2 * (0.5 - c) * u;
    return {
      label: o,
      anchorX: f,
      anchorY: g
    };
  }
  execute_(t, e, i, s, r, o, a, l) {
    let h;
    this.pixelCoordinates_ && Ni(i, this.renderedTransform_) ? h = this.pixelCoordinates_ : (this.pixelCoordinates_ || (this.pixelCoordinates_ = []), h = Ki(
      this.coordinates,
      0,
      this.coordinates.length,
      2,
      i,
      this.pixelCoordinates_
    ), Hg(this.renderedTransform_, i));
    let c = 0;
    const u = s.length;
    let d = 0, f, g, m, _, y, p, v, x, C, E, R, b, F = 0, G = 0, V = null, L = null;
    const $ = this.coordinateCache_, gt = this.viewRotation_, N = Math.round(Math.atan2(-i[1], i[0]) * 1e12) / 1e12, k = {
      context: t,
      pixelRatio: this.pixelRatio,
      resolution: this.resolution,
      rotation: gt
    }, P = this.instructions != s || this.overlaps ? 0 : 200;
    let it, wt, yt, At;
    for (; c < u; ) {
      const T = s[c];
      switch (T[0]) {
        case W.BEGIN_GEOMETRY:
          it = T[1], At = T[3], it.getGeometry() ? a !== void 0 && !Kt(a, At.getExtent()) ? c = T[2] + 1 : ++c : c = T[2];
          break;
        case W.BEGIN_PATH:
          F > P && (this.fill_(t), F = 0), G > P && (t.stroke(), G = 0), !F && !G && (t.beginPath(), _ = NaN, y = NaN), ++c;
          break;
        case W.CIRCLE:
          d = T[1];
          const ht = h[d], _t = h[d + 1], ui = h[d + 2], Fe = h[d + 3], Bt = ui - ht, Xe = Fe - _t, mn = Math.sqrt(Bt * Bt + Xe * Xe);
          t.moveTo(ht + mn, _t), t.arc(ht, _t, mn, 0, 2 * Math.PI, !0), ++c;
          break;
        case W.CLOSE_PATH:
          t.closePath(), ++c;
          break;
        case W.CUSTOM:
          d = T[1], f = T[2];
          const mr = T[3], _n = T[4], _r = T.length == 6 ? T[5] : void 0;
          k.geometry = mr, k.feature = it, c in $ || ($[c] = []);
          const di = $[c];
          _r ? _r(h, d, f, 2, di) : (di[0] = h[d], di[1] = h[d + 1], di.length = 2), _n(di, k), ++c;
          break;
        case W.DRAW_IMAGE:
          d = T[1], f = T[2], x = T[3], g = T[4], m = T[5];
          let hs = T[6];
          const fi = T[7], pr = T[8], yr = T[9], vr = T[10];
          let pn = T[11];
          const Yo = T[12];
          let te = T[13];
          const ye = T[14], Te = T[15];
          if (!x && T.length >= 20) {
            C = T[19], E = T[20], R = T[21], b = T[22];
            const ue = this.drawLabelWithPointPlacement_(
              C,
              E,
              R,
              b
            );
            x = ue.label, T[3] = x;
            const xn = T[23];
            g = (ue.anchorX - xn) * this.pixelRatio, T[4] = g;
            const ve = T[24];
            m = (ue.anchorY - ve) * this.pixelRatio, T[5] = m, hs = x.height, T[6] = hs, te = x.width, T[13] = te;
          }
          let Ye;
          T.length > 25 && (Ye = T[25]);
          let yn, Gi, gi;
          T.length > 17 ? (yn = T[16], Gi = T[17], gi = T[18]) : (yn = Ui, Gi = !1, gi = !1), vr && N ? pn += gt : !vr && !N && (pn -= gt);
          let vn = 0;
          for (; d < f; d += 2) {
            if (Ye && Ye[vn++] < te / this.pixelRatio)
              continue;
            const ue = this.calculateImageOrLabelDimensions_(
              x.width,
              x.height,
              h[d],
              h[d + 1],
              te,
              hs,
              g,
              m,
              pr,
              yr,
              pn,
              Yo,
              r,
              yn,
              Gi || gi,
              it
            ), xn = [
              t,
              e,
              x,
              ue,
              fi,
              Gi ? V : null,
              gi ? L : null
            ];
            if (l) {
              if (ye === "none")
                continue;
              if (ye === "obstacle") {
                l.insert(ue.declutterBox);
                continue;
              } else {
                let ve, je;
                if (Te) {
                  const de = f - d;
                  if (!Te[de]) {
                    Te[de] = xn;
                    continue;
                  }
                  if (ve = Te[de], delete Te[de], je = mc(ve), l.collides(je))
                    continue;
                }
                if (l.collides(ue.declutterBox))
                  continue;
                ve && (l.insert(je), this.replayImageOrLabel_.apply(this, ve)), l.insert(ue.declutterBox);
              }
            }
            this.replayImageOrLabel_.apply(this, xn);
          }
          ++c;
          break;
        case W.DRAW_CHARS:
          const xr = T[1], Yt = T[2], jo = T[3], mg = T[4];
          b = T[5];
          const _g = T[6], xh = T[7], Ch = T[8];
          R = T[9];
          const qo = T[10];
          C = T[11], E = T[12];
          const Mh = [
            T[13],
            T[13]
          ], Ko = this.textStates[E], cs = Ko.font, us = [
            Ko.scale[0] * xh,
            Ko.scale[1] * xh
          ];
          let ds;
          cs in this.widths_ ? ds = this.widths_[cs] : (ds = {}, this.widths_[cs] = ds);
          const Eh = Bd(h, xr, Yt, 2), wh = Math.abs(us[0]) * Hh(cs, C, ds);
          if (mg || wh <= Eh) {
            const ue = this.textStates[E].textAlign, xn = (Eh - wh) * bs[ue], ve = r_(
              h,
              xr,
              Yt,
              2,
              C,
              xn,
              _g,
              Math.abs(us[0]),
              Hh,
              cs,
              ds,
              N ? 0 : this.viewRotation_
            );
            t:
              if (ve) {
                const je = [];
                let de, Cr, Mr, ee, xe;
                if (R)
                  for (de = 0, Cr = ve.length; de < Cr; ++de) {
                    xe = ve[de], Mr = xe[4], ee = this.createLabel(Mr, E, "", R), g = xe[2] + (us[0] < 0 ? -qo : qo), m = jo * ee.height + (0.5 - jo) * 2 * qo * us[1] / us[0] - Ch;
                    const qe = this.calculateImageOrLabelDimensions_(
                      ee.width,
                      ee.height,
                      xe[0],
                      xe[1],
                      ee.width,
                      ee.height,
                      g,
                      m,
                      0,
                      0,
                      xe[3],
                      Mh,
                      !1,
                      Ui,
                      !1,
                      it
                    );
                    if (l && l.collides(qe.declutterBox))
                      break t;
                    je.push([
                      t,
                      e,
                      ee,
                      qe,
                      1,
                      null,
                      null
                    ]);
                  }
                if (b)
                  for (de = 0, Cr = ve.length; de < Cr; ++de) {
                    xe = ve[de], Mr = xe[4], ee = this.createLabel(Mr, E, b, ""), g = xe[2], m = jo * ee.height - Ch;
                    const qe = this.calculateImageOrLabelDimensions_(
                      ee.width,
                      ee.height,
                      xe[0],
                      xe[1],
                      ee.width,
                      ee.height,
                      g,
                      m,
                      0,
                      0,
                      xe[3],
                      Mh,
                      !1,
                      Ui,
                      !1,
                      it
                    );
                    if (l && l.collides(qe.declutterBox))
                      break t;
                    je.push([
                      t,
                      e,
                      ee,
                      qe,
                      1,
                      null,
                      null
                    ]);
                  }
                l && l.load(je.map(mc));
                for (let qe = 0, pg = je.length; qe < pg; ++qe)
                  this.replayImageOrLabel_.apply(this, je[qe]);
              }
          }
          ++c;
          break;
        case W.END_GEOMETRY:
          if (o !== void 0) {
            it = T[1];
            const ue = o(it, At);
            if (ue)
              return ue;
          }
          ++c;
          break;
        case W.FILL:
          P ? F++ : this.fill_(t), ++c;
          break;
        case W.MOVE_TO_LINE_TO:
          for (d = T[1], f = T[2], wt = h[d], yt = h[d + 1], p = wt + 0.5 | 0, v = yt + 0.5 | 0, (p !== _ || v !== y) && (t.moveTo(wt, yt), _ = p, y = v), d += 2; d < f; d += 2)
            wt = h[d], yt = h[d + 1], p = wt + 0.5 | 0, v = yt + 0.5 | 0, (d == f - 2 || p !== _ || v !== y) && (t.lineTo(wt, yt), _ = p, y = v);
          ++c;
          break;
        case W.SET_FILL_STYLE:
          V = T, this.alignFill_ = T[2], F && (this.fill_(t), F = 0, G && (t.stroke(), G = 0)), t.fillStyle = T[1], ++c;
          break;
        case W.SET_STROKE_STYLE:
          L = T, G && (t.stroke(), G = 0), this.setStrokeStyle_(t, T), ++c;
          break;
        case W.STROKE:
          P ? G++ : t.stroke(), ++c;
          break;
        default:
          ++c;
          break;
      }
    }
    F && this.fill_(t), G && t.stroke();
  }
  execute(t, e, i, s, r, o) {
    this.viewRotation_ = s, this.execute_(
      t,
      e,
      i,
      this.instructions,
      r,
      void 0,
      void 0,
      o
    );
  }
  executeHitDetection(t, e, i, s, r) {
    return this.viewRotation_ = i, this.execute_(
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
const h_ = l_, da = ["Polygon", "Circle", "LineString", "Image", "Text", "Default"];
class c_ {
  constructor(t, e, i, s, r, o) {
    this.maxExtent_ = t, this.overlaps_ = s, this.pixelRatio_ = i, this.resolution_ = e, this.renderBuffer_ = o, this.executorsByZIndex_ = {}, this.hitDetectionContext_ = null, this.hitDetectionTransform_ = $e(), this.createExecutors_(r);
  }
  clip(t, e) {
    const i = this.getClipCoords(e);
    t.beginPath(), t.moveTo(i[0], i[1]), t.lineTo(i[2], i[3]), t.lineTo(i[4], i[5]), t.lineTo(i[6], i[7]), t.clip();
  }
  createExecutors_(t) {
    for (const e in t) {
      let i = this.executorsByZIndex_[e];
      i === void 0 && (i = {}, this.executorsByZIndex_[e] = i);
      const s = t[e];
      for (const r in s) {
        const o = s[r];
        i[r] = new h_(
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
      const i = this.executorsByZIndex_[e];
      for (let s = 0, r = t.length; s < r; ++s)
        if (t[s] in i)
          return !0;
    }
    return !1;
  }
  forEachFeatureAtCoordinate(t, e, i, s, r, o) {
    s = Math.round(s);
    const a = s * 2 + 1, l = Ii(
      this.hitDetectionTransform_,
      s + 0.5,
      s + 0.5,
      1 / e,
      -1 / e,
      -i,
      -t[0],
      -t[1]
    ), h = !this.hitDetectionContext_;
    h && (this.hitDetectionContext_ = pe(
      a,
      a
    ));
    const c = this.hitDetectionContext_;
    c.canvas.width !== a || c.canvas.height !== a ? (c.canvas.width = a, c.canvas.height = a) : h || c.clearRect(0, 0, a, a);
    let u;
    this.renderBuffer_ !== void 0 && (u = se(), Ss(u, t), Js(
      u,
      e * (this.renderBuffer_ + s),
      u
    ));
    const d = u_(s);
    let f;
    function g(C, E) {
      const R = c.getImageData(
        0,
        0,
        a,
        a
      ).data;
      for (let b = 0, F = d.length; b < F; b++)
        if (R[d[b]] > 0) {
          if (!o || f !== "Image" && f !== "Text" || o.includes(C)) {
            const G = (d[b] - 3) / 4, V = s - G % a, L = s - (G / a | 0), $ = r(C, E, V * V + L * L);
            if ($)
              return $;
          }
          c.clearRect(0, 0, a, a);
          break;
        }
    }
    const m = Object.keys(this.executorsByZIndex_).map(Number);
    m.sort(tn);
    let _, y, p, v, x;
    for (_ = m.length - 1; _ >= 0; --_) {
      const C = m[_].toString();
      for (p = this.executorsByZIndex_[C], y = da.length - 1; y >= 0; --y)
        if (f = da[y], v = p[f], v !== void 0 && (x = v.executeHitDetection(
          c,
          l,
          i,
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
    const i = e[0], s = e[1], r = e[2], o = e[3], a = [i, s, i, o, r, o, r, s];
    return Ki(a, 0, 8, 2, t, a), a;
  }
  isEmpty() {
    return Hn(this.executorsByZIndex_);
  }
  execute(t, e, i, s, r, o, a) {
    const l = Object.keys(this.executorsByZIndex_).map(Number);
    l.sort(tn), this.maxExtent_ && (t.save(), this.clip(t, i)), o = o || da;
    let h, c, u, d, f, g;
    for (a && l.reverse(), h = 0, c = l.length; h < c; ++h) {
      const m = l[h].toString();
      for (f = this.executorsByZIndex_[m], u = 0, d = o.length; u < d; ++u) {
        const _ = o[u];
        g = f[_], g !== void 0 && g.execute(
          t,
          e,
          i,
          s,
          r,
          a
        );
      }
    }
    this.maxExtent_ && t.restore();
  }
}
const fa = {};
function u_(n) {
  if (fa[n] !== void 0)
    return fa[n];
  const t = n * 2 + 1, e = n * n, i = new Array(e + 1);
  for (let r = 0; r <= n; ++r)
    for (let o = 0; o <= n; ++o) {
      const a = r * r + o * o;
      if (a > e)
        break;
      let l = i[a];
      l || (l = [], i[a] = l), l.push(((n + r) * t + (n + o)) * 4 + 3), r > 0 && l.push(((n - r) * t + (n + o)) * 4 + 3), o > 0 && (l.push(((n + r) * t + (n - o)) * 4 + 3), r > 0 && l.push(((n - r) * t + (n - o)) * 4 + 3));
    }
  const s = [];
  for (let r = 0, o = i.length; r < o; ++r)
    i[r] && s.push(...i[r]);
  return fa[n] = s, s;
}
const pc = c_;
class d_ extends Xd {
  constructor(t, e, i, s, r, o, a) {
    super(), this.context_ = t, this.pixelRatio_ = e, this.extent_ = i, this.transform_ = s, this.viewRotation_ = r, this.squaredTolerance_ = o, this.userTransform_ = a, this.contextFillState_ = null, this.contextStrokeState_ = null, this.contextTextState_ = null, this.fillState_ = null, this.strokeState_ = null, this.image_ = null, this.imageAnchorX_ = 0, this.imageAnchorY_ = 0, this.imageHeight_ = 0, this.imageOpacity_ = 0, this.imageOriginX_ = 0, this.imageOriginY_ = 0, this.imageRotateWithView_ = !1, this.imageRotation_ = 0, this.imageScale_ = [0, 0], this.imageWidth_ = 0, this.text_ = "", this.textOffsetX_ = 0, this.textOffsetY_ = 0, this.textRotateWithView_ = !1, this.textRotation_ = 0, this.textScale_ = [0, 0], this.textFillState_ = null, this.textStrokeState_ = null, this.textState_ = null, this.pixelCoordinates_ = [], this.tmpLocalTransform_ = $e();
  }
  drawImages_(t, e, i, s) {
    if (!this.image_)
      return;
    const r = Ki(
      t,
      e,
      i,
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
        Ii(
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
  drawText_(t, e, i, s) {
    if (!this.textState_ || this.text_ === "")
      return;
    this.textFillState_ && this.setContextFillState_(this.textFillState_), this.textStrokeState_ && this.setContextStrokeState_(this.textStrokeState_), this.setContextTextState_(this.textState_);
    const r = Ki(
      t,
      e,
      i,
      s,
      this.transform_,
      this.pixelCoordinates_
    ), o = this.context_;
    let a = this.textRotation_;
    for (this.textRotateWithView_ && (a += this.viewRotation_); e < i; e += s) {
      const l = r[e] + this.textOffsetX_, h = r[e + 1] + this.textOffsetY_;
      a !== 0 || this.textScale_[0] != 1 || this.textScale_[1] != 1 ? (o.translate(l - this.textOffsetX_, h - this.textOffsetY_), o.rotate(a), o.translate(this.textOffsetX_, this.textOffsetY_), o.scale(this.textScale_[0], this.textScale_[1]), this.textStrokeState_ && o.strokeText(this.text_, 0, 0), this.textFillState_ && o.fillText(this.text_, 0, 0), o.setTransform(1, 0, 0, 1, 0, 0)) : (this.textStrokeState_ && o.strokeText(this.text_, l, h), this.textFillState_ && o.fillText(this.text_, l, h));
    }
  }
  moveToLineTo_(t, e, i, s, r) {
    const o = this.context_, a = Ki(
      t,
      e,
      i,
      s,
      this.transform_,
      this.pixelCoordinates_
    );
    o.moveTo(a[0], a[1]);
    let l = a.length;
    r && (l -= 2);
    for (let h = 2; h < l; h += 2)
      o.lineTo(a[h], a[h + 1]);
    return r && o.closePath(), i;
  }
  drawRings_(t, e, i, s) {
    for (let r = 0, o = i.length; r < o; ++r)
      e = this.moveToLineTo_(
        t,
        e,
        i[r],
        s,
        !0
      );
    return e;
  }
  drawCircle(t) {
    if (!!Kt(this.extent_, t.getExtent())) {
      if (this.fillState_ || this.strokeState_) {
        this.fillState_ && this.setContextFillState_(this.fillState_), this.strokeState_ && this.setContextStrokeState_(this.strokeState_);
        const e = c1(
          t,
          this.transform_,
          this.pixelCoordinates_
        ), i = e[2] - e[0], s = e[3] - e[1], r = Math.sqrt(i * i + s * s), o = this.context_;
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
    const i = e.getGeometryFunction()(t);
    !i || !Kt(this.extent_, i.getExtent()) || (this.setStyle(e), this.drawGeometry(i));
  }
  drawGeometryCollection(t) {
    const e = t.getGeometriesArray();
    for (let i = 0, s = e.length; i < s; ++i)
      this.drawGeometry(e[i]);
  }
  drawPoint(t) {
    this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    ));
    const e = t.getFlatCoordinates(), i = t.getStride();
    this.image_ && this.drawImages_(e, 0, e.length, i), this.text_ !== "" && this.drawText_(e, 0, e.length, i);
  }
  drawMultiPoint(t) {
    this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    ));
    const e = t.getFlatCoordinates(), i = t.getStride();
    this.image_ && this.drawImages_(e, 0, e.length, i), this.text_ !== "" && this.drawText_(e, 0, e.length, i);
  }
  drawLineString(t) {
    if (this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    )), !!Kt(this.extent_, t.getExtent())) {
      if (this.strokeState_) {
        this.setContextStrokeState_(this.strokeState_);
        const e = this.context_, i = t.getFlatCoordinates();
        e.beginPath(), this.moveToLineTo_(
          i,
          0,
          i.length,
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
    if (!!Kt(this.extent_, e)) {
      if (this.strokeState_) {
        this.setContextStrokeState_(this.strokeState_);
        const i = this.context_, s = t.getFlatCoordinates();
        let r = 0;
        const o = t.getEnds(), a = t.getStride();
        i.beginPath();
        for (let l = 0, h = o.length; l < h; ++l)
          r = this.moveToLineTo_(
            s,
            r,
            o[l],
            a,
            !1
          );
        i.stroke();
      }
      if (this.text_ !== "") {
        const i = t.getFlatMidpoints();
        this.drawText_(i, 0, i.length, 2);
      }
    }
  }
  drawPolygon(t) {
    if (this.squaredTolerance_ && (t = t.simplifyTransformed(
      this.squaredTolerance_,
      this.userTransform_
    )), !!Kt(this.extent_, t.getExtent())) {
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
    )), !!Kt(this.extent_, t.getExtent())) {
      if (this.strokeState_ || this.fillState_) {
        this.fillState_ && this.setContextFillState_(this.fillState_), this.strokeState_ && this.setContextStrokeState_(this.strokeState_);
        const e = this.context_, i = t.getOrientedFlatCoordinates();
        let s = 0;
        const r = t.getEndss(), o = t.getStride();
        e.beginPath();
        for (let a = 0, l = r.length; a < l; ++a) {
          const h = r[a];
          s = this.drawRings_(i, s, h, o);
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
    const e = this.context_, i = this.contextFillState_;
    i ? i.fillStyle != t.fillStyle && (i.fillStyle = t.fillStyle, e.fillStyle = t.fillStyle) : (e.fillStyle = t.fillStyle, this.contextFillState_ = {
      fillStyle: t.fillStyle
    });
  }
  setContextStrokeState_(t) {
    const e = this.context_, i = this.contextStrokeState_;
    i ? (i.lineCap != t.lineCap && (i.lineCap = t.lineCap, e.lineCap = t.lineCap), Ni(i.lineDash, t.lineDash) || e.setLineDash(
      i.lineDash = t.lineDash
    ), i.lineDashOffset != t.lineDashOffset && (i.lineDashOffset = t.lineDashOffset, e.lineDashOffset = t.lineDashOffset), i.lineJoin != t.lineJoin && (i.lineJoin = t.lineJoin, e.lineJoin = t.lineJoin), i.lineWidth != t.lineWidth && (i.lineWidth = t.lineWidth, e.lineWidth = t.lineWidth), i.miterLimit != t.miterLimit && (i.miterLimit = t.miterLimit, e.miterLimit = t.miterLimit), i.strokeStyle != t.strokeStyle && (i.strokeStyle = t.strokeStyle, e.strokeStyle = t.strokeStyle)) : (e.lineCap = t.lineCap, e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset, e.lineJoin = t.lineJoin, e.lineWidth = t.lineWidth, e.miterLimit = t.miterLimit, e.strokeStyle = t.strokeStyle, this.contextStrokeState_ = {
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
    const e = this.context_, i = this.contextTextState_, s = t.textAlign ? t.textAlign : $s;
    i ? (i.font != t.font && (i.font = t.font, e.font = t.font), i.textAlign != s && (i.textAlign = s, e.textAlign = s), i.textBaseline != t.textBaseline && (i.textBaseline = t.textBaseline, e.textBaseline = t.textBaseline)) : (e.font = t.font, e.textAlign = s, e.textBaseline = t.textBaseline, this.contextTextState_ = {
      font: t.font,
      textAlign: s,
      textBaseline: t.textBaseline
    });
  }
  setFillStrokeStyle(t, e) {
    if (!t)
      this.fillState_ = null;
    else {
      const i = t.getColor();
      this.fillState_ = {
        fillStyle: ke(
          i || ai
        )
      };
    }
    if (!e)
      this.strokeState_ = null;
    else {
      const i = e.getColor(), s = e.getLineCap(), r = e.getLineDash(), o = e.getLineDashOffset(), a = e.getLineJoin(), l = e.getWidth(), h = e.getMiterLimit(), c = r || Ns;
      this.strokeState_ = {
        lineCap: s !== void 0 ? s : no,
        lineDash: this.pixelRatio_ === 1 ? c : c.map((u) => u * this.pixelRatio_),
        lineDashOffset: (o || Ds) * this.pixelRatio_,
        lineJoin: a !== void 0 ? a : Xn,
        lineWidth: (l !== void 0 ? l : Bs) * this.pixelRatio_,
        miterLimit: h !== void 0 ? h : ks,
        strokeStyle: ke(
          i || Gs
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
    const i = t.getPixelRatio(this.pixelRatio_), s = t.getAnchor(), r = t.getOrigin();
    this.image_ = t.getImage(this.pixelRatio_), this.imageAnchorX_ = s[0] * i, this.imageAnchorY_ = s[1] * i, this.imageHeight_ = e[1] * i, this.imageOpacity_ = t.getOpacity(), this.imageOriginX_ = r[0], this.imageOriginY_ = r[1], this.imageRotateWithView_ = t.getRotateWithView(), this.imageRotation_ = t.getRotation();
    const o = t.getScaleArray();
    this.imageScale_ = [
      o[0] * this.pixelRatio_ / i,
      o[1] * this.pixelRatio_ / i
    ], this.imageWidth_ = e[0] * i;
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
          fillStyle: ke(
            f || ai
          )
        };
      }
      const i = t.getStroke();
      if (!i)
        this.textStrokeState_ = null;
      else {
        const f = i.getColor(), g = i.getLineCap(), m = i.getLineDash(), _ = i.getLineDashOffset(), y = i.getLineJoin(), p = i.getWidth(), v = i.getMiterLimit();
        this.textStrokeState_ = {
          lineCap: g !== void 0 ? g : no,
          lineDash: m || Ns,
          lineDashOffset: _ || Ds,
          lineJoin: y !== void 0 ? y : Xn,
          lineWidth: p !== void 0 ? p : Bs,
          miterLimit: v !== void 0 ? v : ks,
          strokeStyle: ke(
            f || Gs
          )
        };
      }
      const s = t.getFont(), r = t.getOffsetX(), o = t.getOffsetY(), a = t.getRotateWithView(), l = t.getRotation(), h = t.getScaleArray(), c = t.getText(), u = t.getTextAlign(), d = t.getTextBaseline();
      this.textState_ = {
        font: s !== void 0 ? s : cd,
        textAlign: u !== void 0 ? u : $s,
        textBaseline: d !== void 0 ? d : so
      }, this.text_ = c !== void 0 ? Array.isArray(c) ? c.reduce((f, g, m) => f += m % 2 ? " " : g, "") : c : "", this.textOffsetX_ = r !== void 0 ? this.pixelRatio_ * r : 0, this.textOffsetY_ = o !== void 0 ? this.pixelRatio_ * o : 0, this.textRotateWithView_ = a !== void 0 ? a : !1, this.textRotation_ = l !== void 0 ? l : 0, this.textScale_ = [
        this.pixelRatio_ * h[0],
        this.pixelRatio_ * h[1]
      ];
    }
  }
}
const f_ = d_, De = 0.5;
function g_(n, t, e, i, s, r, o) {
  const a = n[0] * De, l = n[1] * De, h = pe(a, l);
  h.imageSmoothingEnabled = !1;
  const c = h.canvas, u = new f_(
    h,
    De,
    s,
    null,
    o
  ), d = e.length, f = Math.floor((256 * 256 * 256 - 1) / d), g = {};
  for (let _ = 1; _ <= d; ++_) {
    const y = e[_ - 1], p = y.getStyleFunction() || i;
    if (!i)
      continue;
    let v = p(y, r);
    if (!v)
      continue;
    Array.isArray(v) || (v = [v]);
    const C = "#" + ("000000" + (_ * f).toString(16)).slice(-6);
    for (let E = 0, R = v.length; E < R; ++E) {
      const b = v[E], F = b.getGeometryFunction()(y);
      if (!F || !Kt(s, F.getExtent()))
        continue;
      const G = b.clone(), V = G.getFill();
      V && V.setColor(C);
      const L = G.getStroke();
      L && (L.setColor(C), L.setLineDash(null)), G.setText(void 0);
      const $ = b.getImage();
      if ($ && $.getOpacity() !== 0) {
        const k = $.getImageSize();
        if (!k)
          continue;
        const P = pe(
          k[0],
          k[1],
          void 0,
          { alpha: !1 }
        ), it = P.canvas;
        P.fillStyle = C, P.fillRect(0, 0, it.width, it.height), G.setImage(
          new Ts({
            img: it,
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
      const gt = G.getZIndex() || 0;
      let N = g[gt];
      N || (N = {}, g[gt] = N, N.Polygon = [], N.Circle = [], N.LineString = [], N.Point = []), N[F.getType().replace("Multi", "")].push(
        F,
        G
      );
    }
  }
  const m = Object.keys(g).map(Number).sort(tn);
  for (let _ = 0, y = m.length; _ < y; ++_) {
    const p = g[m[_]];
    for (const v in p) {
      const x = p[v];
      for (let C = 0, E = x.length; C < E; C += 2) {
        u.setStyle(x[C + 1]);
        for (let R = 0, b = t.length; R < b; ++R)
          u.setTransform(t[R]), u.drawGeometry(x[C]);
      }
    }
  }
  return h.getImageData(0, 0, c.width, c.height);
}
function m_(n, t, e) {
  const i = [];
  if (e) {
    const s = Math.floor(Math.round(n[0]) * De), r = Math.floor(Math.round(n[1]) * De), o = (Et(s, 0, e.width - 1) + Et(r, 0, e.height - 1) * e.width) * 4, a = e.data[o], l = e.data[o + 1], c = e.data[o + 2] + 256 * (l + 256 * a), u = Math.floor((256 * 256 * 256 - 1) / t.length);
    c && c % u === 0 && i.push(t[c / u - 1]);
  }
  return i;
}
const __ = 0.5, jd = {
  Point: S_,
  LineString: M_,
  Polygon: T_,
  MultiPoint: R_,
  MultiLineString: E_,
  MultiPolygon: w_,
  GeometryCollection: C_,
  Circle: v_
};
function p_(n, t) {
  return parseInt(q(n), 10) - parseInt(q(t), 10);
}
function y_(n, t) {
  const e = Ha(n, t);
  return e * e;
}
function Ha(n, t) {
  return __ * n / t;
}
function v_(n, t, e, i, s) {
  const r = e.getFill(), o = e.getStroke();
  if (r || o) {
    const l = n.getBuilder(e.getZIndex(), "Circle");
    l.setFillStrokeStyle(r, o), l.drawCircle(t, i);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || n).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, i);
  }
}
function yc(n, t, e, i, s, r, o) {
  let a = !1;
  const l = e.getImage();
  if (l) {
    const h = l.getImageState();
    h == Pt.LOADED || h == Pt.ERROR ? l.unlistenImageChange(s) : (h == Pt.IDLE && l.load(), l.listenImageChange(s), a = !0);
  }
  return x_(
    n,
    t,
    e,
    i,
    r,
    o
  ), a;
}
function x_(n, t, e, i, s, r) {
  const o = e.getGeometryFunction()(t);
  if (!o)
    return;
  const a = o.simplifyTransformed(
    i,
    s
  );
  if (e.getRenderer())
    qd(n, a, e, t);
  else {
    const h = jd[a.getType()];
    h(
      n,
      a,
      e,
      t,
      r
    );
  }
}
function qd(n, t, e, i) {
  if (t.getType() == "GeometryCollection") {
    const r = t.getGeometries();
    for (let o = 0, a = r.length; o < a; ++o)
      qd(n, r[o], e, i);
    return;
  }
  n.getBuilder(e.getZIndex(), "Default").drawCustom(
    t,
    i,
    e.getRenderer(),
    e.getHitDetectionRenderer()
  );
}
function C_(n, t, e, i, s) {
  const r = t.getGeometriesArray();
  let o, a;
  for (o = 0, a = r.length; o < a; ++o) {
    const l = jd[r[o].getType()];
    l(
      n,
      r[o],
      e,
      i,
      s
    );
  }
}
function M_(n, t, e, i, s) {
  const r = e.getStroke();
  if (r) {
    const a = n.getBuilder(
      e.getZIndex(),
      "LineString"
    );
    a.setFillStrokeStyle(null, r), a.drawLineString(t, i);
  }
  const o = e.getText();
  if (o && o.getText()) {
    const a = (s || n).getBuilder(
      e.getZIndex(),
      "Text"
    );
    a.setTextStyle(o), a.drawText(t, i);
  }
}
function E_(n, t, e, i, s) {
  const r = e.getStroke();
  if (r) {
    const a = n.getBuilder(
      e.getZIndex(),
      "LineString"
    );
    a.setFillStrokeStyle(null, r), a.drawMultiLineString(t, i);
  }
  const o = e.getText();
  if (o && o.getText()) {
    const a = (s || n).getBuilder(
      e.getZIndex(),
      "Text"
    );
    a.setTextStyle(o), a.drawText(t, i);
  }
}
function w_(n, t, e, i, s) {
  const r = e.getFill(), o = e.getStroke();
  if (o || r) {
    const l = n.getBuilder(e.getZIndex(), "Polygon");
    l.setFillStrokeStyle(r, o), l.drawMultiPolygon(t, i);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || n).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, i);
  }
}
function S_(n, t, e, i, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != Pt.LOADED)
      return;
    let l = n;
    if (s) {
      const c = r.getDeclutterMode();
      if (c !== "none")
        if (l = s, c === "obstacle") {
          const u = n.getBuilder(
            e.getZIndex(),
            "Image"
          );
          u.setImageStyle(r, a), u.drawPoint(t, i);
        } else
          o && o.getText() && (a = {});
    }
    const h = l.getBuilder(
      e.getZIndex(),
      "Image"
    );
    h.setImageStyle(r, a), h.drawPoint(t, i);
  }
  if (o && o.getText()) {
    let l = n;
    s && (l = s);
    const h = l.getBuilder(e.getZIndex(), "Text");
    h.setTextStyle(o, a), h.drawText(t, i);
  }
}
function R_(n, t, e, i, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != Pt.LOADED)
      return;
    let l = n;
    if (s) {
      const c = r.getDeclutterMode();
      if (c !== "none")
        if (l = s, c === "obstacle") {
          const u = n.getBuilder(
            e.getZIndex(),
            "Image"
          );
          u.setImageStyle(r, a), u.drawMultiPoint(t, i);
        } else
          o && o.getText() && (a = {});
    }
    const h = l.getBuilder(
      e.getZIndex(),
      "Image"
    );
    h.setImageStyle(r, a), h.drawMultiPoint(t, i);
  }
  if (o && o.getText()) {
    let l = n;
    s && (l = s);
    const h = l.getBuilder(e.getZIndex(), "Text");
    h.setTextStyle(o, a), h.drawText(t, i);
  }
}
function T_(n, t, e, i, s) {
  const r = e.getFill(), o = e.getStroke();
  if (r || o) {
    const l = n.getBuilder(e.getZIndex(), "Polygon");
    l.setFillStrokeStyle(r, o), l.drawPolygon(t, i);
  }
  const a = e.getText();
  if (a && a.getText()) {
    const l = (s || n).getBuilder(
      e.getZIndex(),
      "Text"
    );
    l.setTextStyle(a), l.drawText(t, i);
  }
}
class b_ extends Yd {
  constructor(t) {
    super(t), this.boundHandleStyleImageChange_ = this.handleStyleImageChange_.bind(this), this.animatingOrInteracting_, this.hitDetectionImageData_ = null, this.renderedFeatures_ = null, this.renderedRevision_ = -1, this.renderedResolution_ = NaN, this.renderedExtent_ = se(), this.wrappedRenderedExtent_ = se(), this.renderedRotation_, this.renderedCenter_ = null, this.renderedProjection_ = null, this.renderedRenderOrder_ = null, this.replayGroup_ = null, this.replayGroupChanged = !0, this.declutterExecutorGroup = null, this.clipping = !0, this.compositionContext_ = null, this.opacity_ = 1;
  }
  renderWorlds(t, e, i) {
    const s = e.extent, r = e.viewState, o = r.center, a = r.resolution, l = r.projection, h = r.rotation, c = l.getExtent(), u = this.getLayer().getSource(), d = e.pixelRatio, f = e.viewHints, g = !(f[Wt.ANIMATING] || f[Wt.INTERACTING]), m = this.compositionContext_, _ = Math.round(e.size[0] * d), y = Math.round(e.size[1] * d), p = u.getWrapX() && l.canWrapX(), v = p ? pt(c) : null, x = p ? Math.ceil((s[2] - c[2]) / v) + 1 : 1;
    let C = p ? Math.floor((s[0] - c[0]) / v) : 0;
    do {
      const E = this.getRenderTransform(
        o,
        a,
        h,
        d,
        _,
        y,
        C * v
      );
      t.execute(
        m,
        1,
        E,
        h,
        g,
        void 0,
        i
      );
    } while (++C < x);
  }
  setupCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = pe(
        this.context.canvas.width,
        this.context.canvas.height,
        gc
      );
      this.compositionContext_ = t;
    } else
      this.compositionContext_ = this.context;
  }
  releaseCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = this.context.globalAlpha;
      this.context.globalAlpha = this.opacity_, this.context.drawImage(this.compositionContext_.canvas, 0, 0), this.context.globalAlpha = t, hd(this.compositionContext_), gc.push(this.compositionContext_.canvas), this.compositionContext_ = null;
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
    const i = t.pixelRatio, s = t.layerStatesArray[t.layerIndex];
    Xg(this.pixelTransform, 1 / i, 1 / i), _l(this.inversePixelTransform, this.pixelTransform);
    const r = Yu(this.pixelTransform);
    this.useContainer(e, r, this.getBackground(t));
    const o = this.context, a = o.canvas, l = this.replayGroup_, h = this.declutterExecutorGroup;
    if ((!l || l.isEmpty()) && (!h || h.isEmpty()))
      return null;
    const c = Math.round(t.size[0] * i), u = Math.round(t.size[1] * i);
    a.width != c || a.height != u ? (a.width = c, a.height = u, a.style.transform !== r && (a.style.transform = r)) : this.containerReused || o.clearRect(0, 0, c, u), this.preRender(o, t);
    const d = t.viewState;
    d.projection, this.opacity_ = s.opacity, this.setupCompositionContext_();
    let f = !1, g = !0;
    if (s.extent && this.clipping) {
      const m = Mi(s.extent);
      g = Kt(m, t.extent), f = g && !Vi(m, t.extent), f && this.clipUnrotated(this.compositionContext_, t, m);
    }
    return g && this.renderWorlds(l, t), f && this.compositionContext_.restore(), this.releaseCompositionContext_(), this.postRender(o, t), this.renderedRotation_ !== d.rotation && (this.renderedRotation_ = d.rotation, this.hitDetectionImageData_ = null), this.container;
  }
  getFeatures(t) {
    return new Promise(
      function(e) {
        if (!this.hitDetectionImageData_ && !this.animatingOrInteracting_) {
          const i = [this.context.canvas.width, this.context.canvas.height];
          Nt(this.pixelTransform, i);
          const s = this.renderedCenter_, r = this.renderedResolution_, o = this.renderedRotation_, a = this.renderedProjection_, l = this.wrappedRenderedExtent_, h = this.getLayer(), c = [], u = i[0] * De, d = i[1] * De;
          c.push(
            this.getRenderTransform(
              s,
              r,
              o,
              De,
              u,
              d,
              0
            ).slice()
          );
          const f = h.getSource(), g = a.getExtent();
          if (f.getWrapX() && a.canWrapX() && !Vi(g, l)) {
            let m = l[0];
            const _ = pt(g);
            let y = 0, p;
            for (; m < g[0]; )
              --y, p = _ * y, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  De,
                  u,
                  d,
                  p
                ).slice()
              ), m += _;
            for (y = 0, m = l[2]; m > g[2]; )
              ++y, p = _ * y, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  De,
                  u,
                  d,
                  p
                ).slice()
              ), m -= _;
          }
          this.hitDetectionImageData_ = g_(
            i,
            c,
            this.renderedFeatures_,
            h.getStyleFunction(),
            l,
            r,
            o
          );
        }
        e(
          m_(t, this.renderedFeatures_, this.hitDetectionImageData_)
        );
      }.bind(this)
    );
  }
  forEachFeatureAtCoordinate(t, e, i, s, r) {
    if (!this.replayGroup_)
      return;
    const o = e.viewState.resolution, a = e.viewState.rotation, l = this.getLayer(), h = {}, c = function(f, g, m) {
      const _ = q(f), y = h[_];
      if (y) {
        if (y !== !0 && m < y.distanceSq) {
          if (m === 0)
            return h[_] = !0, r.splice(r.lastIndexOf(y), 1), s(f, l, g);
          y.geometry = g, y.distanceSq = m;
        }
      } else {
        if (m === 0)
          return h[_] = !0, s(f, l, g);
        r.push(
          h[_] = {
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
      i,
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
    const e = this.getLayer(), i = e.getSource();
    if (!i)
      return !1;
    const s = t.viewHints[Wt.ANIMATING], r = t.viewHints[Wt.INTERACTING], o = e.getUpdateWhileAnimating(), a = e.getUpdateWhileInteracting();
    if (this.ready && !o && s || !a && r)
      return this.animatingOrInteracting_ = !0, !0;
    this.animatingOrInteracting_ = !1;
    const l = t.extent, h = t.viewState, c = h.projection, u = h.resolution, d = t.pixelRatio, f = e.getRevision(), g = e.getRenderBuffer();
    let m = e.getRenderOrder();
    m === void 0 && (m = p_);
    const _ = h.center.slice(), y = Js(
      l,
      g * u
    ), p = y.slice(), v = [y.slice()], x = c.getExtent();
    if (i.getWrapX() && c.canWrapX() && !Vi(x, t.extent)) {
      const N = pt(x), k = Math.max(pt(y) / 2, N);
      y[0] = x[0] - k, y[2] = x[2] + k, rd(_, c);
      const P = Qu(v[0], c);
      P[0] < x[0] && P[2] < x[2] ? v.push([
        P[0] + N,
        P[1],
        P[2] + N,
        P[3]
      ]) : P[0] > x[0] && P[2] > x[2] && v.push([
        P[0] - N,
        P[1],
        P[2] - N,
        P[3]
      ]);
    }
    if (this.ready && this.renderedResolution_ == u && this.renderedRevision_ == f && this.renderedRenderOrder_ == m && Vi(this.wrappedRenderedExtent_, y))
      return Ni(this.renderedExtent_, p) || (this.hitDetectionImageData_ = null, this.renderedExtent_ = p), this.renderedCenter_ = _, this.replayGroupChanged = !1, !0;
    this.replayGroup_ = null;
    const C = new fc(
      Ha(u, d),
      y,
      u,
      d
    );
    let E;
    this.getLayer().getDeclutter() && (E = new fc(
      Ha(u, d),
      y,
      u,
      d
    ));
    let R;
    for (let N = 0, k = v.length; N < k; ++N)
      i.loadFeatures(v[N], u, c);
    const b = y_(u, d);
    let F = !0;
    const G = function(N) {
      let k;
      const P = N.getStyleFunction() || e.getStyleFunction();
      if (P && (k = P(N, u)), k) {
        const it = this.renderFeature(
          N,
          b,
          k,
          C,
          R,
          E
        );
        F = F && !it;
      }
    }.bind(this), V = Il(y), L = i.getFeaturesInExtent(V);
    m && L.sort(m);
    for (let N = 0, k = L.length; N < k; ++N)
      G(L[N]);
    this.renderedFeatures_ = L, this.ready = F;
    const $ = C.finish(), gt = new pc(
      y,
      u,
      d,
      i.getOverlaps(),
      $,
      e.getRenderBuffer()
    );
    return E && (this.declutterExecutorGroup = new pc(
      y,
      u,
      d,
      i.getOverlaps(),
      E.finish(),
      e.getRenderBuffer()
    )), this.renderedResolution_ = u, this.renderedRevision_ = f, this.renderedRenderOrder_ = m, this.renderedExtent_ = p, this.wrappedRenderedExtent_ = y, this.renderedCenter_ = _, this.renderedProjection_ = c, this.replayGroup_ = gt, this.hitDetectionImageData_ = null, this.replayGroupChanged = !0, !0;
  }
  renderFeature(t, e, i, s, r, o) {
    if (!i)
      return !1;
    let a = !1;
    if (Array.isArray(i))
      for (let l = 0, h = i.length; l < h; ++l)
        a = yc(
          s,
          t,
          i[l],
          e,
          this.boundHandleStyleImageChange_,
          r,
          o
        ) || a;
    else
      a = yc(
        s,
        t,
        i,
        e,
        this.boundHandleStyleImageChange_,
        r,
        o
      );
    return a;
  }
}
const L_ = b_;
class I_ extends Vm {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new L_(this);
  }
}
const Ze = I_;
class P_ {
  constructor(t) {
    this.rbush_ = new Wd(t), this.items_ = {};
  }
  insert(t, e) {
    const i = {
      minX: t[0],
      minY: t[1],
      maxX: t[2],
      maxY: t[3],
      value: e
    };
    this.rbush_.insert(i), this.items_[q(e)] = i;
  }
  load(t, e) {
    const i = new Array(e.length);
    for (let s = 0, r = e.length; s < r; s++) {
      const o = t[s], a = e[s], l = {
        minX: o[0],
        minY: o[1],
        maxX: o[2],
        maxY: o[3],
        value: a
      };
      i[s] = l, this.items_[q(a)] = l;
    }
    this.rbush_.load(i);
  }
  remove(t) {
    const e = q(t), i = this.items_[e];
    return delete this.items_[e], this.rbush_.remove(i) !== null;
  }
  update(t, e) {
    const i = this.items_[q(e)], s = [i.minX, i.minY, i.maxX, i.maxY];
    Fs(s, t) || (this.remove(e), this.insert(t, e));
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
    let i;
    for (let s = 0, r = t.length; s < r; s++)
      if (i = e(t[s]), i)
        return i;
    return i;
  }
  isEmpty() {
    return Hn(this.items_);
  }
  clear() {
    this.rbush_.clear(), this.items_ = {};
  }
  getExtent(t) {
    const e = this.rbush_.toJSON();
    return _e(e.minX, e.minY, e.maxX, e.maxY, t);
  }
  concat(t) {
    this.rbush_.load(t.rbush_.all());
    for (const e in t.items_)
      this.items_[e] = t.items_[e];
  }
}
const fo = P_;
class A_ extends Oe {
  constructor(t) {
    super(), this.projection = Q(t.projection), this.attributions_ = vc(t.attributions), this.attributionsCollapsible_ = t.attributionsCollapsible !== void 0 ? t.attributionsCollapsible : !0, this.loading = !1, this.state_ = t.state !== void 0 ? t.state : "ready", this.wrapX_ = t.wrapX !== void 0 ? t.wrapX : !1, this.interpolate_ = !!t.interpolate, this.viewResolver = null, this.viewRejector = null;
    const e = this;
    this.viewPromise_ = new Promise(function(i, s) {
      e.viewResolver = i, e.viewRejector = s;
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
    return H();
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
    this.attributions_ = vc(t), this.changed();
  }
  setState(t) {
    this.state_ = t, this.changed();
  }
}
function vc(n) {
  return n ? Array.isArray(n) ? function(t) {
    return n;
  } : typeof n == "function" ? n : function(t) {
    return [n];
  } : null;
}
const Kd = A_, jt = {
  ADDFEATURE: "addfeature",
  CHANGEFEATURE: "changefeature",
  CLEAR: "clear",
  REMOVEFEATURE: "removefeature",
  FEATURESLOADSTART: "featuresloadstart",
  FEATURESLOADEND: "featuresloadend",
  FEATURESLOADERROR: "featuresloaderror"
};
function O_(n, t) {
  return [[-1 / 0, -1 / 0, 1 / 0, 1 / 0]];
}
function F_(n, t) {
  return [n];
}
let N_ = !1;
function D_(n, t, e, i, s, r, o) {
  const a = new XMLHttpRequest();
  a.open(
    "GET",
    typeof n == "function" ? n(e, i, s) : n,
    !0
  ), t.getType() == "arraybuffer" && (a.responseType = "arraybuffer"), a.withCredentials = N_, a.onload = function(l) {
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
function xc(n, t) {
  return function(e, i, s, r, o) {
    const a = this;
    D_(
      n,
      t,
      e,
      i,
      s,
      function(l, h) {
        a.addFeatures(l), r !== void 0 && r(l);
      },
      o || nn
    );
  };
}
class pi extends Re {
  constructor(t, e, i) {
    super(t), this.feature = e, this.features = i;
  }
}
class k_ extends Kd {
  constructor(t) {
    t = t || {}, super({
      attributions: t.attributions,
      interpolate: !0,
      projection: void 0,
      state: "ready",
      wrapX: t.wrapX !== void 0 ? t.wrapX : !0
    }), this.on, this.once, this.un, this.loader_ = nn, this.format_ = t.format, this.overlaps_ = t.overlaps === void 0 ? !0 : t.overlaps, this.url_ = t.url, t.loader !== void 0 ? this.loader_ = t.loader : this.url_ !== void 0 && (Y(this.format_, 7), this.loader_ = xc(
      this.url_,
      this.format_
    )), this.strategy_ = t.strategy !== void 0 ? t.strategy : O_;
    const e = t.useSpatialIndex !== void 0 ? t.useSpatialIndex : !0;
    this.featuresRtree_ = e ? new fo() : null, this.loadedExtentsRtree_ = new fo(), this.loadingExtentsCount_ = 0, this.nullGeometryFeatures_ = {}, this.idIndex_ = {}, this.uidIndex_ = {}, this.featureChangeKeys_ = {}, this.featuresCollection_ = null;
    let i, s;
    Array.isArray(t.features) ? s = t.features : t.features && (i = t.features, s = i.getArray()), !e && i === void 0 && (i = new Ee(s)), s !== void 0 && this.addFeaturesInternal(s), i !== void 0 && this.bindFeaturesCollection_(i);
  }
  addFeature(t) {
    this.addFeatureInternal(t), this.changed();
  }
  addFeatureInternal(t) {
    const e = q(t);
    if (!this.addToIndex_(e, t)) {
      this.featuresCollection_ && this.featuresCollection_.remove(t);
      return;
    }
    this.setupChangeEvents_(e, t);
    const i = t.getGeometry();
    if (i) {
      const s = i.getExtent();
      this.featuresRtree_ && this.featuresRtree_.insert(s, t);
    } else
      this.nullGeometryFeatures_[e] = t;
    this.dispatchEvent(
      new pi(jt.ADDFEATURE, t)
    );
  }
  setupChangeEvents_(t, e) {
    this.featureChangeKeys_[t] = [
      et(e, U.CHANGE, this.handleFeatureChange_, this),
      et(
        e,
        Wn.PROPERTYCHANGE,
        this.handleFeatureChange_,
        this
      )
    ];
  }
  addToIndex_(t, e) {
    let i = !0;
    const s = e.getId();
    return s !== void 0 && (s.toString() in this.idIndex_ ? i = !1 : this.idIndex_[s.toString()] = e), i && (Y(!(t in this.uidIndex_), 30), this.uidIndex_[t] = e), i;
  }
  addFeatures(t) {
    this.addFeaturesInternal(t), this.changed();
  }
  addFeaturesInternal(t) {
    const e = [], i = [], s = [];
    for (let r = 0, o = t.length; r < o; r++) {
      const a = t[r], l = q(a);
      this.addToIndex_(l, a) && i.push(a);
    }
    for (let r = 0, o = i.length; r < o; r++) {
      const a = i[r], l = q(a);
      this.setupChangeEvents_(l, a);
      const h = a.getGeometry();
      if (h) {
        const c = h.getExtent();
        e.push(c), s.push(a);
      } else
        this.nullGeometryFeatures_[l] = a;
    }
    if (this.featuresRtree_ && this.featuresRtree_.load(e, s), this.hasListener(jt.ADDFEATURE))
      for (let r = 0, o = i.length; r < o; r++)
        this.dispatchEvent(
          new pi(jt.ADDFEATURE, i[r])
        );
  }
  bindFeaturesCollection_(t) {
    let e = !1;
    this.addEventListener(
      jt.ADDFEATURE,
      function(i) {
        e || (e = !0, t.push(i.feature), e = !1);
      }
    ), this.addEventListener(
      jt.REMOVEFEATURE,
      function(i) {
        e || (e = !0, t.remove(i.feature), e = !1);
      }
    ), t.addEventListener(
      Dt.ADD,
      function(i) {
        e || (e = !0, this.addFeature(i.element), e = !1);
      }.bind(this)
    ), t.addEventListener(
      Dt.REMOVE,
      function(i) {
        e || (e = !0, this.removeFeature(i.element), e = !1);
      }.bind(this)
    ), this.featuresCollection_ = t;
  }
  clear(t) {
    if (t) {
      for (const i in this.featureChangeKeys_)
        this.featureChangeKeys_[i].forEach(mt);
      this.featuresCollection_ || (this.featureChangeKeys_ = {}, this.idIndex_ = {}, this.uidIndex_ = {});
    } else if (this.featuresRtree_) {
      const i = function(s) {
        this.removeFeatureInternal(s);
      }.bind(this);
      this.featuresRtree_.forEach(i);
      for (const s in this.nullGeometryFeatures_)
        this.removeFeatureInternal(this.nullGeometryFeatures_[s]);
    }
    this.featuresCollection_ && this.featuresCollection_.clear(), this.featuresRtree_ && this.featuresRtree_.clear(), this.nullGeometryFeatures_ = {};
    const e = new pi(jt.CLEAR);
    this.dispatchEvent(e), this.changed();
  }
  forEachFeature(t) {
    if (this.featuresRtree_)
      return this.featuresRtree_.forEach(t);
    this.featuresCollection_ && this.featuresCollection_.forEach(t);
  }
  forEachFeatureAtCoordinateDirect(t, e) {
    const i = [t[0], t[1], t[0], t[1]];
    return this.forEachFeatureInExtent(i, function(s) {
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
      function(i) {
        if (i.getGeometry().intersectsExtent(t)) {
          const r = e(i);
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
    return this.featuresCollection_ ? t = this.featuresCollection_.getArray().slice(0) : this.featuresRtree_ && (t = this.featuresRtree_.getAll(), Hn(this.nullGeometryFeatures_) || Qt(t, Object.values(this.nullGeometryFeatures_))), t;
  }
  getFeaturesAtCoordinate(t) {
    const e = [];
    return this.forEachFeatureAtCoordinateDirect(t, function(i) {
      e.push(i);
    }), e;
  }
  getFeaturesInExtent(t, e) {
    if (this.featuresRtree_) {
      if (!(e && e.canWrapX() && this.getWrapX()))
        return this.featuresRtree_.getInExtent(t);
      const s = e0(t, e);
      return [].concat(
        ...s.map((r) => this.featuresRtree_.getInExtent(r))
      );
    } else
      return this.featuresCollection_ ? this.featuresCollection_.getArray().slice(0) : [];
  }
  getClosestFeatureToCoordinate(t, e) {
    const i = t[0], s = t[1];
    let r = null;
    const o = [NaN, NaN];
    let a = 1 / 0;
    const l = [-1 / 0, -1 / 0, 1 / 0, 1 / 0];
    return e = e || en, this.featuresRtree_.forEachInExtent(
      l,
      function(h) {
        if (e(h)) {
          const c = h.getGeometry(), u = a;
          if (a = c.closestPointXY(
            i,
            s,
            o,
            a
          ), a < u) {
            r = h;
            const d = Math.sqrt(a);
            l[0] = i - d, l[1] = s - d, l[2] = i + d, l[3] = s + d;
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
    const e = t.target, i = q(e), s = e.getGeometry();
    if (!s)
      i in this.nullGeometryFeatures_ || (this.featuresRtree_ && this.featuresRtree_.remove(e), this.nullGeometryFeatures_[i] = e);
    else {
      const o = s.getExtent();
      i in this.nullGeometryFeatures_ ? (delete this.nullGeometryFeatures_[i], this.featuresRtree_ && this.featuresRtree_.insert(o, e)) : this.featuresRtree_ && this.featuresRtree_.update(o, e);
    }
    const r = e.getId();
    if (r !== void 0) {
      const o = r.toString();
      this.idIndex_[o] !== e && (this.removeFromIdIndex_(e), this.idIndex_[o] = e);
    } else
      this.removeFromIdIndex_(e), this.uidIndex_[i] = e;
    this.changed(), this.dispatchEvent(
      new pi(jt.CHANGEFEATURE, e)
    );
  }
  hasFeature(t) {
    const e = t.getId();
    return e !== void 0 ? e in this.idIndex_ : q(t) in this.uidIndex_;
  }
  isEmpty() {
    return this.featuresRtree_ ? this.featuresRtree_.isEmpty() && Hn(this.nullGeometryFeatures_) : this.featuresCollection_ ? this.featuresCollection_.getLength() === 0 : !0;
  }
  loadFeatures(t, e, i) {
    const s = this.loadedExtentsRtree_, r = this.strategy_(t, e, i);
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      s.forEachInExtent(
        l,
        function(c) {
          return Vi(c.extent, l);
        }
      ) || (++this.loadingExtentsCount_, this.dispatchEvent(
        new pi(jt.FEATURESLOADSTART)
      ), this.loader_.call(
        this,
        l,
        e,
        i,
        function(c) {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new pi(
              jt.FEATURESLOADEND,
              void 0,
              c
            )
          );
        }.bind(this),
        function() {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new pi(jt.FEATURESLOADERROR)
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
    let i;
    e.forEachInExtent(t, function(s) {
      if (Fs(s.extent, t))
        return i = s, !0;
    }), i && e.remove(i);
  }
  removeFeature(t) {
    if (!t)
      return;
    const e = q(t);
    e in this.nullGeometryFeatures_ ? delete this.nullGeometryFeatures_[e] : this.featuresRtree_ && this.featuresRtree_.remove(t), this.removeFeatureInternal(t) && this.changed();
  }
  removeFeatureInternal(t) {
    const e = q(t), i = this.featureChangeKeys_[e];
    if (!i)
      return;
    i.forEach(mt), delete this.featureChangeKeys_[e];
    const s = t.getId();
    return s !== void 0 && delete this.idIndex_[s.toString()], delete this.uidIndex_[e], this.dispatchEvent(
      new pi(jt.REMOVEFEATURE, t)
    ), t;
  }
  removeFromIdIndex_(t) {
    let e = !1;
    for (const i in this.idIndex_)
      if (this.idIndex_[i] === t) {
        delete this.idIndex_[i], e = !0;
        break;
      }
    return e;
  }
  setLoader(t) {
    this.loader_ = t;
  }
  setUrl(t) {
    Y(this.format_, 7), this.url_ = t, this.setLoader(xc(t, this.format_));
  }
}
const Ve = k_;
class G_ extends So {
  constructor(t, e, i) {
    super(), i = i || {}, this.tileCoord = t, this.state = e, this.interimTile = null, this.key = "", this.transition_ = i.transition === void 0 ? 250 : i.transition, this.transitionStarts_ = {}, this.interpolate = !!i.interpolate;
  }
  changed() {
    this.dispatchEvent(U.CHANGE);
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
    H();
  }
  getAlpha(t, e) {
    if (!this.transition_)
      return 1;
    let i = this.transitionStarts_[t];
    if (!i)
      i = e, this.transitionStarts_[t] = i;
    else if (i === -1)
      return 1;
    const s = e - i + 1e3 / 60;
    return s >= this.transition_ ? 1 : yd(s / this.transition_);
  }
  inTransition(t) {
    return this.transition_ ? this.transitionStarts_[t] !== -1 : !1;
  }
  endTransition(t) {
    this.transition_ && (this.transitionStarts_[t] = -1);
  }
}
const Jd = G_;
class $_ extends Jd {
  constructor(t, e, i, s, r, o) {
    super(t, e, o), this.crossOrigin_ = s, this.src_ = i, this.key = i, this.image_ = new Image(), s !== null && (this.image_.crossOrigin = s), this.unlisten_ = null, this.tileLoadFunction_ = r;
  }
  getImage() {
    return this.image_;
  }
  setImage(t) {
    this.image_ = t, this.state = z.LOADED, this.unlistenImage_(), this.changed();
  }
  handleImageError_() {
    this.state = z.ERROR, this.unlistenImage_(), this.image_ = B_(), this.changed();
  }
  handleImageLoad_() {
    const t = this.image_;
    t.naturalWidth && t.naturalHeight ? this.state = z.LOADED : this.state = z.EMPTY, this.unlistenImage_(), this.changed();
  }
  load() {
    this.state == z.ERROR && (this.state = z.IDLE, this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_)), this.state == z.IDLE && (this.state = z.LOADING, this.changed(), this.tileLoadFunction_(this, this.src_), this.unlisten_ = Hd(
      this.image_,
      this.handleImageLoad_.bind(this),
      this.handleImageError_.bind(this)
    ));
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function B_() {
  const n = pe(1, 1);
  return n.fillStyle = "rgba(0,0,0,0)", n.fillRect(0, 0, 1, 1), n.canvas;
}
const Qd = $_;
class z_ {
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
    const i = this.entries_[t];
    return Y(i !== void 0, 15), i === this.newest_ || (i === this.oldest_ ? (this.oldest_ = this.oldest_.newer, this.oldest_.older = null) : (i.newer.older = i.older, i.older.newer = i.newer), i.newer = null, i.older = this.newest_, this.newest_.newer = i, this.newest_ = i), i.value_;
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
    let e = 0, i;
    for (i = this.newest_; i; i = i.older)
      t[e++] = i.key_;
    return t;
  }
  getValues() {
    const t = new Array(this.count_);
    let e = 0, i;
    for (i = this.newest_; i; i = i.older)
      t[e++] = i.value_;
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
    const i = {
      key_: t,
      newer: null,
      older: this.newest_,
      value_: e
    };
    this.newest_ ? this.newest_.newer = i : this.oldest_ = i, this.newest_ = i, this.entries_[t] = i, ++this.count_;
  }
  setSize(t) {
    this.highWaterMark = t;
  }
}
const Z_ = z_;
function Cc(n, t, e, i) {
  return i !== void 0 ? (i[0] = n, i[1] = t, i[2] = e, i) : [n, t, e];
}
function ko(n, t, e) {
  return n + "/" + t + "/" + e;
}
function tf(n) {
  return ko(n[0], n[1], n[2]);
}
function V_(n) {
  return n.split("/").map(Number);
}
function U_(n) {
  return (n[1] << n[0]) + n[2];
}
function W_(n, t) {
  const e = n[0], i = n[1], s = n[2];
  if (t.getMinZoom() > e || e > t.getMaxZoom())
    return !1;
  const r = t.getFullTileRange(e);
  return r ? r.containsXY(i, s) : !0;
}
class H_ extends Z_ {
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
    const t = this.peekFirstKey(), i = V_(t)[0];
    this.forEach(
      function(s) {
        s.tileCoord[0] !== i && (this.remove(tf(s.tileCoord)), s.release());
      }.bind(this)
    );
  }
}
const ef = H_;
class nf {
  constructor(t, e, i, s) {
    this.minX = t, this.maxX = e, this.minY = i, this.maxY = s;
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
function wn(n, t, e, i, s) {
  return s !== void 0 ? (s.minX = n, s.maxX = t, s.minY = e, s.maxY = i, s) : new nf(n, t, e, i);
}
const sf = nf, Mc = [
  "fullscreenchange",
  "webkitfullscreenchange",
  "MSFullscreenChange"
], Ec = {
  ENTERFULLSCREEN: "enterfullscreen",
  LEAVEFULLSCREEN: "leavefullscreen"
};
class X_ extends Gt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      target: t.target
    }), this.on, this.once, this.un, this.keys_ = t.keys !== void 0 ? t.keys : !1, this.source_ = t.source, this.isInFullscreen_ = !1, this.boundHandleMapTargetChange_ = this.handleMapTargetChange_.bind(this), this.cssClassName_ = t.className !== void 0 ? t.className : "ol-full-screen", this.documentListeners_ = [], this.activeClassName_ = t.activeClassName !== void 0 ? t.activeClassName.split(" ") : [this.cssClassName_ + "-true"], this.inactiveClassName_ = t.inactiveClassName !== void 0 ? t.inactiveClassName.split(" ") : [this.cssClassName_ + "-false"];
    const e = t.label !== void 0 ? t.label : "\u2922";
    this.labelNode_ = typeof e == "string" ? document.createTextNode(e) : e;
    const i = t.labelActive !== void 0 ? t.labelActive : "\xD7";
    this.labelActiveNode_ = typeof i == "string" ? document.createTextNode(i) : i;
    const s = t.tipLabel ? t.tipLabel : "Toggle full-screen";
    this.button_ = document.createElement("button"), this.button_.title = s, this.button_.setAttribute("type", "button"), this.button_.appendChild(this.labelNode_), this.button_.addEventListener(
      U.CLICK,
      this.handleClick_.bind(this),
      !1
    ), this.setClassName_(this.button_, this.isInFullscreen_), this.element.className = `${this.cssClassName_} ${ss} ${Ao}`, this.element.appendChild(this.button_);
  }
  handleClick_(t) {
    t.preventDefault(), this.handleFullScreen_();
  }
  handleFullScreen_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = t.getOwnerDocument();
    if (!!wc(e))
      if (Sc(e))
        j_(e);
      else {
        let i;
        this.source_ ? i = typeof this.source_ == "string" ? e.getElementById(this.source_) : this.source_ : i = t.getTargetElement(), this.keys_ ? Y_(i) : rf(i);
      }
  }
  handleFullScreenChange_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = this.isInFullscreen_;
    this.isInFullscreen_ = Sc(t.getOwnerDocument()), e !== this.isInFullscreen_ && (this.setClassName_(this.button_, this.isInFullscreen_), this.isInFullscreen_ ? (io(this.labelActiveNode_, this.labelNode_), this.dispatchEvent(Ec.ENTERFULLSCREEN)) : (io(this.labelNode_, this.labelActiveNode_), this.dispatchEvent(Ec.LEAVEFULLSCREEN)), t.updateSize());
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
    for (let i = 0, s = t.length; i < s; ++i)
      mt(t[i]);
    t.length = 0;
    const e = this.getMap();
    if (e) {
      const i = e.getOwnerDocument();
      wc(i) ? this.element.classList.remove(Vh) : this.element.classList.add(Vh);
      for (let s = 0, r = Mc.length; s < r; ++s)
        t.push(
          et(i, Mc[s], this.handleFullScreenChange_, this)
        );
      this.handleFullScreenChange_();
    }
  }
}
function wc(n) {
  const t = n.body;
  return !!(t.webkitRequestFullscreen || t.requestFullscreen && n.fullscreenEnabled);
}
function Sc(n) {
  return !!(n.webkitIsFullScreen || n.fullscreenElement);
}
function rf(n) {
  n.requestFullscreen ? n.requestFullscreen() : n.webkitRequestFullscreen && n.webkitRequestFullscreen();
}
function Y_(n) {
  n.webkitRequestFullscreen ? n.webkitRequestFullscreen() : rf(n);
}
function j_(n) {
  n.exitFullscreen ? n.exitFullscreen() : n.webkitExitFullscreen && n.webkitExitFullscreen();
}
const q_ = X_, ga = "units", K_ = [1, 2, 5], _s = 25.4 / 0.28;
class J_ extends Gt {
  constructor(t) {
    t = t || {};
    const e = document.createElement("div");
    e.style.pointerEvents = "none", super({
      element: e,
      render: t.render,
      target: t.target
    }), this.on, this.once, this.un;
    const i = t.className !== void 0 ? t.className : t.bar ? "ol-scale-bar" : "ol-scale-line";
    this.innerElement_ = document.createElement("div"), this.innerElement_.className = i + "-inner", this.element.className = i + " " + ss, this.element.appendChild(this.innerElement_), this.viewState_ = null, this.minWidth_ = t.minWidth !== void 0 ? t.minWidth : 64, this.maxWidth_ = t.maxWidth, this.renderedVisible_ = !1, this.renderedWidth_ = void 0, this.renderedHTML_ = "", this.addChangeListener(ga, this.handleUnitsChanged_), this.setUnits(t.units || "metric"), this.scaleBar_ = t.bar || !1, this.scaleBarSteps_ = t.steps || 4, this.scaleBarText_ = t.text || !1, this.dpi_ = t.dpi || void 0;
  }
  getUnits() {
    return this.get(ga);
  }
  handleUnitsChanged_() {
    this.updateElement_();
  }
  setUnits(t) {
    this.set(ga, t);
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
    const e = t.center, i = t.projection, s = this.getUnits(), r = s == "degrees" ? "degrees" : "m";
    let o = ao(
      i,
      t.resolution,
      e,
      r
    );
    const a = this.minWidth_ * (this.dpi_ || _s) / _s, l = this.maxWidth_ !== void 0 ? this.maxWidth_ * (this.dpi_ || _s) / _s : void 0;
    let h = a * o, c = "";
    if (s == "degrees") {
      const v = Yn.degrees;
      h *= v, h < v / 60 ? (c = "\u2033", o *= 3600) : h < v ? (c = "\u2032", o *= 60) : c = "\xB0";
    } else
      s == "imperial" ? h < 0.9144 ? (c = "in", o /= 0.0254) : h < 1609.344 ? (c = "ft", o /= 0.3048) : (c = "mi", o /= 1609.344) : s == "nautical" ? (o /= 1852, c = "NM") : s == "metric" ? h < 1e-3 ? (c = "\u03BCm", o *= 1e6) : h < 1 ? (c = "mm", o *= 1e3) : h < 1e3 ? c = "m" : (c = "km", o /= 1e3) : s == "us" ? h < 0.9144 ? (c = "in", o *= 39.37) : h < 1609.344 ? (c = "ft", o /= 0.30480061) : (c = "mi", o /= 1609.3472) : Y(!1, 33);
    let u = 3 * Math.floor(Math.log(a * o) / Math.log(10)), d, f, g, m, _, y;
    for (; ; ) {
      g = Math.floor(u / 3);
      const v = Math.pow(10, g);
      if (d = K_[(u % 3 + 3) % 3] * v, f = Math.round(d / o), isNaN(f)) {
        this.element.style.display = "none", this.renderedVisible_ = !1;
        return;
      }
      if (l !== void 0 && f >= l) {
        d = m, f = _, g = y;
        break;
      } else if (f >= a)
        break;
      m = d, _ = f, y = g, ++u;
    }
    const p = this.scaleBar_ ? this.createScaleBar(f, d, c) : d.toFixed(g < 0 ? -g : 0) + " " + c;
    this.renderedHTML_ != p && (this.innerElement_.innerHTML = p, this.renderedHTML_ = p), this.renderedWidth_ != f && (this.innerElement_.style.width = f + "px", this.renderedWidth_ = f), this.renderedVisible_ || (this.element.style.display = "", this.renderedVisible_ = !0);
  }
  createScaleBar(t, e, i) {
    const s = this.getScaleForResolution(), r = s < 1 ? Math.round(1 / s).toLocaleString() + " : 1" : "1 : " + Math.round(s).toLocaleString(), o = this.scaleBarSteps_, a = t / o, l = [this.createMarker("absolute")];
    for (let c = 0; c < o; ++c) {
      const u = c % 2 === 0 ? "ol-scale-singlebar-odd" : "ol-scale-singlebar-even";
      l.push(
        `<div><div class="ol-scale-singlebar ${u}" style="width: ${a}px;"></div>` + this.createMarker("relative") + (c % 2 === 0 || o === 2 ? this.createStepText(c, t, !1, e, i) : "") + "</div>"
      );
    }
    return l.push(this.createStepText(o, t, !0, e, i)), (this.scaleBarText_ ? `<div class="ol-scale-text" style="width: ${t}px;">` + r + "</div>" : "") + l.join("");
  }
  createMarker(t) {
    return `<div class="ol-scale-step-marker" style="position: ${t}; top: ${t === "absolute" ? 3 : -10}px;"></div>`;
  }
  createStepText(t, e, i, s, r) {
    const a = (t === 0 ? 0 : Math.round(s / this.scaleBarSteps_ * t * 100) / 100) + (t === 0 ? "" : " " + r), l = t === 0 ? -3 : e / this.scaleBarSteps_ * -1, h = t === 0 ? 0 : e / this.scaleBarSteps_ * 2;
    return `<div class="ol-scale-step-text" style="margin-left: ${l}px;text-align: ${t === 0 ? "left" : "center"};min-width: ${h}px;left: ${i ? e + "px" : "unset"};">` + a + "</div>";
  }
  getScaleForResolution() {
    const t = ao(
      this.viewState_.projection,
      this.viewState_.resolution,
      this.viewState_.center,
      "m"
    ), e = this.dpi_ || _s, i = 1e3 / 25.4;
    return t * i * e;
  }
  render(t) {
    const e = t.frameState;
    e ? this.viewState_ = e.viewState : this.viewState_ = null, this.updateElement_();
  }
}
const Q_ = J_;
class Go extends Di {
  constructor(t, e, i) {
    super(), i !== void 0 && e === void 0 ? this.setFlatCoordinates(i, t) : (e = e || 0, this.setCenterAndRadius(t, e, i));
  }
  clone() {
    const t = new Go(
      this.flatCoordinates.slice(),
      void 0,
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    const r = this.flatCoordinates, o = t - r[0], a = e - r[1], l = o * o + a * a;
    if (l < s) {
      if (l === 0)
        for (let h = 0; h < this.stride; ++h)
          i[h] = r[h];
      else {
        const h = this.getRadius() / Math.sqrt(l);
        i[0] = r[0] + h * o, i[1] = r[1] + h * a;
        for (let c = 2; c < this.stride; ++c)
          i[c] = r[c];
      }
      return i.length = this.stride, l;
    } else
      return s;
  }
  containsXY(t, e) {
    const i = this.flatCoordinates, s = t - i[0], r = e - i[1];
    return s * s + r * r <= this.getRadiusSquared_();
  }
  getCenter() {
    return this.flatCoordinates.slice(0, this.stride);
  }
  computeExtent(t) {
    const e = this.flatCoordinates, i = e[this.stride] - e[0];
    return _e(
      e[0] - i,
      e[1] - i,
      e[0] + i,
      e[1] + i,
      t
    );
  }
  getRadius() {
    return Math.sqrt(this.getRadiusSquared_());
  }
  getRadiusSquared_() {
    const t = this.flatCoordinates[this.stride] - this.flatCoordinates[0], e = this.flatCoordinates[this.stride + 1] - this.flatCoordinates[1];
    return t * t + e * e;
  }
  getType() {
    return "Circle";
  }
  intersectsExtent(t) {
    const e = this.getExtent();
    if (Kt(t, e)) {
      const i = this.getCenter();
      return t[0] <= i[0] && t[2] >= i[0] || t[1] <= i[1] && t[3] >= i[1] ? !0 : yl(t, this.intersectsCoordinate.bind(this));
    }
    return !1;
  }
  setCenter(t) {
    const e = this.stride, i = this.flatCoordinates[e] - this.flatCoordinates[0], s = t.slice();
    s[e] = s[0] + i;
    for (let r = 1; r < e; ++r)
      s[e + r] = t[r];
    this.setFlatCoordinates(this.layout, s), this.changed();
  }
  setCenterAndRadius(t, e, i) {
    this.setLayout(i, t, 0), this.flatCoordinates || (this.flatCoordinates = []);
    const s = this.flatCoordinates;
    let r = Cd(s, 0, t, this.stride);
    s[r++] = s[0] + e;
    for (let o = 1, a = this.stride; o < a; ++o)
      s[r++] = s[o];
    s.length = r, this.changed();
  }
  getCoordinates() {
    return null;
  }
  setCoordinates(t, e) {
  }
  setRadius(t) {
    this.flatCoordinates[this.stride] = this.flatCoordinates[0] + t, this.changed();
  }
  rotate(t, e) {
    const i = this.getCenter(), s = this.getStride();
    this.setCenter(
      Fl(i, 0, i.length, s, t, e, i)
    ), this.changed();
  }
  translate(t, e) {
    const i = this.getCenter(), s = this.getStride();
    this.setCenter(
      vd(i, 0, i.length, s, t, e, i)
    ), this.changed();
  }
}
Go.prototype.transform;
const t2 = Go;
class go extends xd {
  constructor(t) {
    super(), this.geometries_ = t || null, this.changeEventsKeys_ = [], this.listenGeometriesChange_();
  }
  unlistenGeometriesChange_() {
    this.changeEventsKeys_.forEach(mt), this.changeEventsKeys_.length = 0;
  }
  listenGeometriesChange_() {
    if (!!this.geometries_)
      for (let t = 0, e = this.geometries_.length; t < e; ++t)
        this.changeEventsKeys_.push(
          et(this.geometries_[t], U.CHANGE, this.changed, this)
        );
  }
  clone() {
    const t = new go(null);
    return t.setGeometries(this.geometries_), t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    if (s < dn(this.getExtent(), t, e))
      return s;
    const r = this.geometries_;
    for (let o = 0, a = r.length; o < a; ++o)
      s = r[o].closestPointXY(
        t,
        e,
        i,
        s
      );
    return s;
  }
  containsXY(t, e) {
    const i = this.geometries_;
    for (let s = 0, r = i.length; s < r; ++s)
      if (i[s].containsXY(t, e))
        return !0;
    return !1;
  }
  computeExtent(t) {
    Qs(t);
    const e = this.geometries_;
    for (let i = 0, s = e.length; i < s; ++i)
      Ku(t, e[i].getExtent());
    return t;
  }
  getGeometries() {
    return Rc(this.geometries_);
  }
  getGeometriesArray() {
    return this.geometries_;
  }
  getGeometriesArrayRecursive() {
    let t = [];
    const e = this.geometries_;
    for (let i = 0, s = e.length; i < s; ++i)
      e[i].getType() === this.getType() ? t = t.concat(
        e[i].getGeometriesArrayRecursive()
      ) : t.push(e[i]);
    return t;
  }
  getSimplifiedGeometry(t) {
    if (this.simplifiedGeometryRevision !== this.getRevision() && (this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = this.getRevision()), t < 0 || this.simplifiedGeometryMaxMinSquaredTolerance !== 0 && t < this.simplifiedGeometryMaxMinSquaredTolerance)
      return this;
    const e = [], i = this.geometries_;
    let s = !1;
    for (let r = 0, o = i.length; r < o; ++r) {
      const a = i[r], l = a.getSimplifiedGeometry(t);
      e.push(l), l !== a && (s = !0);
    }
    if (s) {
      const r = new go(null);
      return r.setGeometriesArray(e), r;
    } else
      return this.simplifiedGeometryMaxMinSquaredTolerance = t, this;
  }
  getType() {
    return "GeometryCollection";
  }
  intersectsExtent(t) {
    const e = this.geometries_;
    for (let i = 0, s = e.length; i < s; ++i)
      if (e[i].intersectsExtent(t))
        return !0;
    return !1;
  }
  isEmpty() {
    return this.geometries_.length === 0;
  }
  rotate(t, e) {
    const i = this.geometries_;
    for (let s = 0, r = i.length; s < r; ++s)
      i[s].rotate(t, e);
    this.changed();
  }
  scale(t, e, i) {
    i || (i = Pi(this.getExtent()));
    const s = this.geometries_;
    for (let r = 0, o = s.length; r < o; ++r)
      s[r].scale(t, e, i);
    this.changed();
  }
  setGeometries(t) {
    this.setGeometriesArray(Rc(t));
  }
  setGeometriesArray(t) {
    this.unlistenGeometriesChange_(), this.geometries_ = t, this.listenGeometriesChange_(), this.changed();
  }
  applyTransform(t) {
    const e = this.geometries_;
    for (let i = 0, s = e.length; i < s; ++i)
      e[i].applyTransform(t);
    this.changed();
  }
  translate(t, e) {
    const i = this.geometries_;
    for (let s = 0, r = i.length; s < r; ++s)
      i[s].translate(t, e);
    this.changed();
  }
  disposeInternal() {
    this.unlistenGeometriesChange_(), super.disposeInternal();
  }
}
function Rc(n) {
  const t = [];
  for (let e = 0, i = n.length; e < i; ++e)
    t.push(n[e].clone());
  return t;
}
const of = go;
class mo extends Di {
  constructor(t, e, i) {
    if (super(), this.ends_ = [], this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, Array.isArray(t[0]))
      this.setCoordinates(
        t,
        e
      );
    else if (e !== void 0 && i)
      this.setFlatCoordinates(
        e,
        t
      ), this.ends_ = i;
    else {
      let s = this.getLayout();
      const r = t, o = [], a = [];
      for (let l = 0, h = r.length; l < h; ++l) {
        const c = r[l];
        l === 0 && (s = c.getLayout()), Qt(o, c.getFlatCoordinates()), a.push(o.length);
      }
      this.setFlatCoordinates(s, o), this.ends_ = a;
    }
  }
  appendLineString(t) {
    this.flatCoordinates ? Qt(this.flatCoordinates, t.getFlatCoordinates().slice()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new mo(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    return s < dn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Dl(
        this.flatCoordinates,
        0,
        this.ends_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), Gl(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      this.maxDelta_,
      !1,
      t,
      e,
      i,
      s
    ));
  }
  getCoordinateAtM(t, e, i) {
    return this.layout != "XYM" && this.layout != "XYZM" || this.flatCoordinates.length === 0 ? null : (e = e !== void 0 ? e : !1, i = i !== void 0 ? i : !1, Tm(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t,
      e,
      i
    ));
  }
  getCoordinates() {
    return Zs(
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
    return t < 0 || this.ends_.length <= t ? null : new li(
      this.flatCoordinates.slice(
        t === 0 ? 0 : this.ends_[t - 1],
        this.ends_[t]
      ),
      this.layout
    );
  }
  getLineStrings() {
    const t = this.flatCoordinates, e = this.ends_, i = this.layout, s = [];
    let r = 0;
    for (let o = 0, a = e.length; o < a; ++o) {
      const l = e[o], h = new li(
        t.slice(r, l),
        i
      );
      s.push(h), r = l;
    }
    return s;
  }
  getFlatMidpoints() {
    const t = [], e = this.flatCoordinates;
    let i = 0;
    const s = this.ends_, r = this.stride;
    for (let o = 0, a = s.length; o < a; ++o) {
      const l = s[o], h = $d(
        e,
        i,
        l,
        r,
        0.5
      );
      Qt(t, h), i = l;
    }
    return t;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], i = [];
    return e.length = g1(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t,
      e,
      0,
      i
    ), new mo(e, "XY", i);
  }
  getType() {
    return "MultiLineString";
  }
  intersectsExtent(t) {
    return C1(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 2), this.flatCoordinates || (this.flatCoordinates = []);
    const i = $l(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.ends_
    );
    this.flatCoordinates.length = i.length === 0 ? 0 : i[i.length - 1], this.changed();
  }
}
const sr = mo;
class th extends Di {
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
    this.flatCoordinates ? Qt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.changed();
  }
  clone() {
    const t = new th(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, i, s) {
    if (s < dn(this.getExtent(), t, e))
      return s;
    const r = this.flatCoordinates, o = this.stride;
    for (let a = 0, l = r.length; a < l; a += o) {
      const h = ri(
        t,
        e,
        r[a],
        r[a + 1]
      );
      if (h < s) {
        s = h;
        for (let c = 0; c < o; ++c)
          i[c] = r[a + c];
        i.length = o;
      }
    }
    return s;
  }
  getCoordinates() {
    return Ei(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getPoint(t) {
    const e = this.flatCoordinates ? this.flatCoordinates.length / this.stride : 0;
    return t < 0 || e <= t ? null : new Se(
      this.flatCoordinates.slice(
        t * this.stride,
        (t + 1) * this.stride
      ),
      this.layout
    );
  }
  getPoints() {
    const t = this.flatCoordinates, e = this.layout, i = this.stride, s = [];
    for (let r = 0, o = t.length; r < o; r += i) {
      const a = new Se(t.slice(r, r + i), e);
      s.push(a);
    }
    return s;
  }
  getType() {
    return "MultiPoint";
  }
  intersectsExtent(t) {
    const e = this.flatCoordinates, i = this.stride;
    for (let s = 0, r = e.length; s < r; s += i) {
      const o = e[s], a = e[s + 1];
      if (pl(t, o, a))
        return !0;
    }
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = No(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const $o = th;
function e2(n, t, e, i) {
  const s = [];
  let r = se();
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = qu(
      n,
      t,
      l[0],
      i
    ), s.push((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), t = l[l.length - 1];
  }
  return s;
}
class _o extends Di {
  constructor(t, e, i) {
    if (super(), this.endss_ = [], this.flatInteriorPointsRevision_ = -1, this.flatInteriorPoints_ = null, this.maxDelta_ = -1, this.maxDeltaRevision_ = -1, this.orientedRevision_ = -1, this.orientedFlatCoordinates_ = null, !i && !Array.isArray(t[0])) {
      let s = this.getLayout();
      const r = t, o = [], a = [];
      for (let l = 0, h = r.length; l < h; ++l) {
        const c = r[l];
        l === 0 && (s = c.getLayout());
        const u = o.length, d = c.getEnds();
        for (let f = 0, g = d.length; f < g; ++f)
          d[f] += u;
        Qt(o, c.getFlatCoordinates()), a.push(d);
      }
      e = s, t = o, i = a;
    }
    e !== void 0 && i ? (this.setFlatCoordinates(
      e,
      t
    ), this.endss_ = i) : this.setCoordinates(
      t,
      e
    );
  }
  appendPolygon(t) {
    let e;
    if (!this.flatCoordinates)
      this.flatCoordinates = t.getFlatCoordinates().slice(), e = t.getEnds().slice(), this.endss_.push();
    else {
      const i = this.flatCoordinates.length;
      Qt(this.flatCoordinates, t.getFlatCoordinates()), e = t.getEnds().slice();
      for (let s = 0, r = e.length; s < r; ++s)
        e[s] += i;
    }
    this.endss_.push(e), this.changed();
  }
  clone() {
    const t = this.endss_.length, e = new Array(t);
    for (let s = 0; s < t; ++s)
      e[s] = this.endss_[s].slice();
    const i = new _o(
      this.flatCoordinates.slice(),
      this.layout,
      e
    );
    return i.applyProperties(this), i;
  }
  closestPointXY(t, e, i, s) {
    return s < dn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      u1(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), d1(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      this.maxDelta_,
      !0,
      t,
      e,
      i,
      s
    ));
  }
  containsXY(t, e) {
    return v1(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return p1(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), sc(
      e,
      0,
      this.endss_,
      this.stride,
      t
    )) : e = this.flatCoordinates, $a(
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
      const t = e2(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride
      );
      this.flatInteriorPoints_ = x1(
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
    return new $o(this.getFlatInteriorPoints().slice(), "XYM");
  }
  getOrientedFlatCoordinates() {
    if (this.orientedRevision_ != this.getRevision()) {
      const t = this.flatCoordinates;
      w1(t, 0, this.endss_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = sc(
        this.orientedFlatCoordinates_,
        0,
        this.endss_,
        this.stride
      )), this.orientedRevision_ = this.getRevision();
    }
    return this.orientedFlatCoordinates_;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], i = [];
    return e.length = _1(
      this.flatCoordinates,
      0,
      this.endss_,
      this.stride,
      Math.sqrt(t),
      e,
      0,
      i
    ), new _o(e, "XY", i);
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
    const i = this.endss_[t].slice(), s = i[i.length - 1];
    if (e !== 0)
      for (let r = 0, o = i.length; r < o; ++r)
        i[r] -= e;
    return new Ai(
      this.flatCoordinates.slice(e, s),
      this.layout,
      i
    );
  }
  getPolygons() {
    const t = this.layout, e = this.flatCoordinates, i = this.endss_, s = [];
    let r = 0;
    for (let o = 0, a = i.length; o < a; ++o) {
      const l = i[o].slice(), h = l[l.length - 1];
      if (r !== 0)
        for (let u = 0, d = l.length; u < d; ++u)
          l[u] -= r;
      const c = new Ai(
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
    return M1(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 3), this.flatCoordinates || (this.flatCoordinates = []);
    const i = f1(
      this.flatCoordinates,
      0,
      t,
      this.stride,
      this.endss_
    );
    if (i.length === 0)
      this.flatCoordinates.length = 0;
    else {
      const s = i[i.length - 1];
      this.flatCoordinates.length = s.length === 0 ? 0 : s[s.length - 1];
    }
    this.changed();
  }
}
const rr = _o, Or = {
  DRAWSTART: "drawstart",
  DRAWEND: "drawend",
  DRAWABORT: "drawabort"
};
class Fr extends Re {
  constructor(t, e) {
    super(t), this.feature = e;
  }
}
function i2(n, t) {
  const e = [];
  for (let i = 0; i < t.length; ++i) {
    const r = t[i].getGeometry();
    af(n, r, e);
  }
  return e;
}
function Nr(n, t) {
  return ri(n[0], n[1], t[0], t[1]);
}
function An(n, t) {
  const e = n.length;
  return t < 0 ? n[t + e] : t >= e ? n[t - e] : n[t];
}
function Dr(n, t, e) {
  let i, s;
  t < e ? (i = t, s = e) : (i = e, s = t);
  const r = Math.ceil(i), o = Math.floor(s);
  if (r > o) {
    const l = On(n, i), h = On(n, s);
    return Nr(l, h);
  }
  let a = 0;
  if (i < r) {
    const l = On(n, i), h = An(n, r);
    a += Nr(l, h);
  }
  if (o < s) {
    const l = An(n, o), h = On(n, s);
    a += Nr(l, h);
  }
  for (let l = r; l < o - 1; ++l) {
    const h = An(n, l), c = An(n, l + 1);
    a += Nr(h, c);
  }
  return a;
}
function af(n, t, e) {
  if (t instanceof li) {
    kr(n, t.getCoordinates(), !1, e);
    return;
  }
  if (t instanceof sr) {
    const i = t.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s)
      kr(n, i[s], !1, e);
    return;
  }
  if (t instanceof Ai) {
    const i = t.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s)
      kr(n, i[s], !0, e);
    return;
  }
  if (t instanceof rr) {
    const i = t.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length; a < l; ++a)
        kr(n, o[a], !0, e);
    }
    return;
  }
  if (t instanceof of) {
    const i = t.getGeometries();
    for (let s = 0; s < i.length; ++s)
      af(n, i[s], e);
    return;
  }
}
const ma = { index: -1, endIndex: NaN };
function n2(n, t, e, i) {
  const s = n[0], r = n[1];
  let o = 1 / 0, a = -1, l = NaN;
  for (let u = 0; u < t.targets.length; ++u) {
    const d = t.targets[u], f = d.coordinates;
    let g = 1 / 0, m;
    for (let _ = 0; _ < f.length - 1; ++_) {
      const y = f[_], p = f[_ + 1], v = lf(s, r, y, p);
      v.squaredDistance < g && (g = v.squaredDistance, m = _ + v.along);
    }
    g < o && (o = g, d.ring && t.targetIndex === u && (d.endIndex > d.startIndex ? m < d.startIndex && (m += f.length) : d.endIndex < d.startIndex && m > d.startIndex && (m -= f.length)), l = m, a = u);
  }
  const h = t.targets[a];
  let c = h.ring;
  if (t.targetIndex === a && c) {
    const u = On(
      h.coordinates,
      l
    ), d = e.getPixelFromCoordinate(u);
    eo(d, t.startPx) > i && (c = !1);
  }
  if (c) {
    const u = h.coordinates, d = u.length, f = h.startIndex, g = l;
    if (f < g) {
      const m = Dr(
        u,
        f,
        g
      );
      Dr(
        u,
        f,
        g - d
      ) < m && (l -= d);
    } else {
      const m = Dr(
        u,
        f,
        g
      );
      Dr(
        u,
        f,
        g + d
      ) < m && (l += d);
    }
  }
  return ma.index = a, ma.endIndex = l, ma;
}
function kr(n, t, e, i) {
  const s = n[0], r = n[1];
  for (let o = 0, a = t.length - 1; o < a; ++o) {
    const l = t[o], h = t[o + 1], c = lf(s, r, l, h);
    if (c.squaredDistance === 0) {
      const u = o + c.along;
      i.push({
        coordinates: t,
        ring: e,
        startIndex: u,
        endIndex: u
      });
      return;
    }
  }
}
const _a = { along: 0, squaredDistance: 0 };
function lf(n, t, e, i) {
  const s = e[0], r = e[1], o = i[0], a = i[1], l = o - s, h = a - r;
  let c = 0, u = s, d = r;
  return (l !== 0 || h !== 0) && (c = Et(((n - s) * l + (t - r) * h) / (l * l + h * h), 0, 1), u += l * c, d += h * c), _a.along = c, _a.squaredDistance = xl(ri(n, t, u, d), 10), _a;
}
function On(n, t) {
  const e = n.length;
  let i = Math.floor(t);
  const s = t - i;
  i >= e ? i -= e : i < 0 && (i += e);
  let r = i + 1;
  r >= e && (r -= e);
  const o = n[i], a = o[0], l = o[1], h = n[r], c = h[0] - a, u = h[1] - l;
  return [a + c * s, l + u * s];
}
class s2 extends ki {
  constructor(t) {
    const e = t;
    e.stopDown || (e.stopDown = un), super(e), this.on, this.once, this.un, this.shouldHandle_ = !1, this.downPx_ = null, this.downTimeout_, this.lastDragTime_, this.pointerType_, this.freehand_ = !1, this.source_ = t.source ? t.source : null, this.features_ = t.features ? t.features : null, this.snapTolerance_ = t.snapTolerance ? t.snapTolerance : 12, this.type_ = t.type, this.mode_ = o2(this.type_), this.stopClick_ = !!t.stopClick, this.minPoints_ = t.minPoints ? t.minPoints : this.mode_ === "Polygon" ? 3 : 2, this.maxPoints_ = this.mode_ === "Circle" ? 2 : t.maxPoints ? t.maxPoints : 1 / 0, this.finishCondition_ = t.finishCondition ? t.finishCondition : en, this.geometryLayout_ = t.geometryLayout ? t.geometryLayout : "XY";
    let i = t.geometryFunction;
    if (!i) {
      const s = this.mode_;
      if (s === "Circle")
        i = function(r, o, a) {
          const l = o || new t2([NaN, NaN]), h = vt(r[0]), c = oi(
            h,
            vt(r[r.length - 1])
          );
          return l.setCenterAndRadius(
            h,
            Math.sqrt(c),
            this.geometryLayout_
          ), l;
        };
      else {
        let r;
        s === "Point" ? r = Se : s === "LineString" ? r = li : s === "Polygon" && (r = Ai), i = function(o, a, l) {
          return a ? s === "Polygon" ? o[0].length ? a.setCoordinates(
            [o[0].concat([o[0][0]])],
            this.geometryLayout_
          ) : a.setCoordinates([], this.geometryLayout_) : a.setCoordinates(o, this.geometryLayout_) : a = new r(o, this.geometryLayout_), a;
        };
      }
    }
    this.geometryFunction_ = i, this.dragVertexDelay_ = t.dragVertexDelay !== void 0 ? t.dragVertexDelay : 500, this.finishCoordinate_ = null, this.sketchFeature_ = null, this.sketchPoint_ = null, this.sketchCoords_ = null, this.sketchLine_ = null, this.sketchLineCoords_ = null, this.squaredClickTolerance_ = t.clickTolerance ? t.clickTolerance * t.clickTolerance : 36, this.overlay_ = new Ze({
      source: new Ve({
        useSpatialIndex: !1,
        wrapX: t.wrapX ? t.wrapX : !1
      }),
      style: t.style ? t.style : r2(),
      updateWhileInteracting: !0
    }), this.geometryName_ = t.geometryName, this.condition_ = t.condition ? t.condition : Wl, this.freehandCondition_, t.freehand ? this.freehandCondition_ = co : this.freehandCondition_ = t.freehandCondition ? t.freehandCondition : Fd, this.traceCondition_, this.setTrace(t.trace || !1), this.traceState_ = { active: !1 }, this.traceSource_ = t.traceSource || t.source || null, this.addChangeListener(Za.ACTIVE, this.updateState_);
  }
  setTrace(t) {
    let e;
    t ? t === !0 ? e = co : e = t : e = Y1, this.traceCondition_ = e;
  }
  setMap(t) {
    super.setMap(t), this.updateState_();
  }
  getOverlay() {
    return this.overlay_;
  }
  handleEvent(t) {
    t.originalEvent.type === U.CONTEXTMENU && t.originalEvent.preventDefault(), this.freehand_ = this.mode_ !== "Point" && this.freehandCondition_(t);
    let e = t.type === nt.POINTERMOVE, i = !0;
    return !this.freehand_ && this.lastDragTime_ && t.type === nt.POINTERDRAG && (Date.now() - this.lastDragTime_ >= this.dragVertexDelay_ ? (this.downPx_ = t.pixel, this.shouldHandle_ = !this.freehand_, e = !0) : this.lastDragTime_ = void 0, this.shouldHandle_ && this.downTimeout_ !== void 0 && (clearTimeout(this.downTimeout_), this.downTimeout_ = void 0)), this.freehand_ && t.type === nt.POINTERDRAG && this.sketchFeature_ !== null ? (this.addToDrawing_(t.coordinate), i = !1) : this.freehand_ && t.type === nt.POINTERDOWN ? i = !1 : e && this.getPointerCount() < 2 ? (i = t.type === nt.POINTERMOVE, i && this.freehand_ ? (this.handlePointerMove_(t), this.shouldHandle_ && t.originalEvent.preventDefault()) : (t.originalEvent.pointerType === "mouse" || t.type === nt.POINTERDRAG && this.downTimeout_ === void 0) && this.handlePointerMove_(t)) : t.type === nt.DBLCLICK && (i = !1), super.handleEvent(t) && i;
  }
  handleDownEvent(t) {
    return this.shouldHandle_ = !this.freehand_, this.freehand_ ? (this.downPx_ = t.pixel, this.finishCoordinate_ || this.startDrawing_(t.coordinate), !0) : this.condition_(t) ? (this.lastDragTime_ = Date.now(), this.downTimeout_ = setTimeout(
      function() {
        this.handlePointerMove_(
          new ei(
            nt.POINTERMOVE,
            t.map,
            t.originalEvent,
            !1,
            t.frameState
          )
        );
      }.bind(this),
      this.dragVertexDelay_
    ), this.downPx_ = t.pixel, !0) : (this.lastDragTime_ = void 0, !1);
  }
  deactivateTrace_() {
    this.traceState_ = { active: !1 };
  }
  toggleTraceState_(t) {
    if (!this.traceSource_ || !this.traceCondition_(t))
      return;
    if (this.traceState_.active) {
      this.deactivateTrace_();
      return;
    }
    const e = this.getMap(), i = e.getCoordinateFromPixel([
      t.pixel[0] - this.snapTolerance_,
      t.pixel[1] + this.snapTolerance_
    ]), s = e.getCoordinateFromPixel([
      t.pixel[0] + this.snapTolerance_,
      t.pixel[1] - this.snapTolerance_
    ]), r = Ut([i, s]), o = this.traceSource_.getFeaturesInExtent(r);
    if (o.length === 0)
      return;
    const a = i2(t.coordinate, o);
    a.length && (this.traceState_ = {
      active: !0,
      startPx: t.pixel.slice(),
      targets: a,
      targetIndex: -1
    });
  }
  addOrRemoveTracedCoordinates_(t, e) {
    const i = t.startIndex <= t.endIndex, s = t.startIndex <= e;
    i === s ? i && e > t.endIndex || !i && e < t.endIndex ? this.addTracedCoordinates_(t, t.endIndex, e) : (i && e < t.endIndex || !i && e > t.endIndex) && this.removeTracedCoordinates_(e, t.endIndex) : (this.removeTracedCoordinates_(t.startIndex, t.endIndex), this.addTracedCoordinates_(t, t.startIndex, e));
  }
  removeTracedCoordinates_(t, e) {
    if (t === e)
      return;
    let i = 0;
    if (t < e) {
      const s = Math.ceil(t);
      let r = Math.floor(e);
      r === e && (r -= 1), i = r - s + 1;
    } else {
      const s = Math.floor(t);
      let r = Math.ceil(e);
      r === e && (r += 1), i = s - r + 1;
    }
    i > 0 && this.removeLastPoints_(i);
  }
  addTracedCoordinates_(t, e, i) {
    if (e === i)
      return;
    const s = [];
    if (e < i) {
      const r = Math.ceil(e);
      let o = Math.floor(i);
      o === i && (o -= 1);
      for (let a = r; a <= o; ++a)
        s.push(An(t.coordinates, a));
    } else {
      const r = Math.floor(e);
      let o = Math.ceil(i);
      o === i && (o += 1);
      for (let a = r; a >= o; --a)
        s.push(An(t.coordinates, a));
    }
    s.length && this.appendCoordinates(s);
  }
  updateTrace_(t) {
    const e = this.traceState_;
    if (!e.active || e.targetIndex === -1 && eo(e.startPx, t.pixel) < this.snapTolerance_)
      return;
    const i = n2(
      t.coordinate,
      e,
      this.getMap(),
      this.snapTolerance_
    );
    if (e.targetIndex !== i.index) {
      if (e.targetIndex !== -1) {
        const l = e.targets[e.targetIndex];
        this.removeTracedCoordinates_(l.startIndex, l.endIndex);
      }
      const a = e.targets[i.index];
      this.addTracedCoordinates_(
        a,
        a.startIndex,
        i.endIndex
      );
    } else {
      const a = e.targets[e.targetIndex];
      this.addOrRemoveTracedCoordinates_(a, i.endIndex);
    }
    e.targetIndex = i.index;
    const s = e.targets[e.targetIndex];
    s.endIndex = i.endIndex;
    const r = On(
      s.coordinates,
      s.endIndex
    ), o = this.getMap().getPixelFromCoordinate(r);
    t.coordinate = r, t.pixel = [Math.round(o[0]), Math.round(o[1])];
  }
  handleUpEvent(t) {
    let e = !0;
    if (this.getPointerCount() === 0) {
      this.downTimeout_ && (clearTimeout(this.downTimeout_), this.downTimeout_ = void 0), this.handlePointerMove_(t);
      const i = this.traceState_.active;
      if (this.toggleTraceState_(t), this.shouldHandle_) {
        const s = !this.finishCoordinate_;
        s && this.startDrawing_(t.coordinate), !s && this.freehand_ ? this.finishDrawing() : !this.freehand_ && (!s || this.mode_ === "Point") && (this.atFinish_(t.pixel, i) ? this.finishCondition_(t) && this.finishDrawing() : this.addToDrawing_(t.coordinate)), e = !1;
      } else
        this.freehand_ && this.abortDrawing();
    }
    return !e && this.stopClick_ && t.preventDefault(), e;
  }
  handlePointerMove_(t) {
    if (this.pointerType_ = t.originalEvent.pointerType, this.downPx_ && (!this.freehand_ && this.shouldHandle_ || this.freehand_ && !this.shouldHandle_)) {
      const e = this.downPx_, i = t.pixel, s = e[0] - i[0], r = e[1] - i[1], o = s * s + r * r;
      if (this.shouldHandle_ = this.freehand_ ? o > this.squaredClickTolerance_ : o <= this.squaredClickTolerance_, !this.shouldHandle_)
        return;
    }
    if (!this.finishCoordinate_) {
      this.createOrUpdateSketchPoint_(t.coordinate.slice());
      return;
    }
    this.updateTrace_(t), this.modifyDrawing_(t.coordinate);
  }
  atFinish_(t, e) {
    let i = !1;
    if (this.sketchFeature_) {
      let s = !1, r = [this.finishCoordinate_];
      const o = this.mode_;
      if (o === "Point")
        i = !0;
      else if (o === "Circle")
        i = this.sketchCoords_.length === 2;
      else if (o === "LineString")
        s = !e && this.sketchCoords_.length > this.minPoints_;
      else if (o === "Polygon") {
        const a = this.sketchCoords_;
        s = a[0].length > this.minPoints_, r = [
          a[0][0],
          a[0][a[0].length - 2]
        ], e ? r = [a[0][0]] : r = [
          a[0][0],
          a[0][a[0].length - 2]
        ];
      }
      if (s) {
        const a = this.getMap();
        for (let l = 0, h = r.length; l < h; l++) {
          const c = r[l], u = a.getPixelFromCoordinate(c), d = t[0] - u[0], f = t[1] - u[1], g = this.freehand_ ? 1 : this.snapTolerance_;
          if (i = Math.sqrt(d * d + f * f) <= g, i) {
            this.finishCoordinate_ = c;
            break;
          }
        }
      }
    }
    return i;
  }
  createOrUpdateSketchPoint_(t) {
    this.sketchPoint_ ? this.sketchPoint_.getGeometry().setCoordinates(t) : (this.sketchPoint_ = new Ie(new Se(t)), this.updateSketchFeatures_());
  }
  createOrUpdateCustomSketchLine_(t) {
    this.sketchLine_ || (this.sketchLine_ = new Ie());
    const e = t.getLinearRing(0);
    let i = this.sketchLine_.getGeometry();
    i ? (i.setFlatCoordinates(
      e.getLayout(),
      e.getFlatCoordinates()
    ), i.changed()) : (i = new li(
      e.getFlatCoordinates(),
      e.getLayout()
    ), this.sketchLine_.setGeometry(i));
  }
  startDrawing_(t) {
    const e = this.getMap().getView().getProjection(), i = lo(this.geometryLayout_);
    for (; t.length < i; )
      t.push(0);
    this.finishCoordinate_ = t, this.mode_ === "Point" ? this.sketchCoords_ = t.slice() : this.mode_ === "Polygon" ? (this.sketchCoords_ = [[t.slice(), t.slice()]], this.sketchLineCoords_ = this.sketchCoords_[0]) : this.sketchCoords_ = [t.slice(), t.slice()], this.sketchLineCoords_ && (this.sketchLine_ = new Ie(new li(this.sketchLineCoords_)));
    const s = this.geometryFunction_(
      this.sketchCoords_,
      void 0,
      e
    );
    this.sketchFeature_ = new Ie(), this.geometryName_ && this.sketchFeature_.setGeometryName(this.geometryName_), this.sketchFeature_.setGeometry(s), this.updateSketchFeatures_(), this.dispatchEvent(
      new Fr(Or.DRAWSTART, this.sketchFeature_)
    );
  }
  modifyDrawing_(t) {
    const e = this.getMap(), i = this.sketchFeature_.getGeometry(), s = e.getView().getProjection(), r = lo(this.geometryLayout_);
    let o, a;
    for (; t.length < r; )
      t.push(0);
    this.mode_ === "Point" ? a = this.sketchCoords_ : this.mode_ === "Polygon" ? (o = this.sketchCoords_[0], a = o[o.length - 1], this.atFinish_(e.getPixelFromCoordinate(t)) && (t = this.finishCoordinate_.slice())) : (o = this.sketchCoords_, a = o[o.length - 1]), a[0] = t[0], a[1] = t[1], this.geometryFunction_(
      this.sketchCoords_,
      i,
      s
    ), this.sketchPoint_ && this.sketchPoint_.getGeometry().setCoordinates(t), i.getType() === "Polygon" && this.mode_ !== "Polygon" ? this.createOrUpdateCustomSketchLine_(i) : this.sketchLineCoords_ && this.sketchLine_.getGeometry().setCoordinates(this.sketchLineCoords_), this.updateSketchFeatures_();
  }
  addToDrawing_(t) {
    const e = this.sketchFeature_.getGeometry(), i = this.getMap().getView().getProjection();
    let s, r;
    const o = this.mode_;
    o === "LineString" || o === "Circle" ? (this.finishCoordinate_ = t.slice(), r = this.sketchCoords_, r.length >= this.maxPoints_ && (this.freehand_ ? r.pop() : s = !0), r.push(t.slice()), this.geometryFunction_(r, e, i)) : o === "Polygon" && (r = this.sketchCoords_[0], r.length >= this.maxPoints_ && (this.freehand_ ? r.pop() : s = !0), r.push(t.slice()), s && (this.finishCoordinate_ = r[0]), this.geometryFunction_(this.sketchCoords_, e, i)), this.createOrUpdateSketchPoint_(t.slice()), this.updateSketchFeatures_(), s && this.finishDrawing();
  }
  removeLastPoints_(t) {
    if (!this.sketchFeature_)
      return;
    const e = this.sketchFeature_.getGeometry(), i = this.getMap().getView().getProjection(), s = this.mode_;
    for (let r = 0; r < t; ++r) {
      let o;
      if (s === "LineString" || s === "Circle") {
        if (o = this.sketchCoords_, o.splice(-2, 1), o.length >= 2) {
          this.finishCoordinate_ = o[o.length - 2].slice();
          const a = this.finishCoordinate_.slice();
          o[o.length - 1] = a, this.createOrUpdateSketchPoint_(a);
        }
        this.geometryFunction_(o, e, i), e.getType() === "Polygon" && this.sketchLine_ && this.createOrUpdateCustomSketchLine_(
          e
        );
      } else if (s === "Polygon") {
        o = this.sketchCoords_[0], o.splice(-2, 1);
        const a = this.sketchLine_.getGeometry();
        if (o.length >= 2) {
          const l = o[o.length - 2].slice();
          o[o.length - 1] = l, this.createOrUpdateSketchPoint_(l);
        }
        a.setCoordinates(o), this.geometryFunction_(this.sketchCoords_, e, i);
      }
      if (o.length === 1) {
        this.abortDrawing();
        break;
      }
    }
    this.updateSketchFeatures_();
  }
  removeLastPoint() {
    this.removeLastPoints_(1);
  }
  finishDrawing() {
    const t = this.abortDrawing_();
    if (!t)
      return;
    let e = this.sketchCoords_;
    const i = t.getGeometry(), s = this.getMap().getView().getProjection();
    this.mode_ === "LineString" ? (e.pop(), this.geometryFunction_(e, i, s)) : this.mode_ === "Polygon" && (e[0].pop(), this.geometryFunction_(e, i, s), e = i.getCoordinates()), this.type_ === "MultiPoint" ? t.setGeometry(
      new $o([e])
    ) : this.type_ === "MultiLineString" ? t.setGeometry(
      new sr([e])
    ) : this.type_ === "MultiPolygon" && t.setGeometry(
      new rr([e])
    ), this.dispatchEvent(new Fr(Or.DRAWEND, t)), this.features_ && this.features_.push(t), this.source_ && this.source_.addFeature(t);
  }
  abortDrawing_() {
    this.finishCoordinate_ = null;
    const t = this.sketchFeature_;
    return this.sketchFeature_ = null, this.sketchPoint_ = null, this.sketchLine_ = null, this.overlay_.getSource().clear(!0), this.deactivateTrace_(), t;
  }
  abortDrawing() {
    const t = this.abortDrawing_();
    t && this.dispatchEvent(new Fr(Or.DRAWABORT, t));
  }
  appendCoordinates(t) {
    const e = this.mode_, i = !this.sketchFeature_;
    i && this.startDrawing_(t[0]);
    let s;
    if (e === "LineString" || e === "Circle")
      s = this.sketchCoords_;
    else if (e === "Polygon")
      s = this.sketchCoords_ && this.sketchCoords_.length ? this.sketchCoords_[0] : [];
    else
      return;
    i && s.shift(), s.pop();
    for (let o = 0; o < t.length; o++)
      this.addToDrawing_(t[o]);
    const r = t[t.length - 1];
    this.addToDrawing_(r), this.modifyDrawing_(r);
  }
  extend(t) {
    const i = t.getGeometry();
    this.sketchFeature_ = t, this.sketchCoords_ = i.getCoordinates();
    const s = this.sketchCoords_[this.sketchCoords_.length - 1];
    this.finishCoordinate_ = s.slice(), this.sketchCoords_.push(s.slice()), this.sketchPoint_ = new Ie(new Se(s)), this.updateSketchFeatures_(), this.dispatchEvent(
      new Fr(Or.DRAWSTART, this.sketchFeature_)
    );
  }
  updateSketchFeatures_() {
    const t = [];
    this.sketchFeature_ && t.push(this.sketchFeature_), this.sketchLine_ && t.push(this.sketchLine_), this.sketchPoint_ && t.push(this.sketchPoint_);
    const e = this.overlay_.getSource();
    e.clear(!0), e.addFeatures(t);
  }
  updateState_() {
    const t = this.getMap(), e = this.getActive();
    (!t || !e) && this.abortDrawing(), this.overlay_.setMap(e ? t : null);
  }
}
function r2() {
  const n = Vd();
  return function(t, e) {
    return n[t.getGeometry().getType()];
  };
}
function o2(n) {
  switch (n) {
    case "Point":
    case "MultiPoint":
      return "Point";
    case "LineString":
    case "MultiLineString":
      return "LineString";
    case "Polygon":
    case "MultiPolygon":
      return "Polygon";
    case "Circle":
      return "Circle";
    default:
      throw new Error("Invalid type: " + n);
  }
}
const a2 = s2, Tc = 0, Ls = 1, bc = [0, 0, 0, 0], zn = [], pa = {
  MODIFYSTART: "modifystart",
  MODIFYEND: "modifyend"
};
class ya extends Re {
  constructor(t, e, i) {
    super(t), this.features = e, this.mapBrowserEvent = i;
  }
}
class l2 extends ki {
  constructor(t) {
    super(t), this.on, this.once, this.un, this.boundHandleFeatureChange_ = this.handleFeatureChange_.bind(this), this.condition_ = t.condition ? t.condition : Dd, this.defaultDeleteCondition_ = function(i) {
      return W1(i) && j1(i);
    }, this.deleteCondition_ = t.deleteCondition ? t.deleteCondition : this.defaultDeleteCondition_, this.insertVertexCondition_ = t.insertVertexCondition ? t.insertVertexCondition : co, this.vertexFeature_ = null, this.vertexSegments_ = null, this.lastPixel_ = [0, 0], this.ignoreNextSingleClick_ = !1, this.featuresBeingModified_ = null, this.rBush_ = new fo(), this.pixelTolerance_ = t.pixelTolerance !== void 0 ? t.pixelTolerance : 10, this.snappedToVertex_ = !1, this.changingFeature_ = !1, this.dragSegments_ = [], this.overlay_ = new Ze({
      source: new Ve({
        useSpatialIndex: !1,
        wrapX: !!t.wrapX
      }),
      style: t.style ? t.style : c2(),
      updateWhileAnimating: !0,
      updateWhileInteracting: !0
    }), this.SEGMENT_WRITERS_ = {
      Point: this.writePointGeometry_.bind(this),
      LineString: this.writeLineStringGeometry_.bind(this),
      LinearRing: this.writeLineStringGeometry_.bind(this),
      Polygon: this.writePolygonGeometry_.bind(this),
      MultiPoint: this.writeMultiPointGeometry_.bind(this),
      MultiLineString: this.writeMultiLineStringGeometry_.bind(this),
      MultiPolygon: this.writeMultiPolygonGeometry_.bind(this),
      Circle: this.writeCircleGeometry_.bind(this),
      GeometryCollection: this.writeGeometryCollectionGeometry_.bind(this)
    }, this.source_ = null, this.hitDetection_ = null;
    let e;
    if (t.features ? e = t.features : t.source && (this.source_ = t.source, e = new Ee(this.source_.getFeatures()), this.source_.addEventListener(
      jt.ADDFEATURE,
      this.handleSourceAdd_.bind(this)
    ), this.source_.addEventListener(
      jt.REMOVEFEATURE,
      this.handleSourceRemove_.bind(this)
    )), !e)
      throw new Error(
        "The modify interaction requires features, a source or a layer"
      );
    t.hitDetection && (this.hitDetection_ = t.hitDetection), this.features_ = e, this.features_.forEach(this.addFeature_.bind(this)), this.features_.addEventListener(
      Dt.ADD,
      this.handleFeatureAdd_.bind(this)
    ), this.features_.addEventListener(
      Dt.REMOVE,
      this.handleFeatureRemove_.bind(this)
    ), this.lastPointerEvent_ = null, this.delta_ = [0, 0], this.snapToPointer_ = t.snapToPointer === void 0 ? !this.hitDetection_ : t.snapToPointer;
  }
  addFeature_(t) {
    const e = t.getGeometry();
    if (e) {
      const s = this.SEGMENT_WRITERS_[e.getType()];
      s && s(t, e);
    }
    const i = this.getMap();
    i && i.isRendered() && this.getActive() && this.handlePointerAtPixel_(this.lastPixel_, i), t.addEventListener(U.CHANGE, this.boundHandleFeatureChange_);
  }
  willModifyFeatures_(t, e) {
    if (!this.featuresBeingModified_) {
      this.featuresBeingModified_ = new Ee();
      const i = this.featuresBeingModified_.getArray();
      for (let s = 0, r = e.length; s < r; ++s) {
        const o = e[s];
        for (let a = 0, l = o.length; a < l; ++a) {
          const h = o[a].feature;
          h && !i.includes(h) && this.featuresBeingModified_.push(h);
        }
      }
      this.featuresBeingModified_.getLength() === 0 ? this.featuresBeingModified_ = null : this.dispatchEvent(
        new ya(
          pa.MODIFYSTART,
          this.featuresBeingModified_,
          t
        )
      );
    }
  }
  removeFeature_(t) {
    this.removeFeatureSegmentData_(t), this.vertexFeature_ && this.features_.getLength() === 0 && (this.overlay_.getSource().removeFeature(this.vertexFeature_), this.vertexFeature_ = null), t.removeEventListener(
      U.CHANGE,
      this.boundHandleFeatureChange_
    );
  }
  removeFeatureSegmentData_(t) {
    const e = this.rBush_, i = [];
    e.forEach(
      function(s) {
        t === s.feature && i.push(s);
      }
    );
    for (let s = i.length - 1; s >= 0; --s) {
      const r = i[s];
      for (let o = this.dragSegments_.length - 1; o >= 0; --o)
        this.dragSegments_[o][0] === r && this.dragSegments_.splice(o, 1);
      e.remove(r);
    }
  }
  setActive(t) {
    this.vertexFeature_ && !t && (this.overlay_.getSource().removeFeature(this.vertexFeature_), this.vertexFeature_ = null), super.setActive(t);
  }
  setMap(t) {
    this.overlay_.setMap(t), super.setMap(t);
  }
  getOverlay() {
    return this.overlay_;
  }
  handleSourceAdd_(t) {
    t.feature && this.features_.push(t.feature);
  }
  handleSourceRemove_(t) {
    t.feature && this.features_.remove(t.feature);
  }
  handleFeatureAdd_(t) {
    this.addFeature_(t.element);
  }
  handleFeatureChange_(t) {
    if (!this.changingFeature_) {
      const e = t.target;
      this.removeFeature_(e), this.addFeature_(e);
    }
  }
  handleFeatureRemove_(t) {
    this.removeFeature_(t.element);
  }
  writePointGeometry_(t, e) {
    const i = e.getCoordinates(), s = {
      feature: t,
      geometry: e,
      segment: [i, i]
    };
    this.rBush_.insert(e.getExtent(), s);
  }
  writeMultiPointGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s], a = {
        feature: t,
        geometry: e,
        depth: [s],
        index: s,
        segment: [o, o]
      };
      this.rBush_.insert(e.getExtent(), a);
    }
  }
  writeLineStringGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length - 1; s < r; ++s) {
      const o = i.slice(s, s + 2), a = {
        feature: t,
        geometry: e,
        index: s,
        segment: o
      };
      this.rBush_.insert(Ut(o), a);
    }
  }
  writeMultiLineStringGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length - 1; a < l; ++a) {
        const h = o.slice(a, a + 2), c = {
          feature: t,
          geometry: e,
          depth: [s],
          index: a,
          segment: h
        };
        this.rBush_.insert(Ut(h), c);
      }
    }
  }
  writePolygonGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length - 1; a < l; ++a) {
        const h = o.slice(a, a + 2), c = {
          feature: t,
          geometry: e,
          depth: [s],
          index: a,
          segment: h
        };
        this.rBush_.insert(Ut(h), c);
      }
    }
  }
  writeMultiPolygonGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length; a < l; ++a) {
        const h = o[a];
        for (let c = 0, u = h.length - 1; c < u; ++c) {
          const d = h.slice(c, c + 2), f = {
            feature: t,
            geometry: e,
            depth: [a, s],
            index: c,
            segment: d
          };
          this.rBush_.insert(Ut(d), f);
        }
      }
    }
  }
  writeCircleGeometry_(t, e) {
    const i = e.getCenter(), s = {
      feature: t,
      geometry: e,
      index: Tc,
      segment: [i, i]
    }, r = {
      feature: t,
      geometry: e,
      index: Ls,
      segment: [i, i]
    }, o = [s, r];
    s.featureSegments = o, r.featureSegments = o, this.rBush_.insert(ws(i), s);
    let a = e;
    this.rBush_.insert(a.getExtent(), r);
  }
  writeGeometryCollectionGeometry_(t, e) {
    const i = e.getGeometriesArray();
    for (let s = 0; s < i.length; ++s) {
      const r = i[s], o = this.SEGMENT_WRITERS_[r.getType()];
      o(t, r);
    }
  }
  createOrUpdateVertexFeature_(t, e, i) {
    let s = this.vertexFeature_;
    return s ? s.getGeometry().setCoordinates(t) : (s = new Ie(new Se(t)), this.vertexFeature_ = s, this.overlay_.getSource().addFeature(s)), s.set("features", e), s.set("geometries", i), s;
  }
  handleEvent(t) {
    if (!t.originalEvent)
      return !0;
    this.lastPointerEvent_ = t;
    let e;
    return !t.map.getView().getInteracting() && t.type == nt.POINTERMOVE && !this.handlingDownUpSequence && this.handlePointerMove_(t), this.vertexFeature_ && this.deleteCondition_(t) && (t.type != nt.SINGLECLICK || !this.ignoreNextSingleClick_ ? e = this.removePoint() : e = !0), t.type == nt.SINGLECLICK && (this.ignoreNextSingleClick_ = !1), super.handleEvent(t) && !e;
  }
  handleDragEvent(t) {
    this.ignoreNextSingleClick_ = !1, this.willModifyFeatures_(t, this.dragSegments_);
    const e = [
      t.coordinate[0] + this.delta_[0],
      t.coordinate[1] + this.delta_[1]
    ], i = [], s = [];
    for (let r = 0, o = this.dragSegments_.length; r < o; ++r) {
      const a = this.dragSegments_[r], l = a[0], h = l.feature;
      i.includes(h) || i.push(h);
      const c = l.geometry;
      s.includes(c) || s.push(c);
      const u = l.depth;
      let d;
      const f = l.segment, g = a[1];
      for (; e.length < c.getStride(); )
        e.push(f[g][e.length]);
      switch (c.getType()) {
        case "Point":
          d = e, f[0] = e, f[1] = e;
          break;
        case "MultiPoint":
          d = c.getCoordinates(), d[l.index] = e, f[0] = e, f[1] = e;
          break;
        case "LineString":
          d = c.getCoordinates(), d[l.index + g] = e, f[g] = e;
          break;
        case "MultiLineString":
          d = c.getCoordinates(), d[u[0]][l.index + g] = e, f[g] = e;
          break;
        case "Polygon":
          d = c.getCoordinates(), d[u[0]][l.index + g] = e, f[g] = e;
          break;
        case "MultiPolygon":
          d = c.getCoordinates(), d[u[1]][u[0]][l.index + g] = e, f[g] = e;
          break;
        case "Circle":
          if (f[0] = e, f[1] = e, l.index === Tc)
            this.changingFeature_ = !0, c.setCenter(e), this.changingFeature_ = !1;
          else {
            this.changingFeature_ = !0, t.map.getView().getProjection();
            let m = eo(
              vt(c.getCenter()),
              vt(e)
            );
            c.setRadius(m), this.changingFeature_ = !1;
          }
          break;
      }
      d && this.setGeometryCoordinates_(c, d);
    }
    this.createOrUpdateVertexFeature_(e, i, s);
  }
  handleDownEvent(t) {
    if (!this.condition_(t))
      return !1;
    const e = t.coordinate;
    this.handlePointerAtPixel_(t.pixel, t.map, e), this.dragSegments_.length = 0, this.featuresBeingModified_ = null;
    const i = this.vertexFeature_;
    if (i) {
      t.map.getView().getProjection();
      const s = [], r = i.getGeometry().getCoordinates(), o = Ut([r]), a = this.rBush_.getInExtent(o), l = {};
      a.sort(h2);
      for (let h = 0, c = a.length; h < c; ++h) {
        const u = a[h], d = u.segment;
        let f = q(u.geometry);
        const g = u.depth;
        if (g && (f += "-" + g.join("-")), l[f] || (l[f] = new Array(2)), u.geometry.getType() === "Circle" && u.index === Ls) {
          const m = Ic(
            e,
            u
          );
          Le(m, r) && !l[f][0] && (this.dragSegments_.push([u, 0]), l[f][0] = u);
          continue;
        }
        if (Le(d[0], r) && !l[f][0]) {
          this.dragSegments_.push([u, 0]), l[f][0] = u;
          continue;
        }
        if (Le(d[1], r) && !l[f][1]) {
          if (l[f][0] && l[f][0].index === 0) {
            let m = u.geometry.getCoordinates();
            switch (u.geometry.getType()) {
              case "LineString":
              case "MultiLineString":
                continue;
              case "MultiPolygon":
                m = m[g[1]];
              case "Polygon":
                if (u.index !== m[g[0]].length - 2)
                  continue;
                break;
            }
          }
          this.dragSegments_.push([u, 1]), l[f][1] = u;
          continue;
        }
        q(d) in this.vertexSegments_ && !l[f][0] && !l[f][1] && this.insertVertexCondition_(t) && s.push(u);
      }
      s.length && this.willModifyFeatures_(t, [s]);
      for (let h = s.length - 1; h >= 0; --h)
        this.insertVertex_(s[h], r);
    }
    return !!this.vertexFeature_;
  }
  handleUpEvent(t) {
    for (let e = this.dragSegments_.length - 1; e >= 0; --e) {
      const i = this.dragSegments_[e][0], s = i.geometry;
      if (s.getType() === "Circle") {
        const r = s.getCenter(), o = i.featureSegments[0], a = i.featureSegments[1];
        o.segment[0] = r, o.segment[1] = r, a.segment[0] = r, a.segment[1] = r, this.rBush_.update(ws(r), o);
        let l = s;
        this.rBush_.update(
          l.getExtent(),
          a
        );
      } else
        this.rBush_.update(Ut(i.segment), i);
    }
    return this.featuresBeingModified_ && (this.dispatchEvent(
      new ya(
        pa.MODIFYEND,
        this.featuresBeingModified_,
        t
      )
    ), this.featuresBeingModified_ = null), !1;
  }
  handlePointerMove_(t) {
    this.lastPixel_ = t.pixel, this.handlePointerAtPixel_(t.pixel, t.map, t.coordinate);
  }
  handlePointerAtPixel_(t, e, i) {
    const s = i || e.getCoordinateFromPixel(t);
    e.getView().getProjection();
    const r = function(l, h) {
      return Lc(s, l) - Lc(s, h);
    };
    let o, a;
    if (this.hitDetection_) {
      const l = typeof this.hitDetection_ == "object" ? (h) => h === this.hitDetection_ : void 0;
      e.forEachFeatureAtPixel(
        t,
        (h, c, u) => {
          if (u = u || h.getGeometry(), u.getType() === "Point" && this.features_.getArray().includes(h)) {
            a = u;
            const d = u.getFlatCoordinates().slice(0, 2);
            o = [
              {
                feature: h,
                geometry: u,
                segment: [d, d]
              }
            ];
          }
          return !0;
        },
        { layerFilter: l }
      );
    }
    if (!o) {
      const l = Mi(
        ws(s, bc)
      ), h = e.getView().getResolution() * this.pixelTolerance_, c = Il(
        Js(l, h, bc)
      );
      o = this.rBush_.getInExtent(c);
    }
    if (o && o.length > 0) {
      const l = o.sort(r)[0], h = l.segment;
      let c = Ic(s, l);
      const u = e.getPixelFromCoordinate(c);
      let d = eo(t, u);
      if (a || d <= this.pixelTolerance_) {
        const f = {};
        if (f[q(h)] = !0, this.snapToPointer_ || (this.delta_[0] = c[0] - s[0], this.delta_[1] = c[1] - s[1]), l.geometry.getType() === "Circle" && l.index === Ls)
          this.snappedToVertex_ = !0, this.createOrUpdateVertexFeature_(
            c,
            [l.feature],
            [l.geometry]
          );
        else {
          const g = e.getPixelFromCoordinate(h[0]), m = e.getPixelFromCoordinate(h[1]), _ = oi(u, g), y = oi(u, m);
          d = Math.sqrt(Math.min(_, y)), this.snappedToVertex_ = d <= this.pixelTolerance_, this.snappedToVertex_ && (c = _ > y ? h[1] : h[0]), this.createOrUpdateVertexFeature_(
            c,
            [l.feature],
            [l.geometry]
          );
          const p = {};
          p[q(l.geometry)] = !0;
          for (let v = 1, x = o.length; v < x; ++v) {
            const C = o[v].segment;
            if (Le(h[0], C[0]) && Le(h[1], C[1]) || Le(h[0], C[1]) && Le(h[1], C[0])) {
              const E = q(o[v].geometry);
              E in p || (p[E] = !0, f[q(C)] = !0);
            } else
              break;
          }
        }
        this.vertexSegments_ = f;
        return;
      }
    }
    this.vertexFeature_ && (this.overlay_.getSource().removeFeature(this.vertexFeature_), this.vertexFeature_ = null);
  }
  insertVertex_(t, e) {
    const i = t.segment, s = t.feature, r = t.geometry, o = t.depth, a = t.index;
    let l;
    for (; e.length < r.getStride(); )
      e.push(0);
    switch (r.getType()) {
      case "MultiLineString":
        l = r.getCoordinates(), l[o[0]].splice(a + 1, 0, e);
        break;
      case "Polygon":
        l = r.getCoordinates(), l[o[0]].splice(a + 1, 0, e);
        break;
      case "MultiPolygon":
        l = r.getCoordinates(), l[o[1]][o[0]].splice(a + 1, 0, e);
        break;
      case "LineString":
        l = r.getCoordinates(), l.splice(a + 1, 0, e);
        break;
      default:
        return;
    }
    this.setGeometryCoordinates_(r, l);
    const h = this.rBush_;
    h.remove(t), this.updateSegmentIndices_(r, a, o, 1);
    const c = {
      segment: [i[0], e],
      feature: s,
      geometry: r,
      depth: o,
      index: a
    };
    h.insert(Ut(c.segment), c), this.dragSegments_.push([c, 1]);
    const u = {
      segment: [e, i[1]],
      feature: s,
      geometry: r,
      depth: o,
      index: a + 1
    };
    h.insert(Ut(u.segment), u), this.dragSegments_.push([u, 0]), this.ignoreNextSingleClick_ = !0;
  }
  removePoint() {
    if (this.lastPointerEvent_ && this.lastPointerEvent_.type != nt.POINTERDRAG) {
      const t = this.lastPointerEvent_;
      this.willModifyFeatures_(t, this.dragSegments_);
      const e = this.removeVertex_();
      return this.featuresBeingModified_ && this.dispatchEvent(
        new ya(
          pa.MODIFYEND,
          this.featuresBeingModified_,
          t
        )
      ), this.featuresBeingModified_ = null, e;
    }
    return !1;
  }
  removeVertex_() {
    const t = this.dragSegments_, e = {};
    let i = !1, s, r, o, a, l, h, c, u, d, f, g;
    for (l = t.length - 1; l >= 0; --l)
      o = t[l], f = o[0], g = q(f.feature), f.depth && (g += "-" + f.depth.join("-")), g in e || (e[g] = {}), o[1] === 0 ? (e[g].right = f, e[g].index = f.index) : o[1] == 1 && (e[g].left = f, e[g].index = f.index + 1);
    for (g in e) {
      switch (d = e[g].right, c = e[g].left, h = e[g].index, u = h - 1, c !== void 0 ? f = c : f = d, u < 0 && (u = 0), a = f.geometry, r = a.getCoordinates(), s = r, i = !1, a.getType()) {
        case "MultiLineString":
          r[f.depth[0]].length > 2 && (r[f.depth[0]].splice(h, 1), i = !0);
          break;
        case "LineString":
          r.length > 2 && (r.splice(h, 1), i = !0);
          break;
        case "MultiPolygon":
          s = s[f.depth[1]];
        case "Polygon":
          s = s[f.depth[0]], s.length > 4 && (h == s.length - 1 && (h = 0), s.splice(h, 1), i = !0, h === 0 && (s.pop(), s.push(s[0]), u = s.length - 1));
          break;
      }
      if (i) {
        this.setGeometryCoordinates_(a, r);
        const m = [];
        if (c !== void 0 && (this.rBush_.remove(c), m.push(c.segment[0])), d !== void 0 && (this.rBush_.remove(d), m.push(d.segment[1])), c !== void 0 && d !== void 0) {
          const _ = {
            depth: f.depth,
            feature: f.feature,
            geometry: f.geometry,
            index: u,
            segment: m
          };
          this.rBush_.insert(
            Ut(_.segment),
            _
          );
        }
        this.updateSegmentIndices_(a, h, f.depth, -1), this.vertexFeature_ && (this.overlay_.getSource().removeFeature(this.vertexFeature_), this.vertexFeature_ = null), t.length = 0;
      }
    }
    return i;
  }
  setGeometryCoordinates_(t, e) {
    this.changingFeature_ = !0, t.setCoordinates(e), this.changingFeature_ = !1;
  }
  updateSegmentIndices_(t, e, i, s) {
    this.rBush_.forEachInExtent(
      t.getExtent(),
      function(r) {
        r.geometry === t && (i === void 0 || r.depth === void 0 || Ni(r.depth, i)) && r.index > e && (r.index += s);
      }
    );
  }
}
function h2(n, t) {
  return n.index - t.index;
}
function Lc(n, t, e) {
  const i = t.geometry;
  if (i.getType() === "Circle") {
    let r = i;
    if (t.index === Ls) {
      const o = oi(
        r.getCenter(),
        vt(n)
      ), a = Math.sqrt(o) - r.getRadius();
      return a * a;
    }
  }
  const s = vt(n);
  return zn[0] = vt(t.segment[0]), zn[1] = vt(t.segment[1]), f0(s, zn);
}
function Ic(n, t, e) {
  const i = t.geometry;
  if (i.getType() === "Circle" && t.index === Ls)
    return qn(
      i.getClosestPoint(
        vt(n)
      )
    );
  const s = vt(n);
  return zn[0] = vt(t.segment[0]), zn[1] = vt(t.segment[1]), qn(
    Ml(s, zn)
  );
}
function c2() {
  const n = Vd();
  return function(t, e) {
    return n.Point;
  };
}
const u2 = l2;
function Pc(n) {
  if (n.feature)
    return n.feature;
  if (n.element)
    return n.element;
}
const va = [];
class d2 extends ki {
  constructor(t) {
    t = t || {};
    const e = t;
    e.handleDownEvent || (e.handleDownEvent = en), e.stopDown || (e.stopDown = un), super(e), this.source_ = t.source ? t.source : null, this.vertex_ = t.vertex !== void 0 ? t.vertex : !0, this.edge_ = t.edge !== void 0 ? t.edge : !0, this.features_ = t.features ? t.features : null, this.featuresListenerKeys_ = [], this.featureChangeListenerKeys_ = {}, this.indexedFeaturesExtents_ = {}, this.pendingFeatures_ = {}, this.pixelTolerance_ = t.pixelTolerance !== void 0 ? t.pixelTolerance : 10, this.rBush_ = new fo(), this.GEOMETRY_SEGMENTERS_ = {
      Point: this.segmentPointGeometry_.bind(this),
      LineString: this.segmentLineStringGeometry_.bind(this),
      LinearRing: this.segmentLineStringGeometry_.bind(this),
      Polygon: this.segmentPolygonGeometry_.bind(this),
      MultiPoint: this.segmentMultiPointGeometry_.bind(this),
      MultiLineString: this.segmentMultiLineStringGeometry_.bind(this),
      MultiPolygon: this.segmentMultiPolygonGeometry_.bind(this),
      GeometryCollection: this.segmentGeometryCollectionGeometry_.bind(this),
      Circle: this.segmentCircleGeometry_.bind(this)
    };
  }
  addFeature(t, e) {
    e = e !== void 0 ? e : !0;
    const i = q(t), s = t.getGeometry();
    if (s) {
      const r = this.GEOMETRY_SEGMENTERS_[s.getType()];
      if (r) {
        this.indexedFeaturesExtents_[i] = s.getExtent(
          se()
        );
        const o = [];
        if (r(o, s), o.length === 1)
          this.rBush_.insert(Ut(o[0]), {
            feature: t,
            segment: o[0]
          });
        else if (o.length > 1) {
          const a = o.map((h) => Ut(h)), l = o.map((h) => ({
            feature: t,
            segment: h
          }));
          this.rBush_.load(a, l);
        }
      }
    }
    e && (this.featureChangeListenerKeys_[i] = et(
      t,
      U.CHANGE,
      this.handleFeatureChange_,
      this
    ));
  }
  forEachFeatureAdd_(t) {
    this.addFeature(t);
  }
  forEachFeatureRemove_(t) {
    this.removeFeature(t);
  }
  getFeatures_() {
    let t;
    return this.features_ ? t = this.features_ : this.source_ && (t = this.source_.getFeatures()), t;
  }
  handleEvent(t) {
    const e = this.snapTo(t.pixel, t.coordinate, t.map);
    return e && (t.coordinate = e.vertex.slice(0, 2), t.pixel = e.vertexPixel), super.handleEvent(t);
  }
  handleFeatureAdd_(t) {
    const e = Pc(t);
    this.addFeature(e);
  }
  handleFeatureRemove_(t) {
    const e = Pc(t);
    this.removeFeature(e);
  }
  handleFeatureChange_(t) {
    const e = t.target;
    if (this.handlingDownUpSequence) {
      const i = q(e);
      i in this.pendingFeatures_ || (this.pendingFeatures_[i] = e);
    } else
      this.updateFeature_(e);
  }
  handleUpEvent(t) {
    const e = Object.values(this.pendingFeatures_);
    return e.length && (e.forEach(this.updateFeature_.bind(this)), this.pendingFeatures_ = {}), !1;
  }
  removeFeature(t, e) {
    const i = e !== void 0 ? e : !0, s = q(t), r = this.indexedFeaturesExtents_[s];
    if (r) {
      const o = this.rBush_, a = [];
      o.forEachInExtent(r, function(l) {
        t === l.feature && a.push(l);
      });
      for (let l = a.length - 1; l >= 0; --l)
        o.remove(a[l]);
    }
    i && (mt(this.featureChangeListenerKeys_[s]), delete this.featureChangeListenerKeys_[s]);
  }
  setMap(t) {
    const e = this.getMap(), i = this.featuresListenerKeys_, s = this.getFeatures_();
    e && (i.forEach(mt), i.length = 0, s.forEach(this.forEachFeatureRemove_.bind(this))), super.setMap(t), t && (this.features_ ? i.push(
      et(
        this.features_,
        Dt.ADD,
        this.handleFeatureAdd_,
        this
      ),
      et(
        this.features_,
        Dt.REMOVE,
        this.handleFeatureRemove_,
        this
      )
    ) : this.source_ && i.push(
      et(
        this.source_,
        jt.ADDFEATURE,
        this.handleFeatureAdd_,
        this
      ),
      et(
        this.source_,
        jt.REMOVEFEATURE,
        this.handleFeatureRemove_,
        this
      )
    ), s.forEach(this.forEachFeatureAdd_.bind(this)));
  }
  snapTo(t, e, i) {
    const s = i.getCoordinateFromPixel([
      t[0] - this.pixelTolerance_,
      t[1] + this.pixelTolerance_
    ]), r = i.getCoordinateFromPixel([
      t[0] + this.pixelTolerance_,
      t[1] - this.pixelTolerance_
    ]), o = Ut([s, r]), a = this.rBush_.getInExtent(o), l = a.length;
    if (l === 0)
      return null;
    i.getView().getProjection();
    const h = vt(e);
    let c, u = 1 / 0;
    const d = this.pixelTolerance_ * this.pixelTolerance_, f = () => {
      if (c) {
        const g = i.getPixelFromCoordinate(c);
        if (oi(t, g) <= d)
          return {
            vertex: c,
            vertexPixel: [
              Math.round(g[0]),
              Math.round(g[1])
            ]
          };
      }
      return null;
    };
    if (this.vertex_) {
      for (let m = 0; m < l; ++m) {
        const _ = a[m];
        _.feature.getGeometry().getType() !== "Circle" && _.segment.forEach((y) => {
          const p = vt(y), v = oi(h, p);
          v < u && (c = y, u = v);
        });
      }
      const g = f();
      if (g)
        return g;
    }
    if (this.edge_) {
      for (let m = 0; m < l; ++m) {
        let _ = null;
        const y = a[m];
        if (y.feature.getGeometry().getType() === "Circle") {
          let p = y.feature.getGeometry();
          _ = qn(
            d0(
              h,
              p
            )
          );
        } else {
          const [p, v] = y.segment;
          v && (va[0] = vt(p), va[1] = vt(v), _ = Ml(h, va));
        }
        if (_) {
          const p = oi(h, _);
          p < u && (c = _, u = p);
        }
      }
      const g = f();
      if (g)
        return g;
    }
    return null;
  }
  updateFeature_(t) {
    this.removeFeature(t, !1), this.addFeature(t, !1);
  }
  segmentCircleGeometry_(t, e) {
    this.getMap().getView().getProjection();
    const r = R1(e).getCoordinates()[0];
    for (let o = 0, a = r.length - 1; o < a; ++o)
      t.push(r.slice(o, o + 2));
  }
  segmentGeometryCollectionGeometry_(t, e) {
    const i = e.getGeometriesArray();
    for (let s = 0; s < i.length; ++s) {
      const r = this.GEOMETRY_SEGMENTERS_[i[s].getType()];
      r && r(t, i[s]);
    }
  }
  segmentLineStringGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length - 1; s < r; ++s)
      t.push(i.slice(s, s + 2));
  }
  segmentMultiLineStringGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length - 1; a < l; ++a)
        t.push(o.slice(a, a + 2));
    }
  }
  segmentMultiPointGeometry_(t, e) {
    e.getCoordinates().forEach((i) => {
      t.push([i]);
    });
  }
  segmentMultiPolygonGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length; a < l; ++a) {
        const h = o[a];
        for (let c = 0, u = h.length - 1; c < u; ++c)
          t.push(h.slice(c, c + 2));
      }
    }
  }
  segmentPointGeometry_(t, e) {
    t.push([e.getCoordinates()]);
  }
  segmentPolygonGeometry_(t, e) {
    const i = e.getCoordinates();
    for (let s = 0, r = i.length; s < r; ++s) {
      const o = i[s];
      for (let a = 0, l = o.length - 1; a < l; ++a)
        t.push(o.slice(a, a + 2));
    }
  }
}
const f2 = d2, g2 = 0.5, m2 = 10, Ac = 0.25;
class _2 {
  constructor(t, e, i, s, r, o) {
    this.sourceProj_ = t, this.targetProj_ = e;
    let a = {};
    const l = zs(this.targetProj_, this.sourceProj_);
    this.transformInv_ = function(p) {
      const v = p[0] + "/" + p[1];
      return a[v] || (a[v] = l(p)), a[v];
    }, this.maxSourceExtent_ = s, this.errorThresholdSquared_ = r * r, this.triangles_ = [], this.wrapsXInSource_ = !1, this.canWrapXInSource_ = this.sourceProj_.canWrapX() && !!s && !!this.sourceProj_.getExtent() && pt(s) == pt(this.sourceProj_.getExtent()), this.sourceWorldWidth_ = this.sourceProj_.getExtent() ? pt(this.sourceProj_.getExtent()) : null, this.targetWorldWidth_ = this.targetProj_.getExtent() ? pt(this.targetProj_.getExtent()) : null;
    const h = fn(i), c = Io(i), u = Lo(i), d = bo(i), f = this.transformInv_(h), g = this.transformInv_(c), m = this.transformInv_(u), _ = this.transformInv_(d), y = m2 + (o ? Math.max(
      0,
      Math.ceil(
        Math.log2(
          La(i) / (o * o * 256 * 256)
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
      _,
      y
    ), this.wrapsXInSource_) {
      let p = 1 / 0;
      this.triangles_.forEach(function(v, x, C) {
        p = Math.min(
          p,
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
          ) - p > this.sourceWorldWidth_ / 2) {
            const x = [
              [v.source[0][0], v.source[0][1]],
              [v.source[1][0], v.source[1][1]],
              [v.source[2][0], v.source[2][1]]
            ];
            x[0][0] - p > this.sourceWorldWidth_ / 2 && (x[0][0] -= this.sourceWorldWidth_), x[1][0] - p > this.sourceWorldWidth_ / 2 && (x[1][0] -= this.sourceWorldWidth_), x[2][0] - p > this.sourceWorldWidth_ / 2 && (x[2][0] -= this.sourceWorldWidth_);
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
  addTriangle_(t, e, i, s, r, o) {
    this.triangles_.push({
      source: [s, r, o],
      target: [t, e, i]
    });
  }
  addQuad_(t, e, i, s, r, o, a, l, h) {
    const c = Ut([r, o, a, l]), u = this.sourceWorldWidth_ ? pt(c) / this.sourceWorldWidth_ : null, d = this.sourceWorldWidth_, f = this.sourceProj_.canWrapX() && u > 0.5 && u < 1;
    let g = !1;
    if (h > 0) {
      if (this.targetProj_.isGlobal() && this.targetWorldWidth_) {
        const _ = Ut([t, e, i, s]);
        g = pt(_) / this.targetWorldWidth_ > Ac || g;
      }
      !f && this.sourceProj_.isGlobal() && u && (g = u > Ac || g);
    }
    if (!g && this.maxSourceExtent_ && isFinite(c[0]) && isFinite(c[1]) && isFinite(c[2]) && isFinite(c[3]) && !Kt(c, this.maxSourceExtent_))
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
        const _ = [(t[0] + i[0]) / 2, (t[1] + i[1]) / 2], y = this.transformInv_(_);
        let p;
        f ? p = (qi(r[0], d) + qi(a[0], d)) / 2 - qi(y[0], d) : p = (r[0] + a[0]) / 2 - y[0];
        const v = (r[1] + a[1]) / 2 - y[1];
        g = p * p + v * v > this.errorThresholdSquared_;
      }
      if (g) {
        if (Math.abs(t[0] - i[0]) <= Math.abs(t[1] - i[1])) {
          const _ = [(e[0] + i[0]) / 2, (e[1] + i[1]) / 2], y = this.transformInv_(_), p = [(s[0] + t[0]) / 2, (s[1] + t[1]) / 2], v = this.transformInv_(p);
          this.addQuad_(
            t,
            e,
            _,
            p,
            r,
            o,
            y,
            v,
            h - 1
          ), this.addQuad_(
            p,
            _,
            i,
            s,
            v,
            y,
            a,
            l,
            h - 1
          );
        } else {
          const _ = [(t[0] + e[0]) / 2, (t[1] + e[1]) / 2], y = this.transformInv_(_), p = [(i[0] + s[0]) / 2, (i[1] + s[1]) / 2], v = this.transformInv_(p);
          this.addQuad_(
            t,
            _,
            p,
            s,
            r,
            y,
            v,
            l,
            h - 1
          ), this.addQuad_(
            _,
            e,
            i,
            p,
            y,
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
    (m & 11) == 0 && this.addTriangle_(t, i, s, r, a, l), (m & 14) == 0 && this.addTriangle_(t, i, e, r, a, o), m && ((m & 13) == 0 && this.addTriangle_(e, s, t, o, l, r), (m & 7) == 0 && this.addTriangle_(e, s, i, o, l, a));
  }
  calculateSourceExtent() {
    const t = se();
    return this.triangles_.forEach(function(e, i, s) {
      const r = e.source;
      Ss(t, r[0]), Ss(t, r[1]), Ss(t, r[2]);
    }), t;
  }
  getTriangles() {
    return this.triangles_;
  }
}
const p2 = _2;
let xa;
const hf = [];
function Oc(n, t, e, i, s) {
  n.beginPath(), n.moveTo(0, 0), n.lineTo(t, e), n.lineTo(i, s), n.closePath(), n.save(), n.clip(), n.fillRect(0, 0, Math.max(t, i) + 1, Math.max(e, s)), n.restore();
}
function Ca(n, t) {
  return Math.abs(n[t * 4] - 210) > 2 || Math.abs(n[t * 4 + 3] - 0.75 * 255) > 2;
}
function y2() {
  if (xa === void 0) {
    const n = document.createElement("canvas").getContext("2d");
    n.globalCompositeOperation = "lighter", n.fillStyle = "rgba(210, 0, 0, 0.75)", Oc(n, 4, 5, 4, 0), Oc(n, 4, 5, 0, 5);
    const t = n.getImageData(0, 0, 3, 3).data;
    xa = Ca(t, 0) || Ca(t, 4) || Ca(t, 8);
  }
  return xa;
}
function Fc(n, t, e, i) {
  const s = _d(e, t, n);
  let r = ao(
    t,
    i,
    e
  );
  const o = t.getMetersPerUnit();
  o !== void 0 && (r *= o);
  const a = n.getMetersPerUnit();
  a !== void 0 && (r /= a);
  const l = n.getExtent();
  if (!l || To(l, s)) {
    const h = ao(n, r, s) / r;
    isFinite(h) && h > 0 && (r /= h);
  }
  return r;
}
function v2(n, t, e, i) {
  const s = Pi(e);
  let r = Fc(
    n,
    t,
    s,
    i
  );
  return (!isFinite(r) || r <= 0) && yl(e, function(o) {
    return r = Fc(
      n,
      t,
      o,
      i
    ), isFinite(r) && r > 0;
  }), r;
}
function x2(n, t, e, i, s, r, o, a, l, h, c, u) {
  const d = pe(
    Math.round(e * n),
    Math.round(e * t),
    hf
  );
  if (u || (d.imageSmoothingEnabled = !1), l.length === 0)
    return d.canvas;
  d.scale(e, e);
  function f(x) {
    return Math.round(x * e) / e;
  }
  d.globalCompositeOperation = "lighter";
  const g = se();
  l.forEach(function(x, C, E) {
    Ku(g, x.extent);
  });
  const m = pt(g), _ = ze(g), y = pe(
    Math.round(e * m / i),
    Math.round(e * _ / i)
  );
  u || (y.imageSmoothingEnabled = !1);
  const p = e / i;
  l.forEach(function(x, C, E) {
    const R = x.extent[0] - g[0], b = -(x.extent[3] - g[3]), F = pt(x.extent), G = ze(x.extent);
    x.image.width > 0 && x.image.height > 0 && y.drawImage(
      x.image,
      h,
      h,
      x.image.width - 2 * h,
      x.image.height - 2 * h,
      R * p,
      b * p,
      F * p,
      G * p
    );
  });
  const v = fn(o);
  return a.getTriangles().forEach(function(x, C, E) {
    const R = x.source, b = x.target;
    let F = R[0][0], G = R[0][1], V = R[1][0], L = R[1][1], $ = R[2][0], gt = R[2][1];
    const N = f((b[0][0] - v[0]) / r), k = f(
      -(b[0][1] - v[1]) / r
    ), P = f((b[1][0] - v[0]) / r), it = f(
      -(b[1][1] - v[1]) / r
    ), wt = f((b[2][0] - v[0]) / r), yt = f(
      -(b[2][1] - v[1]) / r
    ), At = F, T = G;
    F = 0, G = 0, V -= At, L -= T, $ -= At, gt -= T;
    const ce = [
      [V, L, 0, 0, P - N],
      [$, gt, 0, 0, wt - N],
      [0, 0, V, L, it - k],
      [0, 0, $, gt, yt - k]
    ], ht = n0(ce);
    if (!!ht) {
      if (d.save(), d.beginPath(), y2() || !u) {
        d.moveTo(P, it);
        const _t = 4, ui = N - P, Fe = k - it;
        for (let Bt = 0; Bt < _t; Bt++)
          d.lineTo(
            P + f((Bt + 1) * ui / _t),
            it + f(Bt * Fe / (_t - 1))
          ), Bt != _t - 1 && d.lineTo(
            P + f((Bt + 1) * ui / _t),
            it + f((Bt + 1) * Fe / (_t - 1))
          );
        d.lineTo(wt, yt);
      } else
        d.moveTo(P, it), d.lineTo(N, k), d.lineTo(wt, yt);
      d.clip(), d.transform(
        ht[0],
        ht[2],
        ht[1],
        ht[3],
        N,
        k
      ), d.translate(
        g[0] - At,
        g[3] - T
      ), d.scale(
        i / e,
        -i / e
      ), d.drawImage(y.canvas, 0, 0), d.restore();
    }
  }), c && (d.save(), d.globalCompositeOperation = "source-over", d.strokeStyle = "black", d.lineWidth = 1, a.getTriangles().forEach(function(x, C, E) {
    const R = x.target, b = (R[0][0] - v[0]) / r, F = -(R[0][1] - v[1]) / r, G = (R[1][0] - v[0]) / r, V = -(R[1][1] - v[1]) / r, L = (R[2][0] - v[0]) / r, $ = -(R[2][1] - v[1]) / r;
    d.beginPath(), d.moveTo(G, V), d.lineTo(b, F), d.lineTo(L, $), d.closePath(), d.stroke();
  }), d.restore()), d.canvas;
}
class C2 extends Jd {
  constructor(t, e, i, s, r, o, a, l, h, c, u, d) {
    super(r, z.IDLE, { interpolate: !!d }), this.renderEdges_ = u !== void 0 ? u : !1, this.pixelRatio_ = a, this.gutter_ = l, this.canvas_ = null, this.sourceTileGrid_ = e, this.targetTileGrid_ = s, this.wrappedTileCoord_ = o || r, this.sourceTiles_ = [], this.sourcesListenerKeys_ = null, this.sourceZ_ = 0;
    const f = s.getTileCoordExtent(
      this.wrappedTileCoord_
    ), g = this.targetTileGrid_.getExtent();
    let m = this.sourceTileGrid_.getExtent();
    const _ = g ? Rs(f, g) : f;
    if (La(_) === 0) {
      this.state = z.EMPTY;
      return;
    }
    const y = t.getExtent();
    y && (m ? m = Rs(m, y) : m = y);
    const p = s.getResolution(
      this.wrappedTileCoord_[0]
    ), v = v2(
      t,
      i,
      _,
      p
    );
    if (!isFinite(v) || v <= 0) {
      this.state = z.EMPTY;
      return;
    }
    const x = c !== void 0 ? c : g2;
    if (this.triangulation_ = new p2(
      t,
      i,
      _,
      m,
      v * x,
      p
    ), this.triangulation_.getTriangles().length === 0) {
      this.state = z.EMPTY;
      return;
    }
    this.sourceZ_ = e.getZForResolution(v);
    let C = this.triangulation_.calculateSourceExtent();
    if (m && (t.canWrapX() ? (C[1] = Et(
      C[1],
      m[1],
      m[3]
    ), C[3] = Et(
      C[3],
      m[1],
      m[3]
    )) : C = Rs(C, m)), !La(C))
      this.state = z.EMPTY;
    else {
      const E = e.getTileRangeForExtentAndZ(
        C,
        this.sourceZ_
      );
      for (let R = E.minX; R <= E.maxX; R++)
        for (let b = E.minY; b <= E.maxY; b++) {
          const F = h(this.sourceZ_, R, b, a);
          F && this.sourceTiles_.push(F);
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
      function(e, i, s) {
        e && e.getState() == z.LOADED && t.push({
          extent: this.sourceTileGrid_.getTileCoordExtent(e.tileCoord),
          image: e.getImage()
        });
      }.bind(this)
    ), this.sourceTiles_.length = 0, t.length === 0)
      this.state = z.ERROR;
    else {
      const e = this.wrappedTileCoord_[0], i = this.targetTileGrid_.getTileSize(e), s = typeof i == "number" ? i : i[0], r = typeof i == "number" ? i : i[1], o = this.targetTileGrid_.getResolution(e), a = this.sourceTileGrid_.getResolution(
        this.sourceZ_
      ), l = this.targetTileGrid_.getTileCoordExtent(
        this.wrappedTileCoord_
      );
      this.canvas_ = x2(
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
        function(e, i, s) {
          const r = e.getState();
          if (r == z.IDLE || r == z.LOADING) {
            t++;
            const o = et(
              e,
              U.CHANGE,
              function(a) {
                const l = e.getState();
                (l == z.LOADED || l == z.ERROR || l == z.EMPTY) && (mt(o), t--, t === 0 && (this.unlistenSources_(), this.reproject_()));
              },
              this
            );
            this.sourcesListenerKeys_.push(o);
          }
        }.bind(this)
      ), t === 0 ? setTimeout(this.reproject_.bind(this), 0) : this.sourceTiles_.forEach(function(e, i, s) {
        e.getState() == z.IDLE && e.load();
      });
    }
  }
  unlistenSources_() {
    this.sourcesListenerKeys_.forEach(mt), this.sourcesListenerKeys_ = null;
  }
  release() {
    this.canvas_ && (hd(this.canvas_.getContext("2d")), hf.push(this.canvas_), this.canvas_ = null), super.release();
  }
}
const Xa = C2, Ma = {
  TILELOADSTART: "tileloadstart",
  TILELOADEND: "tileloadend",
  TILELOADERROR: "tileloaderror"
}, M2 = [0, 0, 0], yi = 5;
class E2 {
  constructor(t) {
    this.minZoom = t.minZoom !== void 0 ? t.minZoom : 0, this.resolutions_ = t.resolutions, Y(
      Pg(
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
    const i = t.extent;
    i !== void 0 && !this.origin_ && !this.origins_ && (this.origin_ = fn(i)), Y(
      !this.origin_ && this.origins_ || this.origin_ && !this.origins_,
      18
    ), this.tileSizes_ = null, t.tileSizes !== void 0 && (this.tileSizes_ = t.tileSizes, Y(this.tileSizes_.length == this.resolutions_.length, 19)), this.tileSize_ = t.tileSize !== void 0 ? t.tileSize : this.tileSizes_ ? null : Sl, Y(
      !this.tileSize_ && this.tileSizes_ || this.tileSize_ && !this.tileSizes_,
      22
    ), this.extent_ = i !== void 0 ? i : null, this.fullTileRanges_ = null, this.tmpSize_ = [0, 0], this.tmpExtent_ = [0, 0, 0, 0], t.sizes !== void 0 ? this.fullTileRanges_ = t.sizes.map(function(s, r) {
      const o = new sf(
        Math.min(0, s[0]),
        Math.max(s[0] - 1, -1),
        Math.min(0, s[1]),
        Math.max(s[1] - 1, -1)
      );
      if (i) {
        const a = this.getTileRangeForExtentAndZ(i, r);
        o.minX = Math.max(a.minX, o.minX), o.maxX = Math.min(a.maxX, o.maxX), o.minY = Math.max(a.minY, o.minY), o.maxY = Math.min(a.maxY, o.maxY);
      }
      return o;
    }, this) : i && this.calculateTileRanges_(i);
  }
  forEachTileCoord(t, e, i) {
    const s = this.getTileRangeForExtentAndZ(t, e);
    for (let r = s.minX, o = s.maxX; r <= o; ++r)
      for (let a = s.minY, l = s.maxY; a <= l; ++a)
        i([e, r, a]);
  }
  forEachTileCoordParentTileRange(t, e, i, s) {
    let r, o, a, l = null, h = t[0] - 1;
    for (this.zoomFactor_ === 2 ? (o = t[1], a = t[2]) : l = this.getTileCoordExtent(t, s); h >= this.minZoom; ) {
      if (this.zoomFactor_ === 2 ? (o = Math.floor(o / 2), a = Math.floor(a / 2), r = wn(o, o, a, a, i)) : r = this.getTileRangeForExtentAndZ(
        l,
        h,
        i
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
  getTileCoordChildTileRange(t, e, i) {
    if (t[0] < this.maxZoom) {
      if (this.zoomFactor_ === 2) {
        const r = t[1] * 2, o = t[2] * 2;
        return wn(
          r,
          r + 1,
          o,
          o + 1,
          e
        );
      }
      const s = this.getTileCoordExtent(
        t,
        i || this.tmpExtent_
      );
      return this.getTileRangeForExtentAndZ(
        s,
        t[0] + 1,
        e
      );
    }
    return null;
  }
  getTileRangeForTileCoordAndZ(t, e, i) {
    if (e > this.maxZoom || e < this.minZoom)
      return null;
    const s = t[0], r = t[1], o = t[2];
    if (e === s)
      return wn(
        r,
        o,
        r,
        o,
        i
      );
    if (this.zoomFactor_) {
      const l = Math.pow(this.zoomFactor_, e - s), h = Math.floor(r * l), c = Math.floor(o * l);
      if (e < s)
        return wn(h, h, c, c, i);
      const u = Math.floor(l * (r + 1)) - 1, d = Math.floor(l * (o + 1)) - 1;
      return wn(h, u, c, d, i);
    }
    const a = this.getTileCoordExtent(t, this.tmpExtent_);
    return this.getTileRangeForExtentAndZ(a, e, i);
  }
  getTileRangeExtent(t, e, i) {
    const s = this.getOrigin(t), r = this.getResolution(t), o = fe(this.getTileSize(t), this.tmpSize_), a = s[0] + e.minX * o[0] * r, l = s[0] + (e.maxX + 1) * o[0] * r, h = s[1] + e.minY * o[1] * r, c = s[1] + (e.maxY + 1) * o[1] * r;
    return _e(a, h, l, c, i);
  }
  getTileRangeForExtentAndZ(t, e, i) {
    const s = M2;
    this.getTileCoordForXYAndZ_(t[0], t[3], e, !1, s);
    const r = s[1], o = s[2];
    return this.getTileCoordForXYAndZ_(t[2], t[1], e, !0, s), wn(
      r,
      s[1],
      o,
      s[2],
      i
    );
  }
  getTileCoordCenter(t) {
    const e = this.getOrigin(t[0]), i = this.getResolution(t[0]), s = fe(this.getTileSize(t[0]), this.tmpSize_);
    return [
      e[0] + (t[1] + 0.5) * s[0] * i,
      e[1] - (t[2] + 0.5) * s[1] * i
    ];
  }
  getTileCoordExtent(t, e) {
    const i = this.getOrigin(t[0]), s = this.getResolution(t[0]), r = fe(this.getTileSize(t[0]), this.tmpSize_), o = i[0] + t[1] * r[0] * s, a = i[1] - (t[2] + 1) * r[1] * s, l = o + r[0] * s, h = a + r[1] * s;
    return _e(o, a, l, h, e);
  }
  getTileCoordForCoordAndResolution(t, e, i) {
    return this.getTileCoordForXYAndResolution_(
      t[0],
      t[1],
      e,
      !1,
      i
    );
  }
  getTileCoordForXYAndResolution_(t, e, i, s, r) {
    const o = this.getZForResolution(i), a = i / this.getResolution(o), l = this.getOrigin(o), h = fe(this.getTileSize(o), this.tmpSize_);
    let c = a * (t - l[0]) / i / h[0], u = a * (l[1] - e) / i / h[1];
    return s ? (c = Sr(c, yi) - 1, u = Sr(u, yi) - 1) : (c = wr(c, yi), u = wr(u, yi)), Cc(o, c, u, r);
  }
  getTileCoordForXYAndZ_(t, e, i, s, r) {
    const o = this.getOrigin(i), a = this.getResolution(i), l = fe(this.getTileSize(i), this.tmpSize_);
    let h = (t - o[0]) / a / l[0], c = (o[1] - e) / a / l[1];
    return s ? (h = Sr(h, yi) - 1, c = Sr(c, yi) - 1) : (h = wr(h, yi), c = wr(c, yi)), Cc(i, h, c, r);
  }
  getTileCoordForCoordAndZ(t, e, i) {
    return this.getTileCoordForXYAndZ_(
      t[0],
      t[1],
      e,
      !1,
      i
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
    const i = gl(
      this.resolutions_,
      t,
      e || 0
    );
    return Et(i, this.minZoom, this.maxZoom);
  }
  tileCoordIntersectsViewport(t, e) {
    return Td(
      e,
      0,
      e.length,
      2,
      this.getTileCoordExtent(t)
    );
  }
  calculateTileRanges_(t) {
    const e = this.resolutions_.length, i = new Array(e);
    for (let s = this.minZoom; s < e; ++s)
      i[s] = this.getTileRangeForExtentAndZ(t, s);
    this.fullTileRanges_ = i;
  }
}
const cf = E2;
function uf(n) {
  let t = n.getDefaultTileGrid();
  return t || (t = T2(n), n.setDefaultTileGrid(t)), t;
}
function w2(n, t, e) {
  const i = t[0], s = n.getTileCoordCenter(t), r = df(e);
  if (To(r, s))
    return t;
  {
    const o = pt(r), a = Math.ceil(
      (r[0] - s[0]) / o
    );
    return s[0] += o * a, n.getTileCoordForCoordAndZ(s, i);
  }
}
function S2(n, t, e, i) {
  i = i !== void 0 ? i : "top-left";
  const s = R2(n, t, e);
  return new cf({
    extent: n,
    origin: Kg(n, i),
    resolutions: s,
    tileSize: e
  });
}
function R2(n, t, e, i) {
  t = t !== void 0 ? t : k0, e = fe(e !== void 0 ? e : Sl);
  const s = ze(n), r = pt(n);
  i = i > 0 ? i : Math.max(r / e[0], s / e[1]);
  const o = t + 1, a = new Array(o);
  for (let l = 0; l < o; ++l)
    a[l] = i / Math.pow(2, l);
  return a;
}
function T2(n, t, e, i) {
  const s = df(n);
  return S2(s, t, e, i);
}
function df(n) {
  n = Q(n);
  let t = n.getExtent();
  if (!t) {
    const e = 180 * Yn.degrees / n.getMetersPerUnit();
    t = _e(-e, -e, e, e);
  }
  return t;
}
class b2 extends Kd {
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
    this.tileGrid && fe(this.tileGrid.getTileSize(this.tileGrid.getMinZoom()), e), this.tileCache = new ef(t.cacheSize || 0), this.tmpSize = [0, 0], this.key_ = t.key || "", this.tileOptions = {
      transition: t.transition,
      interpolate: t.interpolate
    }, this.zDirection = t.zDirection ? t.zDirection : 0;
  }
  canExpireCache() {
    return this.tileCache.canExpireCache();
  }
  expireCache(t, e) {
    const i = this.getTileCacheForProjection(t);
    i && i.expireCache(e);
  }
  forEachLoadedTile(t, e, i, s) {
    const r = this.getTileCacheForProjection(t);
    if (!r)
      return !1;
    let o = !0, a, l, h;
    for (let c = i.minX; c <= i.maxX; ++c)
      for (let u = i.minY; u <= i.maxY; ++u)
        l = ko(e, c, u), h = !1, r.containsKey(l) && (a = r.get(l), h = a.getState() === z.LOADED, h && (h = s(a) !== !1)), h || (o = !1);
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
  getTile(t, e, i, s, r) {
    return H();
  }
  getTileGrid() {
    return this.tileGrid;
  }
  getTileGridForProjection(t) {
    return this.tileGrid ? this.tileGrid : uf(t);
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    return Y(
      e === null || Ne(e, t),
      68
    ), this.tileCache;
  }
  getTilePixelRatio(t) {
    return this.tilePixelRatio_;
  }
  getTilePixelSize(t, e, i) {
    const s = this.getTileGridForProjection(i), r = this.getTilePixelRatio(e), o = fe(s.getTileSize(t), this.tmpSize);
    return r == 1 ? o : vm(o, r, this.tmpSize);
  }
  getTileCoordForTileUrlFunction(t, e) {
    e = e !== void 0 ? e : this.getProjection();
    const i = this.getTileGridForProjection(e);
    return this.getWrapX() && e.isGlobal() && (t = w2(i, t, e)), W_(t, i) ? t : null;
  }
  clear() {
    this.tileCache.clear();
  }
  refresh() {
    this.clear(), super.refresh();
  }
  updateCacheSize(t, e) {
    const i = this.getTileCacheForProjection(e);
    t > i.highWaterMark && (i.highWaterMark = t);
  }
  useTile(t, e, i, s) {
  }
}
class L2 extends Re {
  constructor(t, e) {
    super(t), this.tile = e;
  }
}
const I2 = b2;
function P2(n, t) {
  const e = /\{z\}/g, i = /\{x\}/g, s = /\{y\}/g, r = /\{-y\}/g;
  return function(o, a, l) {
    if (o)
      return n.replace(e, o[0].toString()).replace(i, o[1].toString()).replace(s, o[2].toString()).replace(r, function() {
        const h = o[0], c = t.getFullTileRange(h);
        return Y(c, 55), (c.getHeight() - o[2] - 1).toString();
      });
  };
}
function A2(n, t) {
  const e = n.length, i = new Array(e);
  for (let s = 0; s < e; ++s)
    i[s] = P2(n[s], t);
  return Ya(i);
}
function Ya(n) {
  return n.length === 1 ? n[0] : function(t, e, i) {
    if (t) {
      const s = U_(t), r = qi(s, n.length);
      return n[r](t, e, i);
    } else
      return;
  };
}
function ff(n) {
  const t = [];
  let e = /\{([a-z])-([a-z])\}/.exec(n);
  if (e) {
    const i = e[1].charCodeAt(0), s = e[2].charCodeAt(0);
    let r;
    for (r = i; r <= s; ++r)
      t.push(n.replace(e[0], String.fromCharCode(r)));
    return t;
  }
  if (e = /\{(\d+)-(\d+)\}/.exec(n), e) {
    const i = parseInt(e[2], 10);
    for (let s = parseInt(e[1], 10); s <= i; s++)
      t.push(n.replace(e[0], s.toString()));
    return t;
  }
  return t.push(n), t;
}
class eh extends I2 {
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
    }), this.generateTileUrlFunction_ = this.tileUrlFunction === eh.prototype.tileUrlFunction, this.tileLoadFunction = t.tileLoadFunction, t.tileUrlFunction && (this.tileUrlFunction = t.tileUrlFunction), this.urls = null, t.urls ? this.setUrls(t.urls) : t.url && this.setUrl(t.url), this.tileLoadingKeys_ = {};
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
    const e = t.target, i = q(e), s = e.getState();
    let r;
    s == z.LOADING ? (this.tileLoadingKeys_[i] = !0, r = Ma.TILELOADSTART) : i in this.tileLoadingKeys_ && (delete this.tileLoadingKeys_[i], r = s == z.ERROR ? Ma.TILELOADERROR : s == z.LOADED ? Ma.TILELOADEND : void 0), r != null && this.dispatchEvent(new L2(r, e));
  }
  setTileLoadFunction(t) {
    this.tileCache.clear(), this.tileLoadFunction = t, this.changed();
  }
  setTileUrlFunction(t, e) {
    this.tileUrlFunction = t, this.tileCache.pruneExceptNewestZ(), typeof e < "u" ? this.setKey(e) : this.changed();
  }
  setUrl(t) {
    const e = ff(t);
    this.urls = e, this.setUrls(e);
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.generateTileUrlFunction_ ? this.setTileUrlFunction(A2(t, this.tileGrid), e) : this.setKey(e);
  }
  tileUrlFunction(t, e, i) {
  }
  useTile(t, e, i) {
    const s = ko(t, e, i);
    this.tileCache.containsKey(s) && this.tileCache.get(s);
  }
}
const O2 = eh;
class F2 extends O2 {
  constructor(t) {
    super({
      attributions: t.attributions,
      cacheSize: t.cacheSize,
      opaque: t.opaque,
      projection: t.projection,
      state: t.state,
      tileGrid: t.tileGrid,
      tileLoadFunction: t.tileLoadFunction ? t.tileLoadFunction : N2,
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
    }), this.crossOrigin = t.crossOrigin !== void 0 ? t.crossOrigin : null, this.tileClass = t.tileClass !== void 0 ? t.tileClass : Qd, this.tileCacheForProjection = {}, this.tileGridForProjection = {}, this.reprojectionErrorThreshold_ = t.reprojectionErrorThreshold, this.renderReprojectionEdges_ = !1;
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
    const i = this.getTileCacheForProjection(t);
    this.tileCache.expireCache(
      this.tileCache == i ? e : {}
    );
    for (const s in this.tileCacheForProjection) {
      const r = this.tileCacheForProjection[s];
      r.expireCache(r == i ? e : {});
    }
  }
  getGutterForProjection(t) {
    return this.getProjection() && t && !Ne(this.getProjection(), t) ? 0 : this.getGutter();
  }
  getGutter() {
    return 0;
  }
  getKey() {
    let t = super.getKey();
    return this.getInterpolate() || (t += ":disable-interpolation"), t;
  }
  getOpaque(t) {
    return this.getProjection() && t && !Ne(this.getProjection(), t) ? !1 : super.getOpaque(t);
  }
  getTileGridForProjection(t) {
    const e = this.getProjection();
    if (this.tileGrid && (!e || Ne(e, t)))
      return this.tileGrid;
    {
      const i = q(t);
      return i in this.tileGridForProjection || (this.tileGridForProjection[i] = uf(t)), this.tileGridForProjection[i];
    }
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    if (!e || Ne(e, t))
      return this.tileCache;
    {
      const i = q(t);
      return i in this.tileCacheForProjection || (this.tileCacheForProjection[i] = new ef(
        this.tileCache.highWaterMark
      )), this.tileCacheForProjection[i];
    }
  }
  createTile_(t, e, i, s, r, o) {
    const a = [t, e, i], l = this.getTileCoordForTileUrlFunction(
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
    return c.key = o, c.addEventListener(U.CHANGE, this.handleTileChange.bind(this)), c;
  }
  getTile(t, e, i, s, r) {
    const o = this.getProjection();
    if (!o || !r || Ne(o, r))
      return this.getTileInternal(
        t,
        e,
        i,
        s,
        o || r
      );
    {
      const a = this.getTileCacheForProjection(r), l = [t, e, i];
      let h;
      const c = tf(l);
      a.containsKey(c) && (h = a.get(c));
      const u = this.getKey();
      if (h && h.key == u)
        return h;
      {
        const d = this.getTileGridForProjection(o), f = this.getTileGridForProjection(r), g = this.getTileCoordForTileUrlFunction(
          l,
          r
        ), m = new Xa(
          o,
          d,
          r,
          f,
          l,
          g,
          this.getTilePixelRatio(s),
          this.getGutter(),
          function(_, y, p, v) {
            return this.getTileInternal(_, y, p, v, o);
          }.bind(this),
          this.reprojectionErrorThreshold_,
          this.renderReprojectionEdges_,
          this.getInterpolate()
        );
        return m.key = u, h ? (m.interimTile = h, m.refreshInterimChain(), a.replace(c, m)) : a.set(c, m), m;
      }
    }
  }
  getTileInternal(t, e, i, s, r) {
    let o = null;
    const a = ko(t, e, i), l = this.getKey();
    if (!this.tileCache.containsKey(a))
      o = this.createTile_(t, e, i, s, r, l), this.tileCache.set(a, o);
    else if (o = this.tileCache.get(a), o.key != l) {
      const h = o;
      o = this.createTile_(t, e, i, s, r, l), h.getState() == z.IDLE ? o.interimTile = h.interimTile : o.interimTile = h, o.refreshInterimChain(), this.tileCache.replace(a, o);
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
    const i = Q(t);
    if (i) {
      const s = q(i);
      s in this.tileGridForProjection || (this.tileGridForProjection[s] = e);
    }
  }
  clear() {
    super.clear();
    for (const t in this.tileCacheForProjection)
      this.tileCacheForProjection[t].clear();
  }
}
function N2(n, t) {
  n.getImage().src = t;
}
const D2 = F2;
class k2 extends Ve {
  constructor(t) {
    super({
      attributions: t.attributions,
      wrapX: t.wrapX
    }), this.resolution = void 0, this.distance = t.distance !== void 0 ? t.distance : 20, this.minDistance = t.minDistance || 0, this.interpolationRatio = 0, this.features = [], this.geometryFunction = t.geometryFunction || function(e) {
      const i = e.getGeometry();
      return Y(i.getType() == "Point", 10), i;
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
  loadFeatures(t, e, i) {
    this.source.loadFeatures(t, e, i), e !== this.resolution && (this.resolution = e, this.refresh());
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
    this.source && this.source.removeEventListener(U.CHANGE, this.boundRefresh_), this.source = t, t && t.addEventListener(U.CHANGE, this.boundRefresh_), this.refresh();
  }
  refresh() {
    this.clear(), this.cluster(), this.addFeatures(this.features);
  }
  updateDistance(t, e) {
    const i = t === 0 ? 0 : Math.min(e, t) / t, s = t !== this.distance || this.interpolationRatio !== i;
    this.distance = t, this.minDistance = e, this.interpolationRatio = i, s && this.refresh();
  }
  cluster() {
    if (this.resolution === void 0 || !this.source)
      return;
    const t = se(), e = this.distance * this.resolution, i = this.source.getFeatures(), s = {};
    for (let r = 0, o = i.length; r < o; r++) {
      const a = i[r];
      if (!(q(a) in s)) {
        const l = this.geometryFunction(a);
        if (l) {
          const h = l.getCoordinates();
          ws(h, t), Js(t, e, t);
          const c = this.source.getFeaturesInExtent(t).filter(function(u) {
            const d = q(u);
            return d in s ? !1 : (s[d] = !0, !0);
          });
          this.features.push(this.createCluster(c, t));
        }
      }
    }
  }
  createCluster(t, e) {
    const i = [0, 0];
    for (let a = t.length - 1; a >= 0; --a) {
      const l = this.geometryFunction(t[a]);
      l ? nd(i, l.getCoordinates()) : t.splice(a, 1);
    }
    sd(i, 1 / t.length);
    const s = Pi(e), r = this.interpolationRatio, o = new Se([
      i[0] * (1 - r) + s[0] * r,
      i[1] * (1 - r) + s[1] * r
    ]);
    return this.createCustomCluster_ ? this.createCustomCluster_(o, t) : new Ie({
      geometry: o,
      features: t
    });
  }
}
const G2 = k2;
function Nc(n, t) {
  const e = [];
  Object.keys(t).forEach(function(s) {
    t[s] !== null && t[s] !== void 0 && e.push(s + "=" + encodeURIComponent(t[s]));
  });
  const i = e.join("&");
  return n = n.replace(/[?&]$/, ""), n += n.includes("?") ? "&" : "?", n + i;
}
const Gr = {
  PRELOAD: "preload",
  USE_INTERIM_TILES_ON_ERROR: "useInterimTilesOnError"
};
class $2 extends Po {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.preload, delete e.useInterimTilesOnError, super(e), this.on, this.once, this.un, this.setPreload(t.preload !== void 0 ? t.preload : 0), this.setUseInterimTilesOnError(
      t.useInterimTilesOnError !== void 0 ? t.useInterimTilesOnError : !0
    );
  }
  getPreload() {
    return this.get(Gr.PRELOAD);
  }
  setPreload(t) {
    this.set(Gr.PRELOAD, t);
  }
  getUseInterimTilesOnError() {
    return this.get(Gr.USE_INTERIM_TILES_ON_ERROR);
  }
  setUseInterimTilesOnError(t) {
    this.set(Gr.USE_INTERIM_TILES_ON_ERROR, t);
  }
  getData(t) {
    return super.getData(t);
  }
}
const B2 = $2;
class z2 extends Yd {
  constructor(t) {
    super(t), this.extentChanged = !0, this.renderedExtent_ = null, this.renderedPixelRatio, this.renderedProjection = null, this.renderedRevision, this.renderedTiles = [], this.newTiles_ = !1, this.tmpExtent = se(), this.tmpTileRange_ = new sf(0, 0, 0, 0);
  }
  isDrawableTile(t) {
    const e = this.getLayer(), i = t.getState(), s = e.getUseInterimTilesOnError();
    return i == z.LOADED || i == z.EMPTY || i == z.ERROR && !s;
  }
  getTile(t, e, i, s) {
    const r = s.pixelRatio, o = s.viewState.projection, a = this.getLayer();
    let h = a.getSource().getTile(t, e, i, r, o);
    return h.getState() == z.ERROR && a.getUseInterimTilesOnError() && a.getPreload() > 0 && (this.newTiles_ = !0), this.isDrawableTile(h) || (h = h.getInterimTile()), h;
  }
  getData(t) {
    const e = this.frameState;
    if (!e)
      return null;
    const i = this.getLayer(), s = Nt(
      e.pixelToCoordinateTransform,
      t.slice()
    ), r = i.getExtent();
    if (r && !To(r, s))
      return null;
    const o = e.pixelRatio, a = e.viewState.projection, l = e.viewState, h = i.getRenderSource(), c = h.getTileGridForProjection(l.projection), u = h.getTilePixelRatio(e.pixelRatio);
    for (let d = c.getZForResolution(l.resolution); d >= c.getMinZoom(); --d) {
      const f = c.getTileCoordForCoordAndZ(s, d), g = h.getTile(
        d,
        f[1],
        f[2],
        o,
        a
      );
      if (!(g instanceof Qd || g instanceof Xa) || g instanceof Xa && g.getState() === z.EMPTY)
        return null;
      if (g.getState() !== z.LOADED)
        continue;
      const m = c.getOrigin(d), _ = fe(c.getTileSize(d)), y = c.getResolution(d), p = Math.floor(
        u * ((s[0] - m[0]) / y - f[1] * _[0])
      ), v = Math.floor(
        u * ((m[1] - s[1]) / y - f[2] * _[1])
      ), x = Math.round(
        u * h.getGutterForProjection(l.projection)
      );
      return this.getImageData(g.getImage(), p + x, v + x);
    }
    return null;
  }
  loadedTileCallback(t, e, i) {
    return this.isDrawableTile(i) ? super.loadedTileCallback(t, e, i) : !1;
  }
  prepareFrame(t) {
    return !!this.getLayer().getSource();
  }
  renderFrame(t, e) {
    const i = t.layerStatesArray[t.layerIndex], s = t.viewState, r = s.projection, o = s.resolution, a = s.center, l = s.rotation, h = t.pixelRatio, c = this.getLayer(), u = c.getSource(), d = u.getRevision(), f = u.getTileGridForProjection(r), g = f.getZForResolution(o, u.zDirection), m = f.getResolution(g);
    let _ = t.extent;
    const y = t.viewState.resolution, p = u.getTilePixelRatio(h), v = Math.round(pt(_) / y * h), x = Math.round(ze(_) / y * h), C = i.extent && Mi(i.extent);
    C && (_ = Rs(
      _,
      Mi(i.extent)
    ));
    const E = m * v / 2 / p, R = m * x / 2 / p, b = [
      a[0] - E,
      a[1] - R,
      a[0] + E,
      a[1] + R
    ], F = f.getTileRangeForExtentAndZ(_, g), G = {};
    G[g] = {};
    const V = this.createLoadedTileFinder(
      u,
      r,
      G
    ), L = this.tmpExtent, $ = this.tmpTileRange_;
    this.newTiles_ = !1;
    const gt = l ? Pa(
      s.center,
      y,
      l,
      t.size
    ) : void 0;
    for (let ce = F.minX; ce <= F.maxX; ++ce)
      for (let ht = F.minY; ht <= F.maxY; ++ht) {
        if (l && !f.tileCoordIntersectsViewport([g, ce, ht], gt))
          continue;
        const _t = this.getTile(g, ce, ht, t);
        if (this.isDrawableTile(_t)) {
          const Bt = q(this);
          if (_t.getState() == z.LOADED) {
            G[g][_t.tileCoord.toString()] = _t;
            let Xe = _t.inTransition(Bt);
            Xe && i.opacity !== 1 && (_t.endTransition(Bt), Xe = !1), !this.newTiles_ && (Xe || !this.renderedTiles.includes(_t)) && (this.newTiles_ = !0);
          }
          if (_t.getAlpha(Bt, t.time) === 1)
            continue;
        }
        const ui = f.getTileCoordChildTileRange(
          _t.tileCoord,
          $,
          L
        );
        let Fe = !1;
        ui && (Fe = V(g + 1, ui)), Fe || f.forEachTileCoordParentTileRange(
          _t.tileCoord,
          V,
          $,
          L
        );
      }
    const N = m / o * h / p;
    Ii(
      this.pixelTransform,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / h,
      1 / h,
      l,
      -v / 2,
      -x / 2
    );
    const k = Yu(this.pixelTransform);
    this.useContainer(e, k, this.getBackground(t));
    const P = this.context, it = P.canvas;
    _l(this.inversePixelTransform, this.pixelTransform), Ii(
      this.tempTransform,
      v / 2,
      x / 2,
      N,
      N,
      0,
      -v / 2,
      -x / 2
    ), it.width != v || it.height != x ? (it.width = v, it.height = x) : this.containerReused || P.clearRect(0, 0, v, x), C && this.clipUnrotated(P, t, C), u.getInterpolate() || (P.imageSmoothingEnabled = !1), this.preRender(P, t), this.renderedTiles.length = 0;
    let wt = Object.keys(G).map(Number);
    wt.sort(tn);
    let yt, At, T;
    i.opacity === 1 && (!this.containerReused || u.getOpaque(t.viewState.projection)) ? wt = wt.reverse() : (yt = [], At = []);
    for (let ce = wt.length - 1; ce >= 0; --ce) {
      const ht = wt[ce], _t = u.getTilePixelSize(
        ht,
        h,
        r
      ), Fe = f.getResolution(ht) / m, Bt = _t[0] * Fe * N, Xe = _t[1] * Fe * N, mn = f.getTileCoordForCoordAndZ(
        fn(b),
        ht
      ), mr = f.getTileCoordExtent(mn), _n = Nt(this.tempTransform, [
        p * (mr[0] - b[0]) / m,
        p * (b[3] - mr[3]) / m
      ]), _r = p * u.getGutterForProjection(r), di = G[ht];
      for (const hs in di) {
        const fi = di[hs], pr = fi.tileCoord, yr = mn[1] - pr[1], vr = Math.round(_n[0] - (yr - 1) * Bt), pn = mn[2] - pr[2], Yo = Math.round(_n[1] - (pn - 1) * Xe), te = Math.round(_n[0] - yr * Bt), ye = Math.round(_n[1] - pn * Xe), Te = vr - te, Ye = Yo - ye, yn = g === ht, Gi = yn && fi.getAlpha(q(this), t.time) !== 1;
        let gi = !1;
        if (!Gi)
          if (yt) {
            T = [te, ye, te + Te, ye, te + Te, ye + Ye, te, ye + Ye];
            for (let vn = 0, xr = yt.length; vn < xr; ++vn)
              if (g !== ht && ht < At[vn]) {
                const Yt = yt[vn];
                Kt(
                  [te, ye, te + Te, ye + Ye],
                  [Yt[0], Yt[3], Yt[4], Yt[7]]
                ) && (gi || (P.save(), gi = !0), P.beginPath(), P.moveTo(T[0], T[1]), P.lineTo(T[2], T[3]), P.lineTo(T[4], T[5]), P.lineTo(T[6], T[7]), P.moveTo(Yt[6], Yt[7]), P.lineTo(Yt[4], Yt[5]), P.lineTo(Yt[2], Yt[3]), P.lineTo(Yt[0], Yt[1]), P.clip());
              }
            yt.push(T), At.push(ht);
          } else
            P.clearRect(te, ye, Te, Ye);
        this.drawTileImage(
          fi,
          t,
          te,
          ye,
          Te,
          Ye,
          _r,
          yn
        ), yt && !Gi ? (gi && P.restore(), this.renderedTiles.unshift(fi)) : this.renderedTiles.push(fi), this.updateUsedTiles(t.usedTiles, u, fi);
      }
    }
    return this.renderedRevision = d, this.renderedResolution = m, this.extentChanged = !this.renderedExtent_ || !Fs(this.renderedExtent_, b), this.renderedExtent_ = b, this.renderedPixelRatio = h, this.renderedProjection = r, this.manageTilePyramid(
      t,
      u,
      f,
      h,
      r,
      _,
      g,
      c.getPreload()
    ), this.scheduleExpireCache(t, u), this.postRender(P, t), i.extent && P.restore(), P.imageSmoothingEnabled = !0, k !== it.style.transform && (it.style.transform = k), this.container;
  }
  drawTileImage(t, e, i, s, r, o, a, l) {
    const h = this.getTileImage(t);
    if (!h)
      return;
    const c = q(this), u = e.layerStatesArray[e.layerIndex], d = u.opacity * (l ? t.getAlpha(c, e.time) : 1), f = d !== this.context.globalAlpha;
    f && (this.context.save(), this.context.globalAlpha = d), this.context.drawImage(
      h,
      a,
      a,
      h.width - 2 * a,
      h.height - 2 * a,
      i,
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
      const i = function(s, r, o) {
        const a = q(s);
        a in o.usedTiles && s.expireCache(
          o.viewState.projection,
          o.usedTiles[a]
        );
      }.bind(null, e);
      t.postRenderFunctions.push(
        i
      );
    }
  }
  updateUsedTiles(t, e, i) {
    const s = q(e);
    s in t || (t[s] = {}), t[s][i.getKey()] = !0;
  }
  manageTilePyramid(t, e, i, s, r, o, a, l, h) {
    const c = q(e);
    c in t.wantedTiles || (t.wantedTiles[c] = {});
    const u = t.wantedTiles[c], d = t.tileQueue, f = i.getMinZoom(), g = t.viewState.rotation, m = g ? Pa(
      t.viewState.center,
      t.viewState.resolution,
      g,
      t.size
    ) : void 0;
    let _ = 0, y, p, v, x, C, E;
    for (E = f; E <= a; ++E)
      for (p = i.getTileRangeForExtentAndZ(o, E, p), v = i.getResolution(E), x = p.minX; x <= p.maxX; ++x)
        for (C = p.minY; C <= p.maxY; ++C)
          g && !i.tileCoordIntersectsViewport([E, x, C], m) || (a - E <= l ? (++_, y = e.getTile(E, x, C, s, r), y.getState() == z.IDLE && (u[y.getKey()] = !0, d.isKeyQueued(y.getKey()) || d.enqueue([
            y,
            c,
            i.getTileCoordCenter(y.tileCoord),
            v
          ])), h !== void 0 && h(y)) : e.useTile(E, x, C, r));
    e.updateCacheSize(_, r);
  }
}
const Z2 = z2;
class V2 extends B2 {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new Z2(this);
  }
}
const U2 = V2;
class W2 extends cf {
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
function H2(n, t, e) {
  const i = [], s = [], r = [], o = [], a = [];
  e = e !== void 0 ? e : [];
  const l = "SupportedCRS", h = "TileMatrix", c = "Identifier", u = "ScaleDenominator", d = "TopLeftCorner", f = "TileWidth", g = "TileHeight", m = n[l], _ = Q(m), y = _.getMetersPerUnit(), p = _.getAxisOrientation().substr(0, 2) == "ne";
  return n[h].sort(function(v, x) {
    return x[u] - v[u];
  }), n[h].forEach(function(v) {
    let x;
    if (e.length > 0 ? x = e.find(function(C) {
      return v[c] == C[h] ? !0 : v[c].includes(":") ? !1 : n[c] + ":" + v[c] === C[h];
    }) : x = !0, x) {
      s.push(v[c]);
      const C = v[u] * 28e-5 / y, E = v[f], R = v[g];
      p ? r.push([
        v[d][1],
        v[d][0]
      ]) : r.push(v[d]), i.push(C), o.push(
        E == R ? E : [E, R]
      ), a.push([v.MatrixWidth, v.MatrixHeight]);
    }
  }), new W2({
    extent: t,
    origins: r,
    resolutions: i,
    matrixIds: s,
    tileSizes: o,
    sizes: a
  });
}
class X2 extends D2 {
  constructor(t) {
    const e = t.requestEncoding !== void 0 ? t.requestEncoding : "KVP", i = t.tileGrid;
    let s = t.urls;
    s === void 0 && t.url !== void 0 && (s = ff(t.url)), super({
      attributions: t.attributions,
      attributionsCollapsible: t.attributionsCollapsible,
      cacheSize: t.cacheSize,
      crossOrigin: t.crossOrigin,
      interpolate: t.interpolate,
      projection: t.projection,
      reprojectionErrorThreshold: t.reprojectionErrorThreshold,
      tileClass: t.tileClass,
      tileGrid: i,
      tileLoadFunction: t.tileLoadFunction,
      tilePixelRatio: t.tilePixelRatio,
      urls: s,
      wrapX: t.wrapX !== void 0 ? t.wrapX : !1,
      transition: t.transition,
      zDirection: t.zDirection
    }), this.version_ = t.version !== void 0 ? t.version : "1.0.0", this.format_ = t.format !== void 0 ? t.format : "image/jpeg", this.dimensions_ = t.dimensions !== void 0 ? t.dimensions : {}, this.layer_ = t.layer, this.matrixSet_ = t.matrixSet, this.style_ = t.style, this.requestEncoding_ = e, this.setKey(this.getKeyForDimensions_()), s && s.length > 0 && (this.tileUrlFunction = Ya(
      s.map(this.createFromWMTSTemplate.bind(this))
    ));
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.setTileUrlFunction(
      Ya(
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
    for (const i in this.dimensions_)
      e[t++] = i + "-" + this.dimensions_[i];
    return e.join("/");
  }
  updateDimensions(t) {
    Object.assign(this.dimensions_, t), this.setKey(this.getKeyForDimensions_());
  }
  createFromWMTSTemplate(t) {
    const e = this.requestEncoding_, i = {
      layer: this.layer_,
      style: this.style_,
      tilematrixset: this.matrixSet_
    };
    e == "KVP" && Object.assign(i, {
      Service: "WMTS",
      Request: "GetTile",
      Version: this.version_,
      Format: this.format_
    }), t = e == "KVP" ? Nc(t, i) : t.replace(/\{(\w+?)\}/g, function(o, a) {
      return a.toLowerCase() in i ? i[a.toLowerCase()] : o;
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
        return e == "KVP" ? c = Nc(c, h) : c = c.replace(/\{(\w+?)\}/g, function(u, d) {
          return h[d];
        }), c;
      } else
        return;
    };
  }
}
const Y2 = X2;
function j2(n, t) {
  const i = n.Contents.Layer.find(function(L) {
    return L.Identifier == t.layer;
  });
  if (!i)
    return null;
  const s = n.Contents.TileMatrixSet;
  let r;
  i.TileMatrixSetLink.length > 1 ? "projection" in t ? r = i.TileMatrixSetLink.findIndex(function(L) {
    const gt = s.find(function(P) {
      return P.Identifier == L.TileMatrixSet;
    }).SupportedCRS, N = Q(gt), k = Q(t.projection);
    return N && k ? Ne(N, k) : gt == t.projection;
  }) : r = i.TileMatrixSetLink.findIndex(function(L) {
    return L.TileMatrixSet == t.matrixSet;
  }) : r = 0, r < 0 && (r = 0);
  const o = i.TileMatrixSetLink[r].TileMatrixSet, a = i.TileMatrixSetLink[r].TileMatrixSetLimits;
  let l = i.Format[0];
  "format" in t && (l = t.format), r = i.Style.findIndex(function(L) {
    return "style" in t ? L.Title == t.style : L.isDefault;
  }), r < 0 && (r = 0);
  const h = i.Style[r].Identifier, c = {};
  "Dimension" in i && i.Dimension.forEach(function(L, $, gt) {
    const N = L.Identifier;
    let k = L.Default;
    k === void 0 && (k = L.Value[0]), c[N] = k;
  });
  const d = n.Contents.TileMatrixSet.find(function(L) {
    return L.Identifier == o;
  });
  let f;
  const g = d.SupportedCRS;
  if (g && (f = Q(g)), "projection" in t) {
    const L = Q(t.projection);
    L && (!f || Ne(L, f)) && (f = L);
  }
  let m = !1;
  const _ = f.getAxisOrientation().substr(0, 2) == "ne";
  let y = d.TileMatrix[0], p = {
    MinTileCol: 0,
    MinTileRow: 0,
    MaxTileCol: y.MatrixWidth - 1,
    MaxTileRow: y.MatrixHeight - 1
  };
  if (a) {
    p = a[a.length - 1];
    const L = d.TileMatrix.find(
      ($) => $.Identifier === p.TileMatrix || d.Identifier + ":" + $.Identifier === p.TileMatrix
    );
    L && (y = L);
  }
  const v = y.ScaleDenominator * 28e-5 / f.getMetersPerUnit(), x = _ ? [y.TopLeftCorner[1], y.TopLeftCorner[0]] : y.TopLeftCorner, C = y.TileWidth * v, E = y.TileHeight * v;
  let R = d.BoundingBox;
  R && _ && (R = [
    R[1],
    R[0],
    R[3],
    R[2]
  ]);
  let b = [
    x[0] + C * p.MinTileCol,
    x[1] - E * (1 + p.MaxTileRow),
    x[0] + C * (1 + p.MaxTileCol),
    x[1] - E * p.MinTileRow
  ];
  if (R !== void 0 && !Vi(R, b)) {
    const L = i.WGS84BoundingBox, $ = Q("EPSG:4326").getExtent();
    if (b = R, L)
      m = L[0] === $[0] && L[2] === $[2];
    else {
      const gt = pd(
        R,
        d.SupportedCRS,
        "EPSG:4326"
      );
      m = gt[0] - 1e-10 <= $[0] && gt[2] + 1e-10 >= $[2];
    }
  }
  const F = H2(
    d,
    b,
    a
  ), G = [];
  let V = t.requestEncoding;
  if (V = V !== void 0 ? V : "", "OperationsMetadata" in n && "GetTile" in n.OperationsMetadata) {
    const L = n.OperationsMetadata.GetTile.DCP.HTTP.Get;
    for (let $ = 0, gt = L.length; $ < gt; ++$)
      if (L[$].Constraint) {
        const k = L[$].Constraint.find(function(P) {
          return P.name == "GetEncoding";
        }).AllowedValues.Value;
        if (V === "" && (V = k[0]), V === "KVP")
          k.includes("KVP") && G.push(L[$].href);
        else
          break;
      } else
        L[$].href && (V = "KVP", G.push(L[$].href));
  }
  return G.length === 0 && (V = "REST", i.ResourceURL.forEach(function(L) {
    L.resourceType === "tile" && (l = L.format, G.push(L.template));
  })), {
    urls: G,
    layer: t.layer,
    matrixSet: o,
    format: l,
    projection: f,
    requestEncoding: V,
    tileGrid: F,
    style: h,
    dimensions: c,
    wrapX: m,
    crossOrigin: t.crossOrigin
  };
}
class gf {
  constructor() {
    this.dataProjection = void 0, this.defaultFeatureProjection = void 0, this.supportedMediaTypes = null;
  }
  getReadOptions(t, e) {
    if (e) {
      let i = e.dataProjection ? Q(e.dataProjection) : this.readProjection(t);
      e.extent && i && i.getUnits() === "tile-pixels" && (i = Q(i), i.setWorldExtent(e.extent)), e = {
        dataProjection: i,
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
    return H();
  }
  readFeature(t, e) {
    return H();
  }
  readFeatures(t, e) {
    return H();
  }
  readGeometry(t, e) {
    return H();
  }
  readProjection(t) {
    return H();
  }
  writeFeature(t, e) {
    return H();
  }
  writeFeatures(t, e) {
    return H();
  }
  writeGeometry(t, e) {
    return H();
  }
}
function or(n, t, e) {
  const i = e ? Q(e.featureProjection) : null, s = e ? Q(e.dataProjection) : null;
  let r;
  if (i && s && !Ne(i, s) ? r = (t ? n.clone() : n).transform(
    t ? i : s,
    t ? s : i
  ) : r = n, t && e && e.decimals !== void 0) {
    const o = Math.pow(10, e.decimals), a = function(l) {
      for (let h = 0, c = l.length; h < c; ++h)
        l[h] = Math.round(l[h] * o) / o;
      return l;
    };
    r === n && (r = n.clone()), r.applyTransform(a);
  }
  return r;
}
function ih(n, t) {
  const e = t ? Q(t.featureProjection) : null, i = t ? Q(t.dataProjection) : null;
  return e && i && !Ne(e, i) ? pd(n, i, e) : n;
}
class q2 extends gf {
  constructor() {
    super();
  }
  getType() {
    return "json";
  }
  readFeature(t, e) {
    return this.readFeatureFromObject(
      $r(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatures(t, e) {
    return this.readFeaturesFromObject(
      $r(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatureFromObject(t, e) {
    return H();
  }
  readFeaturesFromObject(t, e) {
    return H();
  }
  readGeometry(t, e) {
    return this.readGeometryFromObject(
      $r(t),
      this.getReadOptions(t, e)
    );
  }
  readGeometryFromObject(t, e) {
    return H();
  }
  readProjection(t) {
    return this.readProjectionFromObject($r(t));
  }
  readProjectionFromObject(t) {
    return H();
  }
  writeFeature(t, e) {
    return JSON.stringify(this.writeFeatureObject(t, e));
  }
  writeFeatureObject(t, e) {
    return H();
  }
  writeFeatures(t, e) {
    return JSON.stringify(this.writeFeaturesObject(t, e));
  }
  writeFeaturesObject(t, e) {
    return H();
  }
  writeGeometry(t, e) {
    return JSON.stringify(this.writeGeometryObject(t, e));
  }
  writeGeometryObject(t, e) {
    return H();
  }
}
function $r(n) {
  if (typeof n == "string") {
    const t = JSON.parse(n);
    return t || null;
  } else
    return n !== null ? n : null;
}
const K2 = q2;
class J2 extends K2 {
  constructor(t) {
    t = t || {}, super(), this.dataProjection = Q(
      t.dataProjection ? t.dataProjection : "EPSG:4326"
    ), t.featureProjection && (this.defaultFeatureProjection = Q(t.featureProjection)), this.geometryName_ = t.geometryName, this.extractGeometryName_ = t.extractGeometryName, this.supportedMediaTypes = [
      "application/geo+json",
      "application/vnd.geo+json"
    ];
  }
  readFeatureFromObject(t, e) {
    let i = null;
    t.type === "Feature" ? i = t : i = {
      type: "Feature",
      geometry: t,
      properties: null
    };
    const s = ja(i.geometry, e), r = new Ie();
    return this.geometryName_ ? r.setGeometryName(this.geometryName_) : this.extractGeometryName_ && "geometry_name" in i !== void 0 && r.setGeometryName(i.geometry_name), r.setGeometry(s), "id" in i && r.setId(i.id), i.properties && r.setProperties(i.properties, !0), r;
  }
  readFeaturesFromObject(t, e) {
    const i = t;
    let s = null;
    if (i.type === "FeatureCollection") {
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
    return ja(t, e);
  }
  readProjectionFromObject(t) {
    const e = t.crs;
    let i;
    return e ? e.type == "name" ? i = Q(e.properties.name) : e.type === "EPSG" ? i = Q("EPSG:" + e.properties.code) : Y(!1, 36) : i = this.dataProjection, i;
  }
  writeFeatureObject(t, e) {
    e = this.adaptOptions(e);
    const i = {
      type: "Feature",
      geometry: null,
      properties: null
    }, s = t.getId();
    if (s !== void 0 && (i.id = s), !t.hasProperties())
      return i;
    const r = t.getProperties(), o = t.getGeometry();
    return o && (i.geometry = qa(o, e), delete r[t.getGeometryName()]), Hn(r) || (i.properties = r), i;
  }
  writeFeaturesObject(t, e) {
    e = this.adaptOptions(e);
    const i = [];
    for (let s = 0, r = t.length; s < r; ++s)
      i.push(this.writeFeatureObject(t[s], e));
    return {
      type: "FeatureCollection",
      features: i
    };
  }
  writeGeometryObject(t, e) {
    return qa(t, this.adaptOptions(e));
  }
}
function ja(n, t) {
  if (!n)
    return null;
  let e;
  switch (n.type) {
    case "Point": {
      e = tp(n);
      break;
    }
    case "LineString": {
      e = ep(
        n
      );
      break;
    }
    case "Polygon": {
      e = rp(n);
      break;
    }
    case "MultiPoint": {
      e = np(
        n
      );
      break;
    }
    case "MultiLineString": {
      e = ip(
        n
      );
      break;
    }
    case "MultiPolygon": {
      e = sp(
        n
      );
      break;
    }
    case "GeometryCollection": {
      e = Q2(
        n
      );
      break;
    }
    default:
      throw new Error("Unsupported GeoJSON type: " + n.type);
  }
  return or(e, !1, t);
}
function Q2(n, t) {
  const e = n.geometries.map(
    function(i) {
      return ja(i, t);
    }
  );
  return new of(e);
}
function tp(n) {
  return new Se(n.coordinates);
}
function ep(n) {
  return new li(n.coordinates);
}
function ip(n) {
  return new sr(n.coordinates);
}
function np(n) {
  return new $o(n.coordinates);
}
function sp(n) {
  return new rr(n.coordinates);
}
function rp(n) {
  return new Ai(n.coordinates);
}
function qa(n, t) {
  n = or(n, !0, t);
  const e = n.getType();
  let i;
  switch (e) {
    case "Point": {
      i = up(n);
      break;
    }
    case "LineString": {
      i = ap(
        n
      );
      break;
    }
    case "Polygon": {
      i = dp(
        n,
        t
      );
      break;
    }
    case "MultiPoint": {
      i = hp(
        n
      );
      break;
    }
    case "MultiLineString": {
      i = lp(
        n
      );
      break;
    }
    case "MultiPolygon": {
      i = cp(
        n,
        t
      );
      break;
    }
    case "GeometryCollection": {
      i = op(
        n,
        t
      );
      break;
    }
    case "Circle": {
      i = {
        type: "GeometryCollection",
        geometries: []
      };
      break;
    }
    default:
      throw new Error("Unsupported geometry type: " + e);
  }
  return i;
}
function op(n, t) {
  return t = Object.assign({}, t), delete t.featureProjection, {
    type: "GeometryCollection",
    geometries: n.getGeometriesArray().map(function(i) {
      return qa(i, t);
    })
  };
}
function ap(n, t) {
  return {
    type: "LineString",
    coordinates: n.getCoordinates()
  };
}
function lp(n, t) {
  return {
    type: "MultiLineString",
    coordinates: n.getCoordinates()
  };
}
function hp(n, t) {
  return {
    type: "MultiPoint",
    coordinates: n.getCoordinates()
  };
}
function cp(n, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "MultiPolygon",
    coordinates: n.getCoordinates(e)
  };
}
function up(n, t) {
  return {
    type: "Point",
    coordinates: n.getCoordinates()
  };
}
function dp(n, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "Polygon",
    coordinates: n.getCoordinates(e)
  };
}
const mf = J2;
let _f = "", pf = !1, yf = "", vf, xf, Cf, Kn = [], Mf, Ef = -1, wf = -1;
function fp(n) {
  _f = n;
}
function gp() {
  return _f;
}
function mp(n) {
  pf = n;
}
function _p() {
  return pf;
}
function pp(n) {
  yf = n;
}
function yp() {
  return yf;
}
function vp(n) {
  vf = n;
}
function xp() {
  return vf;
}
function Cp(n) {
  xf = n;
}
function Mp() {
  return xf;
}
function Ep(n) {
  Cf = n;
}
function wp() {
  return Cf;
}
function Sp(n) {
  Kn.push(n);
}
function Rp(n, t) {
  const e = Kn.findIndex((i) => i.get(t) === n);
  e !== -1 && Kn.splice(e, 1);
}
function Tp(n, t) {
  const e = Kn.findIndex((i) => i.get(t) === n);
  return e !== -1 ? Kn[e] : void 0;
}
function bp() {
  return Kn;
}
function Lp(n) {
  Mf = n;
}
function Ip() {
  return Mf;
}
function Pp(n) {
  Ef = n;
}
function Ap() {
  return Ef;
}
function Op(n) {
  wf = n;
}
function Fp() {
  return wf;
}
function w() {
  return {
    setTheme: fp,
    getTheme: gp,
    setCustomDisplay: mp,
    isCustomDisplay: _p,
    setTargetBoxSize: pp,
    getTargetBoxSize: yp,
    setGeolocation: vp,
    getGeolocation: xp,
    setOptions: Cp,
    getOptions: Mp,
    setMap: Ep,
    getMap: wp,
    addSelectedFeature: Sp,
    removeSelectedFeature: Rp,
    getSelectedFeature: Tp,
    getSelectedFeatures: bp,
    setBorderConstraint: Lp,
    getBorderConstraint: Ip,
    setCurrentItemId: Pp,
    getCurrentItemId: Ap,
    setMaxElement: Op,
    getMaxElement: Fp
  };
}
class Np {
  constructor() {
    this.nbDraw = 0, this.source = new Ve(), this.vector = new Ze({
      source: this.source,
      style: new Zt({
        fill: new Vt({
          color: "rgba(255, 255, 255, 0.2)"
        }),
        stroke: new Xt({
          color: "#ffcc33",
          width: 2
        }),
        image: new we({
          radius: 7,
          fill: new Vt({
            color: "#ffcc33"
          })
        })
      })
    }), w().getMap().addLayer(this.vector), this.modify = new u2({ source: this.source }), w().getMap().addInteraction(this.modify), this.addInteraction();
  }
  removeInteraction() {
    this.draw && w().getMap().removeInteraction(this.draw), this.snap && w().getMap().removeInteraction(this.snap);
  }
  couldContinueToDraw() {
    w().getOptions().maxNbDraw != -1 && (this.nbDraw += 1, this.nbDraw >= w().getOptions().maxNbDraw && this.draw && this.draw.addEventListener("drawend", this.removeInteraction.bind(this)));
  }
  addInteraction() {
    this.draw = new a2({
      source: this.source,
      type: w().getOptions().drawElement
    }), w().getMap().addInteraction(this.draw), this.snap = new f2({ source: this.source }), w().getMap().addInteraction(this.snap), this.draw.addEventListener("drawstart", this.couldContinueToDraw.bind(this));
  }
}
class Dp {
  constructor() {
    this.data = {}, this.vectorSource = new Ve(), this.vectorLayer = new Ze(), fetch(w().getOptions().geojson.url).then((t) => t.json()).then((t) => {
      this.vectorSource = new Ve({
        features: new mf().readFeatures(t)
      }), this.vectorLayer = new Ze({
        source: this.vectorSource,
        style: this.styleFunction
      }), w().getMap().addLayer(this.vectorLayer);
    });
  }
  styleFunction() {
    return new Zt({
      image: new we({
        radius: 5,
        fill: void 0,
        stroke: new Xt({ color: "red", width: 1 })
      })
    });
  }
}
class ot {
  static sendEvent(t, e) {
    dispatchEvent(new CustomEvent(t, { detail: e }));
  }
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Sf = { ATTRIBUTE: 1, CHILD: 2, PROPERTY: 3, BOOLEAN_ATTRIBUTE: 4, EVENT: 5, ELEMENT: 6 }, nh = (n) => (...t) => ({ _$litDirective$: n, values: t });
class sh {
  constructor(t) {
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AT(t, e, i) {
    this._$Ct = t, this._$AM = e, this._$Ci = i;
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
const { I: kp } = wg, Br = (n, t) => t === void 0 ? (n == null ? void 0 : n._$litType$) !== void 0 : (n == null ? void 0 : n._$litType$) === t, Dc = () => document.createComment(""), kc = (n, t, e) => {
  var i;
  const s = n._$AA.parentNode, r = t === void 0 ? n._$AB : t._$AA;
  if (e === void 0) {
    const o = s.insertBefore(Dc(), r), a = s.insertBefore(Dc(), r);
    e = new kp(o, a, n, n.options);
  } else {
    const o = e._$AB.nextSibling, a = e._$AM, l = a !== n;
    if (l) {
      let h;
      (i = e._$AQ) === null || i === void 0 || i.call(e, n), e._$AM = n, e._$AP !== void 0 && (h = n._$AU) !== a._$AU && e._$AP(h);
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
}, Gp = {}, Gc = (n, t = Gp) => n._$AH = t, $c = (n) => n._$AH, $p = (n) => {
  n._$AR();
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Rf = nh(class extends sh {
  constructor(n) {
    super(n), this.et = /* @__PURE__ */ new WeakMap();
  }
  render(n) {
    return [n];
  }
  update(n, [t]) {
    if (Br(this.it) && (!Br(t) || this.it.strings !== t.strings)) {
      const e = $c(n).pop();
      let i = this.et.get(this.it.strings);
      if (i === void 0) {
        const s = document.createDocumentFragment();
        i = Zu(bt, s), i.setConnected(!1), this.et.set(this.it.strings, i);
      }
      Gc(i, [e]), kc(i, void 0, e);
    }
    if (Br(t)) {
      if (!Br(this.it) || this.it.strings !== t.strings) {
        const e = this.et.get(t.strings);
        if (e !== void 0) {
          const i = $c(e).pop();
          $p(n), kc(n, void 0, i), Gc(n, [i]);
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
class Ka extends sh {
  constructor(t) {
    if (super(t), this.it = bt, t.type !== Sf.CHILD)
      throw Error(this.constructor.directiveName + "() can only be used in child bindings");
  }
  render(t) {
    if (t === bt || t == null)
      return this._t = void 0, this.it = t;
    if (t === bi)
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
Ka.directiveName = "unsafeHTML", Ka.resultType = 1;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class Ja extends Ka {
}
Ja.directiveName = "unsafeSVG", Ja.resultType = 2;
const Ue = nh(Ja), Bp = `.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color);margin-left:5px;margin-right:5px;max-width:302px;width:100%;left:calc(50% - 172px);font-family:sans-serif;display:flex;z-index:5}.box-text-container{width:70%}.box-icon-container{width:30%;display:flex}.box-element-title{display:flex}.box-element-title-text{width:900%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color);width:90%}.position-icon{display:flex;justify-content:center;width:50%}.icon-container{width:36px;height:36px;background-color:var(--select-icon-background);border-radius:var(--icon-border-radius)}.icon-container>svg{display:block;margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size)!important;height:var(--svg-icon-size)!important}.icon-container>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
class Tf {
  static getAddressFromCoordinate(t) {
    return fetch(`https://api3.geo.admin.ch/rest/services/api/MapServer/identify?mapExtent=0,0,100,100&imageDisplay=100,100,100&tolerance=20&geometryType=esriGeometryPoint&geometry=${t[0]},${t[1]}&layers=all:ch.bfs.gebaeude_wohnungs_register&returnGeometry=false&sr=2056`).then((e) => e.json());
  }
}
class at {
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
at.info = `
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
at.warning = `
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
at.error = `
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
at.mapPin = `
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
at.mapPinClick = `
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
at.mapPinSelect = `
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
at.information = `
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
at.geolocation = `
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
at.rotation = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="North">
        <g class="icon">
          <path d="M12 27.2375L16.2375 23L20.475 27.2375" class="Vector"/>
          <path d="M12 18V7L20.5 18V7" class="Vector 3"/>
        </g>
      </g>
    </svg>
  `;
at.iconRecenter = `
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
at.iconRemoveSelection = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="RemoveSelection">
        <g class="icon">
          <path d="M16 28C22.627 28 28 22.627 28 16 28 9.373 22.627 4 16 4 9.373 4 4 9.373 4 16 4 22.627 9.373 28 16 28ZM20 12 12 20M20 20 12 12" class="Vector"/>
        </g>
      </g>
    </svg>
  `;
at.search = `
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
at.cross = `
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
at.stack = `
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
var zp = Object.defineProperty, Zp = Object.getOwnPropertyDescriptor, Bo = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Zp(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && zp(t, e, s), s;
};
let Jn = class extends kt {
  constructor() {
    super(), this.currentPosition = [0, 0], this._isRecenterButton = !0, this._currentPosition = "", w().getMap().getView().on("change:center", () => {
      const n = w().getSelectedFeature(w().getCurrentItemId(), w().getOptions().mode.type === "select" ? "objectid" : "id");
      if (n) {
        const t = n.get("geom");
        this._isRecenterButton = t.intersectsExtent(w().getMap().getView().calculateExtent(w().getMap().getSize()));
      }
    }), window.addEventListener("open-select-create-box", (n) => {
      Tf.getAddressFromCoordinate(n.detail).then((t) => {
        this._currentPosition = t.results.length > 0 ? `proche de ${t.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
      });
    });
  }
  connectedCallback() {
    super.connectedCallback();
  }
  render() {
    return Lt`
      <div class="information-box-${w().getTheme()} box-element">
        <div class="box-text-container">
            <div class="box-element-title">
            <div class="box-element-title-text">${w().getOptions().selectionTargetBoxMessage}</div>
            </div>
            <div class="box-element-content">${this._currentPosition}</div>
        </div>
        <div class="box-icon-container">
          <div class="position-icon">
          ${Rf(
      this._isRecenterButton ? Lt`` : Lt`<div class="icon-container" @click="${this.recenter}">
                      ${Ue(at.iconRecenter)}
                    </div>`
    )}
          </div>
          <div class="position-icon">
            <div class="icon-container" @click="${this.unselect}">
              ${Ue(at.iconRemoveSelection)}
            </div>
          </div>
        </div>
      </div>
    `;
  }
  recenter() {
    ot.sendEvent("recenter-selected-element", void 0);
  }
  unselect() {
    const n = w().getOptions();
    n.mode.type === "select" && ot.sendEvent("icon-clicked", w().getCurrentItemId()), n.mode.type === "create" && ot.sendEvent("icon-removed", void 0);
  }
};
Jn.styles = [Mt(Bp)];
Bo([
  cn()
], Jn.prototype, "currentPosition", 2);
Bo([
  ae()
], Jn.prototype, "_isRecenterButton", 2);
Bo([
  ae()
], Jn.prototype, "_currentPosition", 2);
Jn = Bo([
  oe("select-information-box-element")
], Jn);
class bf extends Gt {
  constructor() {
    const t = document.createElement("select-information-box-element");
    super({ element: t }), this.div = t;
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
class Vp {
  static clusterWithIcon(t) {
    const e = t.get("features").length;
    let i;
    return e === 1 && t.get("features")[0].get("isSelected") ? i = new Zt({
      zIndex: 1,
      image: new Ts({
        src: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(at.mapPinSelect),
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && t.get("features")[0].get("isClick") ? i = new Zt({
      zIndex: 1,
      image: new Ts({
        src: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(at.mapPinClick),
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && !t.get("features")[0].get("isClick") ? i = new Zt({
      zIndex: 1,
      image: new Ts({
        src: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(at.mapPin),
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : t.get("features").find((s) => s.get("isClick")) ? i = new Zt({
      image: new we({
        radius: 15,
        stroke: new Xt({
          color: "#fff"
        }),
        fill: new Vt({
          color: "#EF4444"
        })
      }),
      text: new Wa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Vt({
          color: "#fff"
        })
      })
    }) : i = new Zt({
      image: new we({
        radius: 15,
        stroke: new Xt({
          color: "#fff"
        }),
        fill: new Vt({
          color: "#334155"
        })
      }),
      text: new Wa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Vt({
          color: "#fff"
        })
      })
    }), i;
  }
}
class Lf {
  static setCustomStyleWithouInfoBox() {
    const t = w().getOptions();
    w().setCustomDisplay(t.search.displaySearch);
    const e = t.search.displaySearch ? "small" : "no-box";
    w().setTargetBoxSize(e);
  }
}
const Qa = "http://www.w3.org/2001/XMLSchema-instance";
function K(n, t) {
  return Of().createElementNS(n, t);
}
function rn(n, t) {
  return If(n, t, []).join("");
}
function If(n, t, e) {
  if (n.nodeType == Node.CDATA_SECTION_NODE || n.nodeType == Node.TEXT_NODE)
    t ? e.push(String(n.nodeValue).replace(/(\r\n|\r|\n)/g, "")) : e.push(n.nodeValue);
  else {
    let i;
    for (i = n.firstChild; i; i = i.nextSibling)
      If(i, t, e);
  }
  return e;
}
function Xi(n) {
  return "documentElement" in n;
}
function Up(n, t, e) {
  return n.getAttributeNS(t, e) || "";
}
function Yi(n) {
  return new DOMParser().parseFromString(n, "application/xml");
}
function Pf(n, t) {
  return function(e, i) {
    const s = n.call(
      t !== void 0 ? t : this,
      e,
      i
    );
    if (s !== void 0) {
      const r = i[i.length - 1];
      Qt(r, s);
    }
  };
}
function X(n, t) {
  return function(e, i) {
    const s = n.call(
      t !== void 0 ? t : this,
      e,
      i
    );
    s !== void 0 && i[i.length - 1].push(s);
  };
}
function Z(n, t) {
  return function(e, i) {
    const s = n.call(
      t !== void 0 ? t : this,
      e,
      i
    );
    s !== void 0 && (i[i.length - 1] = s);
  };
}
function ge(n, t, e) {
  return function(i, s) {
    const r = n.call(
      e !== void 0 ? e : this,
      i,
      s
    );
    if (r !== void 0) {
      const o = s[s.length - 1], a = t !== void 0 ? t : i.localName;
      let l;
      a in o ? l = o[a] : (l = [], o[a] = l), l.push(r);
    }
  };
}
function O(n, t, e) {
  return function(i, s) {
    const r = n.call(
      e !== void 0 ? e : this,
      i,
      s
    );
    if (r !== void 0) {
      const o = s[s.length - 1], a = t !== void 0 ? t : i.localName;
      o[a] = r;
    }
  };
}
function M(n, t) {
  return function(e, i, s) {
    n.call(
      t !== void 0 ? t : this,
      e,
      i,
      s
    ), s[s.length - 1].node.appendChild(e);
  };
}
function me(n, t) {
  return function(e, i, s) {
    const o = i[i.length - 1].node;
    let a = n;
    a === void 0 && (a = s);
    const l = t !== void 0 ? t : o.namespaceURI;
    return K(l, a);
  };
}
const Af = me();
function dt(n, t, e) {
  e = e !== void 0 ? e : {};
  let i, s;
  for (i = 0, s = n.length; i < s; ++i)
    e[n[i]] = t;
  return e;
}
function Ji(n, t, e, i) {
  let s;
  for (s = t.firstElementChild; s; s = s.nextElementSibling) {
    const r = n[s.namespaceURI];
    if (r !== void 0) {
      const o = r[s.localName];
      o !== void 0 && o.call(i, s, e);
    }
  }
}
function B(n, t, e, i, s) {
  return i.push(n), Ji(t, e, i, s), i.pop();
}
function Wp(n, t, e, i, s, r) {
  const o = (s !== void 0 ? s : e).length;
  let a, l;
  for (let h = 0; h < o; ++h)
    a = e[h], a !== void 0 && (l = t.call(
      r !== void 0 ? r : this,
      a,
      i,
      s !== void 0 ? s[h] : void 0
    ), l !== void 0 && n[l.namespaceURI][l.localName].call(
      r,
      l,
      a,
      i
    ));
}
function St(n, t, e, i, s, r, o) {
  return s.push(n), Wp(t, e, i, s, r, o), s.pop();
}
let Ea;
function Hp() {
  return Ea === void 0 && typeof XMLSerializer < "u" && (Ea = new XMLSerializer()), Ea;
}
let wa;
function Of() {
  return wa === void 0 && typeof document < "u" && (wa = document.implementation.createDocument("", "", null)), wa;
}
class Xp extends gf {
  constructor() {
    super(), this.xmlSerializer_ = Hp();
  }
  getType() {
    return "xml";
  }
  readFeature(t, e) {
    if (t)
      if (typeof t == "string") {
        const i = Yi(t);
        return this.readFeatureFromDocument(i, e);
      } else
        return Xi(t) ? this.readFeatureFromDocument(
          t,
          e
        ) : this.readFeatureFromNode(t, e);
    else
      return null;
  }
  readFeatureFromDocument(t, e) {
    const i = this.readFeaturesFromDocument(t, e);
    return i.length > 0 ? i[0] : null;
  }
  readFeatureFromNode(t, e) {
    return null;
  }
  readFeatures(t, e) {
    if (t)
      if (typeof t == "string") {
        const i = Yi(t);
        return this.readFeaturesFromDocument(i, e);
      } else
        return Xi(t) ? this.readFeaturesFromDocument(
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
    const i = [];
    for (let s = t.firstChild; s; s = s.nextSibling)
      s.nodeType == Node.ELEMENT_NODE && Qt(
        i,
        this.readFeaturesFromNode(s, e)
      );
    return i;
  }
  readFeaturesFromNode(t, e) {
    return H();
  }
  readGeometry(t, e) {
    if (t)
      if (typeof t == "string") {
        const i = Yi(t);
        return this.readGeometryFromDocument(i, e);
      } else
        return Xi(t) ? this.readGeometryFromDocument(
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
        const e = Yi(t);
        return this.readProjectionFromDocument(e);
      } else
        return Xi(t) ? this.readProjectionFromDocument(t) : this.readProjectionFromNode(t);
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
    const i = this.writeFeatureNode(t, e);
    return this.xmlSerializer_.serializeToString(i);
  }
  writeFeatureNode(t, e) {
    return null;
  }
  writeFeatures(t, e) {
    const i = this.writeFeaturesNode(t, e);
    return this.xmlSerializer_.serializeToString(i);
  }
  writeFeaturesNode(t, e) {
    return null;
  }
  writeGeometry(t, e) {
    const i = this.writeGeometryNode(t, e);
    return this.xmlSerializer_.serializeToString(i);
  }
  writeGeometryNode(t, e) {
    return null;
  }
}
const Ff = Xp, hi = "http://www.opengis.net/gml", Yp = /^\s*$/;
class Rt extends Ff {
  constructor(t) {
    super(), t = t || {}, this.featureType = t.featureType, this.featureNS = t.featureNS, this.srsName = t.srsName, this.schemaLocation = "", this.FEATURE_COLLECTION_PARSERS = {}, this.FEATURE_COLLECTION_PARSERS[this.namespace] = {
      featureMember: X(this.readFeaturesInternal),
      featureMembers: Z(this.readFeaturesInternal)
    }, this.supportedMediaTypes = ["application/gml+xml"];
  }
  readFeaturesInternal(t, e) {
    const i = t.localName;
    let s = null;
    if (i == "FeatureCollection")
      s = B(
        [],
        this.FEATURE_COLLECTION_PARSERS,
        t,
        e,
        this
      );
    else if (i == "featureMembers" || i == "featureMember" || i == "member") {
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
              let _ = "", y = 0;
              const p = g.namespaceURI;
              for (const v in a) {
                if (a[v] === p) {
                  _ = v;
                  break;
                }
                ++y;
              }
              _ || (_ = l + y, a[_] = p), o.push(_ + ":" + m);
            }
          }
        }
        i != "featureMember" && (r.featureType = o, r.featureNS = a);
      }
      if (typeof a == "string") {
        const d = a;
        a = {}, a[h] = d;
      }
      const c = {}, u = Array.isArray(o) ? o : [o];
      for (const d in a) {
        const f = {};
        for (let g = 0, m = u.length; g < m; ++g)
          (u[g].includes(":") ? u[g].split(":")[0] : h) === d && (f[u[g].split(":").pop()] = i == "featureMembers" ? X(this.readFeatureElement, this) : Z(this.readFeatureElement, this));
        c[a[d]] = f;
      }
      i == "featureMember" || i == "member" ? s = B(void 0, c, t, e) : s = B([], c, t, e);
    }
    return s === null && (s = []), s;
  }
  readGeometryOrExtent(t, e) {
    const i = e[0];
    return i.srsName = t.firstElementChild.getAttribute("srsName"), i.srsDimension = t.firstElementChild.getAttribute("srsDimension"), B(
      null,
      this.GEOMETRY_PARSERS,
      t,
      e,
      this
    );
  }
  readExtentElement(t, e) {
    const i = e[0], s = this.readGeometryOrExtent(t, e);
    return s ? ih(s, i) : void 0;
  }
  readGeometryElement(t, e) {
    const i = e[0], s = this.readGeometryOrExtent(t, e);
    return s ? or(s, !1, i) : void 0;
  }
  readFeatureElementInternal(t, e, i) {
    let s;
    const r = {};
    for (let o = t.firstElementChild; o; o = o.nextElementSibling) {
      let a;
      const l = o.localName;
      o.childNodes.length === 0 || o.childNodes.length === 1 && (o.firstChild.nodeType === 3 || o.firstChild.nodeType === 4) ? (a = rn(o, !1), Yp.test(a) && (a = void 0)) : (i && (a = l === "boundedBy" ? this.readExtentElement(o, e) : this.readGeometryElement(o, e)), a ? l !== "boundedBy" && (s = l) : a = this.readFeatureElementInternal(o, e, !1));
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
    if (i) {
      const o = new Ie(r);
      s && o.setGeometryName(s);
      const a = t.getAttribute("fid") || Up(t, this.namespace, "id");
      return a && o.setId(a), o;
    } else
      return r;
  }
  readFeatureElement(t, e) {
    return this.readFeatureElementInternal(t, e, !0);
  }
  readPoint(t, e) {
    const i = this.readFlatCoordinatesFromNode(t, e);
    if (i)
      return new Se(i, "XYZ");
  }
  readMultiPoint(t, e) {
    const i = B(
      [],
      this.MULTIPOINT_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new $o(i);
  }
  readMultiLineString(t, e) {
    const i = B(
      [],
      this.MULTILINESTRING_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new sr(i);
  }
  readMultiPolygon(t, e) {
    const i = B(
      [],
      this.MULTIPOLYGON_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new rr(i);
  }
  pointMemberParser(t, e) {
    Ji(this.POINTMEMBER_PARSERS, t, e, this);
  }
  lineStringMemberParser(t, e) {
    Ji(this.LINESTRINGMEMBER_PARSERS, t, e, this);
  }
  polygonMemberParser(t, e) {
    Ji(this.POLYGONMEMBER_PARSERS, t, e, this);
  }
  readLineString(t, e) {
    const i = this.readFlatCoordinatesFromNode(t, e);
    if (i)
      return new li(i, "XYZ");
  }
  readFlatLinearRing(t, e) {
    const i = B(
      null,
      this.GEOMETRY_FLAT_COORDINATES_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return i;
  }
  readLinearRing(t, e) {
    const i = this.readFlatCoordinatesFromNode(t, e);
    if (i)
      return new Ba(i, "XYZ");
  }
  readPolygon(t, e) {
    const i = B(
      [null],
      this.FLAT_LINEAR_RINGS_PARSERS,
      t,
      e,
      this
    );
    if (i && i[0]) {
      const s = i[0], r = [s.length];
      let o, a;
      for (o = 1, a = i.length; o < a; ++o)
        Qt(s, i[o]), r.push(s.length);
      return new Ai(s, "XYZ", r);
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
    const i = this.readGeometryElement(t, [
      this.getReadOptions(t, e || {})
    ]);
    return i || null;
  }
  readFeaturesFromNode(t, e) {
    const i = {
      featureType: this.featureType,
      featureNS: this.featureNS
    };
    return i && Object.assign(i, this.getReadOptions(t, e)), this.readFeaturesInternal(t, [i]) || [];
  }
  readProjectionFromNode(t) {
    return Q(
      this.srsName ? this.srsName : t.firstElementChild.getAttribute("srsName")
    );
  }
}
Rt.prototype.namespace = hi;
Rt.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {}
};
Rt.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {}
};
Rt.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {}
};
Rt.prototype.MULTIPOINT_PARSERS = {
  "http://www.opengis.net/gml": {
    pointMember: X(Rt.prototype.pointMemberParser),
    pointMembers: X(Rt.prototype.pointMemberParser)
  }
};
Rt.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: X(
      Rt.prototype.lineStringMemberParser
    ),
    lineStringMembers: X(
      Rt.prototype.lineStringMemberParser
    )
  }
};
Rt.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml": {
    polygonMember: X(Rt.prototype.polygonMemberParser),
    polygonMembers: X(Rt.prototype.polygonMemberParser)
  }
};
Rt.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: X(Rt.prototype.readFlatCoordinatesFromNode)
  }
};
Rt.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: X(Rt.prototype.readLineString)
  }
};
Rt.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: X(Rt.prototype.readPolygon)
  }
};
Rt.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: Z(Rt.prototype.readFlatLinearRing)
  }
};
const J = Rt;
function jp(n) {
  const t = rn(n, !1);
  return qp(t);
}
function qp(n) {
  const t = /^\s*([+\-]?\d*\.?\d+(?:e[+\-]?\d+)?)\s*$/i.exec(n);
  if (t)
    return parseFloat(t[1]);
}
function ne(n) {
  const t = rn(n, !1);
  return Fn(t);
}
function Fn(n) {
  const t = /^\s*(\d+)\s*$/.exec(n);
  if (t)
    return parseInt(t[1], 10);
}
function rt(n) {
  return rn(n, !1).trim();
}
function It(n, t) {
  n.appendChild(Of().createTextNode(t));
}
const Kp = hi + " http://schemas.opengis.net/gml/2.1.2/feature.xsd", Jp = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class st extends J {
  constructor(t) {
    t = t || {}, super(t), this.FEATURE_COLLECTION_PARSERS[hi].featureMember = X(
      this.readFeaturesInternal
    ), this.schemaLocation = t.schemaLocation ? t.schemaLocation : Kp;
  }
  readFlatCoordinates(t, e) {
    const i = rn(t, !1).replace(/^\s*|\s*$/g, ""), r = e[0].srsName;
    let o = "enu";
    if (r) {
      const h = Q(r);
      h && (o = h.getAxisOrientation());
    }
    const a = i.trim().split(/\s+/), l = [];
    for (let h = 0, c = a.length; h < c; h++) {
      const u = a[h].split(/,+/), d = parseFloat(u[0]), f = parseFloat(u[1]), g = u.length === 3 ? parseFloat(u[2]) : 0;
      o.substr(0, 2) === "en" ? l.push(d, f, g) : l.push(f, d, g);
    }
    return l;
  }
  readBox(t, e) {
    const i = B(
      [null],
      this.BOX_PARSERS_,
      t,
      e,
      this
    );
    return _e(
      i[1][0],
      i[1][1],
      i[1][3],
      i[1][4]
    );
  }
  innerBoundaryIsParser(t, e) {
    const i = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    i && e[e.length - 1].push(i);
  }
  outerBoundaryIsParser(t, e) {
    const i = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    if (i) {
      const s = e[e.length - 1];
      s[0] = i;
    }
  }
  GEOMETRY_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1], r = s.multiSurface, o = s.surface, a = s.multiCurve;
    return Array.isArray(t) ? i = "Envelope" : (i = t.getType(), i === "MultiPolygon" && r === !0 ? i = "MultiSurface" : i === "Polygon" && o === !0 ? i = "Surface" : i === "MultiLineString" && a === !0 && (i = "MultiCurve")), K("http://www.opengis.net/gml", i);
  }
  writeFeatureElement(t, e, i) {
    const s = e.getId();
    s && t.setAttribute("fid", s);
    const r = i[i.length - 1], o = r.featureNS, a = e.getGeometryName();
    r.serializers || (r.serializers = {}, r.serializers[o] = {});
    const l = [], h = [];
    if (e.hasProperties()) {
      const u = e.getProperties();
      for (const d in u) {
        const f = u[d];
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = M(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = M(It)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, St(
      c,
      r.serializers,
      me(void 0, o),
      h,
      i,
      l
    );
  }
  writeCurveOrLineString(t, e, i) {
    const r = i[i.length - 1].srsName;
    if (t.nodeName !== "LineStringSegment" && r && t.setAttribute("srsName", r), t.nodeName === "LineString" || t.nodeName === "LineStringSegment") {
      const o = this.createCoordinatesNode_(t.namespaceURI);
      t.appendChild(o), this.writeCoordinates_(o, e, i);
    } else if (t.nodeName === "Curve") {
      const o = K(t.namespaceURI, "segments");
      t.appendChild(o), this.writeCurveSegments_(o, e, i);
    }
  }
  writeLineStringOrCurveMember(t, e, i) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, i);
    s && (t.appendChild(s), this.writeCurveOrLineString(s, e, i));
  }
  writeMultiCurveOrLineString(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName, a = s.curve;
    o && t.setAttribute("srsName", o);
    const l = e.getLineStrings();
    St(
      { node: t, hasZ: r, srsName: o, curve: a },
      this.LINESTRINGORCURVEMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      i,
      void 0,
      this
    );
  }
  writeGeometryElement(t, e, i) {
    const s = i[i.length - 1], r = Object.assign({}, s);
    r.node = t;
    let o;
    Array.isArray(e) ? o = ih(
      e,
      s
    ) : o = or(
      e,
      !0,
      s
    ), St(
      r,
      this.GEOMETRY_SERIALIZERS,
      this.GEOMETRY_NODE_FACTORY_,
      [o],
      i,
      void 0,
      this
    );
  }
  createCoordinatesNode_(t) {
    const e = K(t, "coordinates");
    return e.setAttribute("decimal", "."), e.setAttribute("cs", ","), e.setAttribute("ts", " "), e;
  }
  writeCoordinates_(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName, a = e.getCoordinates(), l = a.length, h = new Array(l);
    for (let c = 0; c < l; ++c) {
      const u = a[c];
      h[c] = this.getCoords_(u, o, r);
    }
    It(t, h.join(" "));
  }
  writeCurveSegments_(t, e, i) {
    const s = K(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, i);
  }
  writeSurfaceOrPolygon(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      St(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        i,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = K(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, i);
    }
  }
  RING_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), K(
      r.namespaceURI,
      o !== void 0 ? "innerBoundaryIs" : "outerBoundaryIs"
    );
  }
  writeSurfacePatches_(t, e, i) {
    const s = K(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, i);
  }
  writeRing(t, e, i) {
    const s = K(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, i);
  }
  getCoords_(t, e, i) {
    let s = "enu";
    e && (s = Q(e).getAxisOrientation());
    let r = s.substr(0, 2) === "en" ? t[0] + "," + t[1] : t[1] + "," + t[0];
    if (i) {
      const o = t[2] || 0;
      r += "," + o;
    }
    return r;
  }
  writePoint(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName;
    o && t.setAttribute("srsName", o);
    const a = this.createCoordinatesNode_(t.namespaceURI);
    t.appendChild(a);
    const l = e.getCoordinates(), h = this.getCoords_(l, o, r);
    It(a, h);
  }
  writeMultiPoint(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName;
    o && t.setAttribute("srsName", o);
    const a = e.getPoints();
    St(
      { node: t, hasZ: r, srsName: o },
      this.POINTMEMBER_SERIALIZERS,
      me("pointMember"),
      a,
      i,
      void 0,
      this
    );
  }
  writePointMember(t, e, i) {
    const s = K(t.namespaceURI, "Point");
    t.appendChild(s), this.writePoint(s, e, i);
  }
  writeLinearRing(t, e, i) {
    const r = i[i.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = this.createCoordinatesNode_(t.namespaceURI);
    t.appendChild(o), this.writeCoordinates_(o, e, i);
  }
  writeMultiSurfaceOrPolygon(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName, a = s.surface;
    o && t.setAttribute("srsName", o);
    const l = e.getPolygons();
    St(
      { node: t, hasZ: r, srsName: o, surface: a },
      this.SURFACEORPOLYGONMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      i,
      void 0,
      this
    );
  }
  writeSurfaceOrPolygonMember(t, e, i) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, i);
    s && (t.appendChild(s), this.writeSurfaceOrPolygon(s, e, i));
  }
  writeEnvelope(t, e, i) {
    const r = i[i.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = ["lowerCorner", "upperCorner"], a = [e[0] + " " + e[1], e[2] + " " + e[3]];
    St(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      Af,
      a,
      i,
      o,
      this
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1].node;
    return K(
      "http://www.opengis.net/gml",
      Jp[s.nodeName]
    );
  }
}
st.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    coordinates: Z(st.prototype.readFlatCoordinates)
  }
};
st.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {
    innerBoundaryIs: st.prototype.innerBoundaryIsParser,
    outerBoundaryIs: st.prototype.outerBoundaryIsParser
  }
};
st.prototype.BOX_PARSERS_ = {
  "http://www.opengis.net/gml": {
    coordinates: X(st.prototype.readFlatCoordinates)
  }
};
st.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: Z(J.prototype.readPoint),
    MultiPoint: Z(J.prototype.readMultiPoint),
    LineString: Z(J.prototype.readLineString),
    MultiLineString: Z(J.prototype.readMultiLineString),
    LinearRing: Z(J.prototype.readLinearRing),
    Polygon: Z(J.prototype.readPolygon),
    MultiPolygon: Z(J.prototype.readMultiPolygon),
    Box: Z(st.prototype.readBox)
  }
};
st.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: M(st.prototype.writeCurveOrLineString),
    MultiCurve: M(st.prototype.writeMultiCurveOrLineString),
    Point: M(st.prototype.writePoint),
    MultiPoint: M(st.prototype.writeMultiPoint),
    LineString: M(st.prototype.writeCurveOrLineString),
    MultiLineString: M(
      st.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: M(st.prototype.writeLinearRing),
    Polygon: M(st.prototype.writeSurfaceOrPolygon),
    MultiPolygon: M(
      st.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: M(st.prototype.writeSurfaceOrPolygon),
    MultiSurface: M(
      st.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: M(st.prototype.writeEnvelope)
  }
};
st.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: M(
      st.prototype.writeLineStringOrCurveMember
    ),
    curveMember: M(
      st.prototype.writeLineStringOrCurveMember
    )
  }
};
st.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    outerBoundaryIs: M(st.prototype.writeRing),
    innerBoundaryIs: M(st.prototype.writeRing)
  }
};
st.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: M(st.prototype.writePointMember)
  }
};
st.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: M(
      st.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: M(
      st.prototype.writeSurfaceOrPolygonMember
    )
  }
};
st.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: M(It),
    upperCorner: M(It)
  }
};
const ar = st, Qp = hi + " http://schemas.opengis.net/gml/3.1.1/profiles/gmlsfProfile/1.0.0/gmlsf.xsd", ty = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class D extends J {
  constructor(t) {
    t = t || {}, super(t), this.surface_ = t.surface !== void 0 ? t.surface : !1, this.curve_ = t.curve !== void 0 ? t.curve : !1, this.multiCurve_ = t.multiCurve !== void 0 ? t.multiCurve : !0, this.multiSurface_ = t.multiSurface !== void 0 ? t.multiSurface : !0, this.schemaLocation = t.schemaLocation ? t.schemaLocation : Qp, this.hasZ = t.hasZ !== void 0 ? t.hasZ : !1;
  }
  readMultiCurve(t, e) {
    const i = B(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new sr(i);
  }
  readFlatCurveRing(t, e) {
    const i = B(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    ), s = [];
    for (let r = 0, o = i.length; r < o; ++r)
      Qt(s, i[r].getFlatCoordinates());
    return s;
  }
  readMultiSurface(t, e) {
    const i = B(
      [],
      this.MULTISURFACE_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new rr(i);
  }
  curveMemberParser(t, e) {
    Ji(this.CURVEMEMBER_PARSERS, t, e, this);
  }
  surfaceMemberParser(t, e) {
    Ji(this.SURFACEMEMBER_PARSERS, t, e, this);
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
    const i = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    i && e[e.length - 1].push(i);
  }
  exteriorParser(t, e) {
    const i = B(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    if (i) {
      const s = e[e.length - 1];
      s[0] = i;
    }
  }
  readSurface(t, e) {
    const i = B(
      [null],
      this.SURFACE_PARSERS,
      t,
      e,
      this
    );
    if (i && i[0]) {
      const s = i[0], r = [s.length];
      let o, a;
      for (o = 1, a = i.length; o < a; ++o)
        Qt(s, i[o]), r.push(s.length);
      return new Ai(s, "XYZ", r);
    } else
      return;
  }
  readCurve(t, e) {
    const i = B(
      [null],
      this.CURVE_PARSERS,
      t,
      e,
      this
    );
    if (i)
      return new li(i, "XYZ");
  }
  readEnvelope(t, e) {
    const i = B(
      [null],
      this.ENVELOPE_PARSERS,
      t,
      e,
      this
    );
    return _e(
      i[1][0],
      i[1][1],
      i[2][0],
      i[2][1]
    );
  }
  readFlatPos(t, e) {
    let i = rn(t, !1);
    const s = /^\s*([+\-]?\d*\.?\d+(?:[eE][+\-]?\d+)?)\s*/, r = [];
    let o;
    for (; o = s.exec(i); )
      r.push(parseFloat(o[1])), i = i.substr(o[0].length);
    if (i !== "")
      return;
    const l = e[0].srsName;
    let h = "enu";
    if (l && (h = Q(l).getAxisOrientation()), h === "neu") {
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
    const i = rn(t, !1).replace(/^\s*|\s*$/g, ""), s = e[0], r = s.srsName, o = s.srsDimension;
    let a = "enu";
    r && (a = Q(r).getAxisOrientation());
    const l = i.split(/\s+/);
    let h = 2;
    t.getAttribute("srsDimension") ? h = Fn(t.getAttribute("srsDimension")) : t.getAttribute("dimension") ? h = Fn(t.getAttribute("dimension")) : t.parentNode.getAttribute("srsDimension") ? h = Fn(
      t.parentNode.getAttribute("srsDimension")
    ) : o && (h = Fn(o));
    let c, u, d;
    const f = [];
    for (let g = 0, m = l.length; g < m; g += h)
      c = parseFloat(l[g]), u = parseFloat(l[g + 1]), d = h === 3 ? parseFloat(l[g + 2]) : 0, a.substr(0, 2) === "en" ? f.push(c, u, d) : f.push(u, c, d);
    return f;
  }
  writePos_(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = r ? "3" : "2";
    t.setAttribute("srsDimension", o);
    const a = s.srsName;
    let l = "enu";
    a && (l = Q(a).getAxisOrientation());
    const h = e.getCoordinates();
    let c;
    if (l.substr(0, 2) === "en" ? c = h[0] + " " + h[1] : c = h[1] + " " + h[0], r) {
      const u = h[2] || 0;
      c += " " + u;
    }
    It(t, c);
  }
  getCoords_(t, e, i) {
    let s = "enu";
    e && (s = Q(e).getAxisOrientation());
    let r = s.substr(0, 2) === "en" ? t[0] + " " + t[1] : t[1] + " " + t[0];
    if (i) {
      const o = t[2] || 0;
      r += " " + o;
    }
    return r;
  }
  writePosList_(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = r ? "3" : "2";
    t.setAttribute("srsDimension", o);
    const a = s.srsName, l = e.getCoordinates(), h = l.length, c = new Array(h);
    let u;
    for (let d = 0; d < h; ++d)
      u = l[d], c[d] = this.getCoords_(u, a, r);
    It(t, c.join(" "));
  }
  writePoint(t, e, i) {
    const r = i[i.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = K(t.namespaceURI, "pos");
    t.appendChild(o), this.writePos_(o, e, i);
  }
  writeEnvelope(t, e, i) {
    const r = i[i.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = ["lowerCorner", "upperCorner"], a = [e[0] + " " + e[1], e[2] + " " + e[3]];
    St(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      Af,
      a,
      i,
      o,
      this
    );
  }
  writeLinearRing(t, e, i) {
    const r = i[i.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = K(t.namespaceURI, "posList");
    t.appendChild(o), this.writePosList_(o, e, i);
  }
  RING_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), K(
      r.namespaceURI,
      o !== void 0 ? "interior" : "exterior"
    );
  }
  writeSurfaceOrPolygon(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      St(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        i,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = K(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, i);
    }
  }
  writeCurveOrLineString(t, e, i) {
    const r = i[i.length - 1].srsName;
    if (t.nodeName !== "LineStringSegment" && r && t.setAttribute("srsName", r), t.nodeName === "LineString" || t.nodeName === "LineStringSegment") {
      const o = K(t.namespaceURI, "posList");
      t.appendChild(o), this.writePosList_(o, e, i);
    } else if (t.nodeName === "Curve") {
      const o = K(t.namespaceURI, "segments");
      t.appendChild(o), this.writeCurveSegments_(o, e, i);
    }
  }
  writeMultiSurfaceOrPolygon(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName, a = s.surface;
    o && t.setAttribute("srsName", o);
    const l = e.getPolygons();
    St(
      { node: t, hasZ: r, srsName: o, surface: a },
      this.SURFACEORPOLYGONMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      i,
      void 0,
      this
    );
  }
  writeMultiPoint(t, e, i) {
    const s = i[i.length - 1], r = s.srsName, o = s.hasZ;
    r && t.setAttribute("srsName", r);
    const a = e.getPoints();
    St(
      { node: t, hasZ: o, srsName: r },
      this.POINTMEMBER_SERIALIZERS,
      me("pointMember"),
      a,
      i,
      void 0,
      this
    );
  }
  writeMultiCurveOrLineString(t, e, i) {
    const s = i[i.length - 1], r = s.hasZ, o = s.srsName, a = s.curve;
    o && t.setAttribute("srsName", o);
    const l = e.getLineStrings();
    St(
      { node: t, hasZ: r, srsName: o, curve: a },
      this.LINESTRINGORCURVEMEMBER_SERIALIZERS,
      this.MULTIGEOMETRY_MEMBER_NODE_FACTORY_,
      l,
      i,
      void 0,
      this
    );
  }
  writeRing(t, e, i) {
    const s = K(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, i);
  }
  writeSurfaceOrPolygonMember(t, e, i) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, i);
    s && (t.appendChild(s), this.writeSurfaceOrPolygon(s, e, i));
  }
  writePointMember(t, e, i) {
    const s = K(t.namespaceURI, "Point");
    t.appendChild(s), this.writePoint(s, e, i);
  }
  writeLineStringOrCurveMember(t, e, i) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, i);
    s && (t.appendChild(s), this.writeCurveOrLineString(s, e, i));
  }
  writeSurfacePatches_(t, e, i) {
    const s = K(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, i);
  }
  writeCurveSegments_(t, e, i) {
    const s = K(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, i);
  }
  writeGeometryElement(t, e, i) {
    const s = i[i.length - 1], r = Object.assign({}, s);
    r.node = t;
    let o;
    Array.isArray(e) ? o = ih(
      e,
      s
    ) : o = or(
      e,
      !0,
      s
    ), St(
      r,
      this.GEOMETRY_SERIALIZERS,
      this.GEOMETRY_NODE_FACTORY_,
      [o],
      i,
      void 0,
      this
    );
  }
  writeFeatureElement(t, e, i) {
    const s = e.getId();
    s && t.setAttribute("fid", s);
    const r = i[i.length - 1], o = r.featureNS, a = e.getGeometryName();
    r.serializers || (r.serializers = {}, r.serializers[o] = {});
    const l = [], h = [];
    if (e.hasProperties()) {
      const u = e.getProperties();
      for (const d in u) {
        const f = u[d];
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = M(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = M(It)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, St(
      c,
      r.serializers,
      me(void 0, o),
      h,
      i,
      l
    );
  }
  writeFeatureMembers_(t, e, i) {
    const s = i[i.length - 1], r = s.featureType, o = s.featureNS, a = {};
    a[o] = {}, a[o][r] = M(
      this.writeFeatureElement,
      this
    );
    const l = Object.assign({}, s);
    l.node = t, St(
      l,
      a,
      me(r, o),
      e,
      i
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1].node;
    return K(
      this.namespace,
      ty[s.nodeName]
    );
  }
  GEOMETRY_NODE_FACTORY_(t, e, i) {
    const s = e[e.length - 1], r = s.multiSurface, o = s.surface, a = s.curve, l = s.multiCurve;
    return Array.isArray(t) ? i = "Envelope" : (i = t.getType(), i === "MultiPolygon" && r === !0 ? i = "MultiSurface" : i === "Polygon" && o === !0 ? i = "Surface" : i === "LineString" && a === !0 ? i = "Curve" : i === "MultiLineString" && l === !0 && (i = "MultiCurve")), K(this.namespace, i);
  }
  writeGeometryNode(t, e) {
    e = this.adaptOptions(e);
    const i = K(this.namespace, "geom"), s = {
      node: i,
      hasZ: this.hasZ,
      srsName: this.srsName,
      curve: this.curve_,
      surface: this.surface_,
      multiSurface: this.multiSurface_,
      multiCurve: this.multiCurve_
    };
    return e && Object.assign(s, e), this.writeGeometryElement(i, t, [s]), i;
  }
  writeFeaturesNode(t, e) {
    e = this.adaptOptions(e);
    const i = K(this.namespace, "featureMembers");
    i.setAttributeNS(
      Qa,
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
    return e && Object.assign(s, e), this.writeFeatureMembers_(i, t, [s]), i;
  }
}
D.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    pos: Z(D.prototype.readFlatPos),
    posList: Z(D.prototype.readFlatPosList),
    coordinates: Z(ar.prototype.readFlatCoordinates)
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
    Point: Z(J.prototype.readPoint),
    MultiPoint: Z(J.prototype.readMultiPoint),
    LineString: Z(J.prototype.readLineString),
    MultiLineString: Z(J.prototype.readMultiLineString),
    LinearRing: Z(J.prototype.readLinearRing),
    Polygon: Z(J.prototype.readPolygon),
    MultiPolygon: Z(J.prototype.readMultiPolygon),
    Surface: Z(D.prototype.readSurface),
    MultiSurface: Z(D.prototype.readMultiSurface),
    Curve: Z(D.prototype.readCurve),
    MultiCurve: Z(D.prototype.readMultiCurve),
    Envelope: Z(D.prototype.readEnvelope)
  }
};
D.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml": {
    curveMember: X(D.prototype.curveMemberParser),
    curveMembers: X(D.prototype.curveMemberParser)
  }
};
D.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: X(D.prototype.surfaceMemberParser),
    surfaceMembers: X(D.prototype.surfaceMemberParser)
  }
};
D.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: X(J.prototype.readLineString),
    Curve: X(D.prototype.readCurve)
  }
};
D.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: X(J.prototype.readPolygon),
    Surface: X(D.prototype.readSurface)
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
    lowerCorner: X(D.prototype.readFlatPosList),
    upperCorner: X(D.prototype.readFlatPosList)
  }
};
D.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml": {
    PolygonPatch: Z(D.prototype.readPolygonPatch)
  }
};
D.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml": {
    LineStringSegment: Pf(
      D.prototype.readLineStringSegment
    )
  }
};
J.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: Z(J.prototype.readFlatLinearRing),
    Ring: Z(D.prototype.readFlatCurveRing)
  }
};
D.prototype.writeFeatures;
D.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    exterior: M(D.prototype.writeRing),
    interior: M(D.prototype.writeRing)
  }
};
D.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: M(It),
    upperCorner: M(It)
  }
};
D.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: M(
      D.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: M(
      D.prototype.writeSurfaceOrPolygonMember
    )
  }
};
D.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: M(D.prototype.writePointMember)
  }
};
D.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: M(
      D.prototype.writeLineStringOrCurveMember
    ),
    curveMember: M(
      D.prototype.writeLineStringOrCurveMember
    )
  }
};
D.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: M(D.prototype.writeCurveOrLineString),
    MultiCurve: M(D.prototype.writeMultiCurveOrLineString),
    Point: M(D.prototype.writePoint),
    MultiPoint: M(D.prototype.writeMultiPoint),
    LineString: M(D.prototype.writeCurveOrLineString),
    MultiLineString: M(
      D.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: M(D.prototype.writeLinearRing),
    Polygon: M(D.prototype.writeSurfaceOrPolygon),
    MultiPolygon: M(
      D.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: M(D.prototype.writeSurfaceOrPolygon),
    MultiSurface: M(
      D.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: M(D.prototype.writeEnvelope)
  }
};
const tt = D;
class lt extends tt {
  constructor(t) {
    t = t || {}, super(t), this.schemaLocation = t.schemaLocation ? t.schemaLocation : this.namespace + " http://schemas.opengis.net/gml/3.2.1/gml.xsd";
  }
}
lt.prototype.namespace = "http://www.opengis.net/gml/3.2";
lt.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pos: Z(tt.prototype.readFlatPos),
    posList: Z(tt.prototype.readFlatPosList),
    coordinates: Z(ar.prototype.readFlatCoordinates)
  }
};
lt.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    interior: tt.prototype.interiorParser,
    exterior: tt.prototype.exteriorParser
  }
};
lt.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: Z(J.prototype.readPoint),
    MultiPoint: Z(J.prototype.readMultiPoint),
    LineString: Z(J.prototype.readLineString),
    MultiLineString: Z(J.prototype.readMultiLineString),
    LinearRing: Z(J.prototype.readLinearRing),
    Polygon: Z(J.prototype.readPolygon),
    MultiPolygon: Z(J.prototype.readMultiPolygon),
    Surface: Z(lt.prototype.readSurface),
    MultiSurface: Z(tt.prototype.readMultiSurface),
    Curve: Z(lt.prototype.readCurve),
    MultiCurve: Z(tt.prototype.readMultiCurve),
    Envelope: Z(lt.prototype.readEnvelope)
  }
};
lt.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    curveMember: X(tt.prototype.curveMemberParser),
    curveMembers: X(tt.prototype.curveMemberParser)
  }
};
lt.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: X(tt.prototype.surfaceMemberParser),
    surfaceMembers: X(tt.prototype.surfaceMemberParser)
  }
};
lt.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: X(J.prototype.readLineString),
    Curve: X(tt.prototype.readCurve)
  }
};
lt.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: X(J.prototype.readPolygon),
    Surface: X(tt.prototype.readSurface)
  }
};
lt.prototype.SURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    patches: Z(tt.prototype.readPatch)
  }
};
lt.prototype.CURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    segments: Z(tt.prototype.readSegment)
  }
};
lt.prototype.ENVELOPE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: X(tt.prototype.readFlatPosList),
    upperCorner: X(tt.prototype.readFlatPosList)
  }
};
lt.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    PolygonPatch: Z(tt.prototype.readPolygonPatch)
  }
};
lt.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineStringSegment: Pf(
      tt.prototype.readLineStringSegment
    )
  }
};
lt.prototype.MULTIPOINT_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: X(J.prototype.pointMemberParser),
    pointMembers: X(J.prototype.pointMemberParser)
  }
};
lt.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: X(
      J.prototype.lineStringMemberParser
    ),
    lineStringMembers: X(
      J.prototype.lineStringMemberParser
    )
  }
};
lt.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    polygonMember: X(J.prototype.polygonMemberParser),
    polygonMembers: X(J.prototype.polygonMemberParser)
  }
};
lt.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: X(J.prototype.readFlatCoordinatesFromNode)
  }
};
lt.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: X(J.prototype.readLineString)
  }
};
lt.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: X(J.prototype.readPolygon)
  }
};
lt.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LinearRing: Z(J.prototype.readFlatLinearRing),
    Ring: Z(lt.prototype.readFlatCurveRing)
  }
};
lt.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    exterior: M(tt.prototype.writeRing),
    interior: M(tt.prototype.writeRing)
  }
};
lt.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: M(It),
    upperCorner: M(It)
  }
};
lt.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: M(
      tt.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: M(
      tt.prototype.writeSurfaceOrPolygonMember
    )
  }
};
lt.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: M(tt.prototype.writePointMember)
  }
};
lt.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: M(
      tt.prototype.writeLineStringOrCurveMember
    ),
    curveMember: M(
      tt.prototype.writeLineStringOrCurveMember
    )
  }
};
lt.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    Curve: M(tt.prototype.writeCurveOrLineString),
    MultiCurve: M(tt.prototype.writeMultiCurveOrLineString),
    Point: M(lt.prototype.writePoint),
    MultiPoint: M(tt.prototype.writeMultiPoint),
    LineString: M(tt.prototype.writeCurveOrLineString),
    MultiLineString: M(
      tt.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: M(tt.prototype.writeLinearRing),
    Polygon: M(tt.prototype.writeSurfaceOrPolygon),
    MultiPolygon: M(
      tt.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: M(tt.prototype.writeSurfaceOrPolygon),
    MultiSurface: M(
      tt.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: M(tt.prototype.writeEnvelope)
  }
};
const rh = lt;
class ey {
  constructor(t) {
    this.tagName_ = t;
  }
  getTagName() {
    return this.tagName_;
  }
}
const Nf = ey;
class iy extends Nf {
  constructor(t, e) {
    super(t), this.conditions = e, Y(this.conditions.length >= 2, 57);
  }
}
const ny = iy;
class sy extends ny {
  constructor(t) {
    super("And", Array.prototype.slice.call(arguments));
  }
}
const ry = sy;
class oy extends Nf {
  constructor(t, e, i) {
    if (super("BBOX"), this.geometryName = t, this.extent = e, e.length !== 4)
      throw new Error(
        "Expected an extent with four values ([minX, minY, maxX, maxY])"
      );
    this.srsName = i;
  }
}
const ay = oy;
function ly(n) {
  const t = [null].concat(Array.prototype.slice.call(arguments));
  return new (Function.prototype.bind.apply(ry, t))();
}
function hy(n, t, e) {
  return new ay(n, t, e);
}
const Bc = {
  "http://www.opengis.net/gml": {
    boundedBy: O(
      J.prototype.readExtentElement,
      "bounds"
    )
  },
  "http://www.opengis.net/wfs/2.0": {
    member: X(J.prototype.readFeaturesInternal)
  }
}, cy = {
  "http://www.opengis.net/wfs": {
    totalInserted: O(ne),
    totalUpdated: O(ne),
    totalDeleted: O(ne)
  },
  "http://www.opengis.net/wfs/2.0": {
    totalInserted: O(ne),
    totalUpdated: O(ne),
    totalDeleted: O(ne)
  }
}, uy = {
  "http://www.opengis.net/wfs": {
    TransactionSummary: O(
      Zc,
      "transactionSummary"
    ),
    InsertResults: O(Uc, "insertIds")
  },
  "http://www.opengis.net/wfs/2.0": {
    TransactionSummary: O(
      Zc,
      "transactionSummary"
    ),
    InsertResults: O(Uc, "insertIds")
  }
}, dy = {
  "http://www.opengis.net/wfs": {
    PropertyName: M(It)
  },
  "http://www.opengis.net/wfs/2.0": {
    PropertyName: M(It)
  }
}, Df = {
  "http://www.opengis.net/wfs": {
    Insert: M(Wc),
    Update: M(Xc),
    Delete: M(Hc),
    Property: M(Yc),
    Native: M(jc)
  },
  "http://www.opengis.net/wfs/2.0": {
    Insert: M(Wc),
    Update: M(Xc),
    Delete: M(Hc),
    Property: M(Yc),
    Native: M(jc)
  }
}, kf = "feature", oh = "http://www.w3.org/2000/xmlns/", ah = {
  "2.0.0": "http://www.opengis.net/ogc/1.1",
  "1.1.0": "http://www.opengis.net/ogc",
  "1.0.0": "http://www.opengis.net/ogc"
}, tl = {
  "2.0.0": "http://www.opengis.net/wfs/2.0",
  "1.1.0": "http://www.opengis.net/wfs",
  "1.0.0": "http://www.opengis.net/wfs"
}, lh = {
  "2.0.0": "http://www.opengis.net/fes/2.0",
  "1.1.0": "http://www.opengis.net/fes",
  "1.0.0": "http://www.opengis.net/fes"
}, zc = {
  "2.0.0": "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd",
  "1.1.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd",
  "1.0.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/wfs.xsd"
}, hh = {
  "2.0.0": rh,
  "1.1.0": tt,
  "1.0.0": ar
}, fy = "1.1.0";
class gy extends Ff {
  constructor(t) {
    super(), t = t || {}, this.version_ = t.version ? t.version : fy, this.featureType_ = t.featureType, this.featureNS_ = t.featureNS, this.gmlFormat_ = t.gmlFormat ? t.gmlFormat : new hh[this.version_](), this.schemaLocation_ = t.schemaLocation ? t.schemaLocation : zc[this.version_];
  }
  getFeatureType() {
    return this.featureType_;
  }
  setFeatureType(t) {
    this.featureType_ = t;
  }
  readFeaturesFromNode(t, e) {
    const i = {
      node: t
    };
    Object.assign(i, {
      featureType: this.featureType_,
      featureNS: this.featureNS_
    }), Object.assign(i, this.getReadOptions(t, e || {}));
    const s = [i];
    let r;
    this.version_ === "2.0.0" ? r = Bc : r = this.gmlFormat_.FEATURE_COLLECTION_PARSERS;
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
        const e = Yi(t);
        return this.readTransactionResponseFromDocument(e);
      } else
        return Xi(t) ? this.readTransactionResponseFromDocument(
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
        const e = Yi(t);
        return this.readFeatureCollectionMetadataFromDocument(e);
      } else
        return Xi(t) ? this.readFeatureCollectionMetadataFromDocument(
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
    const e = {}, i = Fn(
      t.getAttribute("numberOfFeatures")
    );
    return e.numberOfFeatures = i, B(
      e,
      Bc,
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
      uy,
      t,
      []
    );
  }
  writeGetFeature(t) {
    const e = K(tl[this.version_], "GetFeature");
    e.setAttribute("service", "WFS"), e.setAttribute("version", this.version_), t.handle && e.setAttribute("handle", t.handle), t.outputFormat && e.setAttribute("outputFormat", t.outputFormat), t.maxFeatures !== void 0 && e.setAttribute("maxFeatures", String(t.maxFeatures)), t.resultType && e.setAttribute("resultType", t.resultType), t.startIndex !== void 0 && e.setAttribute("startIndex", String(t.startIndex)), t.count !== void 0 && e.setAttribute("count", String(t.count)), t.viewParams !== void 0 && e.setAttribute("viewParams", t.viewParams), e.setAttributeNS(
      Qa,
      "xsi:schemaLocation",
      this.schemaLocation_
    );
    const i = {
      node: e
    };
    if (Object.assign(i, {
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
      )), Object.assign(i, {
        geometryName: t.geometryName,
        filter: s
      }), ru(
        e,
        t.featureTypes,
        [i]
      );
    } else
      t.featureTypes.forEach((s) => {
        const r = this.combineBboxAndFilter(
          s.geometryName,
          s.bbox,
          t.srsName,
          t.filter
        );
        Object.assign(i, {
          geometryName: s.geometryName,
          filter: r
        }), ru(e, [s.name], [i]);
      });
    return e;
  }
  combineBboxAndFilter(t, e, i, s) {
    const r = hy(t, e, i);
    return s ? ly(s, r) : r;
  }
  writeTransaction(t, e, i, s) {
    const r = [], o = s.version ? s.version : this.version_, a = K(tl[o], "Transaction");
    a.setAttribute("service", "WFS"), a.setAttribute("version", o);
    let l;
    s && (l = s.gmlOptions ? s.gmlOptions : {}, s.handle && a.setAttribute("handle", s.handle)), a.setAttributeNS(
      Qa,
      "xsi:schemaLocation",
      zc[o]
    );
    const h = my(a, l, o, s);
    return t && zr("Insert", t, r, h), e && zr("Update", e, r, h), i && zr("Delete", i, r, h), s.nativeElements && zr(
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
          const i = [{}];
          return this.gmlFormat_.readGeometryElement(e, i), Q(i.pop().srsName);
        }
    }
    return null;
  }
}
function my(n, t, e, i) {
  const s = i.featurePrefix ? i.featurePrefix : kf;
  let r;
  return e === "1.0.0" ? r = 2 : e === "1.1.0" ? r = 3 : e === "2.0.0" && (r = 3.2), Object.assign(
    { node: n },
    {
      version: e,
      featureNS: i.featureNS,
      featureType: i.featureType,
      featurePrefix: s,
      gmlVersion: r,
      hasZ: i.hasZ,
      srsName: i.srsName
    },
    t
  );
}
function zr(n, t, e, i) {
  St(
    i,
    Df,
    me(n),
    t,
    e
  );
}
function Zc(n, t) {
  return B({}, cy, n, t);
}
const _y = {
  "http://www.opengis.net/ogc": {
    FeatureId: X(function(n, t) {
      return n.getAttribute("fid");
    })
  },
  "http://www.opengis.net/ogc/1.1": {
    FeatureId: X(function(n, t) {
      return n.getAttribute("fid");
    })
  }
};
function Vc(n, t) {
  Ji(_y, n, t);
}
const py = {
  "http://www.opengis.net/wfs": {
    Feature: Vc
  },
  "http://www.opengis.net/wfs/2.0": {
    Feature: Vc
  }
};
function Uc(n, t) {
  return B([], py, n, t);
}
function Wc(n, t, e) {
  const i = e[e.length - 1], s = i.featureType, r = i.featureNS, o = i.gmlVersion, a = K(r, s);
  n.appendChild(a), o === 2 ? ar.prototype.writeFeatureElement(a, t, e) : o === 3 ? tt.prototype.writeFeatureElement(a, t, e) : rh.prototype.writeFeatureElement(a, t, e);
}
function Gf(n, t, e) {
  const s = e[e.length - 1].version, r = ah[s], o = K(r, "Filter"), a = K(r, "FeatureId");
  o.appendChild(a), a.setAttribute("fid", t), n.appendChild(o);
}
function ch(n, t) {
  n = n || kf;
  const e = n + ":";
  return t.startsWith(e) ? t : e + t;
}
function Hc(n, t, e) {
  const i = e[e.length - 1];
  Y(t.getId() !== void 0, 26);
  const s = i.featureType, r = i.featurePrefix, o = i.featureNS, a = ch(r, s);
  n.setAttribute("typeName", a), n.setAttributeNS(oh, "xmlns:" + r, o);
  const l = t.getId();
  l !== void 0 && Gf(n, l, e);
}
function Xc(n, t, e) {
  const i = e[e.length - 1];
  Y(t.getId() !== void 0, 27);
  const s = i.version, r = i.featureType, o = i.featurePrefix, a = i.featureNS, l = ch(o, r), h = t.getGeometryName();
  n.setAttribute("typeName", l), n.setAttributeNS(oh, "xmlns:" + o, a);
  const c = t.getId();
  if (c !== void 0) {
    const u = t.getKeys(), d = [];
    for (let f = 0, g = u.length; f < g; f++) {
      const m = t.get(u[f]);
      if (m !== void 0) {
        let _ = u[f];
        m && typeof m.getSimplifiedGeometry == "function" && (_ = h), d.push({ name: _, value: m });
      }
    }
    St(
      {
        version: s,
        gmlVersion: i.gmlVersion,
        node: n,
        hasZ: i.hasZ,
        srsName: i.srsName
      },
      Df,
      me("Property"),
      d,
      e
    ), Gf(n, c, e);
  }
}
function Yc(n, t, e) {
  const i = e[e.length - 1], s = i.version, r = tl[s], o = K(r, "Name"), a = i.gmlVersion;
  if (n.appendChild(o), It(o, t.name), t.value !== void 0 && t.value !== null) {
    const l = K(r, "Value");
    n.appendChild(l), t.value && typeof t.value.getSimplifiedGeometry == "function" ? a === 2 ? ar.prototype.writeGeometryElement(l, t.value, e) : a === 3 ? tt.prototype.writeGeometryElement(l, t.value, e) : rh.prototype.writeGeometryElement(l, t.value, e) : It(l, t.value);
  }
}
function jc(n, t, e) {
  t.vendorId && n.setAttribute("vendorId", t.vendorId), t.safeToIgnore !== void 0 && n.setAttribute("safeToIgnore", String(t.safeToIgnore)), t.value !== void 0 && It(n, t.value);
}
const zo = {
  "http://www.opengis.net/wfs": {
    Query: M(qc)
  },
  "http://www.opengis.net/wfs/2.0": {
    Query: M(qc)
  },
  "http://www.opengis.net/ogc": {
    During: M(Qc),
    And: M(Zr),
    Or: M(Zr),
    Not: M(tu),
    BBOX: M(Kc),
    Contains: M(xi),
    Intersects: M(xi),
    Within: M(xi),
    DWithin: M(Jc),
    PropertyIsEqualTo: M(Ce),
    PropertyIsNotEqualTo: M(Ce),
    PropertyIsLessThan: M(Ce),
    PropertyIsLessThanOrEqualTo: M(Ce),
    PropertyIsGreaterThan: M(Ce),
    PropertyIsGreaterThanOrEqualTo: M(Ce),
    PropertyIsNull: M(eu),
    PropertyIsBetween: M(iu),
    PropertyIsLike: M(nu)
  },
  "http://www.opengis.net/fes/2.0": {
    During: M(Qc),
    And: M(Zr),
    Or: M(Zr),
    Not: M(tu),
    BBOX: M(Kc),
    Contains: M(xi),
    Disjoint: M(xi),
    Intersects: M(xi),
    ResourceId: M(vy),
    Within: M(xi),
    DWithin: M(Jc),
    PropertyIsEqualTo: M(Ce),
    PropertyIsNotEqualTo: M(Ce),
    PropertyIsLessThan: M(Ce),
    PropertyIsLessThanOrEqualTo: M(Ce),
    PropertyIsGreaterThan: M(Ce),
    PropertyIsGreaterThanOrEqualTo: M(Ce),
    PropertyIsNull: M(eu),
    PropertyIsBetween: M(iu),
    PropertyIsLike: M(nu)
  }
};
function qc(n, t, e) {
  const i = e[e.length - 1], s = i.version, r = i.featurePrefix, o = i.featureNS, a = i.propertyNames, l = i.srsName;
  let h;
  r ? h = ch(r, t) : h = t;
  let c;
  s === "2.0.0" ? c = "typeNames" : c = "typeName", n.setAttribute(c, h), l && n.setAttribute("srsName", l), o && n.setAttributeNS(oh, "xmlns:" + r, o);
  const u = Object.assign({}, i);
  u.node = n, St(
    u,
    dy,
    me("PropertyName"),
    a,
    e
  );
  const d = i.filter;
  if (d) {
    const f = K(Zo(s), "Filter");
    n.appendChild(f), yy(f, d, e);
  }
}
function yy(n, t, e) {
  const i = e[e.length - 1], s = { node: n };
  Object.assign(s, { context: i }), St(
    s,
    zo,
    me(t.getTagName()),
    [t],
    e
  );
}
function Kc(n, t, e) {
  const i = e[e.length - 1], r = i.context.version;
  i.srsName = t.srsName;
  const o = hh[r];
  os(r, n, t.geometryName), o.prototype.writeGeometryElement(n, t.extent, e);
}
function vy(n, t, e) {
  n.setAttribute("rid", t.rid);
}
function xi(n, t, e) {
  const i = e[e.length - 1], r = i.context.version;
  i.srsName = t.srsName;
  const o = hh[r];
  os(r, n, t.geometryName), o.prototype.writeGeometryElement(n, t.geometry, e);
}
function Jc(n, t, e) {
  const r = e[e.length - 1].context.version;
  xi(n, t, e);
  const o = K(Zo(r), "Distance");
  It(o, t.distance.toString()), r === "2.0.0" ? o.setAttribute("uom", t.unit) : o.setAttribute("units", t.unit), n.appendChild(o);
}
function Qc(n, t, e) {
  const r = e[e.length - 1].context.version;
  po(lh[r], "ValueReference", n, t.propertyName);
  const o = K(hi, "TimePeriod");
  n.appendChild(o);
  const a = K(hi, "begin");
  o.appendChild(a), su(a, t.begin);
  const l = K(hi, "end");
  o.appendChild(l), su(l, t.end);
}
function Zr(n, t, e) {
  const s = e[e.length - 1].context, r = { node: n };
  Object.assign(r, { context: s });
  const o = t.conditions;
  for (let a = 0, l = o.length; a < l; ++a) {
    const h = o[a];
    St(
      r,
      zo,
      me(h.getTagName()),
      [h],
      e
    );
  }
}
function tu(n, t, e) {
  const s = e[e.length - 1].context, r = { node: n };
  Object.assign(r, { context: s });
  const o = t.condition;
  St(
    r,
    zo,
    me(o.getTagName()),
    [o],
    e
  );
}
function Ce(n, t, e) {
  const r = e[e.length - 1].context.version;
  t.matchCase !== void 0 && n.setAttribute("matchCase", t.matchCase.toString()), os(r, n, t.propertyName), yo(r, n, "" + t.expression);
}
function eu(n, t, e) {
  const r = e[e.length - 1].context.version;
  os(r, n, t.propertyName);
}
function iu(n, t, e) {
  const r = e[e.length - 1].context.version, o = Zo(r);
  os(r, n, t.propertyName);
  const a = K(o, "LowerBoundary");
  n.appendChild(a), yo(r, a, "" + t.lowerBoundary);
  const l = K(o, "UpperBoundary");
  n.appendChild(l), yo(r, l, "" + t.upperBoundary);
}
function nu(n, t, e) {
  const r = e[e.length - 1].context.version;
  n.setAttribute("wildCard", t.wildCard), n.setAttribute("singleChar", t.singleChar), n.setAttribute("escapeChar", t.escapeChar), t.matchCase !== void 0 && n.setAttribute("matchCase", t.matchCase.toString()), os(r, n, t.propertyName), yo(r, n, "" + t.pattern);
}
function po(n, t, e, i) {
  const s = K(n, t);
  It(s, i), e.appendChild(s);
}
function yo(n, t, e) {
  po(Zo(n), "Literal", t, e);
}
function os(n, t, e) {
  n === "2.0.0" ? po(lh[n], "ValueReference", t, e) : po(ah[n], "PropertyName", t, e);
}
function su(n, t) {
  const e = K(hi, "TimeInstant");
  n.appendChild(e);
  const i = K(hi, "timePosition");
  e.appendChild(i), It(i, t);
}
function ru(n, t, e) {
  const i = e[e.length - 1], s = Object.assign({}, i);
  s.node = n, St(
    s,
    zo,
    me("Query"),
    t,
    e
  );
}
function Zo(n) {
  let t;
  return n === "2.0.0" ? t = lh[n] : t = ah[n], t;
}
const xy = gy;
class $f {
  static getSource(t, e) {
    return new Ve({
      format: new xy({
        version: "2.0.0"
      }),
      url: function(i) {
        if (e === "")
          t + "" + i.join(",");
        else if (e.includes("<BBOX>")) {
          const s = `<BBOX><ValueReference>geometry</ValueReference><Envelope srsName="urn:ogc:def:crs:EPSG::2056"><lowerCorner>${i[0]} ${i[1]}</lowerCorner><upperCorner>${i[2]} ${i[3]}</upperCorner></Envelope></BBOX>`;
          t = `${t}&${e}`.replace("<BBOX>", s);
        } else
          console.error("The replacement string <BBOX> cannot be found. You lose the BBOX optimization."), t = `${t}&${e}`;
        return t;
      },
      strategy: F_
    });
  }
}
class Cy {
  constructor() {
    this.control = new bf(), this.store = w();
    const t = this.store.getMap(), e = this.store.getOptions(), i = new Ze(), s = $f.getSource(this.store.getOptions().wfs.url, "");
    this.displayDataOnMap(t, i, e, s), t.on("click", (r) => {
      t.forEachFeatureAtPixel(r.pixel, (o) => {
        var a;
        o && ((a = o.getGeometry()) == null ? void 0 : a.getType()) === "Point" && o.getProperties().features.length === 1 && (this.store.getSelectedFeature(o.getProperties().features[0].get("objectid"), "objectid") === void 0 && this.store.addSelectedFeature(o.getProperties().features[0]), ot.sendEvent("icon-clicked", o.getProperties().features[0].get("objectid")));
      });
    }), window.addEventListener("recenter-selected-element", () => {
      var a;
      const r = this.store.getCurrentItemId(), o = (a = this.store.getSelectedFeature(r, "objectid")) == null ? void 0 : a.get("geom").getCoordinates();
      t.getView().setCenter(o);
    });
  }
  displayDataOnMap(t, e, i, s) {
    const r = new G2({
      distance: i.cluster.distance,
      minDistance: i.cluster.minDistance,
      source: s
    });
    e.setSource(r), e.setStyle(function(o) {
      return Vp.clusterWithIcon(o);
    }), t.addLayer(e), this.control.disable(), t.addControl(this.control), this.toogleDataSelection(e);
  }
  setCurrentElement(t) {
    var e;
    (e = this.store.getSelectedFeature(this.store.getCurrentItemId(), "objectid")) == null || e.set("isSelected", void 0), this.store.setCurrentItemId(t.get("objectid"));
  }
  setIconToDisplay(t, e) {
    t.set("isClick", e), t.set("isSelected", e);
  }
  removeSelectedItem(t) {
    this.removeItem(t), this.control.hide(), ot.sendEvent("rule-validation", void 0), Lf.setCustomStyleWithouInfoBox();
  }
  removeItem(t) {
    this.setIconToDisplay(t, void 0), this.store.removeSelectedFeature(t.get("objectid"), "objectid");
  }
  setInformationBox(t) {
    this.setIconToDisplay(t, !0), this.control.show(), ot.sendEvent("open-select-create-box", t.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select");
  }
  toogleDataSelection(t) {
    window.addEventListener("authorize-clicked", (e) => {
      var s;
      const i = this.store.getSelectedFeature(e.detail, "objectid");
      i && (i.get("isClick") ? this.store.getMaxElement() === 1 || this.store.getCurrentItemId() === i.get("objectid") ? this.removeSelectedItem(i) : (this.setCurrentElement(i), i.set("isSelected", !0), ot.sendEvent("open-select-create-box", i.get("geom").getCoordinates()), this.control.show()) : this.store.getMaxElement() === 1 ? ((s = t.getSource()) == null || s.getFeatures().forEach((o) => {
        o.get("features").forEach((a) => {
          a.get("isClick") && (this.setIconToDisplay(a, void 0), this.store.removeSelectedFeature(a.get("objectid"), "objectid"));
        });
      }), this.store.setCurrentItemId(i.get("objectid")), ot.sendEvent("rule-validation", void 0), this.setInformationBox(i)) : this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement() ? (this.setCurrentElement(i), this.setInformationBox(i)) : this.removeItem(i)), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
    });
  }
}
class My {
  constructor() {
    var e;
    this.vectorLayer = new Ze(), this.vectorSource = new Ve();
    const t = w().getGeolocation();
    if (t) {
      const i = new Ie();
      i.setStyle(
        new Zt({
          image: new we({
            radius: 6,
            fill: new Vt({
              color: "#3399CC"
            }),
            stroke: new Xt({
              color: "#fff",
              width: 2
            })
          })
        })
      ), t.on("change:position", function() {
        const s = t.getPosition();
        i.setGeometry(s ? new Se(s) : void 0);
      }), (e = this.vectorSource) == null || e.addFeature(i), this.vectorLayer.setSource(this.vectorSource), w().getMap().addLayer(this.vectorLayer);
    }
  }
}
class Ey {
  read(t) {
    if (t)
      if (typeof t == "string") {
        const e = Yi(t);
        return this.readFromDocument(e);
      } else
        return Xi(t) ? this.readFromDocument(t) : this.readFromNode(t);
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
const Bf = Ey, wy = "http://www.w3.org/1999/xlink";
function uh(n) {
  return n.getAttributeNS(wy, "href");
}
const le = [null, "http://www.opengis.net/ows/1.1"], Sy = dt(le, {
  ServiceIdentification: O(qy),
  ServiceProvider: O(Jy),
  OperationsMetadata: O(Yy)
});
class Ry extends Bf {
  constructor() {
    super();
  }
  readFromNode(t) {
    const e = B({}, Sy, t, []);
    return e || null;
  }
}
const Ty = dt(le, {
  DeliveryPoint: O(rt),
  City: O(rt),
  AdministrativeArea: O(rt),
  PostalCode: O(rt),
  Country: O(rt),
  ElectronicMailAddress: O(rt)
}), by = dt(le, {
  Value: ge(Qy)
}), Ly = dt(le, {
  AllowedValues: O(zy)
}), Iy = dt(le, {
  Phone: O(jy),
  Address: O(By)
}), Py = dt(le, {
  HTTP: O(Hy)
}), Ay = dt(le, {
  Get: ge(Wy),
  Post: void 0
}), Oy = dt(le, {
  DCP: O(Uy)
}), Fy = dt(le, {
  Operation: Xy
}), Ny = dt(le, {
  Voice: O(rt),
  Facsimile: O(rt)
}), Dy = dt(le, {
  Constraint: ge(Zy)
}), ky = dt(le, {
  IndividualName: O(rt),
  PositionName: O(rt),
  ContactInfo: O(Vy)
}), Gy = dt(le, {
  Abstract: O(rt),
  AccessConstraints: O(rt),
  Fees: O(rt),
  Title: O(rt),
  ServiceTypeVersion: O(rt),
  ServiceType: O(rt)
}), $y = dt(le, {
  ProviderName: O(rt),
  ProviderSite: O(uh),
  ServiceContact: O(Ky)
});
function By(n, t) {
  return B({}, Ty, n, t);
}
function zy(n, t) {
  return B({}, by, n, t);
}
function Zy(n, t) {
  const e = n.getAttribute("name");
  if (!!e)
    return B({ name: e }, Ly, n, t);
}
function Vy(n, t) {
  return B({}, Iy, n, t);
}
function Uy(n, t) {
  return B({}, Py, n, t);
}
function Wy(n, t) {
  const e = uh(n);
  if (!!e)
    return B(
      { href: e },
      Dy,
      n,
      t
    );
}
function Hy(n, t) {
  return B({}, Ay, n, t);
}
function Xy(n, t) {
  const e = n.getAttribute("name"), i = B({}, Oy, n, t);
  if (!i)
    return;
  const s = t[t.length - 1];
  s[e] = i;
}
function Yy(n, t) {
  return B({}, Fy, n, t);
}
function jy(n, t) {
  return B({}, Ny, n, t);
}
function qy(n, t) {
  return B({}, Gy, n, t);
}
function Ky(n, t) {
  return B({}, ky, n, t);
}
function Jy(n, t) {
  return B({}, $y, n, t);
}
function Qy(n, t) {
  return rt(n);
}
const tv = Ry, He = [null, "http://www.opengis.net/wmts/1.0"], as = [null, "http://www.opengis.net/ows/1.1"], ev = dt(He, {
  Contents: O(fv)
});
class iv extends Bf {
  constructor() {
    super(), this.owsParser_ = new tv();
  }
  readFromNode(t) {
    let e = t.getAttribute("version");
    e && (e = e.trim());
    let i = this.owsParser_.readFromNode(t);
    return i ? (i.version = e, i = B(
      i,
      ev,
      t,
      []
    ), i || null) : null;
  }
}
const nv = dt(He, {
  Layer: ge(gv),
  TileMatrixSet: ge(mv)
}), sv = dt(
  He,
  {
    Style: ge(_v),
    Format: ge(rt),
    TileMatrixSetLink: ge(pv),
    Dimension: ge(yv),
    ResourceURL: ge(vv)
  },
  dt(as, {
    Title: O(rt),
    Abstract: O(rt),
    WGS84BoundingBox: O(zf),
    Identifier: O(rt)
  })
), rv = dt(
  He,
  {
    LegendURL: ge(xv)
  },
  dt(as, {
    Title: O(rt),
    Identifier: O(rt)
  })
), ov = dt(He, {
  TileMatrixSet: O(rt),
  TileMatrixSetLimits: O(Mv)
}), av = dt(He, {
  TileMatrixLimits: X(Ev)
}), lv = dt(He, {
  TileMatrix: O(rt),
  MinTileRow: O(ne),
  MaxTileRow: O(ne),
  MinTileCol: O(ne),
  MaxTileCol: O(ne)
}), hv = dt(
  He,
  {
    Default: O(rt),
    Value: ge(rt)
  },
  dt(as, {
    Identifier: O(rt)
  })
), cv = dt(as, {
  LowerCorner: X(el),
  UpperCorner: X(el)
}), uv = dt(
  He,
  {
    WellKnownScaleSet: O(rt),
    TileMatrix: ge(Cv)
  },
  dt(as, {
    SupportedCRS: O(rt),
    Identifier: O(rt),
    BoundingBox: O(zf)
  })
), dv = dt(
  He,
  {
    TopLeftCorner: O(el),
    ScaleDenominator: O(jp),
    TileWidth: O(ne),
    TileHeight: O(ne),
    MatrixWidth: O(ne),
    MatrixHeight: O(ne)
  },
  dt(as, {
    Identifier: O(rt)
  })
);
function fv(n, t) {
  return B({}, nv, n, t);
}
function gv(n, t) {
  return B({}, sv, n, t);
}
function mv(n, t) {
  return B({}, uv, n, t);
}
function _v(n, t) {
  const e = B({}, rv, n, t);
  if (!e)
    return;
  const i = n.getAttribute("isDefault") === "true";
  return e.isDefault = i, e;
}
function pv(n, t) {
  return B({}, ov, n, t);
}
function yv(n, t) {
  return B({}, hv, n, t);
}
function vv(n, t) {
  const e = n.getAttribute("format"), i = n.getAttribute("template"), s = n.getAttribute("resourceType"), r = {};
  return e && (r.format = e), i && (r.template = i), s && (r.resourceType = s), r;
}
function zf(n, t) {
  const e = B(
    [],
    cv,
    n,
    t
  );
  if (e.length == 2)
    return Ut(e);
}
function xv(n, t) {
  const e = {};
  return e.format = n.getAttribute("format"), e.href = uh(n), e;
}
function el(n, t) {
  const e = rt(n).split(/\s+/);
  if (!e || e.length != 2)
    return;
  const i = +e[0], s = +e[1];
  if (!(isNaN(i) || isNaN(s)))
    return [i, s];
}
function Cv(n, t) {
  return B({}, dv, n, t);
}
function Mv(n, t) {
  return B([], av, n, t);
}
function Ev(n, t) {
  return B({}, lv, n, t);
}
const wv = iv;
class Sv {
  constructor() {
    const t = new wv(), e = w().getOptions();
    let i = !0;
    const s = [];
    Promise.all(e.wmts.map((r) => {
      fetch(r.capability).then((o) => o.text()).then(function(o) {
        const a = new U2({
          opacity: 1
        }), l = t.read(o), h = j2(l, {
          layer: r.layer,
          matrixSet: r.projection
        });
        h && (a.setSource(new Y2(h)), a.setVisible(i), s.push(a), w().getMap().getLayers().insertAt(0, a), i = !1, w().getBorderConstraint() && a.setExtent(w().getBorderConstraint()));
      });
    })), e.borderUrl !== "" && window.addEventListener("border-contraint-enabled", () => {
      s.forEach((r) => r.setExtent(w().getBorderConstraint()));
    }), window.addEventListener("layer-selected", (r) => {
      var o;
      s.forEach((a) => a.setVisible(!1)), (o = s.find((a) => {
        const l = a.getSource();
        return l && l.getLayer() === r.detail.layer ? a : void 0;
      })) == null || o.setVisible(!0);
    });
  }
}
const Rv = `:root,:host{--ol-background-color: white;--ol-accent-background-color: #F5F5F5;--ol-subtle-background-color: rgba(128, 128, 128, .25);--ol-partial-background-color: rgba(255, 255, 255, .75);--ol-foreground-color: #333333;--ol-subtle-foreground-color: #666666;--ol-brand-color: #00AAFF}.ol-box{box-sizing:border-box;border-radius:2px;border:1.5px solid var(--ol-background-color);background-color:var(--ol-partial-background-color)}.ol-mouse-position{top:8px;right:8px;position:absolute}.ol-scale-line{background:var(--ol-partial-background-color);border-radius:4px;bottom:8px;left:8px;padding:2px;position:absolute}.ol-scale-line-inner{border:1px solid var(--ol-subtle-foreground-color);border-top:none;color:var(--ol-foreground-color);font-size:10px;text-align:center;margin:1px;will-change:contents,width;transition:all .25s}.ol-scale-bar{position:absolute;bottom:8px;left:8px}.ol-scale-bar-inner{display:flex}.ol-scale-step-marker{width:1px;height:15px;background-color:var(--ol-foreground-color);float:right;z-index:10}.ol-scale-step-text{position:absolute;bottom:-5px;font-size:10px;z-index:11;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-text{position:absolute;font-size:12px;text-align:center;bottom:25px;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-singlebar{position:relative;height:10px;z-index:9;box-sizing:border-box;border:1px solid var(--ol-foreground-color)}.ol-scale-singlebar-even{background-color:var(--ol-subtle-foreground-color)}.ol-scale-singlebar-odd{background-color:var(--ol-background-color)}.ol-unsupported{display:none}.ol-viewport,.ol-unselectable{-webkit-touch-callout:none;-webkit-user-select:none;-moz-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}.ol-viewport canvas{all:unset}.ol-selectable{-webkit-touch-callout:default;-webkit-user-select:text;-moz-user-select:text;user-select:text}.ol-grabbing{cursor:-webkit-grabbing;cursor:-moz-grabbing;cursor:grabbing}.ol-grab{cursor:move;cursor:-webkit-grab;cursor:-moz-grab;cursor:grab}.ol-control{position:absolute;background-color:var(--ol-subtle-background-color);border-radius:4px}.ol-zoom{top:.5em;left:.5em}.ol-rotate{top:.5em;right:.5em;transition:opacity .25s linear,visibility 0s linear}.ol-rotate.ol-hidden{opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s linear .25s}.ol-zoom-extent{top:4.643em;left:.5em}.ol-full-screen{right:.5em;top:.5em}.ol-control button{display:block;margin:1px;padding:0;color:var(--ol-subtle-foreground-color);font-weight:700;text-decoration:none;font-size:inherit;text-align:center;height:1.375em;width:1.375em;line-height:.4em;background-color:var(--ol-background-color);border:none;border-radius:2px}.ol-control button::-moz-focus-inner{border:none;padding:0}.ol-zoom-extent button{line-height:1.4em}.ol-compass{display:block;font-weight:400;will-change:transform}.ol-touch .ol-control button{font-size:1.5em}.ol-touch .ol-zoom-extent{top:5.5em}.ol-control button:hover,.ol-control button:focus{text-decoration:none;outline:1px solid var(--ol-subtle-foreground-color);color:var(--ol-foreground-color)}.ol-zoom .ol-zoom-in{border-radius:2px 2px 0 0}.ol-zoom .ol-zoom-out{border-radius:0 0 2px 2px}.ol-attribution{text-align:right;bottom:.5em;right:.5em;max-width:calc(100% - 1.3em);display:flex;flex-flow:row-reverse;align-items:center}.ol-attribution a{color:var(--ol-subtle-foreground-color);text-decoration:none}.ol-attribution ul{margin:0;padding:1px .5em;color:var(--ol-foreground-color);text-shadow:0 0 2px var(--ol-background-color);font-size:12px}.ol-attribution li{display:inline;list-style:none}.ol-attribution li:not(:last-child):after{content:" "}.ol-attribution img{max-height:2em;max-width:inherit;vertical-align:middle}.ol-attribution button{flex-shrink:0}.ol-attribution.ol-collapsed ul{display:none}.ol-attribution:not(.ol-collapsed){background:var(--ol-partial-background-color)}.ol-attribution.ol-uncollapsible{bottom:0;right:0;border-radius:4px 0 0}.ol-attribution.ol-uncollapsible img{margin-top:-.2em;max-height:1.6em}.ol-attribution.ol-uncollapsible button{display:none}.ol-zoomslider{top:4.5em;left:.5em;height:200px}.ol-zoomslider button{position:relative;height:10px}.ol-touch .ol-zoomslider{top:5.5em}.ol-overviewmap{left:.5em;bottom:.5em}.ol-overviewmap.ol-uncollapsible{bottom:0;left:0;border-radius:0 4px 0 0}.ol-overviewmap .ol-overviewmap-map,.ol-overviewmap button{display:block}.ol-overviewmap .ol-overviewmap-map{border:1px solid var(--ol-subtle-foreground-color);height:150px;width:150px}.ol-overviewmap:not(.ol-collapsed) button{bottom:0;left:0;position:absolute}.ol-overviewmap.ol-collapsed .ol-overviewmap-map,.ol-overviewmap.ol-uncollapsible button{display:none}.ol-overviewmap:not(.ol-collapsed){background:var(--ol-subtle-background-color)}.ol-overviewmap-box{border:1.5px dotted var(--ol-subtle-foreground-color)}.ol-overviewmap .ol-overviewmap-box:hover{cursor:move}
`, Tv = `#map{width:100%;height:100%}.ol-layer{background-color:#80808020}
`, Vo = `.left-buttons-control-container{display:flex;position:absolute;width:var(--icon-width);flex-direction:column;left:var(--side-distance)}.right-buttons-control-container{display:flex;position:absolute;right:var(--side-distance);width:var(--icon-width);flex-direction:column}.ol-zoom{position:relative;width:var(--icon-width)!important;top:0px;left:0px;background-color:var(--control-background-color)!important}.ol-full-screen{position:relative;width:var(--icon-width)!important;top:0px;right:0px;margin-top:var(--top-distance);background-color:var(--control-background-color)!important}.center-control,.rotation-control{margin-top:var(--top-distance)}.ol-zoom>button{margin:0}.ol-full-screen>button,.ol-full-screen-custom-small>button,.ol-full-screen-custom-medium>button,.ol-full-screen-custom-large>button{border-radius:var(--icon-border-radius);margin:0;cursor:pointer}.ol-zoom-in,.ol-zoom-out,.information-control,.center-control,.rotation-control,.ol-full-screen-true,.ol-full-screen-false{width:var(--icon-width)!important;height:var(--icon-height)!important;background-color:var(--control-background-color)!important;border-radius:var(--icon-border-radius);cursor:pointer}.ol-zoom-in:hover,.ol-zoom-out:hover,.information-control:hover,.center-control:hover,.rotation-control:hover,.ol-full-screen-true:hover,.ol-full-screen-false:hover{background-color:var(--control-background-color-hover)!important;outline:none!important}.ol-zoom-in{border-radius:0!important;border-top-right-radius:var(--icon-border-radius)!important;border-top-left-radius:var(--icon-border-radius)!important}.ol-zoom-out{border-radius:0!important;border-bottom-right-radius:var(--icon-border-radius)!important;border-bottom-left-radius:var(--icon-border-radius)!important}.ol-zoom-in>div>svg,.ol-zoom-out>div>svg,.ol-full-screen-true>div>svg,.ol-full-screen-false>div>svg{width:var(--svg-icon-size)!important;height:var(--svg-icon-size)!important}.ol-zoom-in>div>svg>g>.icon,.ol-zoom-out>div>svg>g>.icon,.ol-full-screen-true>div>svg>g>.icon,.ol-full-screen-false>div>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}@media only screen and (min-width: 420px){.left-buttons-control-container,.right-buttons-control-container{top:var(--top-distance)}}@media only screen and (max-width: 419px){.left-buttons-control-container,.right-buttons-control-container{top:calc(calc(var(--top-distance) * 2) + var(--box-height))}}
`, dh = `.notification-element-info-light{--notification-background-color: #DBEAFE;--notification-stroke-color: #1D4ED8;--notification-text-color: #1D4ED8}.notification-element-info-dark{--notification-background-color: #2563EB;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-warning-light{--notification-background-color: #FEF3C7;--notification-stroke-color: #B45309;--notification-text-color: #B45309}.notification-element-warning-dark{--notification-background-color: #D97706;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-error-light{--notification-background-color: #FEE2E2;--notification-stroke-color: #B91C1C;--notification-text-color: #B91C1C}.notification-element-error-dark{--notification-background-color: #DC2626;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.control-notification-manager{position:absolute;bottom:10px;left:calc((100% - 334px)/2);max-width:302px;width:100%;height:62px;display:grid}.notification-box{position:relative;grid-area:1 / 1 / 2 / 2}.notification-element{font-family:sans-serif;--icon-size: 32px;background-color:var(--notification-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);z-index:10;margin-left:5px;margin-right:5px;max-width:302px;width:100%;grid-template-columns:100%;grid-template-rows:100%}.notification-title>div>svg{display:block;width:var(--icon-size);height:var(--icon-size);padding-right:10px}.notification-icon-container{height:100%}.notification-title>div>svg>g>.icon{fill:none;stroke:var(--notification-stroke-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round}.notification-title{display:flex}.notification-title-text{font-weight:400;font-size:12px;line-height:15px;color:var(--notification-text-color)}
`;
var bv = Object.defineProperty, Lv = Object.getOwnPropertyDescriptor, lr = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Lv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && bv(t, e, s), s;
};
let on = class extends kt {
  constructor() {
    super(), this.type = "info", this.message = "", this.icon = "", this.theme = "";
  }
  firstUpdated() {
    switch (this.type) {
      case "info":
        this.icon = at.info, this.theme = `notification-element-info-${w().getTheme()}`;
        break;
      case "warning":
        this.icon = at.warning, this.theme = `notification-element-warning-${w().getTheme()}`;
        break;
      case "error":
        this.icon = at.error, this.theme = `notification-element-error-${w().getTheme()}`;
        break;
    }
  }
  render() {
    return Lt`
      <div class="notification-element ${this.theme}">
        <div class="notification-title">
          <div class="notification-icon-container">
            ${Ue(this.icon)}
          </div>
          <div class="notification-title-text">${this.message}</div>
        </div>  
      </div>
    `;
  }
};
on.styles = [Mt(dh)];
lr([
  cn()
], on.prototype, "type", 2);
lr([
  cn()
], on.prototype, "message", 2);
lr([
  ae()
], on.prototype, "icon", 2);
lr([
  ae()
], on.prototype, "theme", 2);
on = lr([
  oe("notification-box")
], on);
class ps extends Gt {
  constructor(t, e, i) {
    const s = document.createElement(
      "notification-box"
    );
    s.type = e.type, s.message = e.message, super({ element: s }), this.ruleType = e.rule.type, this.div = s, this.div.classList.add("notification-box"), this.div.style.zIndex = `${i}`, this.setTarget(t);
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
let ou = /[-+]?([0-9]*\.[0-9]+|[0-9]+)([eE][-+]?[0-9]+)?/, au = new RegExp("^" + ou.source + "(\\s" + ou.source + "){1,}");
const Iv = (n) => {
  let t = n.split(";"), e = t.pop(), i = (t.shift() || "").split("=").pop(), s = 0;
  function r(p) {
    let v = e.substring(s).match(p);
    return v ? (s += v[0].length, v[0]) : null;
  }
  function o(p) {
    return p && i.match(/\d+/) && (p.crs = {
      type: "name",
      properties: {
        name: "urn:ogc:def:crs:EPSG::" + i
      }
    }), p;
  }
  function a() {
    r(/^\s*/);
  }
  function l() {
    a();
    let p = 0, v = [], x = [v], C = v, E;
    for (; E = r(/^(\()/) || r(/^(\))/) || r(/^(,)/) || r(au); ) {
      if (E === "(")
        x.push(C), C = [], x[x.length - 1].push(C), p++;
      else if (E === ")") {
        if (C.length === 0 || (C = x.pop(), !C))
          return null;
        if (p--, p === 0)
          break;
      } else if (E === ",")
        C = [], x[x.length - 1].push(C);
      else if (!E.split(/\s/g).some(isNaN))
        Array.prototype.push.apply(C, E.split(/\s/g).map(parseFloat));
      else
        return null;
      a();
    }
    return p !== 0 ? null : v;
  }
  function h() {
    let p = [], v, x;
    for (; x = r(au) || r(/^(,)/); )
      x === "," ? (p.push(v), v = []) : x.split(/\s/g).some(isNaN) || (v || (v = []), Array.prototype.push.apply(v, x.split(/\s/g).map(parseFloat))), a();
    if (v)
      p.push(v);
    else
      return null;
    return p.length ? p : null;
  }
  function c() {
    if (!r(/^(point(\sz)?)/i) || (a(), !r(/^(\()/)))
      return null;
    let p = h();
    return !p || (a(), !r(/^(\))/)) ? null : {
      type: "Point",
      coordinates: p[0]
    };
  }
  function u() {
    if (!r(/^(multipoint(\sz)?)/i))
      return null;
    a(), e = "MULTIPOINT (" + e.substring(e.indexOf("(") + 1, e.length - 1).replace(/\(/g, "").replace(/\)/g, "") + ")";
    let v = l();
    return v ? (a(), {
      type: "MultiPoint",
      coordinates: v
    }) : null;
  }
  function d() {
    if (!r(/^(multilinestring(\sz)?)/i))
      return null;
    a();
    let p = l();
    return p ? (a(), {
      type: "MultiLineString",
      coordinates: p
    }) : null;
  }
  function f() {
    if (!r(/^(linestring(\sz)?)/i) || (a(), !r(/^(\()/)))
      return null;
    let p = h();
    return !p || !r(/^(\))/) ? null : {
      type: "LineString",
      coordinates: p
    };
  }
  function g() {
    if (!r(/^(polygon(\sz)?)/i))
      return null;
    a();
    let p = l();
    return p ? {
      type: "Polygon",
      coordinates: p
    } : null;
  }
  function m() {
    if (!r(/^(multipolygon(\sz)?)/i))
      return null;
    a();
    let p = l();
    return p ? {
      type: "MultiPolygon",
      coordinates: p
    } : null;
  }
  function _() {
    let p = [], v;
    if (!r(/^(geometrycollection)/i) || (a(), !r(/^(\()/)))
      return null;
    for (; v = y(); )
      p.push(v), a(), r(/^(,)/), a();
    return r(/^(\))/) ? {
      type: "GeometryCollection",
      geometries: p
    } : null;
  }
  function y() {
    return c() || f() || g() || u() || d() || m() || _();
  }
  return o(y());
}, Zf = (n) => {
  n.type === "Feature" && (n = n.geometry);
  function t(a) {
    return a.join(" ");
  }
  function e(a) {
    return a.map(t).join(", ");
  }
  function i(a) {
    return a.map(e).map(r).join(", ");
  }
  function s(a) {
    return a.map(i).map(r).join(", ");
  }
  function r(a) {
    return "(" + a + ")";
  }
  let o = n;
  switch (o.type) {
    case "Point":
      return o.coordinates && o.coordinates.length === 3 ? "POINT Z (" + t(o.coordinates) + ")" : "POINT (" + t(o.coordinates) + ")";
    case "LineString":
      return o.coordinates && o.coordinates[0] && o.coordinates[0].length === 3 ? "LINESTRING Z (" + e(o.coordinates) + ")" : "LINESTRING (" + e(o.coordinates) + ")";
    case "Polygon":
      return o.coordinates && o.coordinates[0] && o.coordinates[0][0] && o.coordinates[0][0].length === 3 ? "POLYGON Z (" + i(o.coordinates) + ")" : "POLYGON (" + i(o.coordinates) + ")";
    case "MultiPoint":
      return o.coordinates && o.coordinates[0] && o.coordinates[0].length === 3 ? "MULTIPOINT Z (" + e(o.coordinates) + ")" : "MULTIPOINT (" + e(o.coordinates) + ")";
    case "MultiLineString":
      return o.coordinates && o.coordinates[0] && o.coordinates[0][0] && o.coordinates[0][0].length === 3 ? "MULTILINESTRING Z (" + i(o.coordinates) + ")" : "MULTILINESTRING (" + i(o.coordinates) + ")";
    case "MultiPolygon":
      return o.coordinates && o.coordinates[0] && o.coordinates[0][0] && o.coordinates[0][0] && o.coordinates[0][0][0].length === 3 ? "MULTIPOLYGON Z (" + s(o.coordinates) + ")" : "MULTIPOLYGON (" + s(o.coordinates) + ")";
    case "GeometryCollection":
      return "GEOMETRYCOLLECTION (" + o.geometries.map(Zf).join(", ") + ")";
    default:
      throw new Error("stringify requires a valid GeoJSON Feature or geometry object as input");
  }
};
var lu = {
  parse: Iv,
  stringify: Zf
};
class Vf extends Gt {
  constructor() {
    const t = document.createElement("div");
    t.classList.add("control-notification-manager"), super({
      element: t
    }), this.div = t;
  }
}
Vf.style = [Mt(dh)];
class Pv {
  constructor() {
    this.validZoomConstraint = !0, this.validAreaConstraint = !0, this.validMaxElementConstraint = !0, this.notificationControl = new Vf();
    const t = w().getOptions();
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
      default:
        w().getMap().addControl(new ps(this.notificationControl.div, {
          type: "error",
          message: "Veuillez s\xE9lectionner un mode de fonctionnement valide.",
          rule: {
            type: "NOT_VALID_MODE"
          }
        }, 5));
    }
    w().getMap().addControl(this.notificationControl), this.setup(t.notifications);
  }
  setupTargetMode() {
    window.addEventListener("current-center-position", (t) => {
      if (this.validZoomConstraint && this.validAreaConstraint) {
        const e = {
          type: "Point",
          coordinates: t.detail
        };
        ot.sendEvent("position-selected", [{ geometry: lu.stringify(e) }]);
      }
    });
  }
  setupSelectMode() {
    window.addEventListener("icon-clicked", (t) => {
      const e = w().getSelectedFeatures();
      this.validZoomConstraint && e.length > 0 && (this.checkMaxElementContraint(e), this.validMaxElementConstraint && ot.sendEvent("position-selected", this.generateExportData(e)), ot.sendEvent("authorize-clicked", t.detail));
    }), window.addEventListener("rule-validation", () => {
      const t = w().getSelectedFeatures();
      this.checkMaxElementContraint(t), this.validZoomConstraint && this.validMaxElementConstraint && t.length > 0 && ot.sendEvent("position-selected", this.generateExportData(t));
    });
  }
  setupCreateMode() {
    window.addEventListener("icon-created", () => {
      const t = w().getSelectedFeatures();
      this.checkMaxElementContraint(t), this.validZoomConstraint && this.validMaxElementConstraint && t.length > 0 && ot.sendEvent("position-selected", this.generateExportData(t)), ot.sendEvent("authorize-created", void 0);
    }), window.addEventListener("rule-validation", () => {
      const t = w().getSelectedFeatures();
      this.checkMaxElementContraint(t), this.validZoomConstraint && this.validMaxElementConstraint && t.length > 0 && ot.sendEvent("position-selected", this.generateExportData(t));
    }), window.addEventListener("icon-removed", () => {
      ot.sendEvent("position-selected", void 0), ot.sendEvent("remove-created-icon", void 0);
    });
  }
  setup(t) {
    t.forEach((e) => {
      e.rule.type === "ZOOM_CONSTRAINT" && this.setupZoomContraint(e), e.rule.type === "AREA_CONSTRAINT" && this.setupInclusionAreaConstraint(e), e.rule.type === "MAX_SELECTION" && this.setupMaxSelectionConstraint(e), e.type === "info" && (this.infosNotificationControl = new ps(this.notificationControl.div, e, 1), w().getMap().addControl(this.infosNotificationControl));
    });
  }
  setupZoomContraint(t) {
    this.zoomNotificationControl = new ps(this.notificationControl.div, t, 4), this.zoomNotificationControl.disable(), w().getMap().addControl(this.zoomNotificationControl), this.hasValidZoom(t) && (this.validZoomConstraint = !1, this.zoomNotificationControl.show()), w().getMap().getView().on("change:resolution", () => {
      this.checkZoomConstraint(t);
    });
  }
  setupInclusionAreaConstraint(t) {
    this.inclusionNotificationControl = new ps(this.notificationControl.div, t, 2), this.inclusionNotificationControl.disable(), w().getMap().addControl(this.inclusionNotificationControl), window.addEventListener("inclusion-area-included", (e) => {
      this.checkInclusionAreaConstraint(e.detail, t.rule.couldBypass);
    });
  }
  setupMaxSelectionConstraint(t) {
    const e = t.rule.maxElement;
    e !== void 0 && w().setMaxElement(e), t.message = t.message.replace("{x}", `${e}`), this.maxElementNotificationControl = new ps(this.notificationControl.div, t, 3), this.maxElementNotificationControl.disable(), w().getMap().addControl(this.maxElementNotificationControl);
  }
  hasValidZoom(t) {
    const e = w().getMap().getView().getZoom();
    return e && t.rule.minZoom && e < t.rule.minZoom;
  }
  checkZoomConstraint(t) {
    var e, i;
    this.hasValidZoom(t) ? ((i = this.zoomNotificationControl) == null || i.show(), this.validZoomConstraint = !1, ot.sendEvent("position-selected", void 0)) : ((e = this.zoomNotificationControl) == null || e.hide(), this.validZoomConstraint = !0, ot.sendEvent("rule-validation", void 0));
  }
  checkInclusionAreaConstraint(t, e) {
    var i, s;
    t ? ((i = this.inclusionNotificationControl) == null || i.hide(), this.validAreaConstraint = !0) : ((s = this.inclusionNotificationControl) == null || s.show(), e ? this.validAreaConstraint = !0 : (this.validAreaConstraint = !1, ot.sendEvent("position-selected", void 0)));
  }
  checkMaxElementContraint(t) {
    var e, i;
    w().getMaxElement() >= 0 && (t.length >= w().getMaxElement() ? t.length > w().getMaxElement() && (this.validMaxElementConstraint = !1, (e = this.maxElementNotificationControl) == null || e.show()) : (this.validMaxElementConstraint = !0, (i = this.maxElementNotificationControl) == null || i.hide()));
  }
  generateExportData(t) {
    const e = [];
    return t.forEach((i) => {
      e.push({
        id: i.get("objectid"),
        geometry: lu.stringify({
          type: "Point",
          coordinates: i.get("geom").getCoordinates()
        })
      });
    }), e;
  }
}
const Av = `:host>.no-box{--box-height: 0px;--top-distance: 10px}:host>.select{--box-height: 68px;--top-distance: 10px}:host>.large{--box-height: 79px;--top-distance: 10px}:host>.medium{--box-height: 64px;--top-distance: 10px}:host>.small{--box-height: 49px;--top-distance: 10px}:host>.light{--control-background-color: rgb(30 41 59 / 75%);--control-background-color-hover: rgb(30 41 59 / 100%);--control-icon-color: white;--information-box-background-color: white;--information-box-title-color: #1E293B;--information-cross-hover-color: rgb(30 41 59 / 75%);--information-box-text-color: #334155;--select-icon-background: #1E293B;--icon-border-color: #CBD5E1}:host>.dark{--control-background-color: rgb(255 255 255 / 75%);--control-background-color-hover: rgb(255 255 255 / 100%);--control-icon-color: #1E293B;--information-box-background-color: #1F2937;--information-box-title-color: #F3F4F6;--information-cross-hover-color: rgb(255 255 255 / 75%);--information-box-text-color: #9CA3AF;--select-icon-background: rgb(255,255,255, .75);--icon-border-color: #334155}:host>#map{--icon-width: 36px;--icon-height: 36px;--side-distance: 10px;--icon-border-radius: 4px;--box-border-radius: 4px;--svg-icon-size: 26px;--icon-stroke-width: 2px}
`, Ov = `@keyframes fadeIn{0%{opacity:0;visibility:inherit}to{opacity:1}}@keyframes fadeOut{0%{opacity:1}to{opacity:0;visibility:hidden}}.fade-in{animation:fadeIn .3s forwards}.fade-out{animation:fadeOut .3s forwards}.disabled{visibility:hidden}
`;
class Fv {
  static getOptions(t) {
    const e = {
      zoom: 15,
      minZoom: 1,
      maxZoom: 20,
      displayZoom: !0,
      displayScaleLine: !1,
      fullscreen: !0,
      defaultCenter: [2539057, 1181111],
      enableGeolocation: !1,
      enableCenterButton: !0,
      enableDraw: !0,
      maxNbDraw: 0,
      drawElement: "Point",
      onlyOneDraw: !1,
      enableRotation: !0,
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
      geojson: {
        url: ""
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
      borderUrl: ""
    };
    t.zoom !== void 0 && (e.zoom = t.zoom), t.minZoom !== void 0 && (e.minZoom = t.minZoom), t.maxZoom !== void 0 && (e.maxZoom = t.maxZoom), t.displayZoom !== void 0 && (e.displayZoom = t.displayZoom), t.search !== void 0 && (e.search = t.search), t.displayScaleLine !== void 0 && (e.displayScaleLine = t.displayScaleLine), t.fullscreen !== void 0 && (e.fullscreen = t.fullscreen), t.defaultCenter !== void 0 && (e.defaultCenter = t.defaultCenter), t.enableGeolocation !== void 0 && (e.enableGeolocation = t.enableGeolocation), t.enableCenterButton !== void 0 && (e.enableCenterButton = t.enableCenterButton), t.enableDraw !== void 0 && (e.enableDraw = t.enableDraw), t.maxNbDraw !== void 0 && (e.maxNbDraw = t.maxNbDraw), t.drawElement !== void 0 && (e.drawElement = t.drawElement), t.onlyOneDraw !== void 0 && (e.onlyOneDraw = t.onlyOneDraw), t.enableRotation !== void 0 && (e.enableRotation = t.enableRotation), t.information !== void 0 && (e.information = t.information), t.notifications !== void 0 && t.notifications.length > 0 && (e.notifications = t.notifications), t.mode !== void 0 && (e.mode = t.mode), t.cluster !== void 0 && (e.cluster = t.cluster), t.geojson !== void 0 && (e.geojson = t.geojson), t.geolocationInformation !== void 0 && (e.geolocationInformation = t.geolocationInformation), t.wfs !== void 0 && (e.wfs = t.wfs), t.wmts !== void 0 && (e.wmts = t.wmts), t.inclusionArea !== void 0 && (e.inclusionArea = t.inclusionArea), t.selectionTargetBoxMessage !== void 0 && (e.selectionTargetBoxMessage = t.selectionTargetBoxMessage), t.borderUrl !== void 0 && (e.borderUrl = t.borderUrl), w().setOptions(e);
  }
}
class Nv {
  constructor() {
    const t = $f.getSource(w().getOptions().inclusionArea.url, w().getOptions().inclusionArea.filter), e = new Ze({
      source: t,
      style: new Zt({
        stroke: new Xt({
          color: "red",
          width: 1
        })
      })
    });
    w().getMap().addLayer(e), window.addEventListener("current-center-position", (i) => {
      var r;
      const s = t.getClosestFeatureToCoordinate(
        i.detail
      );
      if (((r = s.getGeometry()) == null ? void 0 : r.getType()) === "Polygon") {
        const o = s.getGeometry();
        ot.sendEvent("inclusion-area-included", o == null ? void 0 : o.intersectsCoordinate(i.detail));
      }
    });
  }
}
const Uo = `svg{margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size);height:var(--svg-icon-size)}svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
var Dv = Object.defineProperty, kv = Object.getOwnPropertyDescriptor, Gv = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? kv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && Dv(t, e, s), s;
};
let il = class extends kt {
  constructor() {
    super();
  }
  render() {
    return Lt`<div class="ol-unselectable ol-control center-control">
                  <div>
                    <div class="control-${w().getTheme()}">
                      ${Ue(at.geolocation)}
                    </div>
                  </div>
                </div>
    `;
  }
};
il.styles = [Mt(Uo), Mt(Vo)];
il = Gv([
  oe("geolocation-control-button")
], il);
class $v extends Gt {
  constructor(t) {
    const e = document.createElement("geolocation-control-button");
    super({
      element: e
    }), e.addEventListener("click", this.centerMap.bind(this), !1), this.setTarget(t);
  }
  centerMap() {
    const t = w().getGeolocation();
    if (t) {
      const e = t.getPosition(), i = this.getMap();
      if (i) {
        const s = i.getSize(), r = i.getView();
        e && s && r.centerOn(e, s, [570, 500]);
      }
    }
  }
}
var Bv = Object.defineProperty, zv = Object.getOwnPropertyDescriptor, Zv = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? zv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && Bv(t, e, s), s;
};
let nl = class extends kt {
  render() {
    return Lt`<div class="control-${w().getTheme()}">${Ue(at.rotation)}</div>`;
  }
};
nl.styles = [Mt(Uo)];
nl = Zv([
  oe("rotation-control-button")
], nl);
class hu extends Gt {
  constructor(t) {
    const e = document.createElement("div"), i = document.createElement("rotation-control-button");
    e.appendChild(i);
    const s = document.createElement("div");
    s.className = "rotation-control ", s.appendChild(e), super({
      element: s
    }), e.addEventListener("click", this.resetRotation.bind(this), !1), this.setTarget(t);
  }
  resetRotation() {
    w().getMap().getView().setRotation(0);
  }
}
const Vv = `@media only screen and (min-width: 420px){.custom-popup-element{right:calc(.5em + 40px)}}@media only screen and (max-width: 419px){.custom-popup-element{left:calc(50% - 172px)}}.custom-popup-element{font-family:sans-serif;position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color);z-index:10;margin-left:5px;margin-right:5px;max-width:302px;width:100%}.custom-popup-element:after{content:"";width:var(--progress-width);height:4px;background:#008C6F;position:absolute;bottom:-1px;left:0;border-bottom-left-radius:4px;border-bottom-right-radius:var(--border-radius-right)}.custom-popup-title{display:flex}.custom-popup-title-text{width:90%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.custom-popup-title-svg{width:10%;justify-content:flex-end;display:flex;fill:none;stroke:var(--information-box-title-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round;cursor:pointer}.custom-popup-title-svg:hover{stroke:var(--information-cross-hover-color)}.custom-popup-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}
`;
var Uv = Object.defineProperty, Wv = Object.getOwnPropertyDescriptor, fh = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Wv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && Uv(t, e, s), s;
};
let Ws = class extends kt {
  constructor() {
    super(), this._width = 100, this._borderRadiusRight = 0, window.addEventListener("clear-information-box-interval", this.clear.bind(this), !0), window.addEventListener("open-information-box", () => {
      this._width = 100;
      const n = w().getOptions().information.duration / 100;
      this.interval = setInterval(() => {
        this._width > 0 ? (this._width < 100 && (this._borderRadiusRight = 0), this._width--) : this.closeBox();
      }, n);
    });
  }
  render() {
    return Lt`
      <div class="information-box-${w().getTheme()} custom-popup-element" style="--progress-width: ${this._width}%; --border-radius-right: ${this._borderRadiusRight}px">
        <div class="custom-popup-title">
          <div class="custom-popup-title-text">${w().getOptions().information.title}</div>
          <svg _width="20" height="20" viewBox="0 0 20 20" class="custom-popup-title-svg" @click="${this.closeBox}">
            <path d="M15.4 4.59998L4.60004 15.4"></path>
            <path d="M15.4 15.4L4.60004 4.59998"></path>
          </svg>
        </div>
        <div class="custom-popup-content">${w().getOptions().information.content}</div>
        <div class="custom-progress-element"></div>
      </div>`;
  }
  clear() {
    clearInterval(this.interval);
  }
  closeBox() {
    clearInterval(this.interval), ot.sendEvent("close-information-box", {});
  }
};
Ws.styles = [Mt(Vv)];
fh([
  ae()
], Ws.prototype, "_width", 2);
fh([
  ae()
], Ws.prototype, "_borderRadiusRight", 2);
Ws = fh([
  oe("information-box")
], Ws);
class Hv extends Gt {
  constructor() {
    const t = document.createElement("information-box");
    super({ element: t }), this.div = t;
  }
  show() {
    this.div.classList.remove("fade-out"), this.div.classList.add("fade-in");
  }
  hide() {
    this.div.classList.remove("fade-in"), this.div.classList.add("fade-out");
  }
}
var Xv = Object.defineProperty, Yv = Object.getOwnPropertyDescriptor, jv = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Yv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && Xv(t, e, s), s;
};
let sl = class extends kt {
  constructor() {
    super();
  }
  render() {
    return Lt`<div class="information-control">
                  <div>
                    <div class="control-${w().getTheme()}">
                      ${Ue(at.information)}
                    </div>
                  </div>
                </div>
    `;
  }
};
sl.styles = [Mt(Uo), Mt(Vo)];
sl = jv([
  oe("information-control-button")
], sl);
class qv extends Gt {
  constructor(t) {
    const e = document.createElement("information-control-button");
    super({
      element: e
    }), this.informationIsOpen = !0, e.addEventListener("click", this.toogleInformationBox.bind(this), !1), window.addEventListener("close-information-box", this.closeInformationBox.bind(this), !1), this.control = new Hv(), w().getMap().addControl(this.control), this.openInformationBox(), this.setTarget(t);
  }
  closeInformationBox() {
    ot.sendEvent("clear-information-box-interval", {}), this.control.hide(), this.informationIsOpen = !1;
  }
  openInformationBox() {
    this.control.show(), ot.sendEvent("open-information-box", {}), this.informationIsOpen = !0;
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
const Kv = nh(class extends sh {
  constructor(n) {
    var t;
    if (super(n), n.type !== Sf.ATTRIBUTE || n.name !== "class" || ((t = n.strings) === null || t === void 0 ? void 0 : t.length) > 2)
      throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.");
  }
  render(n) {
    return " " + Object.keys(n).filter((t) => n[t]).join(" ") + " ";
  }
  update(n, [t]) {
    var e, i;
    if (this.nt === void 0) {
      this.nt = /* @__PURE__ */ new Set(), n.strings !== void 0 && (this.st = new Set(n.strings.join(" ").split(/\s/).filter((r) => r !== "")));
      for (const r in t)
        t[r] && !(!((e = this.st) === null || e === void 0) && e.has(r)) && this.nt.add(r);
      return this.render(t);
    }
    const s = n.element.classList;
    this.nt.forEach((r) => {
      r in t || (s.remove(r), this.nt.delete(r));
    });
    for (const r in t) {
      const o = !!t[r];
      o === this.nt.has(r) || ((i = this.st) === null || i === void 0 ? void 0 : i.has(r)) || (o ? (s.add(r), this.nt.add(r)) : (s.remove(r), this.nt.delete(r)));
    }
    return bi;
  }
}), Uf = `.layer-container{left:calc(50% - 151px);position:absolute;max-width:302px;width:100%;top:var(--top-distance);z-index:0}.layer-title-container{border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color)}.layer-text{width:calc(100% - 13px);height:36px;padding:0 0 0 11px;font-size:14px;line-height:17px;font-weight:400;background-color:var(--information-box-background-color);color:var(--information-box-text-color);margin:0;align-items:center;display:flex}.layer-svg-container{width:29px;height:36px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-radius:var(--icon-border-radius)}li{height:64px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--information-box-text-color)}li>.image-container{width:56px;display:flex;align-items:center;justify-content:center;height:inherit}li>.image-container>img{width:46px;height:46px;border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color)}.selected-layer{border:2px solid #DC2626!important;border-radius:var(--icon-border-radius)}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var Jv = Object.defineProperty, Qv = Object.getOwnPropertyDescriptor, gh = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? Qv(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && Jv(t, e, s), s;
};
let vo = class extends kt {
  constructor() {
    super(...arguments), this._currentSelectedIndex = 0;
  }
  selectLayer(n, t) {
    ot.sendEvent("layer-selected", n), this._currentSelectedIndex = t;
  }
  render() {
    return Lt`
                <ul>
                  ${w().getOptions().wmts.map(
      (n, t) => Lt`<li tabindex="0" @click=${() => this.selectLayer(n, t)}>
                          <div class="image-container">
                            <img class=${Kv({ "selected-layer": this._currentSelectedIndex === t })} src="${n.thumbnail}"/>
                          </div>
                          <p>${n.name}</p>
                        </li>`
    )}
                </ul>
              `;
  }
};
vo.styles = [Mt(Uf)];
gh([
  ae()
], vo.prototype, "_currentSelectedIndex", 2);
vo = gh([
  oe("layer-list")
], vo);
let rl = class extends kt {
  render() {
    return Lt`<div class="layer-container" style="z-index: 5">
                  <div class="layer-title-container">
                      <p class="layer-text">Affichage de la carte</p>
                      <div class="layer-svg-container">
                        <div class="cross-div" @click="${this.closeBox}">
                          ${Ue(at.cross)}
                        </div>
                      </div>
                  </div>
                  <layer-list />
              </div>`;
  }
  closeBox() {
    ot.sendEvent("layer-selection-closed", void 0);
  }
};
rl.styles = [Mt(Uf)];
rl = gh([
  oe("layer-selection")
], rl);
class tx extends Gt {
  constructor() {
    const t = document.createElement("layer-selection");
    super({ element: t });
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
var ex = Object.defineProperty, ix = Object.getOwnPropertyDescriptor, nx = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? ix(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && ex(t, e, s), s;
};
let ol = class extends kt {
  render() {
    return Lt`<div class="ol-unselectable ol-control center-control">
                  <div>
                    <div class="control-${w().getTheme()}">
                      ${Ue(at.stack)}
                    </div>
                  </div>
                </div> `;
  }
};
ol.styles = [Mt(Uo), Mt(Vo)];
ol = nx([
  oe("geo-layer-control-button")
], ol);
class sx extends Gt {
  constructor(t) {
    const e = document.createElement(
      "geo-layer-control-button"
    );
    super({
      element: e
    }), this.isOpen = !1, this.layerSelection = new tx(), this.layerSelection.disable(), w().getMap().addControl(this.layerSelection), e.addEventListener("click", () => {
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
class cu extends Gt {
  constructor(t) {
    const e = document.createElement("div");
    e.className = t, super({
      element: e
    }), this.div = e;
  }
}
class rx {
  static setupIcon() {
    const t = w().getOptions(), e = w().getMap(), i = new cu("left-buttons-control-container");
    e.addControl(i);
    const s = new cu("right-buttons-control-container");
    e.addControl(s), e.addControl(new qv(s.div)), t.fullscreen && e.addControl(
      new q_({
        label: at.fullScreenLabel(),
        labelActive: at.fullScreenLabelActive(),
        className: "ol-full-screen",
        target: s.div
      })
    ), e.addControl(new sx(s.div)), t.displayZoom && e.addControl(
      new Pd({
        zoomInLabel: at.zoomInLabel(),
        zoomOutLabel: at.zoomOutLabel(),
        className: "ol-zoom",
        target: i.div
      })
    ), t.enableCenterButton && e.addControl(new $v(i.div)), t.enableRotation && e.getView().on("change:rotation", (r) => {
      e.getControls().forEach((o) => {
        o instanceof hu && e.removeControl(o);
      }), r.target.getRotation() !== 0 && e.addControl(new hu(i.div));
    });
  }
}
var ox = Object.defineProperty, ax = Object.getOwnPropertyDescriptor, lx = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? ax(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && ox(t, e, s), s;
};
class hx {
  constructor() {
    w().getMap().getView().on("change:center", (t) => {
      ot.sendEvent("current-center-position", t.target.getCenter());
    });
  }
}
let uu = class extends kt {
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
uu = lx([
  oe("target-element")
], uu);
class cx extends Gt {
  constructor() {
    const t = document.createElement("target-element");
    super({ element: t }), new hx();
  }
}
const ux = `.box-element{left:calc(50% - 172px);font-family:sans-serif}.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color);margin-left:5px;margin-right:5px;max-width:302px;width:100%}.box-element-title{display:flex}.box-element-title-text{width:90%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}
`;
var dx = Object.defineProperty, fx = Object.getOwnPropertyDescriptor, hr = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? fx(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && dx(t, e, s), s;
};
let an = class extends kt {
  constructor() {
    super(), this.defaultPosition = [0, 0], this._currentPosition = "", this._reversePosition = "", this._lastPosition = this.defaultPosition;
    const n = 20;
    window.addEventListener("current-center-position", (t) => {
      w().getOptions().geolocationInformation.reverseLocation ? (Math.abs(this._lastPosition[0] - t.detail[0]) > n || Math.abs(this._lastPosition[1] - t.detail[1]) > n) && (this._lastPosition = t.detail, this.searchAddress(t.detail)) : this._reversePosition = "", this._currentPosition = w().getOptions().geolocationInformation.currentLocation ? `${t.detail[0].toFixed(6)}, ${t.detail[1].toFixed(6)}` : "";
    });
  }
  connectedCallback() {
    super.connectedCallback();
  }
  searchAddress(n) {
    Tf.getAddressFromCoordinate(n).then((t) => {
      this._reversePosition = t.results.length > 0 ? `proche de ${t.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
    });
  }
  firstUpdated() {
    w().getOptions().geolocationInformation.reverseLocation ? this.searchAddress(this.defaultPosition) : this._reversePosition = "", this._currentPosition = w().getOptions().geolocationInformation.currentLocation ? `${this.defaultPosition[0].toFixed(6)}, ${this.defaultPosition[1].toFixed(6)}` : "";
  }
  render() {
    return Lt`
      <div class="information-box-${w().getTheme()} box-element">
        <div class="box-element-title">
          <div class="box-element-title-text">${w().getOptions().selectionTargetBoxMessage}</div>
        </div>
        <div class="box-element-content">${this._reversePosition}</div>
        <div class="box-element-content">${this._currentPosition}</div>
      </div>
    `;
  }
};
an.styles = [Mt(ux)];
hr([
  cn()
], an.prototype, "defaultPosition", 2);
hr([
  ae()
], an.prototype, "_currentPosition", 2);
hr([
  ae()
], an.prototype, "_reversePosition", 2);
hr([
  ae()
], an.prototype, "_lastPosition", 2);
an = hr([
  oe("target-information-box-element")
], an);
class gx extends Gt {
  constructor() {
    const t = document.createElement("target-information-box-element");
    t.defaultPosition = w().getOptions().defaultCenter, super({ element: t });
  }
}
function mx(n) {
  n("EPSG:4326", "+title=WGS 84 (long/lat) +proj=longlat +ellps=WGS84 +datum=WGS84 +units=degrees"), n("EPSG:4269", "+title=NAD83 (long/lat) +proj=longlat +a=6378137.0 +b=6356752.31414036 +ellps=GRS80 +datum=NAD83 +units=degrees"), n("EPSG:3857", "+title=WGS 84 / Pseudo-Mercator +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"), n.WGS84 = n["EPSG:4326"], n["EPSG:3785"] = n["EPSG:3857"], n.GOOGLE = n["EPSG:3857"], n["EPSG:900913"] = n["EPSG:3857"], n["EPSG:102113"] = n["EPSG:3857"];
}
var ln = 1, hn = 2, Hr = 3, _x = 4, al = 5, du = 6378137, px = 6356752314e-3, fu = 0.0066943799901413165, Is = 484813681109536e-20, S = Math.PI / 2, yx = 0.16666666666666666, vx = 0.04722222222222222, xx = 0.022156084656084655, I = 1e-10, zt = 0.017453292519943295, Ge = 57.29577951308232, ct = Math.PI / 4, Hs = Math.PI * 2, Tt = 3.14159265359, he = {};
he.greenwich = 0;
he.lisbon = -9.131906111111;
he.paris = 2.337229166667;
he.bogota = -74.080916666667;
he.madrid = -3.687938888889;
he.rome = 12.452333333333;
he.bern = 7.439583333333;
he.jakarta = 106.807719444444;
he.ferro = -17.666666666667;
he.brussels = 4.367975;
he.stockholm = 18.058277777778;
he.athens = 23.7163375;
he.oslo = 10.722916666667;
const Cx = {
  ft: { to_meter: 0.3048 },
  "us-ft": { to_meter: 1200 / 3937 }
};
var gu = /[\s_\-\/\(\)]/g;
function Oi(n, t) {
  if (n[t])
    return n[t];
  for (var e = Object.keys(n), i = t.toLowerCase().replace(gu, ""), s = -1, r, o; ++s < e.length; )
    if (r = e[s], o = r.toLowerCase().replace(gu, ""), o === i)
      return n[r];
}
function ll(n) {
  var t = {}, e = n.split("+").map(function(a) {
    return a.trim();
  }).filter(function(a) {
    return a;
  }).reduce(function(a, l) {
    var h = l.split("=");
    return h.push(!0), a[h[0].toLowerCase()] = h[1], a;
  }, {}), i, s, r, o = {
    proj: "projName",
    datum: "datumCode",
    rf: function(a) {
      t.rf = parseFloat(a);
    },
    lat_0: function(a) {
      t.lat0 = a * zt;
    },
    lat_1: function(a) {
      t.lat1 = a * zt;
    },
    lat_2: function(a) {
      t.lat2 = a * zt;
    },
    lat_ts: function(a) {
      t.lat_ts = a * zt;
    },
    lon_0: function(a) {
      t.long0 = a * zt;
    },
    lon_1: function(a) {
      t.long1 = a * zt;
    },
    lon_2: function(a) {
      t.long2 = a * zt;
    },
    alpha: function(a) {
      t.alpha = parseFloat(a) * zt;
    },
    gamma: function(a) {
      t.rectified_grid_angle = parseFloat(a);
    },
    lonc: function(a) {
      t.longc = a * zt;
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
      var l = Oi(Cx, a);
      l && (t.to_meter = l.to_meter);
    },
    from_greenwich: function(a) {
      t.from_greenwich = a * zt;
    },
    pm: function(a) {
      var l = Oi(he, a);
      t.from_greenwich = (l || parseFloat(a)) * zt;
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
  for (i in e)
    s = e[i], i in o ? (r = o[i], typeof r == "function" ? r(s) : t[r] = s) : t[i] = s;
  return typeof t.datumCode == "string" && t.datumCode !== "WGS84" && (t.datumCode = t.datumCode.toLowerCase()), t;
}
var Xs = 1, Wf = 2, Hf = 3, xo = 4, Xf = 5, mh = -1, Mx = /\s/, Ex = /[A-Za-z]/, wx = /[A-Za-z84_]/, Wo = /[,\]]/, Yf = /[\d\.E\-\+]/;
function ci(n) {
  if (typeof n != "string")
    throw new Error("not a string");
  this.text = n.trim(), this.level = 0, this.place = 0, this.root = null, this.stack = [], this.currentObject = null, this.state = Xs;
}
ci.prototype.readCharicter = function() {
  var n = this.text[this.place++];
  if (this.state !== xo)
    for (; Mx.test(n); ) {
      if (this.place >= this.text.length)
        return;
      n = this.text[this.place++];
    }
  switch (this.state) {
    case Xs:
      return this.neutral(n);
    case Wf:
      return this.keyword(n);
    case xo:
      return this.quoted(n);
    case Xf:
      return this.afterquote(n);
    case Hf:
      return this.number(n);
    case mh:
      return;
  }
};
ci.prototype.afterquote = function(n) {
  if (n === '"') {
    this.word += '"', this.state = xo;
    return;
  }
  if (Wo.test(n)) {
    this.word = this.word.trim(), this.afterItem(n);
    return;
  }
  throw new Error(`havn't handled "` + n + '" in afterquote yet, index ' + this.place);
};
ci.prototype.afterItem = function(n) {
  if (n === ",") {
    this.word !== null && this.currentObject.push(this.word), this.word = null, this.state = Xs;
    return;
  }
  if (n === "]") {
    this.level--, this.word !== null && (this.currentObject.push(this.word), this.word = null), this.state = Xs, this.currentObject = this.stack.pop(), this.currentObject || (this.state = mh);
    return;
  }
};
ci.prototype.number = function(n) {
  if (Yf.test(n)) {
    this.word += n;
    return;
  }
  if (Wo.test(n)) {
    this.word = parseFloat(this.word), this.afterItem(n);
    return;
  }
  throw new Error(`havn't handled "` + n + '" in number yet, index ' + this.place);
};
ci.prototype.quoted = function(n) {
  if (n === '"') {
    this.state = Xf;
    return;
  }
  this.word += n;
};
ci.prototype.keyword = function(n) {
  if (wx.test(n)) {
    this.word += n;
    return;
  }
  if (n === "[") {
    var t = [];
    t.push(this.word), this.level++, this.root === null ? this.root = t : this.currentObject.push(t), this.stack.push(this.currentObject), this.currentObject = t, this.state = Xs;
    return;
  }
  if (Wo.test(n)) {
    this.afterItem(n);
    return;
  }
  throw new Error(`havn't handled "` + n + '" in keyword yet, index ' + this.place);
};
ci.prototype.neutral = function(n) {
  if (Ex.test(n)) {
    this.word = n, this.state = Wf;
    return;
  }
  if (n === '"') {
    this.word = "", this.state = xo;
    return;
  }
  if (Yf.test(n)) {
    this.word = n, this.state = Hf;
    return;
  }
  if (Wo.test(n)) {
    this.afterItem(n);
    return;
  }
  throw new Error(`havn't handled "` + n + '" in neutral yet, index ' + this.place);
};
ci.prototype.output = function() {
  for (; this.place < this.text.length; )
    this.readCharicter();
  if (this.state === mh)
    return this.root;
  throw new Error('unable to parse string "' + this.text + '". State is ' + this.state);
};
function Sx(n) {
  var t = new ci(n);
  return t.output();
}
function mu(n, t, e) {
  Array.isArray(t) && (e.unshift(t), t = null);
  var i = t ? {} : n, s = e.reduce(function(r, o) {
    return Nn(o, r), r;
  }, i);
  t && (n[t] = s);
}
function Nn(n, t) {
  if (!Array.isArray(n)) {
    t[n] = !0;
    return;
  }
  var e = n.shift();
  if (e === "PARAMETER" && (e = n.shift()), n.length === 1) {
    if (Array.isArray(n[0])) {
      t[e] = {}, Nn(n[0], t[e]);
      return;
    }
    t[e] = n[0];
    return;
  }
  if (!n.length) {
    t[e] = !0;
    return;
  }
  if (e === "TOWGS84") {
    t[e] = n;
    return;
  }
  if (e === "AXIS") {
    e in t || (t[e] = []), t[e].push(n);
    return;
  }
  Array.isArray(e) || (t[e] = {});
  var i;
  switch (e) {
    case "UNIT":
    case "PRIMEM":
    case "VERT_DATUM":
      t[e] = {
        name: n[0].toLowerCase(),
        convert: n[1]
      }, n.length === 3 && Nn(n[2], t[e]);
      return;
    case "SPHEROID":
    case "ELLIPSOID":
      t[e] = {
        name: n[0],
        a: n[1],
        rf: n[2]
      }, n.length === 4 && Nn(n[3], t[e]);
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
      n[0] = ["name", n[0]], mu(t, e, n);
      return;
    default:
      for (i = -1; ++i < n.length; )
        if (!Array.isArray(n[i]))
          return Nn(n, t[e]);
      return mu(t, e, n);
  }
}
var Rx = 0.017453292519943295;
function Tx(n, t) {
  var e = t[0], i = t[1];
  !(e in n) && i in n && (n[e] = n[i], t.length === 3 && (n[e] = t[2](n[e])));
}
function Qe(n) {
  return n * Rx;
}
function bx(n) {
  if (n.type === "GEOGCS" ? n.projName = "longlat" : n.type === "LOCAL_CS" ? (n.projName = "identity", n.local = !0) : typeof n.PROJECTION == "object" ? n.projName = Object.keys(n.PROJECTION)[0] : n.projName = n.PROJECTION, n.AXIS) {
    for (var t = "", e = 0, i = n.AXIS.length; e < i; ++e) {
      var s = [n.AXIS[e][0].toLowerCase(), n.AXIS[e][1].toLowerCase()];
      s[0].indexOf("north") !== -1 || (s[0] === "y" || s[0] === "lat") && s[1] === "north" ? t += "n" : s[0].indexOf("south") !== -1 || (s[0] === "y" || s[0] === "lat") && s[1] === "south" ? t += "s" : s[0].indexOf("east") !== -1 || (s[0] === "x" || s[0] === "lon") && s[1] === "east" ? t += "e" : (s[0].indexOf("west") !== -1 || (s[0] === "x" || s[0] === "lon") && s[1] === "west") && (t += "w");
    }
    t.length === 2 && (t += "u"), t.length === 3 && (n.axis = t);
  }
  n.UNIT && (n.units = n.UNIT.name.toLowerCase(), n.units === "metre" && (n.units = "meter"), n.UNIT.convert && (n.type === "GEOGCS" ? n.DATUM && n.DATUM.SPHEROID && (n.to_meter = n.UNIT.convert * n.DATUM.SPHEROID.a) : n.to_meter = n.UNIT.convert));
  var r = n.GEOGCS;
  n.type === "GEOGCS" && (r = n), r && (r.DATUM ? n.datumCode = r.DATUM.name.toLowerCase() : n.datumCode = r.name.toLowerCase(), n.datumCode.slice(0, 2) === "d_" && (n.datumCode = n.datumCode.slice(2)), (n.datumCode === "new_zealand_geodetic_datum_1949" || n.datumCode === "new_zealand_1949") && (n.datumCode = "nzgd49"), (n.datumCode === "wgs_1984" || n.datumCode === "world_geodetic_system_1984") && (n.PROJECTION === "Mercator_Auxiliary_Sphere" && (n.sphere = !0), n.datumCode = "wgs84"), n.datumCode.slice(-6) === "_ferro" && (n.datumCode = n.datumCode.slice(0, -6)), n.datumCode.slice(-8) === "_jakarta" && (n.datumCode = n.datumCode.slice(0, -8)), ~n.datumCode.indexOf("belge") && (n.datumCode = "rnb72"), r.DATUM && r.DATUM.SPHEROID && (n.ellps = r.DATUM.SPHEROID.name.replace("_19", "").replace(/[Cc]larke\_18/, "clrk"), n.ellps.toLowerCase().slice(0, 13) === "international" && (n.ellps = "intl"), n.a = r.DATUM.SPHEROID.a, n.rf = parseFloat(r.DATUM.SPHEROID.rf, 10)), r.DATUM && r.DATUM.TOWGS84 && (n.datum_params = r.DATUM.TOWGS84), ~n.datumCode.indexOf("osgb_1936") && (n.datumCode = "osgb36"), ~n.datumCode.indexOf("osni_1952") && (n.datumCode = "osni52"), (~n.datumCode.indexOf("tm65") || ~n.datumCode.indexOf("geodetic_datum_of_1965")) && (n.datumCode = "ire65"), n.datumCode === "ch1903+" && (n.datumCode = "ch1903"), ~n.datumCode.indexOf("israel") && (n.datumCode = "isr93")), n.b && !isFinite(n.b) && (n.b = n.a);
  function o(h) {
    var c = n.to_meter || 1;
    return h * c;
  }
  var a = function(h) {
    return Tx(n, h);
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
    ["lat0", "latitude_of_center", Qe],
    ["longitude_of_center", "Longitude_Of_Center"],
    ["longitude_of_center", "Longitude_of_center"],
    ["longc", "longitude_of_center", Qe],
    ["x0", "false_easting", o],
    ["y0", "false_northing", o],
    ["long0", "central_meridian", Qe],
    ["lat0", "latitude_of_origin", Qe],
    ["lat0", "standard_parallel_1", Qe],
    ["lat1", "standard_parallel_1", Qe],
    ["lat2", "standard_parallel_2", Qe],
    ["azimuth", "Azimuth"],
    ["alpha", "azimuth", Qe],
    ["srsCode", "name"]
  ];
  l.forEach(a), !n.long0 && n.longc && (n.projName === "Albers_Conic_Equal_Area" || n.projName === "Lambert_Azimuthal_Equal_Area") && (n.long0 = n.longc), !n.lat_ts && n.lat1 && (n.projName === "Stereographic_South_Pole" || n.projName === "Polar Stereographic (variant B)") && (n.lat0 = Qe(n.lat1 > 0 ? 90 : -90), n.lat_ts = n.lat1);
}
function jf(n) {
  var t = Sx(n), e = t.shift(), i = t.shift();
  t.unshift(["name", i]), t.unshift(["type", e]);
  var s = {};
  return Nn(t, s), bx(s), s;
}
function qt(n) {
  var t = this;
  if (arguments.length === 2) {
    var e = arguments[1];
    typeof e == "string" ? e.charAt(0) === "+" ? qt[n] = ll(arguments[1]) : qt[n] = jf(arguments[1]) : qt[n] = e;
  } else if (arguments.length === 1) {
    if (Array.isArray(n))
      return n.map(function(i) {
        Array.isArray(i) ? qt.apply(t, i) : qt(i);
      });
    if (typeof n == "string") {
      if (n in qt)
        return qt[n];
    } else
      "EPSG" in n ? qt["EPSG:" + n.EPSG] = n : "ESRI" in n ? qt["ESRI:" + n.ESRI] = n : "IAU2000" in n ? qt["IAU2000:" + n.IAU2000] = n : console.log(n);
    return;
  }
}
mx(qt);
function Lx(n) {
  return typeof n == "string";
}
function Ix(n) {
  return n in qt;
}
var Px = ["PROJECTEDCRS", "PROJCRS", "GEOGCS", "GEOCCS", "PROJCS", "LOCAL_CS", "GEODCRS", "GEODETICCRS", "GEODETICDATUM", "ENGCRS", "ENGINEERINGCRS"];
function Ax(n) {
  return Px.some(function(t) {
    return n.indexOf(t) > -1;
  });
}
var Ox = ["3857", "900913", "3785", "102113"];
function Fx(n) {
  var t = Oi(n, "authority");
  if (!!t) {
    var e = Oi(t, "epsg");
    return e && Ox.indexOf(e) > -1;
  }
}
function Nx(n) {
  var t = Oi(n, "extension");
  if (!!t)
    return Oi(t, "proj4");
}
function Dx(n) {
  return n[0] === "+";
}
function kx(n) {
  if (Lx(n)) {
    if (Ix(n))
      return qt[n];
    if (Ax(n)) {
      var t = jf(n);
      if (Fx(t))
        return qt["EPSG:3857"];
      var e = Nx(t);
      return e ? ll(e) : t;
    }
    if (Dx(n))
      return ll(n);
  } else
    return n;
}
function _u(n, t) {
  n = n || {};
  var e, i;
  if (!t)
    return n;
  for (i in t)
    e = t[i], e !== void 0 && (n[i] = e);
  return n;
}
function We(n, t, e) {
  var i = n * t;
  return e / Math.sqrt(1 - i * i);
}
function cr(n) {
  return n < 0 ? -1 : 1;
}
function A(n) {
  return Math.abs(n) <= Tt ? n : n - cr(n) * Hs;
}
function Ae(n, t, e) {
  var i = n * e, s = 0.5 * n;
  return i = Math.pow((1 - i) / (1 + i), s), Math.tan(0.5 * (S - t)) / i;
}
function Ys(n, t) {
  for (var e = 0.5 * n, i, s, r = S - 2 * Math.atan(t), o = 0; o <= 15; o++)
    if (i = n * Math.sin(r), s = S - 2 * Math.atan(t * Math.pow((1 - i) / (1 + i), e)) - r, r += s, Math.abs(s) <= 1e-10)
      return r;
  return -9999;
}
function Gx() {
  var n = this.b / this.a;
  this.es = 1 - n * n, "x0" in this || (this.x0 = 0), "y0" in this || (this.y0 = 0), this.e = Math.sqrt(this.es), this.lat_ts ? this.sphere ? this.k0 = Math.cos(this.lat_ts) : this.k0 = We(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) : this.k0 || (this.k ? this.k0 = this.k : this.k0 = 1);
}
function $x(n) {
  var t = n.x, e = n.y;
  if (e * Ge > 90 && e * Ge < -90 && t * Ge > 180 && t * Ge < -180)
    return null;
  var i, s;
  if (Math.abs(Math.abs(e) - S) <= I)
    return null;
  if (this.sphere)
    i = this.x0 + this.a * this.k0 * A(t - this.long0), s = this.y0 + this.a * this.k0 * Math.log(Math.tan(ct + 0.5 * e));
  else {
    var r = Math.sin(e), o = Ae(this.e, e, r);
    i = this.x0 + this.a * this.k0 * A(t - this.long0), s = this.y0 - this.a * this.k0 * Math.log(o);
  }
  return n.x = i, n.y = s, n;
}
function Bx(n) {
  var t = n.x - this.x0, e = n.y - this.y0, i, s;
  if (this.sphere)
    s = S - 2 * Math.atan(Math.exp(-e / (this.a * this.k0)));
  else {
    var r = Math.exp(-e / (this.a * this.k0));
    if (s = Ys(this.e, r), s === -9999)
      return null;
  }
  return i = A(this.long0 + t / (this.a * this.k0)), n.x = i, n.y = s, n;
}
var zx = ["Mercator", "Popular Visualisation Pseudo Mercator", "Mercator_1SP", "Mercator_Auxiliary_Sphere", "merc"];
const Zx = {
  init: Gx,
  forward: $x,
  inverse: Bx,
  names: zx
};
function Vx() {
}
function pu(n) {
  return n;
}
var Ux = ["longlat", "identity"];
const Wx = {
  init: Vx,
  forward: pu,
  inverse: pu,
  names: Ux
};
var Hx = [Zx, Wx], Xr = {}, Co = [];
function qf(n, t) {
  var e = Co.length;
  return n.names ? (Co[e] = n, n.names.forEach(function(i) {
    Xr[i.toLowerCase()] = e;
  }), this) : (console.log(t), !0);
}
function Xx(n) {
  if (!n)
    return !1;
  var t = n.toLowerCase();
  if (typeof Xr[t] < "u" && Co[Xr[t]])
    return Co[Xr[t]];
}
function Yx() {
  Hx.forEach(qf);
}
const jx = {
  start: Yx,
  add: qf,
  get: Xx
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
var qx = j.WGS84 = {
  a: 6378137,
  rf: 298.257223563,
  ellipseName: "WGS 84"
};
j.sphere = {
  a: 6370997,
  b: 6370997,
  ellipseName: "Normal Sphere (r=6370997)"
};
function Kx(n, t, e, i) {
  var s = n * n, r = t * t, o = (s - r) / s, a = 0;
  i ? (n *= 1 - o * (yx + o * (vx + o * xx)), s = n * n, o = 0) : a = Math.sqrt(o);
  var l = (s - r) / r;
  return {
    es: o,
    e: a,
    ep2: l
  };
}
function Jx(n, t, e, i, s) {
  if (!n) {
    var r = Oi(j, i);
    r || (r = qx), n = r.a, t = r.b, e = r.rf;
  }
  return e && !t && (t = (1 - 1 / e) * n), (e === 0 || Math.abs(n - t) < I) && (s = !0, t = n), {
    a: n,
    b: t,
    rf: e,
    sphere: s
  };
}
var $t = {};
$t.wgs84 = {
  towgs84: "0,0,0",
  ellipse: "WGS84",
  datumName: "WGS84"
};
$t.ch1903 = {
  towgs84: "674.374,15.056,405.346",
  ellipse: "bessel",
  datumName: "swiss"
};
$t.ggrs87 = {
  towgs84: "-199.87,74.79,246.62",
  ellipse: "GRS80",
  datumName: "Greek_Geodetic_Reference_System_1987"
};
$t.nad83 = {
  towgs84: "0,0,0",
  ellipse: "GRS80",
  datumName: "North_American_Datum_1983"
};
$t.nad27 = {
  nadgrids: "@conus,@alaska,@ntv2_0.gsb,@ntv1_can.dat",
  ellipse: "clrk66",
  datumName: "North_American_Datum_1927"
};
$t.potsdam = {
  towgs84: "598.1,73.7,418.2,0.202,0.045,-2.455,6.7",
  ellipse: "bessel",
  datumName: "Potsdam Rauenberg 1950 DHDN"
};
$t.carthage = {
  towgs84: "-263.0,6.0,431.0",
  ellipse: "clark80",
  datumName: "Carthage 1934 Tunisia"
};
$t.hermannskogel = {
  towgs84: "577.326,90.129,463.919,5.137,1.474,5.297,2.4232",
  ellipse: "bessel",
  datumName: "Hermannskogel"
};
$t.osni52 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "airy",
  datumName: "Irish National"
};
$t.ire65 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "mod_airy",
  datumName: "Ireland 1965"
};
$t.rassadiran = {
  towgs84: "-133.63,-157.5,-158.62",
  ellipse: "intl",
  datumName: "Rassadiran"
};
$t.nzgd49 = {
  towgs84: "59.47,-5.04,187.44,0.47,-0.1,1.024,-4.5993",
  ellipse: "intl",
  datumName: "New Zealand Geodetic Datum 1949"
};
$t.osgb36 = {
  towgs84: "446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894",
  ellipse: "airy",
  datumName: "Airy 1830"
};
$t.s_jtsk = {
  towgs84: "589,76,480",
  ellipse: "bessel",
  datumName: "S-JTSK (Ferro)"
};
$t.beduaram = {
  towgs84: "-106,-87,188",
  ellipse: "clrk80",
  datumName: "Beduaram"
};
$t.gunung_segara = {
  towgs84: "-403,684,41",
  ellipse: "bessel",
  datumName: "Gunung Segara Jakarta"
};
$t.rnb72 = {
  towgs84: "106.869,-52.2978,103.724,-0.33657,0.456955,-1.84218,1",
  ellipse: "intl",
  datumName: "Reseau National Belge 1972"
};
function Qx(n, t, e, i, s, r, o) {
  var a = {};
  return n === void 0 || n === "none" ? a.datum_type = al : a.datum_type = _x, t && (a.datum_params = t.map(parseFloat), (a.datum_params[0] !== 0 || a.datum_params[1] !== 0 || a.datum_params[2] !== 0) && (a.datum_type = ln), a.datum_params.length > 3 && (a.datum_params[3] !== 0 || a.datum_params[4] !== 0 || a.datum_params[5] !== 0 || a.datum_params[6] !== 0) && (a.datum_type = hn, a.datum_params[3] *= Is, a.datum_params[4] *= Is, a.datum_params[5] *= Is, a.datum_params[6] = a.datum_params[6] / 1e6 + 1)), o && (a.datum_type = Hr, a.grids = o), a.a = e, a.b = i, a.es = s, a.ep2 = r, a;
}
var Kf = {};
function t3(n, t) {
  var e = new DataView(t), i = n3(e), s = s3(e, i);
  s.nSubgrids > 1 && console.log("Only single NTv2 subgrids are currently supported, subsequent sub grids are ignored");
  var r = r3(e, s, i), o = { header: s, subgrids: r };
  return Kf[n] = o, o;
}
function e3(n) {
  if (n === void 0)
    return null;
  var t = n.split(",");
  return t.map(i3);
}
function i3(n) {
  if (n.length === 0)
    return null;
  var t = n[0] === "@";
  return t && (n = n.slice(1)), n === "null" ? { name: "null", mandatory: !t, grid: null, isNull: !0 } : {
    name: n,
    mandatory: !t,
    grid: Kf[n] || null,
    isNull: !1
  };
}
function Dn(n) {
  return n / 3600 * Math.PI / 180;
}
function n3(n) {
  var t = n.getInt32(8, !1);
  return t === 11 ? !1 : (t = n.getInt32(8, !0), t !== 11 && console.warn("Failed to detect nadgrid endian-ness, defaulting to little-endian"), !0);
}
function s3(n, t) {
  return {
    nFields: n.getInt32(8, t),
    nSubgridFields: n.getInt32(24, t),
    nSubgrids: n.getInt32(40, t),
    shiftType: hl(n, 56, 56 + 8).trim(),
    fromSemiMajorAxis: n.getFloat64(120, t),
    fromSemiMinorAxis: n.getFloat64(136, t),
    toSemiMajorAxis: n.getFloat64(152, t),
    toSemiMinorAxis: n.getFloat64(168, t)
  };
}
function hl(n, t, e) {
  return String.fromCharCode.apply(null, new Uint8Array(n.buffer.slice(t, e)));
}
function r3(n, t, e) {
  for (var i = 176, s = [], r = 0; r < t.nSubgrids; r++) {
    var o = a3(n, i, e), a = l3(n, i, o, e), l = Math.round(
      1 + (o.upperLongitude - o.lowerLongitude) / o.longitudeInterval
    ), h = Math.round(
      1 + (o.upperLatitude - o.lowerLatitude) / o.latitudeInterval
    );
    s.push({
      ll: [Dn(o.lowerLongitude), Dn(o.lowerLatitude)],
      del: [Dn(o.longitudeInterval), Dn(o.latitudeInterval)],
      lim: [l, h],
      count: o.gridNodeCount,
      cvs: o3(a)
    });
  }
  return s;
}
function o3(n) {
  return n.map(function(t) {
    return [Dn(t.longitudeShift), Dn(t.latitudeShift)];
  });
}
function a3(n, t, e) {
  return {
    name: hl(n, t + 8, t + 16).trim(),
    parent: hl(n, t + 24, t + 24 + 8).trim(),
    lowerLatitude: n.getFloat64(t + 72, e),
    upperLatitude: n.getFloat64(t + 88, e),
    lowerLongitude: n.getFloat64(t + 104, e),
    upperLongitude: n.getFloat64(t + 120, e),
    latitudeInterval: n.getFloat64(t + 136, e),
    longitudeInterval: n.getFloat64(t + 152, e),
    gridNodeCount: n.getInt32(t + 168, e)
  };
}
function l3(n, t, e, i) {
  for (var s = t + 176, r = 16, o = [], a = 0; a < e.gridNodeCount; a++) {
    var l = {
      latitudeShift: n.getFloat32(s + a * r, i),
      longitudeShift: n.getFloat32(s + a * r + 4, i),
      latitudeAccuracy: n.getFloat32(s + a * r + 8, i),
      longitudeAccuracy: n.getFloat32(s + a * r + 12, i)
    };
    o.push(l);
  }
  return o;
}
function Be(n, t) {
  if (!(this instanceof Be))
    return new Be(n);
  t = t || function(h) {
    if (h)
      throw h;
  };
  var e = kx(n);
  if (typeof e != "object") {
    t(n);
    return;
  }
  var i = Be.projections.get(e.projName);
  if (!i) {
    t(n);
    return;
  }
  if (e.datumCode && e.datumCode !== "none") {
    var s = Oi($t, e.datumCode);
    s && (e.datum_params = e.datum_params || (s.towgs84 ? s.towgs84.split(",") : null), e.ellps = s.ellipse, e.datumName = s.datumName ? s.datumName : e.datumCode);
  }
  e.k0 = e.k0 || 1, e.axis = e.axis || "enu", e.ellps = e.ellps || "wgs84", e.lat1 = e.lat1 || e.lat0;
  var r = Jx(e.a, e.b, e.rf, e.ellps, e.sphere), o = Kx(r.a, r.b, r.rf, e.R_A), a = e3(e.nadgrids), l = e.datum || Qx(
    e.datumCode,
    e.datum_params,
    r.a,
    r.b,
    o.es,
    o.ep2,
    a
  );
  _u(this, e), _u(this, i), this.a = r.a, this.b = r.b, this.rf = r.rf, this.sphere = r.sphere, this.es = o.es, this.e = o.e, this.ep2 = o.ep2, this.datum = l, this.init(), t(null, this);
}
Be.projections = jx;
Be.projections.start();
function h3(n, t) {
  return n.datum_type !== t.datum_type || n.a !== t.a || Math.abs(n.es - t.es) > 5e-11 ? !1 : n.datum_type === ln ? n.datum_params[0] === t.datum_params[0] && n.datum_params[1] === t.datum_params[1] && n.datum_params[2] === t.datum_params[2] : n.datum_type === hn ? n.datum_params[0] === t.datum_params[0] && n.datum_params[1] === t.datum_params[1] && n.datum_params[2] === t.datum_params[2] && n.datum_params[3] === t.datum_params[3] && n.datum_params[4] === t.datum_params[4] && n.datum_params[5] === t.datum_params[5] && n.datum_params[6] === t.datum_params[6] : !0;
}
function Jf(n, t, e) {
  var i = n.x, s = n.y, r = n.z ? n.z : 0, o, a, l, h;
  if (s < -S && s > -1.001 * S)
    s = -S;
  else if (s > S && s < 1.001 * S)
    s = S;
  else {
    if (s < -S)
      return { x: -1 / 0, y: -1 / 0, z: n.z };
    if (s > S)
      return { x: 1 / 0, y: 1 / 0, z: n.z };
  }
  return i > Math.PI && (i -= 2 * Math.PI), a = Math.sin(s), h = Math.cos(s), l = a * a, o = e / Math.sqrt(1 - t * l), {
    x: (o + r) * h * Math.cos(i),
    y: (o + r) * h * Math.sin(i),
    z: (o * (1 - t) + r) * a
  };
}
function Qf(n, t, e, i) {
  var s = 1e-12, r = s * s, o = 30, a, l, h, c, u, d, f, g, m, _, y, p, v, x = n.x, C = n.y, E = n.z ? n.z : 0, R, b, F;
  if (a = Math.sqrt(x * x + C * C), l = Math.sqrt(x * x + C * C + E * E), a / e < s) {
    if (R = 0, l / e < s)
      return b = S, F = -i, {
        x: n.x,
        y: n.y,
        z: n.z
      };
  } else
    R = Math.atan2(C, x);
  h = E / l, c = a / l, u = 1 / Math.sqrt(1 - t * (2 - t) * c * c), g = c * (1 - t) * u, m = h * u, v = 0;
  do
    v++, f = e / Math.sqrt(1 - t * m * m), F = a * g + E * m - f * (1 - t * m * m), d = t * f / (f + F), u = 1 / Math.sqrt(1 - d * (2 - d) * c * c), _ = c * (1 - d) * u, y = h * u, p = y * g - _ * m, g = _, m = y;
  while (p * p > r && v < o);
  return b = Math.atan(y / Math.abs(_)), {
    x: R,
    y: b,
    z: F
  };
}
function c3(n, t, e) {
  if (t === ln)
    return {
      x: n.x + e[0],
      y: n.y + e[1],
      z: n.z + e[2]
    };
  if (t === hn) {
    var i = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6];
    return {
      x: h * (n.x - l * n.y + a * n.z) + i,
      y: h * (l * n.x + n.y - o * n.z) + s,
      z: h * (-a * n.x + o * n.y + n.z) + r
    };
  }
}
function u3(n, t, e) {
  if (t === ln)
    return {
      x: n.x - e[0],
      y: n.y - e[1],
      z: n.z - e[2]
    };
  if (t === hn) {
    var i = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6], c = (n.x - i) / h, u = (n.y - s) / h, d = (n.z - r) / h;
    return {
      x: c + l * u - a * d,
      y: -l * c + u + o * d,
      z: a * c - o * u + d
    };
  }
}
function Vr(n) {
  return n === ln || n === hn;
}
function d3(n, t, e) {
  if (h3(n, t) || n.datum_type === al || t.datum_type === al)
    return e;
  var i = n.a, s = n.es;
  if (n.datum_type === Hr) {
    var r = yu(n, !1, e);
    if (r !== 0)
      return;
    i = du, s = fu;
  }
  var o = t.a, a = t.b, l = t.es;
  if (t.datum_type === Hr && (o = du, a = px, l = fu), s === l && i === o && !Vr(n.datum_type) && !Vr(t.datum_type))
    return e;
  if (e = Jf(e, s, i), Vr(n.datum_type) && (e = c3(e, n.datum_type, n.datum_params)), Vr(t.datum_type) && (e = u3(e, t.datum_type, t.datum_params)), e = Qf(e, l, o, a), t.datum_type === Hr) {
    var h = yu(t, !0, e);
    if (h !== 0)
      return;
  }
  return e;
}
function yu(n, t, e) {
  if (n.grids === null || n.grids.length === 0)
    return console.log("Grid shift grids not found"), -1;
  for (var i = { x: -e.x, y: e.y }, s = { x: Number.NaN, y: Number.NaN }, r = [], o = 0; o < n.grids.length; o++) {
    var a = n.grids[o];
    if (r.push(a.name), a.isNull) {
      s = i;
      break;
    }
    if (a.mandatory, a.grid === null) {
      if (a.mandatory)
        return console.log("Unable to find mandatory grid '" + a.name + "'"), -1;
      continue;
    }
    var l = a.grid.subgrids[0], h = (Math.abs(l.del[1]) + Math.abs(l.del[0])) / 1e4, c = l.ll[0] - h, u = l.ll[1] - h, d = l.ll[0] + (l.lim[0] - 1) * l.del[0] + h, f = l.ll[1] + (l.lim[1] - 1) * l.del[1] + h;
    if (!(u > i.y || c > i.x || f < i.y || d < i.x) && (s = f3(i, t, l), !isNaN(s.x)))
      break;
  }
  return isNaN(s.x) ? (console.log("Failed to find a grid shift table for location '" + -i.x * Ge + " " + i.y * Ge + " tried: '" + r + "'"), -1) : (e.x = -s.x, e.y = s.y, 0);
}
function f3(n, t, e) {
  var i = { x: Number.NaN, y: Number.NaN };
  if (isNaN(n.x))
    return i;
  var s = { x: n.x, y: n.y };
  s.x -= e.ll[0], s.y -= e.ll[1], s.x = A(s.x - Math.PI) + Math.PI;
  var r = vu(s, e);
  if (t) {
    if (isNaN(r.x))
      return i;
    r.x = s.x - r.x, r.y = s.y - r.y;
    var o = 9, a = 1e-12, l, h;
    do {
      if (h = vu(r, e), isNaN(h.x)) {
        console.log("Inverse grid shift iteration failed, presumably at grid edge.  Using first approximation.");
        break;
      }
      l = { x: s.x - (h.x + r.x), y: s.y - (h.y + r.y) }, r.x += l.x, r.y += l.y;
    } while (o-- && Math.abs(l.x) > a && Math.abs(l.y) > a);
    if (o < 0)
      return console.log("Inverse grid shift iterator failed to converge."), i;
    i.x = A(r.x + e.ll[0]), i.y = r.y + e.ll[1];
  } else
    isNaN(r.x) || (i.x = n.x + r.x, i.y = n.y + r.y);
  return i;
}
function vu(n, t) {
  var e = { x: n.x / t.del[0], y: n.y / t.del[1] }, i = { x: Math.floor(e.x), y: Math.floor(e.y) }, s = { x: e.x - 1 * i.x, y: e.y - 1 * i.y }, r = { x: Number.NaN, y: Number.NaN }, o;
  if (i.x < 0 || i.x >= t.lim[0] || i.y < 0 || i.y >= t.lim[1])
    return r;
  o = i.y * t.lim[0] + i.x;
  var a = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o++;
  var l = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o += t.lim[0];
  var h = { x: t.cvs[o][0], y: t.cvs[o][1] };
  o--;
  var c = { x: t.cvs[o][0], y: t.cvs[o][1] }, u = s.x * s.y, d = s.x * (1 - s.y), f = (1 - s.x) * (1 - s.y), g = (1 - s.x) * s.y;
  return r.x = f * a.x + d * l.x + g * c.x + u * h.x, r.y = f * a.y + d * l.y + g * c.y + u * h.y, r;
}
function xu(n, t, e) {
  var i = e.x, s = e.y, r = e.z || 0, o, a, l, h = {};
  for (l = 0; l < 3; l++)
    if (!(t && l === 2 && e.z === void 0))
      switch (l === 0 ? (o = i, "ew".indexOf(n.axis[l]) !== -1 ? a = "x" : a = "y") : l === 1 ? (o = s, "ns".indexOf(n.axis[l]) !== -1 ? a = "y" : a = "x") : (o = r, a = "z"), n.axis[l]) {
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
function tg(n) {
  var t = {
    x: n[0],
    y: n[1]
  };
  return n.length > 2 && (t.z = n[2]), n.length > 3 && (t.m = n[3]), t;
}
function g3(n) {
  Cu(n.x), Cu(n.y);
}
function Cu(n) {
  if (typeof Number.isFinite == "function") {
    if (Number.isFinite(n))
      return;
    throw new TypeError("coordinates must be finite numbers");
  }
  if (typeof n != "number" || n !== n || !isFinite(n))
    throw new TypeError("coordinates must be finite numbers");
}
function m3(n, t) {
  return (n.datum.datum_type === ln || n.datum.datum_type === hn) && t.datumCode !== "WGS84" || (t.datum.datum_type === ln || t.datum.datum_type === hn) && n.datumCode !== "WGS84";
}
function Mo(n, t, e, i) {
  var s;
  if (Array.isArray(e) && (e = tg(e)), g3(e), n.datum && t.datum && m3(n, t) && (s = new Be("WGS84"), e = Mo(n, s, e, i), n = s), i && n.axis !== "enu" && (e = xu(n, !1, e)), n.projName === "longlat")
    e = {
      x: e.x * zt,
      y: e.y * zt,
      z: e.z || 0
    };
  else if (n.to_meter && (e = {
    x: e.x * n.to_meter,
    y: e.y * n.to_meter,
    z: e.z || 0
  }), e = n.inverse(e), !e)
    return;
  if (n.from_greenwich && (e.x += n.from_greenwich), e = d3(n.datum, t.datum, e), !!e)
    return t.from_greenwich && (e = {
      x: e.x - t.from_greenwich,
      y: e.y,
      z: e.z || 0
    }), t.projName === "longlat" ? e = {
      x: e.x * Ge,
      y: e.y * Ge,
      z: e.z || 0
    } : (e = t.forward(e), t.to_meter && (e = {
      x: e.x / t.to_meter,
      y: e.y / t.to_meter,
      z: e.z || 0
    })), i && t.axis !== "enu" ? xu(t, !0, e) : e;
}
var Mu = Be("WGS84");
function Sa(n, t, e, i) {
  var s, r, o;
  return Array.isArray(e) ? (s = Mo(n, t, e, i) || { x: NaN, y: NaN }, e.length > 2 ? typeof n.name < "u" && n.name === "geocent" || typeof t.name < "u" && t.name === "geocent" ? typeof s.z == "number" ? [s.x, s.y, s.z].concat(e.splice(3)) : [s.x, s.y, e[2]].concat(e.splice(3)) : [s.x, s.y].concat(e.splice(2)) : [s.x, s.y]) : (r = Mo(n, t, e, i), o = Object.keys(e), o.length === 2 || o.forEach(function(a) {
    if (typeof n.name < "u" && n.name === "geocent" || typeof t.name < "u" && t.name === "geocent") {
      if (a === "x" || a === "y" || a === "z")
        return;
    } else if (a === "x" || a === "y")
      return;
    r[a] = e[a];
  }), r);
}
function Eu(n) {
  return n instanceof Be ? n : n.oProj ? n.oProj : Be(n);
}
function re(n, t, e) {
  n = Eu(n);
  var i = !1, s;
  return typeof t > "u" ? (t = n, n = Mu, i = !0) : (typeof t.x < "u" || Array.isArray(t)) && (e = t, t = n, n = Mu, i = !0), t = Eu(t), e ? Sa(n, t, e) : (s = {
    forward: function(r, o) {
      return Sa(n, t, r, o);
    },
    inverse: function(r, o) {
      return Sa(t, n, r, o);
    }
  }, i && (s.oProj = t), s);
}
var wu = 6, eg = "AJSAJS", ig = "AFAFAF", kn = 65, ie = 73, Me = 79, Cs = 86, Ms = 90;
const _3 = {
  forward: ng,
  inverse: p3,
  toPoint: sg
};
function ng(n, t) {
  return t = t || 5, x3(y3({
    lat: n[1],
    lon: n[0]
  }), t);
}
function p3(n) {
  var t = _h(og(n.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat, t.lon, t.lat] : [t.left, t.bottom, t.right, t.top];
}
function sg(n) {
  var t = _h(og(n.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat] : [(t.left + t.right) / 2, (t.top + t.bottom) / 2];
}
function Ra(n) {
  return n * (Math.PI / 180);
}
function Su(n) {
  return 180 * (n / Math.PI);
}
function y3(n) {
  var t = n.lat, e = n.lon, i = 6378137, s = 669438e-8, r = 0.9996, o, a, l, h, c, u, d, f = Ra(t), g = Ra(e), m, _;
  _ = Math.floor((e + 180) / 6) + 1, e === 180 && (_ = 60), t >= 56 && t < 64 && e >= 3 && e < 12 && (_ = 32), t >= 72 && t < 84 && (e >= 0 && e < 9 ? _ = 31 : e >= 9 && e < 21 ? _ = 33 : e >= 21 && e < 33 ? _ = 35 : e >= 33 && e < 42 && (_ = 37)), o = (_ - 1) * 6 - 180 + 3, m = Ra(o), a = s / (1 - s), l = i / Math.sqrt(1 - s * Math.sin(f) * Math.sin(f)), h = Math.tan(f) * Math.tan(f), c = a * Math.cos(f) * Math.cos(f), u = Math.cos(f) * (g - m), d = i * ((1 - s / 4 - 3 * s * s / 64 - 5 * s * s * s / 256) * f - (3 * s / 8 + 3 * s * s / 32 + 45 * s * s * s / 1024) * Math.sin(2 * f) + (15 * s * s / 256 + 45 * s * s * s / 1024) * Math.sin(4 * f) - 35 * s * s * s / 3072 * Math.sin(6 * f));
  var y = r * l * (u + (1 - h + c) * u * u * u / 6 + (5 - 18 * h + h * h + 72 * c - 58 * a) * u * u * u * u * u / 120) + 5e5, p = r * (d + l * Math.tan(f) * (u * u / 2 + (5 - h + 9 * c + 4 * c * c) * u * u * u * u / 24 + (61 - 58 * h + h * h + 600 * c - 330 * a) * u * u * u * u * u * u / 720));
  return t < 0 && (p += 1e7), {
    northing: Math.round(p),
    easting: Math.round(y),
    zoneNumber: _,
    zoneLetter: v3(t)
  };
}
function _h(n) {
  var t = n.northing, e = n.easting, i = n.zoneLetter, s = n.zoneNumber;
  if (s < 0 || s > 60)
    return null;
  var r = 0.9996, o = 6378137, a = 669438e-8, l, h = (1 - Math.sqrt(1 - a)) / (1 + Math.sqrt(1 - a)), c, u, d, f, g, m, _, y, p, v = e - 5e5, x = t;
  i < "N" && (x -= 1e7), _ = (s - 1) * 6 - 180 + 3, l = a / (1 - a), m = x / r, y = m / (o * (1 - a / 4 - 3 * a * a / 64 - 5 * a * a * a / 256)), p = y + (3 * h / 2 - 27 * h * h * h / 32) * Math.sin(2 * y) + (21 * h * h / 16 - 55 * h * h * h * h / 32) * Math.sin(4 * y) + 151 * h * h * h / 96 * Math.sin(6 * y), c = o / Math.sqrt(1 - a * Math.sin(p) * Math.sin(p)), u = Math.tan(p) * Math.tan(p), d = l * Math.cos(p) * Math.cos(p), f = o * (1 - a) / Math.pow(1 - a * Math.sin(p) * Math.sin(p), 1.5), g = v / (c * r);
  var C = p - c * Math.tan(p) / f * (g * g / 2 - (5 + 3 * u + 10 * d - 4 * d * d - 9 * l) * g * g * g * g / 24 + (61 + 90 * u + 298 * d + 45 * u * u - 252 * l - 3 * d * d) * g * g * g * g * g * g / 720);
  C = Su(C);
  var E = (g - (1 + 2 * u + d) * g * g * g / 6 + (5 - 2 * d + 28 * u - 3 * d * d + 8 * l + 24 * u * u) * g * g * g * g * g / 120) / Math.cos(p);
  E = _ + Su(E);
  var R;
  if (n.accuracy) {
    var b = _h({
      northing: n.northing + n.accuracy,
      easting: n.easting + n.accuracy,
      zoneLetter: n.zoneLetter,
      zoneNumber: n.zoneNumber
    });
    R = {
      top: b.lat,
      right: b.lon,
      bottom: C,
      left: E
    };
  } else
    R = {
      lat: C,
      lon: E
    };
  return R;
}
function v3(n) {
  var t = "Z";
  return 84 >= n && n >= 72 ? t = "X" : 72 > n && n >= 64 ? t = "W" : 64 > n && n >= 56 ? t = "V" : 56 > n && n >= 48 ? t = "U" : 48 > n && n >= 40 ? t = "T" : 40 > n && n >= 32 ? t = "S" : 32 > n && n >= 24 ? t = "R" : 24 > n && n >= 16 ? t = "Q" : 16 > n && n >= 8 ? t = "P" : 8 > n && n >= 0 ? t = "N" : 0 > n && n >= -8 ? t = "M" : -8 > n && n >= -16 ? t = "L" : -16 > n && n >= -24 ? t = "K" : -24 > n && n >= -32 ? t = "J" : -32 > n && n >= -40 ? t = "H" : -40 > n && n >= -48 ? t = "G" : -48 > n && n >= -56 ? t = "F" : -56 > n && n >= -64 ? t = "E" : -64 > n && n >= -72 ? t = "D" : -72 > n && n >= -80 && (t = "C"), t;
}
function x3(n, t) {
  var e = "00000" + n.easting, i = "00000" + n.northing;
  return n.zoneNumber + n.zoneLetter + C3(n.easting, n.northing, n.zoneNumber) + e.substr(e.length - 5, t) + i.substr(i.length - 5, t);
}
function C3(n, t, e) {
  var i = rg(e), s = Math.floor(n / 1e5), r = Math.floor(t / 1e5) % 20;
  return M3(s, r, i);
}
function rg(n) {
  var t = n % wu;
  return t === 0 && (t = wu), t;
}
function M3(n, t, e) {
  var i = e - 1, s = eg.charCodeAt(i), r = ig.charCodeAt(i), o = s + n - 1, a = r + t, l = !1;
  o > Ms && (o = o - Ms + kn - 1, l = !0), (o === ie || s < ie && o > ie || (o > ie || s < ie) && l) && o++, (o === Me || s < Me && o > Me || (o > Me || s < Me) && l) && (o++, o === ie && o++), o > Ms && (o = o - Ms + kn - 1), a > Cs ? (a = a - Cs + kn - 1, l = !0) : l = !1, (a === ie || r < ie && a > ie || (a > ie || r < ie) && l) && a++, (a === Me || r < Me && a > Me || (a > Me || r < Me) && l) && (a++, a === ie && a++), a > Cs && (a = a - Cs + kn - 1);
  var h = String.fromCharCode(o) + String.fromCharCode(a);
  return h;
}
function og(n) {
  if (n && n.length === 0)
    throw "MGRSPoint coverting from nothing";
  for (var t = n.length, e = null, i = "", s, r = 0; !/[A-Z]/.test(s = n.charAt(r)); ) {
    if (r >= 2)
      throw "MGRSPoint bad conversion from: " + n;
    i += s, r++;
  }
  var o = parseInt(i, 10);
  if (r === 0 || r + 3 > t)
    throw "MGRSPoint bad conversion from: " + n;
  var a = n.charAt(r++);
  if (a <= "A" || a === "B" || a === "Y" || a >= "Z" || a === "I" || a === "O")
    throw "MGRSPoint zone letter " + a + " not handled: " + n;
  e = n.substring(r, r += 2);
  for (var l = rg(o), h = E3(e.charAt(0), l), c = w3(e.charAt(1), l); c < S3(a); )
    c += 2e6;
  var u = t - r;
  if (u % 2 !== 0)
    throw `MGRSPoint has to have an even number 
of digits after the zone letter and two 100km letters - front 
half for easting meters, second half for 
northing meters` + n;
  var d = u / 2, f = 0, g = 0, m, _, y, p, v;
  return d > 0 && (m = 1e5 / Math.pow(10, d), _ = n.substring(r, r + d), f = parseFloat(_) * m, y = n.substring(r + d), g = parseFloat(y) * m), p = f + h, v = g + c, {
    easting: p,
    northing: v,
    zoneLetter: a,
    zoneNumber: o,
    accuracy: m
  };
}
function E3(n, t) {
  for (var e = eg.charCodeAt(t - 1), i = 1e5, s = !1; e !== n.charCodeAt(0); ) {
    if (e++, e === ie && e++, e === Me && e++, e > Ms) {
      if (s)
        throw "Bad character: " + n;
      e = kn, s = !0;
    }
    i += 1e5;
  }
  return i;
}
function w3(n, t) {
  if (n > "V")
    throw "MGRSPoint given invalid Northing " + n;
  for (var e = ig.charCodeAt(t - 1), i = 0, s = !1; e !== n.charCodeAt(0); ) {
    if (e++, e === ie && e++, e === Me && e++, e > Cs) {
      if (s)
        throw "Bad character: " + n;
      e = kn, s = !0;
    }
    i += 1e5;
  }
  return i;
}
function S3(n) {
  var t;
  switch (n) {
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
  throw "Invalid zone letter: " + n;
}
function Qn(n, t, e) {
  if (!(this instanceof Qn))
    return new Qn(n, t, e);
  if (Array.isArray(n))
    this.x = n[0], this.y = n[1], this.z = n[2] || 0;
  else if (typeof n == "object")
    this.x = n.x, this.y = n.y, this.z = n.z || 0;
  else if (typeof n == "string" && typeof t > "u") {
    var i = n.split(",");
    this.x = parseFloat(i[0], 10), this.y = parseFloat(i[1], 10), this.z = parseFloat(i[2], 10) || 0;
  } else
    this.x = n, this.y = t, this.z = e || 0;
  console.warn("proj4.Point will be removed in version 3, use proj4.toPoint");
}
Qn.fromMGRS = function(n) {
  return new Qn(sg(n));
};
Qn.prototype.toMGRS = function(n) {
  return ng([this.x, this.y], n);
};
var R3 = 1, T3 = 0.25, Ru = 0.046875, Tu = 0.01953125, bu = 0.01068115234375, b3 = 0.75, L3 = 0.46875, I3 = 0.013020833333333334, P3 = 0.007120768229166667, A3 = 0.3645833333333333, O3 = 0.005696614583333333, F3 = 0.3076171875;
function ag(n) {
  var t = [];
  t[0] = R3 - n * (T3 + n * (Ru + n * (Tu + n * bu))), t[1] = n * (b3 - n * (Ru + n * (Tu + n * bu)));
  var e = n * n;
  return t[2] = e * (L3 - n * (I3 + n * P3)), e *= n, t[3] = e * (A3 - n * O3), t[4] = e * n * F3, t;
}
function Ho(n, t, e, i) {
  return e *= t, t *= t, i[0] * n - e * (i[1] + t * (i[2] + t * (i[3] + t * i[4])));
}
var N3 = 20;
function lg(n, t, e) {
  for (var i = 1 / (1 - t), s = n, r = N3; r; --r) {
    var o = Math.sin(s), a = 1 - t * o * o;
    if (a = (Ho(s, o, Math.cos(s), e) - n) * (a * Math.sqrt(a)) * i, s -= a, Math.abs(a) < I)
      return s;
  }
  return s;
}
function D3() {
  this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.es && (this.en = ag(this.es), this.ml0 = Ho(this.lat0, Math.sin(this.lat0), Math.cos(this.lat0), this.en));
}
function k3(n) {
  var t = n.x, e = n.y, i = A(t - this.long0), s, r, o, a = Math.sin(e), l = Math.cos(e);
  if (this.es) {
    var c = l * i, u = Math.pow(c, 2), d = this.ep2 * Math.pow(l, 2), f = Math.pow(d, 2), g = Math.abs(l) > I ? Math.tan(e) : 0, m = Math.pow(g, 2), _ = Math.pow(m, 2);
    s = 1 - this.es * Math.pow(a, 2), c = c / Math.sqrt(s);
    var y = Ho(e, a, l, this.en);
    r = this.a * (this.k0 * c * (1 + u / 6 * (1 - m + d + u / 20 * (5 - 18 * m + _ + 14 * d - 58 * m * d + u / 42 * (61 + 179 * _ - _ * m - 479 * m))))) + this.x0, o = this.a * (this.k0 * (y - this.ml0 + a * i * c / 2 * (1 + u / 12 * (5 - m + 9 * d + 4 * f + u / 30 * (61 + _ - 58 * m + 270 * d - 330 * m * d + u / 56 * (1385 + 543 * _ - _ * m - 3111 * m)))))) + this.y0;
  } else {
    var h = l * Math.sin(i);
    if (Math.abs(Math.abs(h) - 1) < I)
      return 93;
    if (r = 0.5 * this.a * this.k0 * Math.log((1 + h) / (1 - h)) + this.x0, o = l * Math.cos(i) / Math.sqrt(1 - Math.pow(h, 2)), h = Math.abs(o), h >= 1) {
      if (h - 1 > I)
        return 93;
      o = 0;
    } else
      o = Math.acos(o);
    e < 0 && (o = -o), o = this.a * this.k0 * (o - this.lat0) + this.y0;
  }
  return n.x = r, n.y = o, n;
}
function G3(n) {
  var t, e, i, s, r = (n.x - this.x0) * (1 / this.a), o = (n.y - this.y0) * (1 / this.a);
  if (this.es)
    if (t = this.ml0 + o / this.k0, e = lg(t, this.es, this.en), Math.abs(e) < S) {
      var u = Math.sin(e), d = Math.cos(e), f = Math.abs(d) > I ? Math.tan(e) : 0, g = this.ep2 * Math.pow(d, 2), m = Math.pow(g, 2), _ = Math.pow(f, 2), y = Math.pow(_, 2);
      t = 1 - this.es * Math.pow(u, 2);
      var p = r * Math.sqrt(t) / this.k0, v = Math.pow(p, 2);
      t = t * f, i = e - t * v / (1 - this.es) * 0.5 * (1 - v / 12 * (5 + 3 * _ - 9 * g * _ + g - 4 * m - v / 30 * (61 + 90 * _ - 252 * g * _ + 45 * y + 46 * g - v / 56 * (1385 + 3633 * _ + 4095 * y + 1574 * y * _)))), s = A(this.long0 + p * (1 - v / 6 * (1 + 2 * _ + g - v / 20 * (5 + 28 * _ + 24 * y + 8 * g * _ + 6 * g - v / 42 * (61 + 662 * _ + 1320 * y + 720 * y * _)))) / d);
    } else
      i = S * cr(o), s = 0;
  else {
    var a = Math.exp(r / this.k0), l = 0.5 * (a - 1 / a), h = this.lat0 + o / this.k0, c = Math.cos(h);
    t = Math.sqrt((1 - Math.pow(c, 2)) / (1 + Math.pow(l, 2))), i = Math.asin(t), o < 0 && (i = -i), l === 0 && c === 0 ? s = 0 : s = A(Math.atan2(l, c) + this.long0);
  }
  return n.x = s, n.y = i, n;
}
var $3 = ["Fast_Transverse_Mercator", "Fast Transverse Mercator"];
const Yr = {
  init: D3,
  forward: k3,
  inverse: G3,
  names: $3
};
function hg(n) {
  var t = Math.exp(n);
  return t = (t - 1 / t) / 2, t;
}
function Pe(n, t) {
  n = Math.abs(n), t = Math.abs(t);
  var e = Math.max(n, t), i = Math.min(n, t) / (e || 1);
  return e * Math.sqrt(1 + Math.pow(i, 2));
}
function B3(n) {
  var t = 1 + n, e = t - 1;
  return e === 0 ? n : n * Math.log(t) / e;
}
function z3(n) {
  var t = Math.abs(n);
  return t = B3(t * (1 + t / (Pe(1, t) + 1))), n < 0 ? -t : t;
}
function ph(n, t) {
  for (var e = 2 * Math.cos(2 * t), i = n.length - 1, s = n[i], r = 0, o; --i >= 0; )
    o = -r + e * s + n[i], r = s, s = o;
  return t + o * Math.sin(2 * t);
}
function Z3(n, t) {
  for (var e = 2 * Math.cos(t), i = n.length - 1, s = n[i], r = 0, o; --i >= 0; )
    o = -r + e * s + n[i], r = s, s = o;
  return Math.sin(t) * o;
}
function V3(n) {
  var t = Math.exp(n);
  return t = (t + 1 / t) / 2, t;
}
function cg(n, t, e) {
  for (var i = Math.sin(t), s = Math.cos(t), r = hg(e), o = V3(e), a = 2 * s * o, l = -2 * i * r, h = n.length - 1, c = n[h], u = 0, d = 0, f = 0, g, m; --h >= 0; )
    g = d, m = u, d = c, u = f, c = -g + a * d - l * u + n[h], f = -m + l * d + a * u;
  return a = i * o, l = s * r, [a * c - l * f, a * f + l * c];
}
function U3() {
  if (!this.approx && (isNaN(this.es) || this.es <= 0))
    throw new Error('Incorrect elliptical usage. Try using the +approx option in the proj string, or PROJECTION["Fast_Transverse_Mercator"] in the WKT.');
  this.approx && (Yr.init.apply(this), this.forward = Yr.forward, this.inverse = Yr.inverse), this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.cgb = [], this.cbg = [], this.utg = [], this.gtu = [];
  var n = this.es / (1 + Math.sqrt(1 - this.es)), t = n / (2 - n), e = t;
  this.cgb[0] = t * (2 + t * (-2 / 3 + t * (-2 + t * (116 / 45 + t * (26 / 45 + t * (-2854 / 675)))))), this.cbg[0] = t * (-2 + t * (2 / 3 + t * (4 / 3 + t * (-82 / 45 + t * (32 / 45 + t * (4642 / 4725)))))), e = e * t, this.cgb[1] = e * (7 / 3 + t * (-8 / 5 + t * (-227 / 45 + t * (2704 / 315 + t * (2323 / 945))))), this.cbg[1] = e * (5 / 3 + t * (-16 / 15 + t * (-13 / 9 + t * (904 / 315 + t * (-1522 / 945))))), e = e * t, this.cgb[2] = e * (56 / 15 + t * (-136 / 35 + t * (-1262 / 105 + t * (73814 / 2835)))), this.cbg[2] = e * (-26 / 15 + t * (34 / 21 + t * (8 / 5 + t * (-12686 / 2835)))), e = e * t, this.cgb[3] = e * (4279 / 630 + t * (-332 / 35 + t * (-399572 / 14175))), this.cbg[3] = e * (1237 / 630 + t * (-12 / 5 + t * (-24832 / 14175))), e = e * t, this.cgb[4] = e * (4174 / 315 + t * (-144838 / 6237)), this.cbg[4] = e * (-734 / 315 + t * (109598 / 31185)), e = e * t, this.cgb[5] = e * (601676 / 22275), this.cbg[5] = e * (444337 / 155925), e = Math.pow(t, 2), this.Qn = this.k0 / (1 + t) * (1 + e * (1 / 4 + e * (1 / 64 + e / 256))), this.utg[0] = t * (-0.5 + t * (2 / 3 + t * (-37 / 96 + t * (1 / 360 + t * (81 / 512 + t * (-96199 / 604800)))))), this.gtu[0] = t * (0.5 + t * (-2 / 3 + t * (5 / 16 + t * (41 / 180 + t * (-127 / 288 + t * (7891 / 37800)))))), this.utg[1] = e * (-1 / 48 + t * (-1 / 15 + t * (437 / 1440 + t * (-46 / 105 + t * (1118711 / 3870720))))), this.gtu[1] = e * (13 / 48 + t * (-3 / 5 + t * (557 / 1440 + t * (281 / 630 + t * (-1983433 / 1935360))))), e = e * t, this.utg[2] = e * (-17 / 480 + t * (37 / 840 + t * (209 / 4480 + t * (-5569 / 90720)))), this.gtu[2] = e * (61 / 240 + t * (-103 / 140 + t * (15061 / 26880 + t * (167603 / 181440)))), e = e * t, this.utg[3] = e * (-4397 / 161280 + t * (11 / 504 + t * (830251 / 7257600))), this.gtu[3] = e * (49561 / 161280 + t * (-179 / 168 + t * (6601661 / 7257600))), e = e * t, this.utg[4] = e * (-4583 / 161280 + t * (108847 / 3991680)), this.gtu[4] = e * (34729 / 80640 + t * (-3418889 / 1995840)), e = e * t, this.utg[5] = e * (-20648693 / 638668800), this.gtu[5] = e * (212378941 / 319334400);
  var i = ph(this.cbg, this.lat0);
  this.Zb = -this.Qn * (i + Z3(this.gtu, 2 * i));
}
function W3(n) {
  var t = A(n.x - this.long0), e = n.y;
  e = ph(this.cbg, e);
  var i = Math.sin(e), s = Math.cos(e), r = Math.sin(t), o = Math.cos(t);
  e = Math.atan2(i, o * s), t = Math.atan2(r * s, Pe(i, s * o)), t = z3(Math.tan(t));
  var a = cg(this.gtu, 2 * e, 2 * t);
  e = e + a[0], t = t + a[1];
  var l, h;
  return Math.abs(t) <= 2.623395162778 ? (l = this.a * (this.Qn * t) + this.x0, h = this.a * (this.Qn * e + this.Zb) + this.y0) : (l = 1 / 0, h = 1 / 0), n.x = l, n.y = h, n;
}
function H3(n) {
  var t = (n.x - this.x0) * (1 / this.a), e = (n.y - this.y0) * (1 / this.a);
  e = (e - this.Zb) / this.Qn, t = t / this.Qn;
  var i, s;
  if (Math.abs(t) <= 2.623395162778) {
    var r = cg(this.utg, 2 * e, 2 * t);
    e = e + r[0], t = t + r[1], t = Math.atan(hg(t));
    var o = Math.sin(e), a = Math.cos(e), l = Math.sin(t), h = Math.cos(t);
    e = Math.atan2(o * h, Pe(l, h * a)), t = Math.atan2(l, h * a), i = A(t + this.long0), s = ph(this.cgb, e);
  } else
    i = 1 / 0, s = 1 / 0;
  return n.x = i, n.y = s, n;
}
var X3 = ["Extended_Transverse_Mercator", "Extended Transverse Mercator", "etmerc", "Transverse_Mercator", "Transverse Mercator", "tmerc"];
const jr = {
  init: U3,
  forward: W3,
  inverse: H3,
  names: X3
};
function Y3(n, t) {
  if (n === void 0) {
    if (n = Math.floor((A(t) + Math.PI) * 30 / Math.PI) + 1, n < 0)
      return 0;
    if (n > 60)
      return 60;
  }
  return n;
}
var j3 = "etmerc";
function q3() {
  var n = Y3(this.zone, this.long0);
  if (n === void 0)
    throw new Error("unknown utm zone");
  this.lat0 = 0, this.long0 = (6 * Math.abs(n) - 183) * zt, this.x0 = 5e5, this.y0 = this.utmSouth ? 1e7 : 0, this.k0 = 0.9996, jr.init.apply(this), this.forward = jr.forward, this.inverse = jr.inverse;
}
var K3 = ["Universal Transverse Mercator System", "utm"];
const J3 = {
  init: q3,
  names: K3,
  dependsOn: j3
};
function yh(n, t) {
  return Math.pow((1 - n) / (1 + n), t);
}
var Q3 = 20;
function tC() {
  var n = Math.sin(this.lat0), t = Math.cos(this.lat0);
  t *= t, this.rc = Math.sqrt(1 - this.es) / (1 - this.es * n * n), this.C = Math.sqrt(1 + this.es * t * t / (1 - this.es)), this.phic0 = Math.asin(n / this.C), this.ratexp = 0.5 * this.C * this.e, this.K = Math.tan(0.5 * this.phic0 + ct) / (Math.pow(Math.tan(0.5 * this.lat0 + ct), this.C) * yh(this.e * n, this.ratexp));
}
function eC(n) {
  var t = n.x, e = n.y;
  return n.y = 2 * Math.atan(this.K * Math.pow(Math.tan(0.5 * e + ct), this.C) * yh(this.e * Math.sin(e), this.ratexp)) - S, n.x = this.C * t, n;
}
function iC(n) {
  for (var t = 1e-14, e = n.x / this.C, i = n.y, s = Math.pow(Math.tan(0.5 * i + ct) / this.K, 1 / this.C), r = Q3; r > 0 && (i = 2 * Math.atan(s * yh(this.e * Math.sin(n.y), -0.5 * this.e)) - S, !(Math.abs(i - n.y) < t)); --r)
    n.y = i;
  return r ? (n.x = e, n.y = i, n) : null;
}
var nC = ["gauss"];
const vh = {
  init: tC,
  forward: eC,
  inverse: iC,
  names: nC
};
function sC() {
  vh.init.apply(this), this.rc && (this.sinc0 = Math.sin(this.phic0), this.cosc0 = Math.cos(this.phic0), this.R2 = 2 * this.rc, this.title || (this.title = "Oblique Stereographic Alternative"));
}
function rC(n) {
  var t, e, i, s;
  return n.x = A(n.x - this.long0), vh.forward.apply(this, [n]), t = Math.sin(n.y), e = Math.cos(n.y), i = Math.cos(n.x), s = this.k0 * this.R2 / (1 + this.sinc0 * t + this.cosc0 * e * i), n.x = s * e * Math.sin(n.x), n.y = s * (this.cosc0 * t - this.sinc0 * e * i), n.x = this.a * n.x + this.x0, n.y = this.a * n.y + this.y0, n;
}
function oC(n) {
  var t, e, i, s, r;
  if (n.x = (n.x - this.x0) / this.a, n.y = (n.y - this.y0) / this.a, n.x /= this.k0, n.y /= this.k0, r = Math.sqrt(n.x * n.x + n.y * n.y)) {
    var o = 2 * Math.atan2(r, this.R2);
    t = Math.sin(o), e = Math.cos(o), s = Math.asin(e * this.sinc0 + n.y * t * this.cosc0 / r), i = Math.atan2(n.x * t, r * this.cosc0 * e - n.y * this.sinc0 * t);
  } else
    s = this.phic0, i = 0;
  return n.x = i, n.y = s, vh.inverse.apply(this, [n]), n.x = A(n.x + this.long0), n;
}
var aC = ["Stereographic_North_Pole", "Oblique_Stereographic", "Polar_Stereographic", "sterea", "Oblique Stereographic Alternative", "Double_Stereographic"];
const lC = {
  init: sC,
  forward: rC,
  inverse: oC,
  names: aC
};
function hC(n, t, e) {
  return t *= e, Math.tan(0.5 * (S + n)) * Math.pow((1 - t) / (1 + t), 0.5 * e);
}
function cC() {
  this.coslat0 = Math.cos(this.lat0), this.sinlat0 = Math.sin(this.lat0), this.sphere ? this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= I && (this.k0 = 0.5 * (1 + cr(this.lat0) * Math.sin(this.lat_ts))) : (Math.abs(this.coslat0) <= I && (this.lat0 > 0 ? this.con = 1 : this.con = -1), this.cons = Math.sqrt(Math.pow(1 + this.e, 1 + this.e) * Math.pow(1 - this.e, 1 - this.e)), this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= I && (this.k0 = 0.5 * this.cons * We(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) / Ae(this.e, this.con * this.lat_ts, this.con * Math.sin(this.lat_ts))), this.ms1 = We(this.e, this.sinlat0, this.coslat0), this.X0 = 2 * Math.atan(this.ssfn_(this.lat0, this.sinlat0, this.e)) - S, this.cosX0 = Math.cos(this.X0), this.sinX0 = Math.sin(this.X0));
}
function uC(n) {
  var t = n.x, e = n.y, i = Math.sin(e), s = Math.cos(e), r, o, a, l, h, c, u = A(t - this.long0);
  return Math.abs(Math.abs(t - this.long0) - Math.PI) <= I && Math.abs(e + this.lat0) <= I ? (n.x = NaN, n.y = NaN, n) : this.sphere ? (r = 2 * this.k0 / (1 + this.sinlat0 * i + this.coslat0 * s * Math.cos(u)), n.x = this.a * r * s * Math.sin(u) + this.x0, n.y = this.a * r * (this.coslat0 * i - this.sinlat0 * s * Math.cos(u)) + this.y0, n) : (o = 2 * Math.atan(this.ssfn_(e, i, this.e)) - S, l = Math.cos(o), a = Math.sin(o), Math.abs(this.coslat0) <= I ? (h = Ae(this.e, e * this.con, this.con * i), c = 2 * this.a * this.k0 * h / this.cons, n.x = this.x0 + c * Math.sin(t - this.long0), n.y = this.y0 - this.con * c * Math.cos(t - this.long0), n) : (Math.abs(this.sinlat0) < I ? (r = 2 * this.a * this.k0 / (1 + l * Math.cos(u)), n.y = r * a) : (r = 2 * this.a * this.k0 * this.ms1 / (this.cosX0 * (1 + this.sinX0 * a + this.cosX0 * l * Math.cos(u))), n.y = r * (this.cosX0 * a - this.sinX0 * l * Math.cos(u)) + this.y0), n.x = r * l * Math.sin(u) + this.x0, n));
}
function dC(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t, e, i, s, r, o = Math.sqrt(n.x * n.x + n.y * n.y);
  if (this.sphere) {
    var a = 2 * Math.atan(o / (2 * this.a * this.k0));
    return t = this.long0, e = this.lat0, o <= I ? (n.x = t, n.y = e, n) : (e = Math.asin(Math.cos(a) * this.sinlat0 + n.y * Math.sin(a) * this.coslat0 / o), Math.abs(this.coslat0) < I ? this.lat0 > 0 ? t = A(this.long0 + Math.atan2(n.x, -1 * n.y)) : t = A(this.long0 + Math.atan2(n.x, n.y)) : t = A(this.long0 + Math.atan2(n.x * Math.sin(a), o * this.coslat0 * Math.cos(a) - n.y * this.sinlat0 * Math.sin(a))), n.x = t, n.y = e, n);
  } else if (Math.abs(this.coslat0) <= I) {
    if (o <= I)
      return e = this.lat0, t = this.long0, n.x = t, n.y = e, n;
    n.x *= this.con, n.y *= this.con, i = o * this.cons / (2 * this.a * this.k0), e = this.con * Ys(this.e, i), t = this.con * A(this.con * this.long0 + Math.atan2(n.x, -1 * n.y));
  } else
    s = 2 * Math.atan(o * this.cosX0 / (2 * this.a * this.k0 * this.ms1)), t = this.long0, o <= I ? r = this.X0 : (r = Math.asin(Math.cos(s) * this.sinX0 + n.y * Math.sin(s) * this.cosX0 / o), t = A(this.long0 + Math.atan2(n.x * Math.sin(s), o * this.cosX0 * Math.cos(s) - n.y * this.sinX0 * Math.sin(s)))), e = -1 * Ys(this.e, Math.tan(0.5 * (S + r)));
  return n.x = t, n.y = e, n;
}
var fC = ["stere", "Stereographic_South_Pole", "Polar Stereographic (variant B)"];
const gC = {
  init: cC,
  forward: uC,
  inverse: dC,
  names: fC,
  ssfn_: hC
};
function mC() {
  var n = this.lat0;
  this.lambda0 = this.long0;
  var t = Math.sin(n), e = this.a, i = this.rf, s = 1 / i, r = 2 * s - Math.pow(s, 2), o = this.e = Math.sqrt(r);
  this.R = this.k0 * e * Math.sqrt(1 - r) / (1 - r * Math.pow(t, 2)), this.alpha = Math.sqrt(1 + r / (1 - r) * Math.pow(Math.cos(n), 4)), this.b0 = Math.asin(t / this.alpha);
  var a = Math.log(Math.tan(Math.PI / 4 + this.b0 / 2)), l = Math.log(Math.tan(Math.PI / 4 + n / 2)), h = Math.log((1 + o * t) / (1 - o * t));
  this.K = a - this.alpha * l + this.alpha * o / 2 * h;
}
function _C(n) {
  var t = Math.log(Math.tan(Math.PI / 4 - n.y / 2)), e = this.e / 2 * Math.log((1 + this.e * Math.sin(n.y)) / (1 - this.e * Math.sin(n.y))), i = -this.alpha * (t + e) + this.K, s = 2 * (Math.atan(Math.exp(i)) - Math.PI / 4), r = this.alpha * (n.x - this.lambda0), o = Math.atan(Math.sin(r) / (Math.sin(this.b0) * Math.tan(s) + Math.cos(this.b0) * Math.cos(r))), a = Math.asin(Math.cos(this.b0) * Math.sin(s) - Math.sin(this.b0) * Math.cos(s) * Math.cos(r));
  return n.y = this.R / 2 * Math.log((1 + Math.sin(a)) / (1 - Math.sin(a))) + this.y0, n.x = this.R * o + this.x0, n;
}
function pC(n) {
  for (var t = n.x - this.x0, e = n.y - this.y0, i = t / this.R, s = 2 * (Math.atan(Math.exp(e / this.R)) - Math.PI / 4), r = Math.asin(Math.cos(this.b0) * Math.sin(s) + Math.sin(this.b0) * Math.cos(s) * Math.cos(i)), o = Math.atan(Math.sin(i) / (Math.cos(this.b0) * Math.cos(i) - Math.sin(this.b0) * Math.tan(s))), a = this.lambda0 + o / this.alpha, l = 0, h = r, c = -1e3, u = 0; Math.abs(h - c) > 1e-7; ) {
    if (++u > 20)
      return;
    l = 1 / this.alpha * (Math.log(Math.tan(Math.PI / 4 + r / 2)) - this.K) + this.e * Math.log(Math.tan(Math.PI / 4 + Math.asin(this.e * Math.sin(h)) / 2)), c = h, h = 2 * Math.atan(Math.exp(l)) - Math.PI / 2;
  }
  return n.x = a, n.y = h, n;
}
var yC = ["somerc"];
const vC = {
  init: mC,
  forward: _C,
  inverse: pC,
  names: yC
};
var In = 1e-7;
function xC(n) {
  var t = ["Hotine_Oblique_Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin"], e = typeof n.PROJECTION == "object" ? Object.keys(n.PROJECTION)[0] : n.PROJECTION;
  return "no_uoff" in n || "no_off" in n || t.indexOf(e) !== -1;
}
function CC() {
  var n, t, e, i, s, r, o, a, l, h, c = 0, u, d = 0, f = 0, g = 0, m = 0, _ = 0, y = 0;
  this.no_off = xC(this), this.no_rot = "no_rot" in this;
  var p = !1;
  "alpha" in this && (p = !0);
  var v = !1;
  if ("rectified_grid_angle" in this && (v = !0), p && (y = this.alpha), v && (c = this.rectified_grid_angle * zt), p || v)
    d = this.longc;
  else if (f = this.long1, m = this.lat1, g = this.long2, _ = this.lat2, Math.abs(m - _) <= In || (n = Math.abs(m)) <= In || Math.abs(n - S) <= In || Math.abs(Math.abs(this.lat0) - S) <= In || Math.abs(Math.abs(_) - S) <= In)
    throw new Error();
  var x = 1 - this.es;
  t = Math.sqrt(x), Math.abs(this.lat0) > I ? (a = Math.sin(this.lat0), e = Math.cos(this.lat0), n = 1 - this.es * a * a, this.B = e * e, this.B = Math.sqrt(1 + this.es * this.B * this.B / x), this.A = this.B * this.k0 * t / n, i = this.B * t / (e * Math.sqrt(n)), s = i * i - 1, s <= 0 ? s = 0 : (s = Math.sqrt(s), this.lat0 < 0 && (s = -s)), this.E = s += i, this.E *= Math.pow(Ae(this.e, this.lat0, a), this.B)) : (this.B = 1 / t, this.A = this.k0, this.E = i = s = 1), p || v ? (p ? (u = Math.asin(Math.sin(y) / i), v || (c = y)) : (u = c, y = Math.asin(i * Math.sin(u))), this.lam0 = d - Math.asin(0.5 * (s - 1 / s) * Math.tan(u)) / this.B) : (r = Math.pow(Ae(this.e, m, Math.sin(m)), this.B), o = Math.pow(Ae(this.e, _, Math.sin(_)), this.B), s = this.E / r, l = (o - r) / (o + r), h = this.E * this.E, h = (h - o * r) / (h + o * r), n = f - g, n < -Math.pi ? g -= Hs : n > Math.pi && (g += Hs), this.lam0 = A(0.5 * (f + g) - Math.atan(h * Math.tan(0.5 * this.B * (f - g)) / l) / this.B), u = Math.atan(2 * Math.sin(this.B * A(f - this.lam0)) / (s - 1 / s)), c = y = Math.asin(i * Math.sin(u))), this.singam = Math.sin(u), this.cosgam = Math.cos(u), this.sinrot = Math.sin(c), this.cosrot = Math.cos(c), this.rB = 1 / this.B, this.ArB = this.A * this.rB, this.BrA = 1 / this.ArB, this.A * this.B, this.no_off ? this.u_0 = 0 : (this.u_0 = Math.abs(this.ArB * Math.atan(Math.sqrt(i * i - 1) / Math.cos(y))), this.lat0 < 0 && (this.u_0 = -this.u_0)), s = 0.5 * u, this.v_pole_n = this.ArB * Math.log(Math.tan(ct - s)), this.v_pole_s = this.ArB * Math.log(Math.tan(ct + s));
}
function MC(n) {
  var t = {}, e, i, s, r, o, a, l, h;
  if (n.x = n.x - this.lam0, Math.abs(Math.abs(n.y) - S) > I) {
    if (o = this.E / Math.pow(Ae(this.e, n.y, Math.sin(n.y)), this.B), a = 1 / o, e = 0.5 * (o - a), i = 0.5 * (o + a), r = Math.sin(this.B * n.x), s = (e * this.singam - r * this.cosgam) / i, Math.abs(Math.abs(s) - 1) < I)
      throw new Error();
    h = 0.5 * this.ArB * Math.log((1 - s) / (1 + s)), a = Math.cos(this.B * n.x), Math.abs(a) < In ? l = this.A * n.x : l = this.ArB * Math.atan2(e * this.cosgam + r * this.singam, a);
  } else
    h = n.y > 0 ? this.v_pole_n : this.v_pole_s, l = this.ArB * n.y;
  return this.no_rot ? (t.x = l, t.y = h) : (l -= this.u_0, t.x = h * this.cosrot + l * this.sinrot, t.y = l * this.cosrot - h * this.sinrot), t.x = this.a * t.x + this.x0, t.y = this.a * t.y + this.y0, t;
}
function EC(n) {
  var t, e, i, s, r, o, a, l = {};
  if (n.x = (n.x - this.x0) * (1 / this.a), n.y = (n.y - this.y0) * (1 / this.a), this.no_rot ? (e = n.y, t = n.x) : (e = n.x * this.cosrot - n.y * this.sinrot, t = n.y * this.cosrot + n.x * this.sinrot + this.u_0), i = Math.exp(-this.BrA * e), s = 0.5 * (i - 1 / i), r = 0.5 * (i + 1 / i), o = Math.sin(this.BrA * t), a = (o * this.cosgam + s * this.singam) / r, Math.abs(Math.abs(a) - 1) < I)
    l.x = 0, l.y = a < 0 ? -S : S;
  else {
    if (l.y = this.E / Math.sqrt((1 + a) / (1 - a)), l.y = Ys(this.e, Math.pow(l.y, 1 / this.B)), l.y === 1 / 0)
      throw new Error();
    l.x = -this.rB * Math.atan2(s * this.cosgam - o * this.singam, Math.cos(this.BrA * t));
  }
  return l.x += this.lam0, l;
}
var wC = ["Hotine_Oblique_Mercator", "Hotine Oblique Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin", "Hotine_Oblique_Mercator_Two_Point_Natural_Origin", "Hotine_Oblique_Mercator_Azimuth_Center", "Oblique_Mercator", "omerc"];
const SC = {
  init: CC,
  forward: MC,
  inverse: EC,
  names: wC
};
function RC() {
  if (this.lat2 || (this.lat2 = this.lat1), this.k0 || (this.k0 = 1), this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, !(Math.abs(this.lat1 + this.lat2) < I)) {
    var n = this.b / this.a;
    this.e = Math.sqrt(1 - n * n);
    var t = Math.sin(this.lat1), e = Math.cos(this.lat1), i = We(this.e, t, e), s = Ae(this.e, this.lat1, t), r = Math.sin(this.lat2), o = Math.cos(this.lat2), a = We(this.e, r, o), l = Ae(this.e, this.lat2, r), h = Ae(this.e, this.lat0, Math.sin(this.lat0));
    Math.abs(this.lat1 - this.lat2) > I ? this.ns = Math.log(i / a) / Math.log(s / l) : this.ns = t, isNaN(this.ns) && (this.ns = t), this.f0 = i / (this.ns * Math.pow(s, this.ns)), this.rh = this.a * this.f0 * Math.pow(h, this.ns), this.title || (this.title = "Lambert Conformal Conic");
  }
}
function TC(n) {
  var t = n.x, e = n.y;
  Math.abs(2 * Math.abs(e) - Math.PI) <= I && (e = cr(e) * (S - 2 * I));
  var i = Math.abs(Math.abs(e) - S), s, r;
  if (i > I)
    s = Ae(this.e, e, Math.sin(e)), r = this.a * this.f0 * Math.pow(s, this.ns);
  else {
    if (i = e * this.ns, i <= 0)
      return null;
    r = 0;
  }
  var o = this.ns * A(t - this.long0);
  return n.x = this.k0 * (r * Math.sin(o)) + this.x0, n.y = this.k0 * (this.rh - r * Math.cos(o)) + this.y0, n;
}
function bC(n) {
  var t, e, i, s, r, o = (n.x - this.x0) / this.k0, a = this.rh - (n.y - this.y0) / this.k0;
  this.ns > 0 ? (t = Math.sqrt(o * o + a * a), e = 1) : (t = -Math.sqrt(o * o + a * a), e = -1);
  var l = 0;
  if (t !== 0 && (l = Math.atan2(e * o, e * a)), t !== 0 || this.ns > 0) {
    if (e = 1 / this.ns, i = Math.pow(t / (this.a * this.f0), e), s = Ys(this.e, i), s === -9999)
      return null;
  } else
    s = -S;
  return r = A(l / this.ns + this.long0), n.x = r, n.y = s, n;
}
var LC = [
  "Lambert Tangential Conformal Conic Projection",
  "Lambert_Conformal_Conic",
  "Lambert_Conformal_Conic_1SP",
  "Lambert_Conformal_Conic_2SP",
  "lcc",
  "Lambert Conic Conformal (1SP)",
  "Lambert Conic Conformal (2SP)"
];
const IC = {
  init: RC,
  forward: TC,
  inverse: bC,
  names: LC
};
function PC() {
  this.a = 6377397155e-3, this.es = 0.006674372230614, this.e = Math.sqrt(this.es), this.lat0 || (this.lat0 = 0.863937979737193), this.long0 || (this.long0 = 0.7417649320975901 - 0.308341501185665), this.k0 || (this.k0 = 0.9999), this.s45 = 0.785398163397448, this.s90 = 2 * this.s45, this.fi0 = this.lat0, this.e2 = this.es, this.e = Math.sqrt(this.e2), this.alfa = Math.sqrt(1 + this.e2 * Math.pow(Math.cos(this.fi0), 4) / (1 - this.e2)), this.uq = 1.04216856380474, this.u0 = Math.asin(Math.sin(this.fi0) / this.alfa), this.g = Math.pow((1 + this.e * Math.sin(this.fi0)) / (1 - this.e * Math.sin(this.fi0)), this.alfa * this.e / 2), this.k = Math.tan(this.u0 / 2 + this.s45) / Math.pow(Math.tan(this.fi0 / 2 + this.s45), this.alfa) * this.g, this.k1 = this.k0, this.n0 = this.a * Math.sqrt(1 - this.e2) / (1 - this.e2 * Math.pow(Math.sin(this.fi0), 2)), this.s0 = 1.37008346281555, this.n = Math.sin(this.s0), this.ro0 = this.k1 * this.n0 / Math.tan(this.s0), this.ad = this.s90 - this.uq;
}
function AC(n) {
  var t, e, i, s, r, o, a, l = n.x, h = n.y, c = A(l - this.long0);
  return t = Math.pow((1 + this.e * Math.sin(h)) / (1 - this.e * Math.sin(h)), this.alfa * this.e / 2), e = 2 * (Math.atan(this.k * Math.pow(Math.tan(h / 2 + this.s45), this.alfa) / t) - this.s45), i = -c * this.alfa, s = Math.asin(Math.cos(this.ad) * Math.sin(e) + Math.sin(this.ad) * Math.cos(e) * Math.cos(i)), r = Math.asin(Math.cos(e) * Math.sin(i) / Math.cos(s)), o = this.n * r, a = this.ro0 * Math.pow(Math.tan(this.s0 / 2 + this.s45), this.n) / Math.pow(Math.tan(s / 2 + this.s45), this.n), n.y = a * Math.cos(o) / 1, n.x = a * Math.sin(o) / 1, this.czech || (n.y *= -1, n.x *= -1), n;
}
function OC(n) {
  var t, e, i, s, r, o, a, l, h = n.x;
  n.x = n.y, n.y = h, this.czech || (n.y *= -1, n.x *= -1), o = Math.sqrt(n.x * n.x + n.y * n.y), r = Math.atan2(n.y, n.x), s = r / Math.sin(this.s0), i = 2 * (Math.atan(Math.pow(this.ro0 / o, 1 / this.n) * Math.tan(this.s0 / 2 + this.s45)) - this.s45), t = Math.asin(Math.cos(this.ad) * Math.sin(i) - Math.sin(this.ad) * Math.cos(i) * Math.cos(s)), e = Math.asin(Math.cos(i) * Math.sin(s) / Math.cos(t)), n.x = this.long0 - e / this.alfa, a = t, l = 0;
  var c = 0;
  do
    n.y = 2 * (Math.atan(Math.pow(this.k, -1 / this.alfa) * Math.pow(Math.tan(t / 2 + this.s45), 1 / this.alfa) * Math.pow((1 + this.e * Math.sin(a)) / (1 - this.e * Math.sin(a)), this.e / 2)) - this.s45), Math.abs(a - n.y) < 1e-10 && (l = 1), a = n.y, c += 1;
  while (l === 0 && c < 15);
  return c >= 15 ? null : n;
}
var FC = ["Krovak", "krovak"];
const NC = {
  init: PC,
  forward: AC,
  inverse: OC,
  names: FC
};
function Jt(n, t, e, i, s) {
  return n * s - t * Math.sin(2 * s) + e * Math.sin(4 * s) - i * Math.sin(6 * s);
}
function ur(n) {
  return 1 - 0.25 * n * (1 + n / 16 * (3 + 1.25 * n));
}
function dr(n) {
  return 0.375 * n * (1 + 0.25 * n * (1 + 0.46875 * n));
}
function fr(n) {
  return 0.05859375 * n * n * (1 + 0.75 * n);
}
function gr(n) {
  return n * n * n * (35 / 3072);
}
function ts(n, t, e) {
  var i = t * e;
  return n / Math.sqrt(1 - i * i);
}
function ls(n) {
  return Math.abs(n) < S ? n : n - cr(n) * Math.PI;
}
function Eo(n, t, e, i, s) {
  var r, o;
  r = n / t;
  for (var a = 0; a < 15; a++)
    if (o = (n - (t * r - e * Math.sin(2 * r) + i * Math.sin(4 * r) - s * Math.sin(6 * r))) / (t - 2 * e * Math.cos(2 * r) + 4 * i * Math.cos(4 * r) - 6 * s * Math.cos(6 * r)), r += o, Math.abs(o) <= 1e-10)
      return r;
  return NaN;
}
function DC() {
  this.sphere || (this.e0 = ur(this.es), this.e1 = dr(this.es), this.e2 = fr(this.es), this.e3 = gr(this.es), this.ml0 = this.a * Jt(this.e0, this.e1, this.e2, this.e3, this.lat0));
}
function kC(n) {
  var t, e, i = n.x, s = n.y;
  if (i = A(i - this.long0), this.sphere)
    t = this.a * Math.asin(Math.cos(s) * Math.sin(i)), e = this.a * (Math.atan2(Math.tan(s), Math.cos(i)) - this.lat0);
  else {
    var r = Math.sin(s), o = Math.cos(s), a = ts(this.a, this.e, r), l = Math.tan(s) * Math.tan(s), h = i * Math.cos(s), c = h * h, u = this.es * o * o / (1 - this.es), d = this.a * Jt(this.e0, this.e1, this.e2, this.e3, s);
    t = a * h * (1 - c * l * (1 / 6 - (8 - l + 8 * u) * c / 120)), e = d - this.ml0 + a * r / o * c * (0.5 + (5 - l + 6 * u) * c / 24);
  }
  return n.x = t + this.x0, n.y = e + this.y0, n;
}
function GC(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t = n.x / this.a, e = n.y / this.a, i, s;
  if (this.sphere) {
    var r = e + this.lat0;
    i = Math.asin(Math.sin(r) * Math.cos(t)), s = Math.atan2(Math.tan(t), Math.cos(r));
  } else {
    var o = this.ml0 / this.a + e, a = Eo(o, this.e0, this.e1, this.e2, this.e3);
    if (Math.abs(Math.abs(a) - S) <= I)
      return n.x = this.long0, n.y = S, e < 0 && (n.y *= -1), n;
    var l = ts(this.a, this.e, Math.sin(a)), h = l * l * l / this.a / this.a * (1 - this.es), c = Math.pow(Math.tan(a), 2), u = t * this.a / l, d = u * u;
    i = a - l * Math.tan(a) / h * u * u * (0.5 - (1 + 3 * c) * u * u / 24), s = u * (1 - d * (c / 3 + (1 + 3 * c) * c * d / 15)) / Math.cos(a);
  }
  return n.x = A(s + this.long0), n.y = ls(i), n;
}
var $C = ["Cassini", "Cassini_Soldner", "cass"];
const BC = {
  init: DC,
  forward: kC,
  inverse: GC,
  names: $C
};
function Ti(n, t) {
  var e;
  return n > 1e-7 ? (e = n * t, (1 - n * n) * (t / (1 - e * e) - 0.5 / n * Math.log((1 - e) / (1 + e)))) : 2 * t;
}
var zC = 1, ZC = 2, VC = 3, UC = 4;
function WC() {
  var n = Math.abs(this.lat0);
  if (Math.abs(n - S) < I ? this.mode = this.lat0 < 0 ? this.S_POLE : this.N_POLE : Math.abs(n) < I ? this.mode = this.EQUIT : this.mode = this.OBLIQ, this.es > 0) {
    var t;
    switch (this.qp = Ti(this.e, 1), this.mmf = 0.5 / (1 - this.es), this.apa = tM(this.es), this.mode) {
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
        this.rq = Math.sqrt(0.5 * this.qp), t = Math.sin(this.lat0), this.sinb1 = Ti(this.e, t) / this.qp, this.cosb1 = Math.sqrt(1 - this.sinb1 * this.sinb1), this.dd = Math.cos(this.lat0) / (Math.sqrt(1 - this.es * t * t) * this.rq * this.cosb1), this.ymf = (this.xmf = this.rq) / this.dd, this.xmf *= this.dd;
        break;
    }
  } else
    this.mode === this.OBLIQ && (this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0));
}
function HC(n) {
  var t, e, i, s, r, o, a, l, h, c, u = n.x, d = n.y;
  if (u = A(u - this.long0), this.sphere) {
    if (r = Math.sin(d), c = Math.cos(d), i = Math.cos(u), this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (e = this.mode === this.EQUIT ? 1 + c * i : 1 + this.sinph0 * r + this.cosph0 * c * i, e <= I)
        return null;
      e = Math.sqrt(2 / e), t = e * c * Math.sin(u), e *= this.mode === this.EQUIT ? r : this.cosph0 * r - this.sinph0 * c * i;
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (i = -i), Math.abs(d + this.lat0) < I)
        return null;
      e = ct - d * 0.5, e = 2 * (this.mode === this.S_POLE ? Math.cos(e) : Math.sin(e)), t = e * Math.sin(u), e *= i;
    }
  } else {
    switch (a = 0, l = 0, h = 0, i = Math.cos(u), s = Math.sin(u), r = Math.sin(d), o = Ti(this.e, r), (this.mode === this.OBLIQ || this.mode === this.EQUIT) && (a = o / this.qp, l = Math.sqrt(1 - a * a)), this.mode) {
      case this.OBLIQ:
        h = 1 + this.sinb1 * a + this.cosb1 * l * i;
        break;
      case this.EQUIT:
        h = 1 + l * i;
        break;
      case this.N_POLE:
        h = S + d, o = this.qp - o;
        break;
      case this.S_POLE:
        h = d - S, o = this.qp + o;
        break;
    }
    if (Math.abs(h) < I)
      return null;
    switch (this.mode) {
      case this.OBLIQ:
      case this.EQUIT:
        h = Math.sqrt(2 / h), this.mode === this.OBLIQ ? e = this.ymf * h * (this.cosb1 * a - this.sinb1 * l * i) : e = (h = Math.sqrt(2 / (1 + l * i))) * a * this.ymf, t = this.xmf * h * l * s;
        break;
      case this.N_POLE:
      case this.S_POLE:
        o >= 0 ? (t = (h = Math.sqrt(o)) * s, e = i * (this.mode === this.S_POLE ? h : -h)) : t = e = 0;
        break;
    }
  }
  return n.x = this.a * t + this.x0, n.y = this.a * e + this.y0, n;
}
function XC(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t = n.x / this.a, e = n.y / this.a, i, s, r, o, a, l, h;
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
        e = -e, s = S - s;
        break;
      case this.S_POLE:
        s -= S;
        break;
    }
    i = e === 0 && (this.mode === this.EQUIT || this.mode === this.OBLIQ) ? 0 : Math.atan2(t, e);
  } else {
    if (h = 0, this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (t /= this.dd, e *= this.dd, l = Math.sqrt(t * t + e * e), l < I)
        return n.x = this.long0, n.y = this.lat0, n;
      o = 2 * Math.asin(0.5 * l / this.rq), r = Math.cos(o), t *= o = Math.sin(o), this.mode === this.OBLIQ ? (h = r * this.sinb1 + e * o * this.cosb1 / l, a = this.qp * h, e = l * this.cosb1 * r - e * this.sinb1 * o) : (h = e * o / l, a = this.qp * h, e = l * r);
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (e = -e), a = t * t + e * e, !a)
        return n.x = this.long0, n.y = this.lat0, n;
      h = 1 - a / this.qp, this.mode === this.S_POLE && (h = -h);
    }
    i = Math.atan2(t, e), s = eM(Math.asin(h), this.apa);
  }
  return n.x = A(this.long0 + i), n.y = s, n;
}
var YC = 0.3333333333333333, jC = 0.17222222222222222, qC = 0.10257936507936508, KC = 0.06388888888888888, JC = 0.0664021164021164, QC = 0.016415012942191543;
function tM(n) {
  var t, e = [];
  return e[0] = n * YC, t = n * n, e[0] += t * jC, e[1] = t * KC, t *= n, e[0] += t * qC, e[1] += t * JC, e[2] = t * QC, e;
}
function eM(n, t) {
  var e = n + n;
  return n + t[0] * Math.sin(e) + t[1] * Math.sin(e + e) + t[2] * Math.sin(e + e + e);
}
var iM = ["Lambert Azimuthal Equal Area", "Lambert_Azimuthal_Equal_Area", "laea"];
const nM = {
  init: WC,
  forward: HC,
  inverse: XC,
  names: iM,
  S_POLE: zC,
  N_POLE: ZC,
  EQUIT: VC,
  OBLIQ: UC
};
function Fi(n) {
  return Math.abs(n) > 1 && (n = n > 1 ? 1 : -1), Math.asin(n);
}
function sM() {
  Math.abs(this.lat1 + this.lat2) < I || (this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e3 = Math.sqrt(this.es), this.sin_po = Math.sin(this.lat1), this.cos_po = Math.cos(this.lat1), this.t1 = this.sin_po, this.con = this.sin_po, this.ms1 = We(this.e3, this.sin_po, this.cos_po), this.qs1 = Ti(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat2), this.cos_po = Math.cos(this.lat2), this.t2 = this.sin_po, this.ms2 = We(this.e3, this.sin_po, this.cos_po), this.qs2 = Ti(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat0), this.cos_po = Math.cos(this.lat0), this.t3 = this.sin_po, this.qs0 = Ti(this.e3, this.sin_po, this.cos_po), Math.abs(this.lat1 - this.lat2) > I ? this.ns0 = (this.ms1 * this.ms1 - this.ms2 * this.ms2) / (this.qs2 - this.qs1) : this.ns0 = this.con, this.c = this.ms1 * this.ms1 + this.ns0 * this.qs1, this.rh = this.a * Math.sqrt(this.c - this.ns0 * this.qs0) / this.ns0);
}
function rM(n) {
  var t = n.x, e = n.y;
  this.sin_phi = Math.sin(e), this.cos_phi = Math.cos(e);
  var i = Ti(this.e3, this.sin_phi, this.cos_phi), s = this.a * Math.sqrt(this.c - this.ns0 * i) / this.ns0, r = this.ns0 * A(t - this.long0), o = s * Math.sin(r) + this.x0, a = this.rh - s * Math.cos(r) + this.y0;
  return n.x = o, n.y = a, n;
}
function oM(n) {
  var t, e, i, s, r, o;
  return n.x -= this.x0, n.y = this.rh - n.y + this.y0, this.ns0 >= 0 ? (t = Math.sqrt(n.x * n.x + n.y * n.y), i = 1) : (t = -Math.sqrt(n.x * n.x + n.y * n.y), i = -1), s = 0, t !== 0 && (s = Math.atan2(i * n.x, i * n.y)), i = t * this.ns0 / this.a, this.sphere ? o = Math.asin((this.c - i * i) / (2 * this.ns0)) : (e = (this.c - i * i) / this.ns0, o = this.phi1z(this.e3, e)), r = A(s / this.ns0 + this.long0), n.x = r, n.y = o, n;
}
function aM(n, t) {
  var e, i, s, r, o, a = Fi(0.5 * t);
  if (n < I)
    return a;
  for (var l = n * n, h = 1; h <= 25; h++)
    if (e = Math.sin(a), i = Math.cos(a), s = n * e, r = 1 - s * s, o = 0.5 * r * r / i * (t / (1 - l) - e / r + 0.5 / n * Math.log((1 - s) / (1 + s))), a = a + o, Math.abs(o) <= 1e-7)
      return a;
  return null;
}
var lM = ["Albers_Conic_Equal_Area", "Albers", "aea"];
const hM = {
  init: sM,
  forward: rM,
  inverse: oM,
  names: lM,
  phi1z: aM
};
function cM() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0), this.infinity_dist = 1e3 * this.a, this.rc = 1;
}
function uM(n) {
  var t, e, i, s, r, o, a, l, h = n.x, c = n.y;
  return i = A(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(i), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, o > 0 || Math.abs(o) <= I ? (a = this.x0 + this.a * r * e * Math.sin(i) / o, l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s) / o) : (a = this.x0 + this.infinity_dist * e * Math.sin(i), l = this.y0 + this.infinity_dist * (this.cos_p14 * t - this.sin_p14 * e * s)), n.x = a, n.y = l, n;
}
function dM(n) {
  var t, e, i, s, r, o;
  return n.x = (n.x - this.x0) / this.a, n.y = (n.y - this.y0) / this.a, n.x /= this.k0, n.y /= this.k0, (t = Math.sqrt(n.x * n.x + n.y * n.y)) ? (s = Math.atan2(t, this.rc), e = Math.sin(s), i = Math.cos(s), o = Fi(i * this.sin_p14 + n.y * e * this.cos_p14 / t), r = Math.atan2(n.x * e, t * this.cos_p14 * i - n.y * this.sin_p14 * e), r = A(this.long0 + r)) : (o = this.phic0, r = 0), n.x = r, n.y = o, n;
}
var fM = ["gnom"];
const gM = {
  init: cM,
  forward: uM,
  inverse: dM,
  names: fM
};
function mM(n, t) {
  var e = 1 - (1 - n * n) / (2 * n) * Math.log((1 - n) / (1 + n));
  if (Math.abs(Math.abs(t) - e) < 1e-6)
    return t < 0 ? -1 * S : S;
  for (var i = Math.asin(0.5 * t), s, r, o, a, l = 0; l < 30; l++)
    if (r = Math.sin(i), o = Math.cos(i), a = n * r, s = Math.pow(1 - a * a, 2) / (2 * o) * (t / (1 - n * n) - r / (1 - a * a) + 0.5 / n * Math.log((1 - a) / (1 + a))), i += s, Math.abs(s) <= 1e-10)
      return i;
  return NaN;
}
function _M() {
  this.sphere || (this.k0 = We(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)));
}
function pM(n) {
  var t = n.x, e = n.y, i, s, r = A(t - this.long0);
  if (this.sphere)
    i = this.x0 + this.a * r * Math.cos(this.lat_ts), s = this.y0 + this.a * Math.sin(e) / Math.cos(this.lat_ts);
  else {
    var o = Ti(this.e, Math.sin(e));
    i = this.x0 + this.a * this.k0 * r, s = this.y0 + this.a * o * 0.5 / this.k0;
  }
  return n.x = i, n.y = s, n;
}
function yM(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t, e;
  return this.sphere ? (t = A(this.long0 + n.x / this.a / Math.cos(this.lat_ts)), e = Math.asin(n.y / this.a * Math.cos(this.lat_ts))) : (e = mM(this.e, 2 * n.y * this.k0 / this.a), t = A(this.long0 + n.x / (this.a * this.k0))), n.x = t, n.y = e, n;
}
var vM = ["cea"];
const xM = {
  init: _M,
  forward: pM,
  inverse: yM,
  names: vM
};
function CM() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Equidistant Cylindrical (Plate Carre)", this.rc = Math.cos(this.lat_ts);
}
function MM(n) {
  var t = n.x, e = n.y, i = A(t - this.long0), s = ls(e - this.lat0);
  return n.x = this.x0 + this.a * i * this.rc, n.y = this.y0 + this.a * s, n;
}
function EM(n) {
  var t = n.x, e = n.y;
  return n.x = A(this.long0 + (t - this.x0) / (this.a * this.rc)), n.y = ls(this.lat0 + (e - this.y0) / this.a), n;
}
var wM = ["Equirectangular", "Equidistant_Cylindrical", "eqc"];
const SM = {
  init: CM,
  forward: MM,
  inverse: EM,
  names: wM
};
var Lu = 20;
function RM() {
  this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = ur(this.es), this.e1 = dr(this.es), this.e2 = fr(this.es), this.e3 = gr(this.es), this.ml0 = this.a * Jt(this.e0, this.e1, this.e2, this.e3, this.lat0);
}
function TM(n) {
  var t = n.x, e = n.y, i, s, r, o = A(t - this.long0);
  if (r = o * Math.sin(e), this.sphere)
    Math.abs(e) <= I ? (i = this.a * o, s = -1 * this.a * this.lat0) : (i = this.a * Math.sin(r) / Math.tan(e), s = this.a * (ls(e - this.lat0) + (1 - Math.cos(r)) / Math.tan(e)));
  else if (Math.abs(e) <= I)
    i = this.a * o, s = -1 * this.ml0;
  else {
    var a = ts(this.a, this.e, Math.sin(e)) / Math.tan(e);
    i = a * Math.sin(r), s = this.a * Jt(this.e0, this.e1, this.e2, this.e3, e) - this.ml0 + a * (1 - Math.cos(r));
  }
  return n.x = i + this.x0, n.y = s + this.y0, n;
}
function bM(n) {
  var t, e, i, s, r, o, a, l, h;
  if (i = n.x - this.x0, s = n.y - this.y0, this.sphere)
    if (Math.abs(s + this.a * this.lat0) <= I)
      t = A(i / this.a + this.long0), e = 0;
    else {
      o = this.lat0 + s / this.a, a = i * i / this.a / this.a + o * o, l = o;
      var c;
      for (r = Lu; r; --r)
        if (c = Math.tan(l), h = -1 * (o * (l * c + 1) - l - 0.5 * (l * l + a) * c) / ((l - o) / c - 1), l += h, Math.abs(h) <= I) {
          e = l;
          break;
        }
      t = A(this.long0 + Math.asin(i * Math.tan(l) / this.a) / Math.sin(e));
    }
  else if (Math.abs(s + this.ml0) <= I)
    e = 0, t = A(this.long0 + i / this.a);
  else {
    o = (this.ml0 + s) / this.a, a = i * i / this.a / this.a + o * o, l = o;
    var u, d, f, g, m;
    for (r = Lu; r; --r)
      if (m = this.e * Math.sin(l), u = Math.sqrt(1 - m * m) * Math.tan(l), d = this.a * Jt(this.e0, this.e1, this.e2, this.e3, l), f = this.e0 - 2 * this.e1 * Math.cos(2 * l) + 4 * this.e2 * Math.cos(4 * l) - 6 * this.e3 * Math.cos(6 * l), g = d / this.a, h = (o * (u * g + 1) - g - 0.5 * u * (g * g + a)) / (this.es * Math.sin(2 * l) * (g * g + a - 2 * o * g) / (4 * u) + (o - g) * (u * f - 2 / Math.sin(2 * l)) - f), l -= h, Math.abs(h) <= I) {
        e = l;
        break;
      }
    u = Math.sqrt(1 - this.es * Math.pow(Math.sin(e), 2)) * Math.tan(e), t = A(this.long0 + Math.asin(i * u / this.a) / Math.sin(e));
  }
  return n.x = t, n.y = e, n;
}
var LM = ["Polyconic", "poly"];
const IM = {
  init: RM,
  forward: TM,
  inverse: bM,
  names: LM
};
function PM() {
  this.A = [], this.A[1] = 0.6399175073, this.A[2] = -0.1358797613, this.A[3] = 0.063294409, this.A[4] = -0.02526853, this.A[5] = 0.0117879, this.A[6] = -55161e-7, this.A[7] = 26906e-7, this.A[8] = -1333e-6, this.A[9] = 67e-5, this.A[10] = -34e-5, this.B_re = [], this.B_im = [], this.B_re[1] = 0.7557853228, this.B_im[1] = 0, this.B_re[2] = 0.249204646, this.B_im[2] = 3371507e-9, this.B_re[3] = -1541739e-9, this.B_im[3] = 0.04105856, this.B_re[4] = -0.10162907, this.B_im[4] = 0.01727609, this.B_re[5] = -0.26623489, this.B_im[5] = -0.36249218, this.B_re[6] = -0.6870983, this.B_im[6] = -1.1651967, this.C_re = [], this.C_im = [], this.C_re[1] = 1.3231270439, this.C_im[1] = 0, this.C_re[2] = -0.577245789, this.C_im[2] = -7809598e-9, this.C_re[3] = 0.508307513, this.C_im[3] = -0.112208952, this.C_re[4] = -0.15094762, this.C_im[4] = 0.18200602, this.C_re[5] = 1.01418179, this.C_im[5] = 1.64497696, this.C_re[6] = 1.9660549, this.C_im[6] = 2.5127645, this.D = [], this.D[1] = 1.5627014243, this.D[2] = 0.5185406398, this.D[3] = -0.03333098, this.D[4] = -0.1052906, this.D[5] = -0.0368594, this.D[6] = 7317e-6, this.D[7] = 0.0122, this.D[8] = 394e-5, this.D[9] = -13e-4;
}
function AM(n) {
  var t, e = n.x, i = n.y, s = i - this.lat0, r = e - this.long0, o = s / Is * 1e-5, a = r, l = 1, h = 0;
  for (t = 1; t <= 10; t++)
    l = l * o, h = h + this.A[t] * l;
  var c = h, u = a, d = 1, f = 0, g, m, _ = 0, y = 0;
  for (t = 1; t <= 6; t++)
    g = d * c - f * u, m = f * c + d * u, d = g, f = m, _ = _ + this.B_re[t] * d - this.B_im[t] * f, y = y + this.B_im[t] * d + this.B_re[t] * f;
  return n.x = y * this.a + this.x0, n.y = _ * this.a + this.y0, n;
}
function OM(n) {
  var t, e = n.x, i = n.y, s = e - this.x0, r = i - this.y0, o = r / this.a, a = s / this.a, l = 1, h = 0, c, u, d = 0, f = 0;
  for (t = 1; t <= 6; t++)
    c = l * o - h * a, u = h * o + l * a, l = c, h = u, d = d + this.C_re[t] * l - this.C_im[t] * h, f = f + this.C_im[t] * l + this.C_re[t] * h;
  for (var g = 0; g < this.iterations; g++) {
    var m = d, _ = f, y, p, v = o, x = a;
    for (t = 2; t <= 6; t++)
      y = m * d - _ * f, p = _ * d + m * f, m = y, _ = p, v = v + (t - 1) * (this.B_re[t] * m - this.B_im[t] * _), x = x + (t - 1) * (this.B_im[t] * m + this.B_re[t] * _);
    m = 1, _ = 0;
    var C = this.B_re[1], E = this.B_im[1];
    for (t = 2; t <= 6; t++)
      y = m * d - _ * f, p = _ * d + m * f, m = y, _ = p, C = C + t * (this.B_re[t] * m - this.B_im[t] * _), E = E + t * (this.B_im[t] * m + this.B_re[t] * _);
    var R = C * C + E * E;
    d = (v * C + x * E) / R, f = (x * C - v * E) / R;
  }
  var b = d, F = f, G = 1, V = 0;
  for (t = 1; t <= 9; t++)
    G = G * b, V = V + this.D[t] * G;
  var L = this.lat0 + V * Is * 1e5, $ = this.long0 + F;
  return n.x = $, n.y = L, n;
}
var FM = ["New_Zealand_Map_Grid", "nzmg"];
const NM = {
  init: PM,
  forward: AM,
  inverse: OM,
  names: FM
};
function DM() {
}
function kM(n) {
  var t = n.x, e = n.y, i = A(t - this.long0), s = this.x0 + this.a * i, r = this.y0 + this.a * Math.log(Math.tan(Math.PI / 4 + e / 2.5)) * 1.25;
  return n.x = s, n.y = r, n;
}
function GM(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t = A(this.long0 + n.x / this.a), e = 2.5 * (Math.atan(Math.exp(0.8 * n.y / this.a)) - Math.PI / 4);
  return n.x = t, n.y = e, n;
}
var $M = ["Miller_Cylindrical", "mill"];
const BM = {
  init: DM,
  forward: kM,
  inverse: GM,
  names: $M
};
var zM = 20;
function ZM() {
  this.sphere ? (this.n = 1, this.m = 0, this.es = 0, this.C_y = Math.sqrt((this.m + 1) / this.n), this.C_x = this.C_y / (this.m + 1)) : this.en = ag(this.es);
}
function VM(n) {
  var t, e, i = n.x, s = n.y;
  if (i = A(i - this.long0), this.sphere) {
    if (!this.m)
      s = this.n !== 1 ? Math.asin(this.n * Math.sin(s)) : s;
    else
      for (var r = this.n * Math.sin(s), o = zM; o; --o) {
        var a = (this.m * s + Math.sin(s) - r) / (this.m + Math.cos(s));
        if (s -= a, Math.abs(a) < I)
          break;
      }
    t = this.a * this.C_x * i * (this.m + Math.cos(s)), e = this.a * this.C_y * s;
  } else {
    var l = Math.sin(s), h = Math.cos(s);
    e = this.a * Ho(s, l, h, this.en), t = this.a * i * h / Math.sqrt(1 - this.es * l * l);
  }
  return n.x = t, n.y = e, n;
}
function UM(n) {
  var t, e, i, s;
  return n.x -= this.x0, i = n.x / this.a, n.y -= this.y0, t = n.y / this.a, this.sphere ? (t /= this.C_y, i = i / (this.C_x * (this.m + Math.cos(t))), this.m ? t = Fi((this.m * t + Math.sin(t)) / this.n) : this.n !== 1 && (t = Fi(Math.sin(t) / this.n)), i = A(i + this.long0), t = ls(t)) : (t = lg(n.y / this.a, this.es, this.en), s = Math.abs(t), s < S ? (s = Math.sin(t), e = this.long0 + n.x * Math.sqrt(1 - this.es * s * s) / (this.a * Math.cos(t)), i = A(e)) : s - I < S && (i = this.long0)), n.x = i, n.y = t, n;
}
var WM = ["Sinusoidal", "sinu"];
const HM = {
  init: ZM,
  forward: VM,
  inverse: UM,
  names: WM
};
function XM() {
}
function YM(n) {
  for (var t = n.x, e = n.y, i = A(t - this.long0), s = e, r = Math.PI * Math.sin(e); ; ) {
    var o = -(s + Math.sin(s) - r) / (1 + Math.cos(s));
    if (s += o, Math.abs(o) < I)
      break;
  }
  s /= 2, Math.PI / 2 - Math.abs(e) < I && (i = 0);
  var a = 0.900316316158 * this.a * i * Math.cos(s) + this.x0, l = 1.4142135623731 * this.a * Math.sin(s) + this.y0;
  return n.x = a, n.y = l, n;
}
function jM(n) {
  var t, e;
  n.x -= this.x0, n.y -= this.y0, e = n.y / (1.4142135623731 * this.a), Math.abs(e) > 0.999999999999 && (e = 0.999999999999), t = Math.asin(e);
  var i = A(this.long0 + n.x / (0.900316316158 * this.a * Math.cos(t)));
  i < -Math.PI && (i = -Math.PI), i > Math.PI && (i = Math.PI), e = (2 * t + Math.sin(2 * t)) / Math.PI, Math.abs(e) > 1 && (e = 1);
  var s = Math.asin(e);
  return n.x = i, n.y = s, n;
}
var qM = ["Mollweide", "moll"];
const KM = {
  init: XM,
  forward: YM,
  inverse: jM,
  names: qM
};
function JM() {
  Math.abs(this.lat1 + this.lat2) < I || (this.lat2 = this.lat2 || this.lat1, this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = ur(this.es), this.e1 = dr(this.es), this.e2 = fr(this.es), this.e3 = gr(this.es), this.sinphi = Math.sin(this.lat1), this.cosphi = Math.cos(this.lat1), this.ms1 = We(this.e, this.sinphi, this.cosphi), this.ml1 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat1), Math.abs(this.lat1 - this.lat2) < I ? this.ns = this.sinphi : (this.sinphi = Math.sin(this.lat2), this.cosphi = Math.cos(this.lat2), this.ms2 = We(this.e, this.sinphi, this.cosphi), this.ml2 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat2), this.ns = (this.ms1 - this.ms2) / (this.ml2 - this.ml1)), this.g = this.ml1 + this.ms1 / this.ns, this.ml0 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat0), this.rh = this.a * (this.g - this.ml0));
}
function QM(n) {
  var t = n.x, e = n.y, i;
  if (this.sphere)
    i = this.a * (this.g - e);
  else {
    var s = Jt(this.e0, this.e1, this.e2, this.e3, e);
    i = this.a * (this.g - s);
  }
  var r = this.ns * A(t - this.long0), o = this.x0 + i * Math.sin(r), a = this.y0 + this.rh - i * Math.cos(r);
  return n.x = o, n.y = a, n;
}
function tE(n) {
  n.x -= this.x0, n.y = this.rh - n.y + this.y0;
  var t, e, i, s;
  this.ns >= 0 ? (e = Math.sqrt(n.x * n.x + n.y * n.y), t = 1) : (e = -Math.sqrt(n.x * n.x + n.y * n.y), t = -1);
  var r = 0;
  if (e !== 0 && (r = Math.atan2(t * n.x, t * n.y)), this.sphere)
    return s = A(this.long0 + r / this.ns), i = ls(this.g - e / this.a), n.x = s, n.y = i, n;
  var o = this.g - e / this.a;
  return i = Eo(o, this.e0, this.e1, this.e2, this.e3), s = A(this.long0 + r / this.ns), n.x = s, n.y = i, n;
}
var eE = ["Equidistant_Conic", "eqdc"];
const iE = {
  init: JM,
  forward: QM,
  inverse: tE,
  names: eE
};
function nE() {
  this.R = this.a;
}
function sE(n) {
  var t = n.x, e = n.y, i = A(t - this.long0), s, r;
  Math.abs(e) <= I && (s = this.x0 + this.R * i, r = this.y0);
  var o = Fi(2 * Math.abs(e / Math.PI));
  (Math.abs(i) <= I || Math.abs(Math.abs(e) - S) <= I) && (s = this.x0, e >= 0 ? r = this.y0 + Math.PI * this.R * Math.tan(0.5 * o) : r = this.y0 + Math.PI * this.R * -Math.tan(0.5 * o));
  var a = 0.5 * Math.abs(Math.PI / i - i / Math.PI), l = a * a, h = Math.sin(o), c = Math.cos(o), u = c / (h + c - 1), d = u * u, f = u * (2 / h - 1), g = f * f, m = Math.PI * this.R * (a * (u - g) + Math.sqrt(l * (u - g) * (u - g) - (g + l) * (d - g))) / (g + l);
  i < 0 && (m = -m), s = this.x0 + m;
  var _ = l + u;
  return m = Math.PI * this.R * (f * _ - a * Math.sqrt((g + l) * (l + 1) - _ * _)) / (g + l), e >= 0 ? r = this.y0 + m : r = this.y0 - m, n.x = s, n.y = r, n;
}
function rE(n) {
  var t, e, i, s, r, o, a, l, h, c, u, d, f;
  return n.x -= this.x0, n.y -= this.y0, u = Math.PI * this.R, i = n.x / u, s = n.y / u, r = i * i + s * s, o = -Math.abs(s) * (1 + r), a = o - 2 * s * s + i * i, l = -2 * o + 1 + 2 * s * s + r * r, f = s * s / l + (2 * a * a * a / l / l / l - 9 * o * a / l / l) / 27, h = (o - a * a / 3 / l) / l, c = 2 * Math.sqrt(-h / 3), u = 3 * f / h / c, Math.abs(u) > 1 && (u >= 0 ? u = 1 : u = -1), d = Math.acos(u) / 3, n.y >= 0 ? e = (-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI : e = -(-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI, Math.abs(i) < I ? t = this.long0 : t = A(this.long0 + Math.PI * (r - 1 + Math.sqrt(1 + 2 * (i * i - s * s) + r * r)) / 2 / i), n.x = t, n.y = e, n;
}
var oE = ["Van_der_Grinten_I", "VanDerGrinten", "vandg"];
const aE = {
  init: nE,
  forward: sE,
  inverse: rE,
  names: oE
};
function lE() {
  this.sin_p12 = Math.sin(this.lat0), this.cos_p12 = Math.cos(this.lat0);
}
function hE(n) {
  var t = n.x, e = n.y, i = Math.sin(n.y), s = Math.cos(n.y), r = A(t - this.long0), o, a, l, h, c, u, d, f, g, m, _, y, p, v, x, C, E, R, b, F, G, V, L;
  return this.sphere ? Math.abs(this.sin_p12 - 1) <= I ? (n.x = this.x0 + this.a * (S - e) * Math.sin(r), n.y = this.y0 - this.a * (S - e) * Math.cos(r), n) : Math.abs(this.sin_p12 + 1) <= I ? (n.x = this.x0 + this.a * (S + e) * Math.sin(r), n.y = this.y0 + this.a * (S + e) * Math.cos(r), n) : (R = this.sin_p12 * i + this.cos_p12 * s * Math.cos(r), C = Math.acos(R), E = C ? C / Math.sin(C) : 1, n.x = this.x0 + this.a * E * s * Math.sin(r), n.y = this.y0 + this.a * E * (this.cos_p12 * i - this.sin_p12 * s * Math.cos(r)), n) : (o = ur(this.es), a = dr(this.es), l = fr(this.es), h = gr(this.es), Math.abs(this.sin_p12 - 1) <= I ? (c = this.a * Jt(o, a, l, h, S), u = this.a * Jt(o, a, l, h, e), n.x = this.x0 + (c - u) * Math.sin(r), n.y = this.y0 - (c - u) * Math.cos(r), n) : Math.abs(this.sin_p12 + 1) <= I ? (c = this.a * Jt(o, a, l, h, S), u = this.a * Jt(o, a, l, h, e), n.x = this.x0 + (c + u) * Math.sin(r), n.y = this.y0 + (c + u) * Math.cos(r), n) : (d = i / s, f = ts(this.a, this.e, this.sin_p12), g = ts(this.a, this.e, i), m = Math.atan((1 - this.es) * d + this.es * f * this.sin_p12 / (g * s)), _ = Math.atan2(Math.sin(r), this.cos_p12 * Math.tan(m) - this.sin_p12 * Math.cos(r)), _ === 0 ? b = Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : Math.abs(Math.abs(_) - Math.PI) <= I ? b = -Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : b = Math.asin(Math.sin(r) * Math.cos(m) / Math.sin(_)), y = this.e * this.sin_p12 / Math.sqrt(1 - this.es), p = this.e * this.cos_p12 * Math.cos(_) / Math.sqrt(1 - this.es), v = y * p, x = p * p, F = b * b, G = F * b, V = G * b, L = V * b, C = f * b * (1 - F * x * (1 - x) / 6 + G / 8 * v * (1 - 2 * x) + V / 120 * (x * (4 - 7 * x) - 3 * y * y * (1 - 7 * x)) - L / 48 * v), n.x = this.x0 + C * Math.sin(_), n.y = this.y0 + C * Math.cos(_), n));
}
function cE(n) {
  n.x -= this.x0, n.y -= this.y0;
  var t, e, i, s, r, o, a, l, h, c, u, d, f, g, m, _, y, p, v, x, C, E, R, b;
  return this.sphere ? (t = Math.sqrt(n.x * n.x + n.y * n.y), t > 2 * S * this.a ? void 0 : (e = t / this.a, i = Math.sin(e), s = Math.cos(e), r = this.long0, Math.abs(t) <= I ? o = this.lat0 : (o = Fi(s * this.sin_p12 + n.y * i * this.cos_p12 / t), a = Math.abs(this.lat0) - S, Math.abs(a) <= I ? this.lat0 >= 0 ? r = A(this.long0 + Math.atan2(n.x, -n.y)) : r = A(this.long0 - Math.atan2(-n.x, n.y)) : r = A(this.long0 + Math.atan2(n.x * i, t * this.cos_p12 * s - n.y * this.sin_p12 * i))), n.x = r, n.y = o, n)) : (l = ur(this.es), h = dr(this.es), c = fr(this.es), u = gr(this.es), Math.abs(this.sin_p12 - 1) <= I ? (d = this.a * Jt(l, h, c, u, S), t = Math.sqrt(n.x * n.x + n.y * n.y), f = d - t, o = Eo(f / this.a, l, h, c, u), r = A(this.long0 + Math.atan2(n.x, -1 * n.y)), n.x = r, n.y = o, n) : Math.abs(this.sin_p12 + 1) <= I ? (d = this.a * Jt(l, h, c, u, S), t = Math.sqrt(n.x * n.x + n.y * n.y), f = t - d, o = Eo(f / this.a, l, h, c, u), r = A(this.long0 + Math.atan2(n.x, n.y)), n.x = r, n.y = o, n) : (t = Math.sqrt(n.x * n.x + n.y * n.y), _ = Math.atan2(n.x, n.y), g = ts(this.a, this.e, this.sin_p12), y = Math.cos(_), p = this.e * this.cos_p12 * y, v = -p * p / (1 - this.es), x = 3 * this.es * (1 - v) * this.sin_p12 * this.cos_p12 * y / (1 - this.es), C = t / g, E = C - v * (1 + v) * Math.pow(C, 3) / 6 - x * (1 + 3 * v) * Math.pow(C, 4) / 24, R = 1 - v * E * E / 2 - C * E * E * E / 6, m = Math.asin(this.sin_p12 * Math.cos(E) + this.cos_p12 * Math.sin(E) * y), r = A(this.long0 + Math.asin(Math.sin(_) * Math.sin(E) / Math.cos(m))), b = Math.sin(m), o = Math.atan2((b - this.es * R * this.sin_p12) * Math.tan(m), b * (1 - this.es)), n.x = r, n.y = o, n));
}
var uE = ["Azimuthal_Equidistant", "aeqd"];
const dE = {
  init: lE,
  forward: hE,
  inverse: cE,
  names: uE
};
function fE() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0);
}
function gE(n) {
  var t, e, i, s, r, o, a, l, h = n.x, c = n.y;
  return i = A(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(i), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, (o > 0 || Math.abs(o) <= I) && (a = this.a * r * e * Math.sin(i), l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s)), n.x = a, n.y = l, n;
}
function mE(n) {
  var t, e, i, s, r, o, a;
  return n.x -= this.x0, n.y -= this.y0, t = Math.sqrt(n.x * n.x + n.y * n.y), e = Fi(t / this.a), i = Math.sin(e), s = Math.cos(e), o = this.long0, Math.abs(t) <= I ? (a = this.lat0, n.x = o, n.y = a, n) : (a = Fi(s * this.sin_p14 + n.y * i * this.cos_p14 / t), r = Math.abs(this.lat0) - S, Math.abs(r) <= I ? (this.lat0 >= 0 ? o = A(this.long0 + Math.atan2(n.x, -n.y)) : o = A(this.long0 - Math.atan2(-n.x, n.y)), n.x = o, n.y = a, n) : (o = A(this.long0 + Math.atan2(n.x * i, t * this.cos_p14 * s - n.y * this.sin_p14 * i)), n.x = o, n.y = a, n));
}
var _E = ["ortho"];
const pE = {
  init: fE,
  forward: gE,
  inverse: mE,
  names: _E
};
var Ct = {
  FRONT: 1,
  RIGHT: 2,
  BACK: 3,
  LEFT: 4,
  TOP: 5,
  BOTTOM: 6
}, ut = {
  AREA_0: 1,
  AREA_1: 2,
  AREA_2: 3,
  AREA_3: 4
};
function yE() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Quadrilateralized Spherical Cube", this.lat0 >= S - ct / 2 ? this.face = Ct.TOP : this.lat0 <= -(S - ct / 2) ? this.face = Ct.BOTTOM : Math.abs(this.long0) <= ct ? this.face = Ct.FRONT : Math.abs(this.long0) <= S + ct ? this.face = this.long0 > 0 ? Ct.RIGHT : Ct.LEFT : this.face = Ct.BACK, this.es !== 0 && (this.one_minus_f = 1 - (this.a - this.b) / this.a, this.one_minus_f_squared = this.one_minus_f * this.one_minus_f);
}
function vE(n) {
  var t = { x: 0, y: 0 }, e, i, s, r, o, a, l = { value: 0 };
  if (n.x -= this.long0, this.es !== 0 ? e = Math.atan(this.one_minus_f_squared * Math.tan(n.y)) : e = n.y, i = n.x, this.face === Ct.TOP)
    r = S - e, i >= ct && i <= S + ct ? (l.value = ut.AREA_0, s = i - S) : i > S + ct || i <= -(S + ct) ? (l.value = ut.AREA_1, s = i > 0 ? i - Tt : i + Tt) : i > -(S + ct) && i <= -ct ? (l.value = ut.AREA_2, s = i + S) : (l.value = ut.AREA_3, s = i);
  else if (this.face === Ct.BOTTOM)
    r = S + e, i >= ct && i <= S + ct ? (l.value = ut.AREA_0, s = -i + S) : i < ct && i >= -ct ? (l.value = ut.AREA_1, s = -i) : i < -ct && i >= -(S + ct) ? (l.value = ut.AREA_2, s = -i - S) : (l.value = ut.AREA_3, s = i > 0 ? -i + Tt : -i - Tt);
  else {
    var h, c, u, d, f, g, m;
    this.face === Ct.RIGHT ? i = Zn(i, +S) : this.face === Ct.BACK ? i = Zn(i, +Tt) : this.face === Ct.LEFT && (i = Zn(i, -S)), d = Math.sin(e), f = Math.cos(e), g = Math.sin(i), m = Math.cos(i), h = f * m, c = f * g, u = d, this.face === Ct.FRONT ? (r = Math.acos(h), s = Ur(r, u, c, l)) : this.face === Ct.RIGHT ? (r = Math.acos(c), s = Ur(r, u, -h, l)) : this.face === Ct.BACK ? (r = Math.acos(-h), s = Ur(r, u, -c, l)) : this.face === Ct.LEFT ? (r = Math.acos(-c), s = Ur(r, u, h, l)) : (r = s = 0, l.value = ut.AREA_0);
  }
  return a = Math.atan(12 / Tt * (s + Math.acos(Math.sin(s) * Math.cos(ct)) - S)), o = Math.sqrt((1 - Math.cos(r)) / (Math.cos(a) * Math.cos(a)) / (1 - Math.cos(Math.atan(1 / Math.cos(s))))), l.value === ut.AREA_1 ? a += S : l.value === ut.AREA_2 ? a += Tt : l.value === ut.AREA_3 && (a += 1.5 * Tt), t.x = o * Math.cos(a), t.y = o * Math.sin(a), t.x = t.x * this.a + this.x0, t.y = t.y * this.a + this.y0, n.x = t.x, n.y = t.y, n;
}
function xE(n) {
  var t = { lam: 0, phi: 0 }, e, i, s, r, o, a, l, h, c, u = { value: 0 };
  if (n.x = (n.x - this.x0) / this.a, n.y = (n.y - this.y0) / this.a, i = Math.atan(Math.sqrt(n.x * n.x + n.y * n.y)), e = Math.atan2(n.y, n.x), n.x >= 0 && n.x >= Math.abs(n.y) ? u.value = ut.AREA_0 : n.y >= 0 && n.y >= Math.abs(n.x) ? (u.value = ut.AREA_1, e -= S) : n.x < 0 && -n.x >= Math.abs(n.y) ? (u.value = ut.AREA_2, e = e < 0 ? e + Tt : e - Tt) : (u.value = ut.AREA_3, e += S), c = Tt / 12 * Math.tan(e), o = Math.sin(c) / (Math.cos(c) - 1 / Math.sqrt(2)), a = Math.atan(o), s = Math.cos(e), r = Math.tan(i), l = 1 - s * s * r * r * (1 - Math.cos(Math.atan(1 / Math.cos(a)))), l < -1 ? l = -1 : l > 1 && (l = 1), this.face === Ct.TOP)
    h = Math.acos(l), t.phi = S - h, u.value === ut.AREA_0 ? t.lam = a + S : u.value === ut.AREA_1 ? t.lam = a < 0 ? a + Tt : a - Tt : u.value === ut.AREA_2 ? t.lam = a - S : t.lam = a;
  else if (this.face === Ct.BOTTOM)
    h = Math.acos(l), t.phi = h - S, u.value === ut.AREA_0 ? t.lam = -a + S : u.value === ut.AREA_1 ? t.lam = -a : u.value === ut.AREA_2 ? t.lam = -a - S : t.lam = a < 0 ? -a - Tt : -a + Tt;
  else {
    var d, f, g;
    d = l, c = d * d, c >= 1 ? g = 0 : g = Math.sqrt(1 - c) * Math.sin(a), c += g * g, c >= 1 ? f = 0 : f = Math.sqrt(1 - c), u.value === ut.AREA_1 ? (c = f, f = -g, g = c) : u.value === ut.AREA_2 ? (f = -f, g = -g) : u.value === ut.AREA_3 && (c = f, f = g, g = -c), this.face === Ct.RIGHT ? (c = d, d = -f, f = c) : this.face === Ct.BACK ? (d = -d, f = -f) : this.face === Ct.LEFT && (c = d, d = f, f = -c), t.phi = Math.acos(-g) - S, t.lam = Math.atan2(f, d), this.face === Ct.RIGHT ? t.lam = Zn(t.lam, -S) : this.face === Ct.BACK ? t.lam = Zn(t.lam, -Tt) : this.face === Ct.LEFT && (t.lam = Zn(t.lam, +S));
  }
  if (this.es !== 0) {
    var m, _, y;
    m = t.phi < 0 ? 1 : 0, _ = Math.tan(t.phi), y = this.b / Math.sqrt(_ * _ + this.one_minus_f_squared), t.phi = Math.atan(Math.sqrt(this.a * this.a - y * y) / (this.one_minus_f * y)), m && (t.phi = -t.phi);
  }
  return t.lam += this.long0, n.x = t.lam, n.y = t.phi, n;
}
function Ur(n, t, e, i) {
  var s;
  return n < I ? (i.value = ut.AREA_0, s = 0) : (s = Math.atan2(t, e), Math.abs(s) <= ct ? i.value = ut.AREA_0 : s > ct && s <= S + ct ? (i.value = ut.AREA_1, s -= S) : s > S + ct || s <= -(S + ct) ? (i.value = ut.AREA_2, s = s >= 0 ? s - Tt : s + Tt) : (i.value = ut.AREA_3, s += S)), s;
}
function Zn(n, t) {
  var e = n + t;
  return e < -Tt ? e += Hs : e > +Tt && (e -= Hs), e;
}
var CE = ["Quadrilateralized Spherical Cube", "Quadrilateralized_Spherical_Cube", "qsc"];
const ME = {
  init: yE,
  forward: vE,
  inverse: xE,
  names: CE
};
var cl = [
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
], Es = [
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
], ug = 0.8487, dg = 1.3523, fg = Ge / 5, EE = 1 / fg, Gn = 18, wo = function(n, t) {
  return n[0] + t * (n[1] + t * (n[2] + t * n[3]));
}, wE = function(n, t) {
  return n[1] + t * (2 * n[2] + t * 3 * n[3]);
};
function SE(n, t, e, i) {
  for (var s = t; i; --i) {
    var r = n(s);
    if (s -= r, Math.abs(r) < e)
      break;
  }
  return s;
}
function RE() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.long0 = this.long0 || 0, this.es = 0, this.title = this.title || "Robinson";
}
function TE(n) {
  var t = A(n.x - this.long0), e = Math.abs(n.y), i = Math.floor(e * fg);
  i < 0 ? i = 0 : i >= Gn && (i = Gn - 1), e = Ge * (e - EE * i);
  var s = {
    x: wo(cl[i], e) * t,
    y: wo(Es[i], e)
  };
  return n.y < 0 && (s.y = -s.y), s.x = s.x * this.a * ug + this.x0, s.y = s.y * this.a * dg + this.y0, s;
}
function bE(n) {
  var t = {
    x: (n.x - this.x0) / (this.a * ug),
    y: Math.abs(n.y - this.y0) / (this.a * dg)
  };
  if (t.y >= 1)
    t.x /= cl[Gn][0], t.y = n.y < 0 ? -S : S;
  else {
    var e = Math.floor(t.y * Gn);
    for (e < 0 ? e = 0 : e >= Gn && (e = Gn - 1); ; )
      if (Es[e][0] > t.y)
        --e;
      else if (Es[e + 1][0] <= t.y)
        ++e;
      else
        break;
    var i = Es[e], s = 5 * (t.y - i[0]) / (Es[e + 1][0] - i[0]);
    s = SE(function(r) {
      return (wo(i, r) - t.y) / wE(i, r);
    }, s, I, 100), t.x /= wo(cl[e], s), t.y = (5 * e + s) * zt, n.y < 0 && (t.y = -t.y);
  }
  return t.x = A(t.x + this.long0), t;
}
var LE = ["Robinson", "robin"];
const IE = {
  init: RE,
  forward: TE,
  inverse: bE,
  names: LE
};
function PE() {
  this.name = "geocent";
}
function AE(n) {
  var t = Jf(n, this.es, this.a);
  return t;
}
function OE(n) {
  var t = Qf(n, this.es, this.a, this.b);
  return t;
}
var FE = ["Geocentric", "geocentric", "geocent", "Geocent"];
const NE = {
  init: PE,
  forward: AE,
  inverse: OE,
  names: FE
};
var Ht = {
  N_POLE: 0,
  S_POLE: 1,
  EQUIT: 2,
  OBLIQ: 3
}, ys = {
  h: { def: 1e5, num: !0 },
  azi: { def: 0, num: !0, degrees: !0 },
  tilt: { def: 0, num: !0, degrees: !0 },
  long0: { def: 0, num: !0 },
  lat0: { def: 0, num: !0 }
};
function DE() {
  if (Object.keys(ys).forEach(function(e) {
    if (typeof this[e] > "u")
      this[e] = ys[e].def;
    else {
      if (ys[e].num && isNaN(this[e]))
        throw new Error("Invalid parameter value, must be numeric " + e + " = " + this[e]);
      ys[e].num && (this[e] = parseFloat(this[e]));
    }
    ys[e].degrees && (this[e] = this[e] * zt);
  }.bind(this)), Math.abs(Math.abs(this.lat0) - S) < I ? this.mode = this.lat0 < 0 ? Ht.S_POLE : Ht.N_POLE : Math.abs(this.lat0) < I ? this.mode = Ht.EQUIT : (this.mode = Ht.OBLIQ, this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0)), this.pn1 = this.h / this.a, this.pn1 <= 0 || this.pn1 > 1e10)
    throw new Error("Invalid height");
  this.p = 1 + this.pn1, this.rp = 1 / this.p, this.h1 = 1 / this.pn1, this.pfact = (this.p + 1) * this.h1, this.es = 0;
  var n = this.tilt, t = this.azi;
  this.cg = Math.cos(t), this.sg = Math.sin(t), this.cw = Math.cos(n), this.sw = Math.sin(n);
}
function kE(n) {
  n.x -= this.long0;
  var t = Math.sin(n.y), e = Math.cos(n.y), i = Math.cos(n.x), s, r;
  switch (this.mode) {
    case Ht.OBLIQ:
      r = this.sinph0 * t + this.cosph0 * e * i;
      break;
    case Ht.EQUIT:
      r = e * i;
      break;
    case Ht.S_POLE:
      r = -t;
      break;
    case Ht.N_POLE:
      r = t;
      break;
  }
  switch (r = this.pn1 / (this.p - r), s = r * e * Math.sin(n.x), this.mode) {
    case Ht.OBLIQ:
      r *= this.cosph0 * t - this.sinph0 * e * i;
      break;
    case Ht.EQUIT:
      r *= t;
      break;
    case Ht.N_POLE:
      r *= -(e * i);
      break;
    case Ht.S_POLE:
      r *= e * i;
      break;
  }
  var o, a;
  return o = r * this.cg + s * this.sg, a = 1 / (o * this.sw * this.h1 + this.cw), s = (s * this.cg - r * this.sg) * this.cw * a, r = o * a, n.x = s * this.a, n.y = r * this.a, n;
}
function GE(n) {
  n.x /= this.a, n.y /= this.a;
  var t = { x: n.x, y: n.y }, e, i, s;
  s = 1 / (this.pn1 - n.y * this.sw), e = this.pn1 * n.x * s, i = this.pn1 * n.y * this.cw * s, n.x = e * this.cg + i * this.sg, n.y = i * this.cg - e * this.sg;
  var r = Pe(n.x, n.y);
  if (Math.abs(r) < I)
    t.x = 0, t.y = n.y;
  else {
    var o, a;
    switch (a = 1 - r * r * this.pfact, a = (this.p - Math.sqrt(a)) / (this.pn1 / r + r / this.pn1), o = Math.sqrt(1 - a * a), this.mode) {
      case Ht.OBLIQ:
        t.y = Math.asin(o * this.sinph0 + n.y * a * this.cosph0 / r), n.y = (o - this.sinph0 * Math.sin(t.y)) * r, n.x *= a * this.cosph0;
        break;
      case Ht.EQUIT:
        t.y = Math.asin(n.y * a / r), n.y = o * r, n.x *= a;
        break;
      case Ht.N_POLE:
        t.y = Math.asin(o), n.y = -n.y;
        break;
      case Ht.S_POLE:
        t.y = -Math.asin(o);
        break;
    }
    t.x = Math.atan2(n.x, n.y);
  }
  return n.x = t.x + this.long0, n.y = t.y, n;
}
var $E = ["Tilted_Perspective", "tpers"];
const BE = {
  init: DE,
  forward: kE,
  inverse: GE,
  names: $E
};
function zE() {
  if (this.flip_axis = this.sweep === "x" ? 1 : 0, this.h = Number(this.h), this.radius_g_1 = this.h / this.a, this.radius_g_1 <= 0 || this.radius_g_1 > 1e10)
    throw new Error();
  if (this.radius_g = 1 + this.radius_g_1, this.C = this.radius_g * this.radius_g - 1, this.es !== 0) {
    var n = 1 - this.es, t = 1 / n;
    this.radius_p = Math.sqrt(n), this.radius_p2 = n, this.radius_p_inv2 = t, this.shape = "ellipse";
  } else
    this.radius_p = 1, this.radius_p2 = 1, this.radius_p_inv2 = 1, this.shape = "sphere";
  this.title || (this.title = "Geostationary Satellite View");
}
function ZE(n) {
  var t = n.x, e = n.y, i, s, r, o;
  if (t = t - this.long0, this.shape === "ellipse") {
    e = Math.atan(this.radius_p2 * Math.tan(e));
    var a = this.radius_p / Pe(this.radius_p * Math.cos(e), Math.sin(e));
    if (s = a * Math.cos(t) * Math.cos(e), r = a * Math.sin(t) * Math.cos(e), o = a * Math.sin(e), (this.radius_g - s) * s - r * r - o * o * this.radius_p_inv2 < 0)
      return n.x = Number.NaN, n.y = Number.NaN, n;
    i = this.radius_g - s, this.flip_axis ? (n.x = this.radius_g_1 * Math.atan(r / Pe(o, i)), n.y = this.radius_g_1 * Math.atan(o / i)) : (n.x = this.radius_g_1 * Math.atan(r / i), n.y = this.radius_g_1 * Math.atan(o / Pe(r, i)));
  } else
    this.shape === "sphere" && (i = Math.cos(e), s = Math.cos(t) * i, r = Math.sin(t) * i, o = Math.sin(e), i = this.radius_g - s, this.flip_axis ? (n.x = this.radius_g_1 * Math.atan(r / Pe(o, i)), n.y = this.radius_g_1 * Math.atan(o / i)) : (n.x = this.radius_g_1 * Math.atan(r / i), n.y = this.radius_g_1 * Math.atan(o / Pe(r, i))));
  return n.x = n.x * this.a, n.y = n.y * this.a, n;
}
function VE(n) {
  var t = -1, e = 0, i = 0, s, r, o, a;
  if (n.x = n.x / this.a, n.y = n.y / this.a, this.shape === "ellipse") {
    this.flip_axis ? (i = Math.tan(n.y / this.radius_g_1), e = Math.tan(n.x / this.radius_g_1) * Pe(1, i)) : (e = Math.tan(n.x / this.radius_g_1), i = Math.tan(n.y / this.radius_g_1) * Pe(1, e));
    var l = i / this.radius_p;
    if (s = e * e + l * l + t * t, r = 2 * this.radius_g * t, o = r * r - 4 * s * this.C, o < 0)
      return n.x = Number.NaN, n.y = Number.NaN, n;
    a = (-r - Math.sqrt(o)) / (2 * s), t = this.radius_g + a * t, e *= a, i *= a, n.x = Math.atan2(e, t), n.y = Math.atan(i * Math.cos(n.x) / t), n.y = Math.atan(this.radius_p_inv2 * Math.tan(n.y));
  } else if (this.shape === "sphere") {
    if (this.flip_axis ? (i = Math.tan(n.y / this.radius_g_1), e = Math.tan(n.x / this.radius_g_1) * Math.sqrt(1 + i * i)) : (e = Math.tan(n.x / this.radius_g_1), i = Math.tan(n.y / this.radius_g_1) * Math.sqrt(1 + e * e)), s = e * e + i * i + t * t, r = 2 * this.radius_g * t, o = r * r - 4 * s * this.C, o < 0)
      return n.x = Number.NaN, n.y = Number.NaN, n;
    a = (-r - Math.sqrt(o)) / (2 * s), t = this.radius_g + a * t, e *= a, i *= a, n.x = Math.atan2(e, t), n.y = Math.atan(i * Math.cos(n.x) / t);
  }
  return n.x = n.x + this.long0, n;
}
var UE = ["Geostationary Satellite View", "Geostationary_Satellite", "geos"];
const WE = {
  init: zE,
  forward: ZE,
  inverse: VE,
  names: UE
};
function HE(n) {
  n.Proj.projections.add(Yr), n.Proj.projections.add(jr), n.Proj.projections.add(J3), n.Proj.projections.add(lC), n.Proj.projections.add(gC), n.Proj.projections.add(vC), n.Proj.projections.add(SC), n.Proj.projections.add(IC), n.Proj.projections.add(NC), n.Proj.projections.add(BC), n.Proj.projections.add(nM), n.Proj.projections.add(hM), n.Proj.projections.add(gM), n.Proj.projections.add(xM), n.Proj.projections.add(SM), n.Proj.projections.add(IM), n.Proj.projections.add(NM), n.Proj.projections.add(BM), n.Proj.projections.add(HM), n.Proj.projections.add(KM), n.Proj.projections.add(iE), n.Proj.projections.add(aE), n.Proj.projections.add(dE), n.Proj.projections.add(pE), n.Proj.projections.add(ME), n.Proj.projections.add(IE), n.Proj.projections.add(NE), n.Proj.projections.add(BE), n.Proj.projections.add(WE);
}
re.defaultDatum = "WGS84";
re.Proj = Be;
re.WGS84 = new re.Proj("WGS84");
re.Point = Qn;
re.toPoint = tg;
re.defs = qt;
re.nadgrid = t3;
re.transform = Mo;
re.mgrs = _3;
re.version = "__VERSION__";
HE(re);
function XE(n) {
  const t = Object.keys(n.defs), e = t.length;
  let i, s;
  for (i = 0; i < e; ++i) {
    const r = t[i];
    if (!Q(r)) {
      const o = n.defs(r);
      let a = o.units;
      !a && o.projName === "longlat" && (a = "degrees"), md(
        new Rl({
          code: r,
          axisOrientation: o.axis,
          metersPerUnit: o.to_meter,
          units: a
        })
      );
    }
  }
  for (i = 0; i < e; ++i) {
    const r = t[i], o = Q(r);
    for (s = 0; s < e; ++s) {
      const a = t[s], l = Q(a);
      if (!dd(r, a))
        if (n.defs[r] === n.defs[a])
          Ga([o, l]);
        else {
          const h = n(r, a);
          q0(
            o,
            l,
            Jh(o, l, h.forward),
            Jh(l, o, h.inverse)
          );
        }
    }
  }
}
class Iu {
  static setupCircles(t, e) {
    let i = [];
    return t.get("isSelected") ? i = [
      new Zt({
        zIndex: 1,
        image: new we({
          radius: 2 * e,
          stroke: new Xt({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Vt({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Zt({
        zIndex: 2,
        image: new we({
          radius: 0.2 * e,
          stroke: new Xt({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Vt({
            color: "#DC2626"
          })
        })
      })
    ] : i = [
      new Zt({
        zIndex: 1,
        image: new we({
          radius: 2 * e,
          stroke: new Xt({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Vt({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Zt({
        zIndex: 2,
        image: new we({
          radius: 0.2 * e,
          stroke: new Xt({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Vt({
            color: "#DC2626"
          })
        })
      })
    ], i;
  }
}
class YE {
  constructor(t) {
    this.control = new bf(), this.store = w();
    const e = this.store.getMap(), i = new Ve();
    this.setupMapForCreation(e, i), window.addEventListener("authorize-created", () => {
      this.createElement(i);
    }), window.addEventListener("remove-created-icon", () => {
      this.deleteElement(i);
    }), window.addEventListener("recenter-selected-element", () => {
      var o;
      const s = this.store.getCurrentItemId(), r = (o = this.store.getSelectedFeature(s, "id")) == null ? void 0 : o.get("geom").getCoordinates();
      e.getView().setCenter(r);
    }), this.addLongClickEvent(t, e), e.on("click", (s) => {
      e.forEachFeatureAtPixel(s.pixel, (r) => {
        var o, a;
        r && ((o = r.getGeometry()) == null ? void 0 : o.getType()) === "Point" && (i.getFeatures().forEach((l) => {
          l.set("isSelected", void 0);
        }), this.store.setCurrentItemId(r.get("id")), (a = this.store.getSelectedFeature(r.get("id"), "id")) == null || a.set("isSelected", !0), ot.sendEvent("open-select-create-box", r.get("geom").getCoordinates()), this.control.show());
      });
    });
  }
  setupMapForCreation(t, e) {
    var o;
    const i = this.store.getOptions(), s = ((o = i.notifications.find((a) => a.rule.type === "ZOOM_CONSTRAINT")) == null ? void 0 : o.rule.minZoom) || i.zoom, r = new Ze({
      source: e,
      visible: !0
    });
    r.setStyle(function(a) {
      return Iu.setupCircles(a, 1);
    }), t.addLayer(r), t.getView().on("change:resolution", () => {
      const a = t.getView().getZoom(), l = t.getView().getResolution();
      a && l && a > s && r.setStyle(function(h) {
        return Iu.setupCircles(h, a / l);
      });
    }), this.control.disable(), t.addControl(this.control);
  }
  createElement(t) {
    if (this.store.getSelectedFeatures().length > this.store.getMaxElement()) {
      this.store.removeSelectedFeature(this.store.getCurrentItemId(), "id");
      return;
    }
    const i = this.store.getSelectedFeature(this.store.getCurrentItemId(), "id");
    i && (this.store.getMaxElement() === 1 ? (t.getFeatures().forEach((s) => t.removeFeature(s)), this.control.hide()) : t.getFeatures().forEach((s) => {
      s.get("id") !== this.store.getCurrentItemId() && s.set("isSelected", void 0);
    }), t.addFeature(i), this.control.show(), ot.sendEvent("open-select-create-box", i.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select")), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
  }
  deleteElement(t) {
    const e = this.store.getSelectedFeature(this.store.getCurrentItemId(), "id");
    e && (t.removeFeature(e), this.control.hide(), this.store.removeSelectedFeature(this.store.getCurrentItemId(), "id"), ot.sendEvent("rule-validation", void 0), Lf.setCustomStyleWithouInfoBox()), this.store.getMap().get("target").className = `${this.store.getTargetBoxSize()} ${this.store.getTheme()}`;
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
  requestElementCreation(t, e, i, s) {
    const r = i.getCoordinateFromPixel([t - s.offsetLeft, e - s.offsetTop]), o = new Se(r), a = new Ie({
      geom: o,
      id: Number(`${Math.round(r[0])}${Math.round(r[1])}`),
      isSelected: !0
    });
    a.setGeometryName("geom"), this.store.getMaxElement() === 1 && this.store.removeSelectedFeature(this.store.getCurrentItemId(), "id"), (this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement()) && (this.store.setCurrentItemId(a.get("id")), this.store.addSelectedFeature(a), ot.sendEvent("icon-created", void 0));
  }
  moveAnalyzer(t, e, i) {
    return Math.abs(e - t[0]) > 10 || Math.abs(i - t[1]) > 10;
  }
  clearCreationTimeout(t) {
    clearTimeout(t), t = void 0;
  }
}
const gg = `.search-container{left:calc(50% - 151px);position:absolute;max-width:302px;width:100%;top:var(--top-distance);z-index:-1}.search-input-container{border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color)}.search-input{width:calc(100% - 13px);height:44px;border:none;outline:none;padding:0 0 0 11px;font-size:14px;background-color:var(--information-box-background-color);color:var(--information-box-text-color)}.search-svg-container{width:29px;height:44px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-radius:var(--icon-border-radius)}ul>:first-child{border-top-right-radius:var(--icon-border-radius);border-top-left-radius:var(--icon-border-radius)}li{height:40px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--information-box-text-color)}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var jE = Object.defineProperty, qE = Object.getOwnPropertyDescriptor, gn = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? qE(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && jE(t, e, s), s;
};
let js = class extends kt {
  constructor() {
    super(), this._results = [], w().getMap().addEventListener("click", () => {
      this._results = [];
    });
  }
  updated(n) {
    if (n.has("locations"))
      if (this.locations && this.locations.results && this.locations.results.length > 0) {
        const t = this.locations.results.length > 5 ? 5 : this.locations.results.length;
        this._results = [];
        for (let e = 0; e < t; e++) {
          let i = "";
          if (this.locations.results[e].attrs.origin == "address") {
            if (this.locations.results[e].attrs.label.trim().startsWith("<b>"))
              continue;
            i = this.locations.results[e].attrs.label.replace("<b>", " - ").replace("</b>", "");
          } else
            this.locations.results[e].attrs.origin == "parcel" && (i = "Parcelle: " + this.locations.results[e].attrs.label.replace("<b>", "").replace("</b>", "").split("(CH")[0]);
          this._results.push({ coordinate: [this.locations.results[e].attrs.lon, this.locations.results[e].attrs.lat], address: i });
        }
      } else
        this._results = [];
  }
  selectAddress(n, t) {
    w().getMap().getView().setCenter(K0([n[0], n[1]], "EPSG:2056")), this._results = [], ot.sendEvent("address_selected", t);
  }
  render() {
    return Lt`
                <ul>
                  ${this._results.map(
      (n) => Lt`<li tabindex="0" @click=${() => this.selectAddress(n.coordinate, n.address)}>${n.address}</li>`
    )}
                </ul>
              `;
  }
};
js.styles = [Mt(gg)];
gn([
  cn({ type: Object })
], js.prototype, "locations", 2);
gn([
  ae()
], js.prototype, "_results", 2);
js = gn([
  oe("location-list")
], js);
let es = class extends kt {
  constructor() {
    super(), this.results = {}, this._hasSearch = !1, window.addEventListener("address_selected", (n) => {
      this.inputElement.value = n.detail, this._hasSearch = !1;
    });
  }
  firstUpdated() {
    this.inputElement.oninput = () => {
      if (this.inputElement.value.length > 1) {
        this._hasSearch = !0;
        const n = w().getOptions();
        let t = `${n.search.requestWithoutCustomValue}&searchText=${this.inputElement.value}`;
        n.search.bboxRestiction !== "" && (t += `&bbox=${n.search.bboxRestiction}`), fetch(t).then((e) => e.json()).then((e) => {
          this.results = e;
        });
      } else
        this._hasSearch = !1, this.results = {};
    };
  }
  clear() {
    this.inputElement.value = "", this.results = {}, this._hasSearch = !1;
  }
  render() {
    return Lt`<div class="search-container">
                    <div class="search-input-container">
                        <input id="search" type="text" class="search-input">
                        <div class="search-svg-container">
                        ${Rf(
      this._hasSearch ? Lt`<div class="cross-div" @click="${this.clear}">
                                        ${Ue(at.cross)}
                                    </div>` : Lt`${Ue(at.search)}`
    )}
                        </div>
                    </div>
                    <location-list locations='${JSON.stringify(this.results)}'/>
                </div>`;
  }
};
es.styles = [Mt(gg)];
gn([
  Vu("#search")
], es.prototype, "inputElement", 2);
gn([
  ae()
], es.prototype, "results", 2);
gn([
  ae()
], es.prototype, "_hasSearch", 2);
es = gn([
  oe("search-location")
], es);
class KE extends Gt {
  constructor() {
    const t = document.createElement("search-location");
    super({ element: t }), this.div = t;
  }
}
class JE {
  constructor() {
    const t = new Zt({
      fill: new Vt({
        color: "#ffffff00"
      }),
      stroke: new Xt({
        color: "#dddddd",
        width: 5
      })
    }), e = new Ze({
      source: new Ve({
        url: () => w().getOptions().borderUrl,
        format: new mf()
      }),
      zIndex: 9999,
      style: t,
      opacity: 0.9
    });
    e.on("change", () => {
      var s, r;
      const i = (s = e.getSource()) == null ? void 0 : s.getExtent();
      if (i) {
        const o = w().getOptions();
        w().getMap().setView(new si({
          extent: i,
          projection: "EPSG:2056",
          center: o.defaultCenter,
          zoom: o.zoom,
          minZoom: o.minZoom,
          maxZoom: o.maxZoom,
          enableRotation: o.enableRotation,
          constrainOnlyCenter: !0
        }));
      }
      w().setBorderConstraint((r = e.getSource()) == null ? void 0 : r.getExtent()), ot.sendEvent("border-contraint-enabled", void 0);
    }), w().getMap().addLayer(e);
  }
}
var QE = Object.defineProperty, tw = Object.getOwnPropertyDescriptor, Xo = (n, t, e, i) => {
  for (var s = i > 1 ? void 0 : i ? tw(t, e) : t, r = n.length - 1, o; r >= 0; r--)
    (o = n[r]) && (s = (i ? o(t, e, s) : o(s)) || s);
  return i && s && QE(t, e, s), s;
};
let is = class extends kt {
  constructor() {
    super(), this.options = {};
  }
  connectedCallback() {
    super.connectedCallback();
  }
  setupTheme(n) {
    n.darkMode ? w().setTheme("dark") : n.lightMode || window.matchMedia("(prefers-color-scheme: light)").matches ? w().setTheme("light") : window.matchMedia("(prefers-color-scheme: dark)").matches ? w().setTheme("dark") : w().setTheme("light");
  }
  setupCustomDisplay(n) {
    n.mode.type === "target" ? (w().setCustomDisplay(n.geolocationInformation.displayBox), this.setupTargetBoxSize(n.geolocationInformation)) : n.search.displaySearch ? (w().setTargetBoxSize("small"), w().setCustomDisplay(!0)) : (w().setTargetBoxSize("no-box"), w().setCustomDisplay(!1));
  }
  setupTargetBoxSize(n) {
    n.currentLocation && n.reverseLocation ? w().setTargetBoxSize("large") : n.currentLocation || n.reverseLocation ? w().setTargetBoxSize("medium") : w().setTargetBoxSize("small");
  }
  firstUpdated() {
    var t;
    Fv.getOptions(this.options);
    const n = w().getOptions();
    this.setupTheme(n), this.setupCustomDisplay(n), re.defs("EPSG:2056", "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"), XE(re), this.view = new si({
      projection: "EPSG:2056",
      center: n.defaultCenter,
      zoom: n.zoom,
      minZoom: n.minZoom,
      maxZoom: n.maxZoom,
      enableRotation: n.enableRotation
    }), w().setMap(new Mm({
      target: this.mapElement,
      controls: [],
      layers: [],
      view: this.view
    })), n.enableGeolocation && (w().setGeolocation(new Rm({
      trackingOptions: {
        enableHighAccuracy: !0
      },
      projection: this.view.getProjection()
    })), (t = w().getGeolocation()) == null || t.setTracking(!0), new My()), n.mode.type === "target" && (w().getMap().addControl(new cx()), n.geolocationInformation.displayBox && w().getMap().addControl(
      new gx()
    )), n.wmts.length > 0 && new Sv(), n.displayScaleLine && w().getMap().addControl(new Q_({ units: "metric" })), n.geojson.url != "" && new Dp(), n.borderUrl !== "" && new JE(), n.mode.type === "select" && n.wfs.url != "" && new Cy(), n.enableDraw && new Np(), n.inclusionArea.url !== "" && new Nv(), n.mode.type === "create" && new YE(this.mapElement), new Pv(), rx.setupIcon(), n.search.displaySearch && n.mode.type !== "target" && w().getMap().addControl(new KE());
  }
  render() {
    return Lt`
    <div id="map" class="${w().getTargetBoxSize()} ${w().getTheme()}">
    </div>   
    `;
  }
};
is.styles = [Mt(Rv), Mt(Tv), Mt(Vo), Mt(dh), Mt(Av), Mt(Ov)];
Xo([
  Vu("#map")
], is.prototype, "mapElement", 2);
Xo([
  ae()
], is.prototype, "view", 2);
Xo([
  cn({ type: Object, attribute: "options" })
], is.prototype, "options", 2);
is = Xo([
  oe("openlayers-element")
], is);
export {
  is as OpenLayersElement
};
