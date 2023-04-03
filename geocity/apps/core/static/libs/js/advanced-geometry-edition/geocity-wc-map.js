/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Lr = window, Ba = Lr.ShadowRoot && (Lr.ShadyCSS === void 0 || Lr.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, ou = Symbol(), eh = /* @__PURE__ */ new WeakMap();
class kf {
  constructor(t, e, n) {
    if (this._$cssResult$ = !0, n !== ou)
      throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (Ba && t === void 0) {
      const n = e !== void 0 && e.length === 1;
      n && (t = eh.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), n && eh.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
}
const yt = (i) => new kf(typeof i == "string" ? i : i + "", void 0, ou), Xf = (i, t) => {
  Ba ? i.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet) : t.forEach((e) => {
    const n = document.createElement("style"), s = Lr.litNonce;
    s !== void 0 && n.setAttribute("nonce", s), n.textContent = e.cssText, i.appendChild(n);
  });
}, ih = Ba ? (i) => i : (i) => i instanceof CSSStyleSheet ? ((t) => {
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
const zr = window, nh = zr.trustedTypes, Gf = nh ? nh.emptyScript : "", sh = zr.reactiveElementPolyfillSupport, aa = { toAttribute(i, t) {
  switch (t) {
    case Boolean:
      i = i ? Gf : null;
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
} }, au = (i, t) => t !== i && (t == t || i == i), jo = { attribute: !0, type: String, converter: aa, reflect: !1, hasChanged: au };
class xn extends HTMLElement {
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
  static createProperty(t, e = jo) {
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
    return this.elementProperties.get(t) || jo;
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
        e.unshift(ih(s));
    } else
      t !== void 0 && e.push(ih(t));
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
    return Xf(e, this.constructor.elementStyles), e;
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
  _$EO(t, e, n = jo) {
    var s;
    const r = this.constructor._$Ep(t, n);
    if (r !== void 0 && n.reflect === !0) {
      const o = (((s = n.converter) === null || s === void 0 ? void 0 : s.toAttribute) !== void 0 ? n.converter : aa).toAttribute(e, n.type);
      this._$El = t, o == null ? this.removeAttribute(r) : this.setAttribute(r, o), this._$El = null;
    }
  }
  _$AK(t, e) {
    var n;
    const s = this.constructor, r = s._$Ev.get(t);
    if (r !== void 0 && this._$El !== r) {
      const o = s.getPropertyOptions(r), a = typeof o.converter == "function" ? { fromAttribute: o.converter } : ((n = o.converter) === null || n === void 0 ? void 0 : n.fromAttribute) !== void 0 ? o.converter : aa;
      this._$El = r, this[r] = a.fromAttribute(e, o.type), this._$El = null;
    }
  }
  requestUpdate(t, e, n) {
    let s = !0;
    t !== void 0 && (((n = n || this.constructor.getPropertyOptions(t)).hasChanged || au)(this[t], e) ? (this._$AL.has(t) || this._$AL.set(t, e), n.reflect === !0 && this._$El !== t && (this._$EC === void 0 && (this._$EC = /* @__PURE__ */ new Map()), this._$EC.set(t, n))) : s = !1), !this.isUpdatePending && s && (this._$E_ = this._$Ej());
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
xn.finalized = !0, xn.elementProperties = /* @__PURE__ */ new Map(), xn.elementStyles = [], xn.shadowRootOptions = { mode: "open" }, sh == null || sh({ ReactiveElement: xn }), ((Do = zr.reactiveElementVersions) !== null && Do !== void 0 ? Do : zr.reactiveElementVersions = []).push("1.5.0");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var ko;
const Fr = window, zn = Fr.trustedTypes, rh = zn ? zn.createPolicy("lit-html", { createHTML: (i) => i }) : void 0, ei = `lit$${(Math.random() + "").slice(9)}$`, Wa = "?" + ei, Hf = `<${Wa}>`, Fn = document, Es = (i = "") => Fn.createComment(i), bs = (i) => i === null || typeof i != "object" && typeof i != "function", lu = Array.isArray, hu = (i) => lu(i) || typeof (i == null ? void 0 : i[Symbol.iterator]) == "function", ls = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, oh = /-->/g, ah = />/g, zi = RegExp(`>|[ \f\r](?:([^\\s"'>=/]+)([ \f\r]*=[ \f\r]*(?:[^ \f\r"'\`<>=]|("|')|))|$)`, "g"), lh = /'/g, hh = /"/g, cu = /^(?:script|style|textarea|title)$/i, Zf = (i) => (t, ...e) => ({ _$litType$: i, strings: t, values: e }), Ct = Zf(1), Pi = Symbol.for("lit-noChange"), Rt = Symbol.for("lit-nothing"), ch = /* @__PURE__ */ new WeakMap(), On = Fn.createTreeWalker(Fn, 129, null, !1), uu = (i, t) => {
  const e = i.length - 1, n = [];
  let s, r = t === 2 ? "<svg>" : "", o = ls;
  for (let l = 0; l < e; l++) {
    const h = i[l];
    let c, u, d = -1, f = 0;
    for (; f < h.length && (o.lastIndex = f, u = o.exec(h), u !== null); )
      f = o.lastIndex, o === ls ? u[1] === "!--" ? o = oh : u[1] !== void 0 ? o = ah : u[2] !== void 0 ? (cu.test(u[2]) && (s = RegExp("</" + u[2], "g")), o = zi) : u[3] !== void 0 && (o = zi) : o === zi ? u[0] === ">" ? (o = s != null ? s : ls, d = -1) : u[1] === void 0 ? d = -2 : (d = o.lastIndex - u[2].length, c = u[1], o = u[3] === void 0 ? zi : u[3] === '"' ? hh : lh) : o === hh || o === lh ? o = zi : o === oh || o === ah ? o = ls : (o = zi, s = void 0);
    const g = o === zi && i[l + 1].startsWith("/>") ? " " : "";
    r += o === ls ? h + Hf : d >= 0 ? (n.push(c), h.slice(0, d) + "$lit$" + h.slice(d) + ei + g) : h + ei + (d === -2 ? (n.push(void 0), l) : g);
  }
  const a = r + (i[e] || "<?>") + (t === 2 ? "</svg>" : "");
  if (!Array.isArray(i) || !i.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return [rh !== void 0 ? rh.createHTML(a) : a, n];
};
class Ps {
  constructor({ strings: t, _$litType$: e }, n) {
    let s;
    this.parts = [];
    let r = 0, o = 0;
    const a = t.length - 1, l = this.parts, [h, c] = uu(t, e);
    if (this.el = Ps.createElement(h, n), On.currentNode = this.el.content, e === 2) {
      const u = this.el.content, d = u.firstChild;
      d.remove(), u.append(...d.childNodes);
    }
    for (; (s = On.nextNode()) !== null && l.length < a; ) {
      if (s.nodeType === 1) {
        if (s.hasAttributes()) {
          const u = [];
          for (const d of s.getAttributeNames())
            if (d.endsWith("$lit$") || d.startsWith(ei)) {
              const f = c[o++];
              if (u.push(d), f !== void 0) {
                const g = s.getAttribute(f.toLowerCase() + "$lit$").split(ei), m = /([.?@])?(.*)/.exec(f);
                l.push({ type: 1, index: r, name: m[2], strings: g, ctor: m[1] === "." ? fu : m[1] === "?" ? gu : m[1] === "@" ? mu : Hs });
              } else
                l.push({ type: 6, index: r });
            }
          for (const d of u)
            s.removeAttribute(d);
        }
        if (cu.test(s.tagName)) {
          const u = s.textContent.split(ei), d = u.length - 1;
          if (d > 0) {
            s.textContent = zn ? zn.emptyScript : "";
            for (let f = 0; f < d; f++)
              s.append(u[f], Es()), On.nextNode(), l.push({ type: 2, index: ++r });
            s.append(u[d], Es());
          }
        }
      } else if (s.nodeType === 8)
        if (s.data === Wa)
          l.push({ type: 2, index: r });
        else {
          let u = -1;
          for (; (u = s.data.indexOf(ei, u + 1)) !== -1; )
            l.push({ type: 7, index: r }), u += ei.length - 1;
        }
      r++;
    }
  }
  static createElement(t, e) {
    const n = Fn.createElement("template");
    return n.innerHTML = t, n;
  }
}
function Ji(i, t, e = i, n) {
  var s, r, o, a;
  if (t === Pi)
    return t;
  let l = n !== void 0 ? (s = e._$Co) === null || s === void 0 ? void 0 : s[n] : e._$Cl;
  const h = bs(t) ? void 0 : t._$litDirective$;
  return (l == null ? void 0 : l.constructor) !== h && ((r = l == null ? void 0 : l._$AO) === null || r === void 0 || r.call(l, !1), h === void 0 ? l = void 0 : (l = new h(i), l._$AT(i, e, n)), n !== void 0 ? ((o = (a = e)._$Co) !== null && o !== void 0 ? o : a._$Co = [])[n] = l : e._$Cl = l), l !== void 0 && (t = Ji(i, l._$AS(i, t.values), l, n)), t;
}
class du {
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
    const { el: { content: n }, parts: s } = this._$AD, r = ((e = t == null ? void 0 : t.creationScope) !== null && e !== void 0 ? e : Fn).importNode(n, !0);
    On.currentNode = r;
    let o = On.nextNode(), a = 0, l = 0, h = s[0];
    for (; h !== void 0; ) {
      if (a === h.index) {
        let c;
        h.type === 2 ? c = new qn(o, o.nextSibling, this, t) : h.type === 1 ? c = new h.ctor(o, h.name, h.strings, this, t) : h.type === 6 && (c = new pu(o, this, t)), this.u.push(c), h = s[++l];
      }
      a !== (h == null ? void 0 : h.index) && (o = On.nextNode(), a++);
    }
    return r;
  }
  p(t) {
    let e = 0;
    for (const n of this.u)
      n !== void 0 && (n.strings !== void 0 ? (n._$AI(t, n, e), e += n.strings.length - 2) : n._$AI(t[e])), e++;
  }
}
class qn {
  constructor(t, e, n, s) {
    var r;
    this.type = 2, this._$AH = Rt, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = n, this.options = s, this._$Cm = (r = s == null ? void 0 : s.isConnected) === null || r === void 0 || r;
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
    t = Ji(this, t, e), bs(t) ? t === Rt || t == null || t === "" ? (this._$AH !== Rt && this._$AR(), this._$AH = Rt) : t !== this._$AH && t !== Pi && this.g(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : hu(t) ? this.k(t) : this.g(t);
  }
  O(t, e = this._$AB) {
    return this._$AA.parentNode.insertBefore(t, e);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  g(t) {
    this._$AH !== Rt && bs(this._$AH) ? this._$AA.nextSibling.data = t : this.T(Fn.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    var e;
    const { values: n, _$litType$: s } = t, r = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = Ps.createElement(s.h, this.options)), s);
    if (((e = this._$AH) === null || e === void 0 ? void 0 : e._$AD) === r)
      this._$AH.p(n);
    else {
      const o = new du(r, this), a = o.v(this.options);
      o.p(n), this.T(a), this._$AH = o;
    }
  }
  _$AC(t) {
    let e = ch.get(t.strings);
    return e === void 0 && ch.set(t.strings, e = new Ps(t)), e;
  }
  k(t) {
    lu(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let n, s = 0;
    for (const r of t)
      s === e.length ? e.push(n = new qn(this.O(Es()), this.O(Es()), this, this.options)) : n = e[s], n._$AI(r), s++;
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
class Hs {
  constructor(t, e, n, s, r) {
    this.type = 1, this._$AH = Rt, this._$AN = void 0, this.element = t, this.name = e, this._$AM = s, this.options = r, n.length > 2 || n[0] !== "" || n[1] !== "" ? (this._$AH = Array(n.length - 1).fill(new String()), this.strings = n) : this._$AH = Rt;
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
      t = Ji(this, t, e, 0), o = !bs(t) || t !== this._$AH && t !== Pi, o && (this._$AH = t);
    else {
      const a = t;
      let l, h;
      for (t = r[0], l = 0; l < r.length - 1; l++)
        h = Ji(this, a[n + l], e, l), h === Pi && (h = this._$AH[l]), o || (o = !bs(h) || h !== this._$AH[l]), h === Rt ? t = Rt : t !== Rt && (t += (h != null ? h : "") + r[l + 1]), this._$AH[l] = h;
    }
    o && !s && this.j(t);
  }
  j(t) {
    t === Rt ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t != null ? t : "");
  }
}
class fu extends Hs {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === Rt ? void 0 : t;
  }
}
const Bf = zn ? zn.emptyScript : "";
class gu extends Hs {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    t && t !== Rt ? this.element.setAttribute(this.name, Bf) : this.element.removeAttribute(this.name);
  }
}
class mu extends Hs {
  constructor(t, e, n, s, r) {
    super(t, e, n, s, r), this.type = 5;
  }
  _$AI(t, e = this) {
    var n;
    if ((t = (n = Ji(this, t, e, 0)) !== null && n !== void 0 ? n : Rt) === Pi)
      return;
    const s = this._$AH, r = t === Rt && s !== Rt || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, o = t !== Rt && (s === Rt || r);
    r && this.element.removeEventListener(this.name, this, s), o && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    var e, n;
    typeof this._$AH == "function" ? this._$AH.call((n = (e = this.options) === null || e === void 0 ? void 0 : e.host) !== null && n !== void 0 ? n : this.element, t) : this._$AH.handleEvent(t);
  }
}
class pu {
  constructor(t, e, n) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = n;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    Ji(this, t);
  }
}
const Wf = { P: "$lit$", A: ei, M: Wa, C: 1, L: uu, R: du, D: hu, V: Ji, I: qn, H: Hs, N: gu, U: mu, B: fu, F: pu }, uh = Fr.litHtmlPolyfillSupport;
uh == null || uh(Ps, qn), ((ko = Fr.litHtmlVersions) !== null && ko !== void 0 ? ko : Fr.litHtmlVersions = []).push("2.5.0");
const vu = (i, t, e) => {
  var n, s;
  const r = (n = e == null ? void 0 : e.renderBefore) !== null && n !== void 0 ? n : t;
  let o = r._$litPart$;
  if (o === void 0) {
    const a = (s = e == null ? void 0 : e.renderBefore) !== null && s !== void 0 ? s : null;
    r._$litPart$ = o = new qn(t.insertBefore(Es(), a), a, void 0, e != null ? e : {});
  }
  return o._$AI(i), o;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var Xo, Go;
class At extends xn {
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
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = vu(e, this.renderRoot, this.renderOptions);
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
    return Pi;
  }
}
At.finalized = !0, At._$litElement$ = !0, (Xo = globalThis.litElementHydrateSupport) === null || Xo === void 0 || Xo.call(globalThis, { LitElement: At });
const dh = globalThis.litElementPolyfillSupport;
dh == null || dh({ LitElement: At });
((Go = globalThis.litElementVersions) !== null && Go !== void 0 ? Go : globalThis.litElementVersions = []).push("3.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Kt = (i) => (t) => typeof t == "function" ? ((e, n) => (customElements.define(e, n), n))(i, t) : ((e, n) => {
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
const Vf = (i, t) => t.kind === "method" && t.descriptor && !("value" in t.descriptor) ? { ...t, finisher(e) {
  e.createProperty(t.key, i);
} } : { kind: "field", key: Symbol(), placement: "own", descriptor: {}, originalKey: t.key, initializer() {
  typeof t.initializer == "function" && (this[t.key] = t.initializer.call(this));
}, finisher(e) {
  e.createProperty(t.key, i);
} };
function Te(i) {
  return (t, e) => e !== void 0 ? ((n, s, r) => {
    s.constructor.createProperty(r, n);
  })(i, t, e) : Vf(i, t);
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function Lt(i) {
  return Te({ ...i, state: !0 });
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Yf = ({ finisher: i, descriptor: t }) => (e, n) => {
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
function Va(i, t) {
  return Yf({ descriptor: (e) => {
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
var Ho;
((Ho = window.HTMLSlotElement) === null || Ho === void 0 ? void 0 : Ho.prototype.assignedElements) != null;
class Uf {
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
const Ge = Uf, Dn = {
  PROPERTYCHANGE: "propertychange"
};
class Jf {
  constructor() {
    this.disposed = !1;
  }
  dispose() {
    this.disposed || (this.disposed = !0, this.disposeInternal());
  }
  disposeInternal() {
  }
}
const Ya = Jf;
function qf(i, t, e) {
  let n, s;
  e = e || qi;
  let r = 0, o = i.length, a = !1;
  for (; r < o; )
    n = r + (o - r >> 1), s = +e(i[n], t), s < 0 ? r = n + 1 : (o = n, a = !s);
  return a ? r : ~r;
}
function qi(i, t) {
  return i > t ? 1 : i < t ? -1 : 0;
}
function Ua(i, t, e) {
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
function Kf(i, t, e) {
  for (; t < e; ) {
    const n = i[t];
    i[t] = i[e], i[e] = n, ++t, --e;
  }
}
function qt(i, t) {
  const e = Array.isArray(t) ? t : [t], n = e.length;
  for (let s = 0; s < n; s++)
    i[i.length] = e[s];
}
function sn(i, t) {
  const e = i.length;
  if (e !== t.length)
    return !1;
  for (let n = 0; n < e; n++)
    if (i[n] !== t[n])
      return !1;
  return !0;
}
function Qf(i, t, e) {
  const n = t || qi;
  return i.every(function(s, r) {
    if (r === 0)
      return !0;
    const o = n(i[r - 1], s);
    return !(o > 0 || e && o === 0);
  });
}
function Ss() {
  return !0;
}
function lo() {
  return !1;
}
function Ki() {
}
function $f(i) {
  let t = !1, e, n, s;
  return function() {
    const r = Array.prototype.slice.call(arguments);
    return (!t || this !== s || !sn(r, n)) && (t = !0, s = this, n = r, e = i.apply(this, arguments)), e;
  };
}
function Zs(i) {
  for (const t in i)
    delete i[t];
}
function jn(i) {
  let t;
  for (t in i)
    return !1;
  return !t;
}
class t0 extends Ya {
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
    const r = e ? new Ge(t) : t;
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
        this.removeEventListener(n, Ki);
      delete o[n];
    }
    return l;
  }
  disposeInternal() {
    this.listeners_ && Zs(this.listeners_);
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
      s !== -1 && (this.pendingRemovals_ && t in this.pendingRemovals_ ? (n[s] = Ki, ++this.pendingRemovals_[t]) : (n.splice(s, 1), n.length === 0 && delete this.listeners_[t]));
    }
  }
}
const ho = t0, V = {
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
  i && i.target && (i.target.removeEventListener(i.type, i.listener), Zs(i));
}
class co extends ho {
  constructor() {
    super(), this.on = this.onInternal, this.once = this.onceInternal, this.un = this.unInternal, this.revision_ = 0;
  }
  changed() {
    ++this.revision_, this.dispatchEvent(V.CHANGE);
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
      e0(n);
    else if (Array.isArray(t))
      for (let s = 0, r = t.length; s < r; ++s)
        this.removeEventListener(t[s], e);
    else
      this.removeEventListener(t, e);
  }
}
co.prototype.on;
co.prototype.once;
co.prototype.un;
function e0(i) {
  if (Array.isArray(i))
    for (let t = 0, e = i.length; t < e; ++t)
      pt(i[t]);
  else
    pt(i);
}
const yu = co;
function B() {
  throw new Error("Unimplemented abstract method.");
}
let i0 = 0;
function rt(i) {
  return i.ol_uid || (i.ol_uid = String(++i0));
}
class fh extends Ge {
  constructor(t, e, n) {
    super(t), this.key = e, this.oldValue = n;
  }
}
class n0 extends yu {
  constructor(t) {
    super(), this.on, this.once, this.un, rt(this), this.values_ = null, t !== void 0 && this.setProperties(t);
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
    n = `change:${t}`, this.hasListener(n) && this.dispatchEvent(new fh(n, t, e)), n = Dn.PROPERTYCHANGE, this.hasListener(n) && this.dispatchEvent(new fh(n, t, e));
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
      delete this.values_[t], jn(this.values_) && (this.values_ = null), e || this.notify(t, n);
    }
  }
}
const Ce = n0, s0 = {
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
class r0 extends Error {
  constructor(t) {
    const e = s0[t];
    super(e), this.code = t, this.name = "AssertionError", this.message = e;
  }
}
const xu = r0, ee = {
  ADD: "add",
  REMOVE: "remove"
}, gh = {
  LENGTH: "length"
};
class fr extends Ge {
  constructor(t, e, n) {
    super(t), this.element = e, this.index = n;
  }
}
class o0 extends Ce {
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
    return this.get(gh.LENGTH);
  }
  insertAt(t, e) {
    if (t < 0 || t > this.getLength())
      throw new Error("Index out of bounds: " + t);
    this.unique_ && this.assertUnique_(e), this.array_.splice(t, 0, e), this.updateLength_(), this.dispatchEvent(
      new fr(ee.ADD, e, t)
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
      new fr(ee.REMOVE, e, t)
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
      new fr(ee.REMOVE, s, t)
    ), this.dispatchEvent(
      new fr(ee.ADD, e, t)
    );
  }
  updateLength_() {
    this.set(gh.LENGTH, this.array_.length);
  }
  assertUnique_(t, e) {
    for (let n = 0, s = this.array_.length; n < s; ++n)
      if (this.array_[n] === t && n !== e)
        throw new xu(58);
  }
}
const Ie = o0, Si = typeof navigator < "u" && typeof navigator.userAgent < "u" ? navigator.userAgent.toLowerCase() : "", a0 = Si.includes("firefox"), l0 = Si.includes("safari") && !Si.includes("chrom");
l0 && (Si.includes("version/15.4") || /cpu (os|iphone os) 15_4 like mac os x/.test(Si));
const h0 = Si.includes("webkit") && !Si.includes("edge"), c0 = Si.includes("macintosh"), Mu = typeof devicePixelRatio < "u" ? devicePixelRatio : 1, Ja = typeof WorkerGlobalScope < "u" && typeof OffscreenCanvas < "u" && self instanceof WorkerGlobalScope, u0 = typeof Image < "u" && Image.prototype.decode, Cu = function() {
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
    throw new xu(t);
}
new Array(6);
function Fe() {
  return [1, 0, 0, 1, 0, 0];
}
function d0(i, t) {
  const e = i[0], n = i[1], s = i[2], r = i[3], o = i[4], a = i[5], l = t[0], h = t[1], c = t[2], u = t[3], d = t[4], f = t[5];
  return i[0] = e * l + s * h, i[1] = n * l + r * h, i[2] = e * c + s * u, i[3] = n * c + r * u, i[4] = e * d + s * f + o, i[5] = n * d + r * f + a, i;
}
function f0(i, t, e, n, s, r, o) {
  return i[0] = t, i[1] = e, i[2] = n, i[3] = s, i[4] = r, i[5] = o, i;
}
function g0(i, t) {
  return i[0] = t[0], i[1] = t[1], i[2] = t[2], i[3] = t[3], i[4] = t[4], i[5] = t[5], i;
}
function Ft(i, t) {
  const e = t[0], n = t[1];
  return t[0] = i[0] * e + i[2] * n + i[4], t[1] = i[1] * e + i[3] * n + i[5], t;
}
function m0(i, t, e) {
  return f0(i, t, 0, 0, e, 0, 0);
}
function _i(i, t, e, n, s, r, o, a) {
  const l = Math.sin(r), h = Math.cos(r);
  return i[0] = n * h, i[1] = s * l, i[2] = -n * l, i[3] = s * h, i[4] = o * n * h - a * n * l + t, i[5] = o * s * l + a * s * h + e, i;
}
function qa(i, t) {
  const e = p0(t);
  Y(e !== 0, 32);
  const n = t[0], s = t[1], r = t[2], o = t[3], a = t[4], l = t[5];
  return i[0] = o / e, i[1] = -s / e, i[2] = -r / e, i[3] = n / e, i[4] = (r * l - o * a) / e, i[5] = -(n * l - s * a) / e, i;
}
function p0(i) {
  return i[0] * i[3] - i[1] * i[2];
}
let mh;
function wu(i) {
  const t = "matrix(" + i.join(", ") + ")";
  if (Ja)
    return t;
  const e = mh || (mh = document.createElement("div"));
  return e.style.transform = t, e.style.transform;
}
const zt = {
  UNKNOWN: 0,
  INTERSECTING: 1,
  ABOVE: 2,
  RIGHT: 4,
  BELOW: 8,
  LEFT: 16
};
function la(i) {
  const t = fe();
  for (let e = 0, n = i.length; e < n; ++e)
    ys(t, i[e]);
  return t;
}
function v0(i, t, e) {
  const n = Math.min.apply(null, i), s = Math.min.apply(null, t), r = Math.max.apply(null, i), o = Math.max.apply(null, t);
  return Me(n, s, r, o, e);
}
function uo(i, t, e) {
  return e ? (e[0] = i[0] - t, e[1] = i[1] - t, e[2] = i[2] + t, e[3] = i[3] + t, e) : [
    i[0] - t,
    i[1] - t,
    i[2] + t,
    i[3] + t
  ];
}
function Eu(i, t) {
  return t ? (t[0] = i[0], t[1] = i[1], t[2] = i[2], t[3] = i[3], t) : i.slice();
}
function rn(i, t, e) {
  let n, s;
  return t < i[0] ? n = i[0] - t : i[2] < t ? n = t - i[2] : n = 0, e < i[1] ? s = i[1] - e : i[3] < e ? s = e - i[3] : s = 0, n * n + s * s;
}
function fo(i, t) {
  return Ka(i, t[0], t[1]);
}
function Mi(i, t) {
  return i[0] <= t[0] && t[2] <= i[2] && i[1] <= t[1] && t[3] <= i[3];
}
function Ka(i, t, e) {
  return i[0] <= t && t <= i[2] && i[1] <= e && e <= i[3];
}
function ha(i, t) {
  const e = i[0], n = i[1], s = i[2], r = i[3], o = t[0], a = t[1];
  let l = zt.UNKNOWN;
  return o < e ? l = l | zt.LEFT : o > s && (l = l | zt.RIGHT), a < n ? l = l | zt.BELOW : a > r && (l = l | zt.ABOVE), l === zt.UNKNOWN && (l = zt.INTERSECTING), l;
}
function fe() {
  return [1 / 0, 1 / 0, -1 / 0, -1 / 0];
}
function Me(i, t, e, n, s) {
  return s ? (s[0] = i, s[1] = t, s[2] = e, s[3] = n, s) : [i, t, e, n];
}
function Bs(i) {
  return Me(1 / 0, 1 / 0, -1 / 0, -1 / 0, i);
}
function bu(i, t) {
  const e = i[0], n = i[1];
  return Me(e, n, e, n, t);
}
function Pu(i, t, e, n, s) {
  const r = Bs(s);
  return _u(r, i, t, e, n);
}
function _s(i, t) {
  return i[0] == t[0] && i[2] == t[2] && i[1] == t[1] && i[3] == t[3];
}
function Su(i, t) {
  return t[0] < i[0] && (i[0] = t[0]), t[2] > i[2] && (i[2] = t[2]), t[1] < i[1] && (i[1] = t[1]), t[3] > i[3] && (i[3] = t[3]), i;
}
function ys(i, t) {
  t[0] < i[0] && (i[0] = t[0]), t[0] > i[2] && (i[2] = t[0]), t[1] < i[1] && (i[1] = t[1]), t[1] > i[3] && (i[3] = t[1]);
}
function _u(i, t, e, n, s) {
  for (; e < n; e += s)
    y0(i, t[e], t[e + 1]);
  return i;
}
function y0(i, t, e) {
  i[0] = Math.min(i[0], t), i[1] = Math.min(i[1], e), i[2] = Math.max(i[2], t), i[3] = Math.max(i[3], e);
}
function Ru(i, t) {
  let e;
  return e = t(go(i)), e || (e = t(mo(i)), e) || (e = t(po(i)), e) || (e = t(Ai(i)), e) ? e : !1;
}
function ca(i) {
  let t = 0;
  return Qa(i) || (t = mt(i) * je(i)), t;
}
function go(i) {
  return [i[0], i[1]];
}
function mo(i) {
  return [i[2], i[1]];
}
function Ri(i) {
  return [(i[0] + i[2]) / 2, (i[1] + i[3]) / 2];
}
function x0(i, t) {
  let e;
  return t === "bottom-left" ? e = go(i) : t === "bottom-right" ? e = mo(i) : t === "top-left" ? e = Ai(i) : t === "top-right" ? e = po(i) : Y(!1, 13), e;
}
function ua(i, t, e, n, s) {
  const [r, o, a, l, h, c, u, d] = da(
    i,
    t,
    e,
    n
  );
  return Me(
    Math.min(r, a, h, u),
    Math.min(o, l, c, d),
    Math.max(r, a, h, u),
    Math.max(o, l, c, d),
    s
  );
}
function da(i, t, e, n) {
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
function je(i) {
  return i[3] - i[1];
}
function xs(i, t, e) {
  const n = e || fe();
  return ie(i, t) ? (i[0] > t[0] ? n[0] = i[0] : n[0] = t[0], i[1] > t[1] ? n[1] = i[1] : n[1] = t[1], i[2] < t[2] ? n[2] = i[2] : n[2] = t[2], i[3] < t[3] ? n[3] = i[3] : n[3] = t[3]) : Bs(n), n;
}
function Ai(i) {
  return [i[0], i[3]];
}
function po(i) {
  return [i[2], i[3]];
}
function mt(i) {
  return i[2] - i[0];
}
function ie(i, t) {
  return i[0] <= t[2] && i[2] >= t[0] && i[1] <= t[3] && i[3] >= t[1];
}
function Qa(i) {
  return i[2] < i[0] || i[3] < i[1];
}
function M0(i, t) {
  return t ? (t[0] = i[0], t[1] = i[1], t[2] = i[2], t[3] = i[3], t) : i;
}
function C0(i, t, e) {
  let n = !1;
  const s = ha(i, t), r = ha(i, e);
  if (s === zt.INTERSECTING || r === zt.INTERSECTING)
    n = !0;
  else {
    const o = i[0], a = i[1], l = i[2], h = i[3], c = t[0], u = t[1], d = e[0], f = e[1], g = (f - u) / (d - c);
    let m, p;
    !!(r & zt.ABOVE) && !(s & zt.ABOVE) && (m = d - (f - h) / g, n = m >= o && m <= l), !n && !!(r & zt.RIGHT) && !(s & zt.RIGHT) && (p = f - (d - l) * g, n = p >= a && p <= h), !n && !!(r & zt.BELOW) && !(s & zt.BELOW) && (m = d - (f - a) / g, n = m >= o && m <= l), !n && !!(r & zt.LEFT) && !(s & zt.LEFT) && (p = f - (d - o) * g, n = p >= a && p <= h);
  }
  return n;
}
function w0(i, t, e, n) {
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
  return v0(r, o, e);
}
function Tu(i, t) {
  const e = t.getExtent(), n = Ri(i);
  if (t.canWrapX() && (n[0] < e[0] || n[0] >= e[2])) {
    const s = mt(e), o = Math.floor(
      (n[0] - e[0]) / s
    ) * s;
    i[0] -= o, i[2] -= o;
  }
  return i;
}
function E0(i, t) {
  if (t.canWrapX()) {
    const e = t.getExtent();
    if (!isFinite(i[0]) || !isFinite(i[2]))
      return [[e[0], i[1], e[2], i[3]]];
    Tu(i, t);
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
function Pt(i, t, e) {
  return Math.min(Math.max(i, t), e);
}
function b0(i, t, e, n, s, r) {
  const o = s - e, a = r - n;
  if (o !== 0 || a !== 0) {
    const l = ((i - e) * o + (t - n) * a) / (o * o + a * a);
    l > 1 ? (e = s, n = r) : l > 0 && (e += o * l, n += a * l);
  }
  return Wi(i, t, e, n);
}
function Wi(i, t, e, n) {
  const s = e - i, r = n - t;
  return s * s + r * r;
}
function P0(i) {
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
function ph(i) {
  return i * 180 / Math.PI;
}
function Vi(i) {
  return i * Math.PI / 180;
}
function An(i, t) {
  const e = i % t;
  return e * t < 0 ? e + t : e;
}
function ti(i, t, e) {
  return i + e * (t - i);
}
function Lu(i, t) {
  const e = Math.pow(10, t);
  return Math.round(i * e) / e;
}
function gr(i, t) {
  return Math.floor(Lu(i, t));
}
function mr(i, t) {
  return Math.ceil(Lu(i, t));
}
const S0 = /^#([a-f0-9]{3}|[a-f0-9]{4}(?:[a-f0-9]{2}){0,2})$/i, _0 = /^([a-z]*)$|^hsla?\(.*\)$/i;
function Ou(i) {
  return typeof i == "string" ? i : Au(i);
}
function R0(i) {
  const t = document.createElement("div");
  if (t.style.color = i, t.style.color !== "") {
    document.body.appendChild(t);
    const e = getComputedStyle(t).color;
    return document.body.removeChild(t), e;
  } else
    return "";
}
const T0 = function() {
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
      s = L0(n), t[n] = s, ++e;
    }
    return s;
  };
}();
function jr(i) {
  return Array.isArray(i) ? i : T0(i);
}
function L0(i) {
  let t, e, n, s, r;
  if (_0.exec(i) && (i = R0(i)), S0.exec(i)) {
    const o = i.length - 1;
    let a;
    o <= 4 ? a = 1 : a = 2;
    const l = o === 4 || o === 8;
    t = parseInt(i.substr(1 + 0 * a, a), 16), e = parseInt(i.substr(1 + 1 * a, a), 16), n = parseInt(i.substr(1 + 2 * a, a), 16), l ? s = parseInt(i.substr(1 + 3 * a, a), 16) : s = 255, a == 1 && (t = (t << 4) + t, e = (e << 4) + e, n = (n << 4) + n, l && (s = (s << 4) + s)), r = [t, e, n, s / 255];
  } else
    i.startsWith("rgba(") ? (r = i.slice(5, -1).split(",").map(Number), vh(r)) : i.startsWith("rgb(") ? (r = i.slice(4, -1).split(",").map(Number), r.push(1), vh(r)) : Y(!1, 14);
  return r;
}
function vh(i) {
  return i[0] = Pt(i[0] + 0.5 | 0, 0, 255), i[1] = Pt(i[1] + 0.5 | 0, 0, 255), i[2] = Pt(i[2] + 0.5 | 0, 0, 255), i[3] = Pt(i[3], 0, 1), i;
}
function Au(i) {
  let t = i[0];
  t != (t | 0) && (t = t + 0.5 | 0);
  let e = i[1];
  e != (e | 0) && (e = e + 0.5 | 0);
  let n = i[2];
  n != (n | 0) && (n = n + 0.5 | 0);
  const s = i[3] === void 0 ? 1 : Math.round(i[3] * 100) / 100;
  return "rgba(" + t + "," + e + "," + n + "," + s + ")";
}
class O0 {
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
    const s = yh(t, e, n);
    return s in this.cache_ ? this.cache_[s] : null;
  }
  set(t, e, n, s) {
    const r = yh(t, e, n);
    this.cache_[r] = s, ++this.cacheSize_;
  }
  setSize(t) {
    this.maxCacheSize_ = t, this.expire();
  }
}
function yh(i, t, e) {
  const n = e ? Ou(e) : "null";
  return t + ":" + i + ":" + n;
}
const kr = new O0(), ut = {
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
class A0 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, this.background_ = t.background;
    const e = Object.assign({}, t);
    typeof t.properties == "object" && (delete e.properties, Object.assign(e, t.properties)), e[ut.OPACITY] = t.opacity !== void 0 ? t.opacity : 1, Y(typeof e[ut.OPACITY] == "number", 64), e[ut.VISIBLE] = t.visible !== void 0 ? t.visible : !0, e[ut.Z_INDEX] = t.zIndex, e[ut.MAX_RESOLUTION] = t.maxResolution !== void 0 ? t.maxResolution : 1 / 0, e[ut.MIN_RESOLUTION] = t.minResolution !== void 0 ? t.minResolution : 0, e[ut.MIN_ZOOM] = t.minZoom !== void 0 ? t.minZoom : -1 / 0, e[ut.MAX_ZOOM] = t.maxZoom !== void 0 ? t.maxZoom : 1 / 0, this.className_ = e.className !== void 0 ? e.className : "ol-layer", delete e.className, this.setProperties(e), this.state_ = null;
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
    return e.opacity = Pt(Math.round(this.getOpacity() * 100) / 100, 0, 1), e.visible = this.getVisible(), e.extent = this.getExtent(), e.zIndex = n === void 0 && !e.managed ? 1 / 0 : n, e.maxResolution = this.getMaxResolution(), e.minResolution = Math.max(this.getMinResolution(), 0), e.minZoom = this.getMinZoom(), e.maxZoom = this.getMaxZoom(), this.state_ = e, e;
  }
  getLayersArray(t) {
    return B();
  }
  getLayerStatesArray(t) {
    return B();
  }
  getExtent() {
    return this.get(ut.EXTENT);
  }
  getMaxResolution() {
    return this.get(ut.MAX_RESOLUTION);
  }
  getMinResolution() {
    return this.get(ut.MIN_RESOLUTION);
  }
  getMinZoom() {
    return this.get(ut.MIN_ZOOM);
  }
  getMaxZoom() {
    return this.get(ut.MAX_ZOOM);
  }
  getOpacity() {
    return this.get(ut.OPACITY);
  }
  getSourceState() {
    return B();
  }
  getVisible() {
    return this.get(ut.VISIBLE);
  }
  getZIndex() {
    return this.get(ut.Z_INDEX);
  }
  setBackground(t) {
    this.background_ = t, this.changed();
  }
  setExtent(t) {
    this.set(ut.EXTENT, t);
  }
  setMaxResolution(t) {
    this.set(ut.MAX_RESOLUTION, t);
  }
  setMinResolution(t) {
    this.set(ut.MIN_RESOLUTION, t);
  }
  setMaxZoom(t) {
    this.set(ut.MAX_ZOOM, t);
  }
  setMinZoom(t) {
    this.set(ut.MIN_ZOOM, t);
  }
  setOpacity(t) {
    Y(typeof t == "number", 64), this.set(ut.OPACITY, t);
  }
  setVisible(t) {
    this.set(ut.VISIBLE, t);
  }
  setZIndex(t) {
    this.set(ut.Z_INDEX, t);
  }
  disposeInternal() {
    this.state_ && (this.state_.layer = null, this.state_ = null), super.disposeInternal();
  }
}
const Iu = A0, Ei = {
  PRERENDER: "prerender",
  POSTRENDER: "postrender",
  PRECOMPOSE: "precompose",
  POSTCOMPOSE: "postcompose",
  RENDERCOMPLETE: "rendercomplete"
};
class I0 extends Iu {
  constructor(t) {
    const e = Object.assign({}, t);
    delete e.source, super(e), this.on, this.once, this.un, this.mapPrecomposeKey_ = null, this.mapRenderKey_ = null, this.sourceChangeKey_ = null, this.renderer_ = null, this.rendered = !1, t.render && (this.render = t.render), t.map && this.setMap(t.map), this.addChangeListener(
      ut.SOURCE,
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
    return this.get(ut.SOURCE) || null;
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
      V.CHANGE,
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
    t || this.unrender(), this.set(ut.MAP, t);
  }
  getMapInternal() {
    return this.get(ut.MAP);
  }
  setMap(t) {
    this.mapPrecomposeKey_ && (pt(this.mapPrecomposeKey_), this.mapPrecomposeKey_ = null), t || this.changed(), this.mapRenderKey_ && (pt(this.mapRenderKey_), this.mapRenderKey_ = null), t && (this.mapPrecomposeKey_ = et(
      t,
      Ei.PRECOMPOSE,
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
    ), this.mapRenderKey_ = et(this, V.CHANGE, t.render, t), this.changed());
  }
  setSource(t) {
    this.set(ut.SOURCE, t);
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
function $a(i, t) {
  if (!i.visible)
    return !1;
  const e = t.resolution;
  if (e < i.minResolution || e >= i.maxResolution)
    return !1;
  const n = t.zoom;
  return n > i.minZoom && n <= i.maxZoom;
}
const vo = I0;
function Nu(i, t) {
  return i[0] += +t[0], i[1] += +t[1], i;
}
function Xr(i, t) {
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
function zu(i, t) {
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
class N0 extends Ya {
  constructor(t) {
    super(), this.map_ = t;
  }
  dispatchRenderEvent(t, e) {
    B();
  }
  calculateMatrices2D(t) {
    const e = t.viewState, n = t.coordinateToPixelTransform, s = t.pixelToCoordinateTransform;
    _i(
      n,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / e.resolution,
      -1 / e.resolution,
      -e.rotation,
      -e.center[0],
      -e.center[1]
    ), qa(s, n);
  }
  forEachFeatureAtCoordinate(t, e, n, s, r, o, a, l) {
    let h;
    const c = e.viewState;
    function u(M, C, E, b) {
      return r.call(o, C, M ? E : null, b);
    }
    const d = c.projection, f = Fu(t.slice(), d), g = [[0, 0]];
    if (d.canWrapX() && s) {
      const M = d.getExtent(), C = mt(M);
      g.push([-C, 0], [C, 0]);
    }
    const m = e.layerStatesArray, p = m.length, v = [], y = [];
    for (let M = 0; M < g.length; M++)
      for (let C = p - 1; C >= 0; --C) {
        const E = m[C], b = E.layer;
        if (b.hasRenderer() && $a(E, c) && a.call(l, b)) {
          const S = b.getRenderer(), O = b.getSource();
          if (S && O) {
            const D = O.getWrapX() ? f : t, H = u.bind(
              null,
              E.managed
            );
            y[0] = D[0] + g[M][0], y[1] = D[1] + g[M][1], h = S.forEachFeatureAtCoordinate(
              y,
              e,
              n,
              H,
              v
            );
          }
          if (h)
            return h;
        }
      }
    if (v.length === 0)
      return;
    const x = 1 / v.length;
    return v.forEach((M, C) => M.distanceSq += C * x), v.sort((M, C) => M.distanceSq - C.distanceSq), v.some((M) => h = M.callback(M.feature, M.layer, M.geometry)), h;
  }
  hasFeatureAtCoordinate(t, e, n, s, r, o) {
    return this.forEachFeatureAtCoordinate(
      t,
      e,
      n,
      s,
      Ss,
      this,
      r,
      o
    ) !== void 0;
  }
  getMap() {
    return this.map_;
  }
  renderFrame(t) {
    B();
  }
  scheduleExpireIconCache(t) {
    kr.canExpireCache() && t.postRenderFunctions.push(z0);
  }
}
function z0(i, t) {
  kr.expire();
}
const F0 = N0;
class D0 extends Ge {
  constructor(t, e, n, s) {
    super(t), this.inversePixelTransform = e, this.frameState = n, this.context = s;
  }
}
const ju = D0, pr = "ol-hidden", j0 = "ol-selectable", Kn = "ol-unselectable", xh = "ol-unsupported", yo = "ol-control", Mh = "ol-collapsed", k0 = new RegExp(
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
), Ch = [
  "style",
  "variant",
  "weight",
  "size",
  "lineHeight",
  "family"
], ku = function(i) {
  const t = i.match(k0);
  if (!t)
    return null;
  const e = {
    lineHeight: "normal",
    size: "1.2em",
    style: "normal",
    weight: "normal",
    variant: "normal"
  };
  for (let n = 0, s = Ch.length; n < s; ++n) {
    const r = t[n + 1];
    r !== void 0 && (e[Ch[n]] = r);
  }
  return e.families = e.family.split(/,\s?/), e;
};
function ge(i, t, e, n) {
  let s;
  return e && e.length ? s = e.shift() : Ja ? s = new OffscreenCanvas(i || 300, t || 300) : s = document.createElement("canvas"), i && (s.width = i), t && (s.height = t), s.getContext("2d", n);
}
function Xu(i) {
  const t = i.canvas;
  t.width = 1, t.height = 1, i.clearRect(0, 0, 1, 1);
}
function X0(i) {
  let t = i.offsetWidth;
  const e = getComputedStyle(i);
  return t += parseInt(e.marginLeft, 10) + parseInt(e.marginRight, 10), t;
}
function G0(i) {
  let t = i.offsetHeight;
  const e = getComputedStyle(i);
  return t += parseInt(e.marginTop, 10) + parseInt(e.marginBottom, 10), t;
}
function Gr(i, t) {
  const e = t.parentNode;
  e && e.replaceChild(i, t);
}
function Hr(i) {
  return i && i.parentNode ? i.parentNode.removeChild(i) : null;
}
function Gu(i) {
  for (; i.lastChild; )
    i.removeChild(i.lastChild);
}
function H0(i, t) {
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
const Hu = "10px sans-serif", si = "#000", Zr = "round", Rs = [], Ts = 0, kn = "round", Ls = 10, Os = "#000", As = "center", Br = "middle", ki = [0, 0, 0, 0], Is = 1, Ke = new Ce();
let Mn = null, fa;
const ga = {}, Z0 = function() {
  const t = "32px ", e = ["monospace", "serif"], n = e.length, s = "wmytzilWMYTZIL@#/&?$%10\uF013";
  let r, o;
  function a(h, c, u) {
    let d = !0;
    for (let f = 0; f < n; ++f) {
      const g = e[f];
      if (o = Wr(
        h + " " + c + " " + t + g,
        s
      ), u != g) {
        const m = Wr(
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
    const c = Ke.getKeys();
    for (let u = 0, d = c.length; u < d; ++u) {
      const f = c[u];
      Ke.get(f) < 100 && (a.apply(this, f.split(`
`)) ? (Zs(ga), Mn = null, fa = void 0, Ke.set(f, 100)) : (Ke.set(f, Ke.get(f) + 1, !0), h = !1));
    }
    h && (clearInterval(r), r = void 0);
  }
  return function(h) {
    const c = ku(h);
    if (!c)
      return;
    const u = c.families;
    for (let d = 0, f = u.length; d < f; ++d) {
      const g = u[d], m = c.style + `
` + c.weight + `
` + g;
      Ke.get(m) === void 0 && (Ke.set(m, 100, !0), a(c.style, c.weight, g) || (Ke.set(m, 0, !0), r === void 0 && (r = setInterval(l, 32))));
    }
  };
}(), B0 = function() {
  let i;
  return function(t) {
    let e = ga[t];
    if (e == null) {
      if (Ja) {
        const n = ku(t), s = Zu(t, "\u017Dg");
        e = (isNaN(Number(n.lineHeight)) ? 1.2 : Number(n.lineHeight)) * (s.actualBoundingBoxAscent + s.actualBoundingBoxDescent);
      } else
        i || (i = document.createElement("div"), i.innerHTML = "M", i.style.minHeight = "0", i.style.maxHeight = "none", i.style.height = "auto", i.style.padding = "0", i.style.border = "none", i.style.position = "absolute", i.style.display = "block", i.style.left = "-99999px"), i.style.font = t, document.body.appendChild(i), e = i.offsetHeight, document.body.removeChild(i);
      ga[t] = e;
    }
    return e;
  };
}();
function Zu(i, t) {
  return Mn || (Mn = ge(1, 1)), i != fa && (Mn.font = i, fa = Mn.font), Mn.measureText(t);
}
function Wr(i, t) {
  return Zu(i, t).width;
}
function wh(i, t, e) {
  if (t in e)
    return e[t];
  const n = t.split(`
`).reduce((s, r) => Math.max(s, Wr(i, r)), 0);
  return e[t] = n, n;
}
function W0(i, t) {
  const e = [], n = [], s = [];
  let r = 0, o = 0, a = 0, l = 0;
  for (let h = 0, c = t.length; h <= c; h += 2) {
    const u = t[h];
    if (u === `
` || h === c) {
      r = Math.max(r, o), s.push(o), o = 0, a += l;
      continue;
    }
    const d = t[h + 1] || i.font, f = Wr(d, u);
    e.push(f), o += f;
    const g = B0(d);
    n.push(g), l = Math.max(l, g);
  }
  return { width: r, height: a, widths: e, heights: n, lineWidths: s };
}
function V0(i, t, e, n, s, r, o, a, l, h, c) {
  i.save(), e !== 1 && (i.globalAlpha *= e), t && i.setTransform.apply(i, t), n.contextInstructions ? (i.translate(l, h), i.scale(c[0], c[1]), Y0(n, i)) : c[0] < 0 || c[1] < 0 ? (i.translate(l, h), i.scale(c[0], c[1]), i.drawImage(
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
function Y0(i, t) {
  const e = i.contextInstructions;
  for (let n = 0, s = e.length; n < s; n += 2)
    Array.isArray(e[n + 1]) ? t[e[n]].apply(
      t,
      e[n + 1]
    ) : t[e[n]] = e[n + 1];
}
class U0 extends F0 {
  constructor(t) {
    super(t), this.fontChangeListenerKey_ = et(
      Ke,
      Dn.PROPERTYCHANGE,
      t.redrawText.bind(t)
    ), this.element_ = document.createElement("div");
    const e = this.element_.style;
    e.position = "absolute", e.width = "100%", e.height = "100%", e.zIndex = "0", this.element_.className = Kn + " ol-layers";
    const n = t.getViewport();
    n.insertBefore(this.element_, n.firstChild || null), this.children_ = [], this.renderedVisible_ = !0;
  }
  dispatchRenderEvent(t, e) {
    const n = this.getMap();
    if (n.hasListener(t)) {
      const s = new ju(t, void 0, e);
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
    this.calculateMatrices2D(t), this.dispatchRenderEvent(Ei.PRECOMPOSE, t);
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
      if (!$a(l, n) || c != "ready" && c != "undefined") {
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
    H0(this.element_, this.children_), this.dispatchRenderEvent(Ei.POSTCOMPOSE, t), this.renderedVisible_ || (this.element_.style.display = "", this.renderedVisible_ = !0), this.scheduleExpireIconCache(t);
  }
}
const J0 = U0;
class xi extends Ge {
  constructor(t, e) {
    super(t), this.layer = e;
  }
}
const Zo = {
  LAYERS: "layers"
};
class el extends Iu {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.layers;
    let n = t.layers;
    super(e), this.on, this.once, this.un, this.layersListenerKeys_ = [], this.listenerKeys_ = {}, this.addChangeListener(Zo.LAYERS, this.handleLayersChanged_), n ? Array.isArray(n) ? n = new Ie(n.slice(), { unique: !0 }) : Y(typeof n.getArray == "function", 43) : n = new Ie(void 0, { unique: !0 }), this.setLayers(n);
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
    Zs(this.listenerKeys_);
    const e = t.getArray();
    for (let n = 0, s = e.length; n < s; n++) {
      const r = e[n];
      this.registerLayerListeners_(r), this.dispatchEvent(new xi("addlayer", r));
    }
    this.changed();
  }
  registerLayerListeners_(t) {
    const e = [
      et(
        t,
        Dn.PROPERTYCHANGE,
        this.handleLayerChange_,
        this
      ),
      et(t, V.CHANGE, this.handleLayerChange_, this)
    ];
    t instanceof el && e.push(
      et(t, "addlayer", this.handleLayerGroupAdd_, this),
      et(t, "removelayer", this.handleLayerGroupRemove_, this)
    ), this.listenerKeys_[rt(t)] = e;
  }
  handleLayerGroupAdd_(t) {
    this.dispatchEvent(new xi("addlayer", t.layer));
  }
  handleLayerGroupRemove_(t) {
    this.dispatchEvent(new xi("removelayer", t.layer));
  }
  handleLayersAdd_(t) {
    const e = t.element;
    this.registerLayerListeners_(e), this.dispatchEvent(new xi("addlayer", e)), this.changed();
  }
  handleLayersRemove_(t) {
    const e = t.element, n = rt(e);
    this.listenerKeys_[n].forEach(pt), delete this.listenerKeys_[n], this.dispatchEvent(new xi("removelayer", e)), this.changed();
  }
  getLayers() {
    return this.get(Zo.LAYERS);
  }
  setLayers(t) {
    const e = this.getLayers();
    if (e) {
      const n = e.getArray();
      for (let s = 0, r = n.length; s < r; ++s)
        this.dispatchEvent(new xi("removelayer", n[s]));
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
      ), l.minZoom = Math.max(l.minZoom, s.minZoom), l.maxZoom = Math.min(l.maxZoom, s.maxZoom), s.extent !== void 0 && (l.extent !== void 0 ? l.extent = xs(
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
const xo = el;
class q0 extends Ge {
  constructor(t, e, n) {
    super(t), this.map = e, this.frameState = n !== void 0 ? n : null;
  }
}
const Cn = q0;
class K0 extends Cn {
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
const vi = K0, Et = {
  SINGLECLICK: "singleclick",
  CLICK: V.CLICK,
  DBLCLICK: V.DBLCLICK,
  POINTERDRAG: "pointerdrag",
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
}, ma = {
  POINTERMOVE: "pointermove",
  POINTERDOWN: "pointerdown",
  POINTERUP: "pointerup",
  POINTEROVER: "pointerover",
  POINTEROUT: "pointerout",
  POINTERENTER: "pointerenter",
  POINTERLEAVE: "pointerleave",
  POINTERCANCEL: "pointercancel"
};
class Q0 extends ho {
  constructor(t, e) {
    super(t), this.map_ = t, this.clickTimeoutId_, this.emulateClicks_ = !1, this.dragging_ = !1, this.dragListenerKeys_ = [], this.moveTolerance_ = e === void 0 ? 1 : e, this.down_ = null;
    const n = this.map_.getViewport();
    this.activePointers_ = [], this.trackedTouches_ = {}, this.element_ = n, this.pointerdownListenerKey_ = et(
      n,
      ma.POINTERDOWN,
      this.handlePointerDown_,
      this
    ), this.originalPointerMoveEvent_, this.relayedListenerKey_ = et(
      n,
      ma.POINTERMOVE,
      this.relayMoveEvent_,
      this
    ), this.boundHandleTouchMove_ = this.handleTouchMove_.bind(this), this.element_.addEventListener(
      V.TOUCHMOVE,
      this.boundHandleTouchMove_,
      Cu ? { passive: !1 } : !1
    );
  }
  emulateClick_(t) {
    let e = new vi(
      Et.CLICK,
      this.map_,
      t
    );
    this.dispatchEvent(e), this.clickTimeoutId_ !== void 0 ? (clearTimeout(this.clickTimeoutId_), this.clickTimeoutId_ = void 0, e = new vi(
      Et.DBLCLICK,
      this.map_,
      t
    ), this.dispatchEvent(e)) : this.clickTimeoutId_ = setTimeout(
      function() {
        this.clickTimeoutId_ = void 0;
        const n = new vi(
          Et.SINGLECLICK,
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
    if (e.type == Et.POINTERUP || e.type == Et.POINTERCANCEL) {
      delete this.trackedTouches_[n];
      for (const s in this.trackedTouches_)
        if (this.trackedTouches_[s].target !== e.target) {
          delete this.trackedTouches_[s];
          break;
        }
    } else
      (e.type == Et.POINTERDOWN || e.type == Et.POINTERMOVE) && (this.trackedTouches_[n] = e);
    this.activePointers_ = Object.values(this.trackedTouches_);
  }
  handlePointerUp_(t) {
    this.updateActivePointers_(t);
    const e = new vi(
      Et.POINTERUP,
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
    const e = new vi(
      Et.POINTERDOWN,
      this.map_,
      t,
      void 0,
      void 0,
      this.activePointers_
    );
    this.dispatchEvent(e), this.down_ = {};
    for (const n in t) {
      const s = t[n];
      this.down_[n] = typeof s == "function" ? Ki : s;
    }
    if (this.dragListenerKeys_.length === 0) {
      const n = this.map_.getOwnerDocument();
      this.dragListenerKeys_.push(
        et(
          n,
          Et.POINTERMOVE,
          this.handlePointerMove_,
          this
        ),
        et(n, Et.POINTERUP, this.handlePointerUp_, this),
        et(
          this.element_,
          Et.POINTERCANCEL,
          this.handlePointerUp_,
          this
        )
      ), this.element_.getRootNode && this.element_.getRootNode() !== n && this.dragListenerKeys_.push(
        et(
          this.element_.getRootNode(),
          Et.POINTERUP,
          this.handlePointerUp_,
          this
        )
      );
    }
  }
  handlePointerMove_(t) {
    if (this.isMoving_(t)) {
      this.updateActivePointers_(t), this.dragging_ = !0;
      const e = new vi(
        Et.POINTERDRAG,
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
      new vi(
        Et.POINTERMOVE,
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
      V.TOUCHMOVE,
      this.boundHandleTouchMove_
    ), this.pointerdownListenerKey_ && (pt(this.pointerdownListenerKey_), this.pointerdownListenerKey_ = null), this.dragListenerKeys_.forEach(pt), this.dragListenerKeys_.length = 0, this.element_ = null, super.disposeInternal();
  }
}
const $0 = Q0, $e = {
  POSTRENDER: "postrender",
  MOVESTART: "movestart",
  MOVEEND: "moveend",
  LOADSTART: "loadstart",
  LOADEND: "loadend"
}, Nt = {
  LAYERGROUP: "layergroup",
  SIZE: "size",
  TARGET: "target",
  VIEW: "view"
}, Vr = 1 / 0;
class tg {
  constructor(t, e) {
    this.priorityFunction_ = t, this.keyFunction_ = e, this.elements_ = [], this.priorities_ = [], this.queuedElements_ = {};
  }
  clear() {
    this.elements_.length = 0, this.priorities_.length = 0, Zs(this.queuedElements_);
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
    return e != Vr ? (this.elements_.push(t), this.priorities_.push(e), this.queuedElements_[this.keyFunction_(t)] = !0, this.siftDown_(0, this.elements_.length - 1), !0) : !1;
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
      o = e[a], l = t(o), l == Vr ? delete this.queuedElements_[this.keyFunction_(o)] : (n[s] = l, e[s++] = o);
    e.length = s, n.length = s, this.heapify_();
  }
}
const eg = tg, X = {
  IDLE: 0,
  LOADING: 1,
  LOADED: 2,
  ERROR: 3,
  EMPTY: 4
};
class ig extends eg {
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
    return e && t[0].addEventListener(V.CHANGE, this.boundHandleTileChange_), e;
  }
  getTilesLoading() {
    return this.tilesLoading_;
  }
  handleTileChange(t) {
    const e = t.target, n = e.getState();
    if (n === X.LOADED || n === X.ERROR || n === X.EMPTY) {
      n !== X.ERROR && e.removeEventListener(V.CHANGE, this.boundHandleTileChange_);
      const s = e.getKey();
      s in this.tilesLoadingKeys_ && (delete this.tilesLoadingKeys_[s], --this.tilesLoading_), this.tileChangeCallback_();
    }
  }
  loadMoreTiles(t, e) {
    let n = 0, s, r, o;
    for (; this.tilesLoading_ < t && n < e && this.getCount() > 0; )
      r = this.dequeue()[0], o = r.getKey(), s = r.getState(), s === X.IDLE && !(o in this.tilesLoadingKeys_) && (this.tilesLoadingKeys_[o] = !0, ++this.tilesLoading_, ++n, r.load());
  }
}
const ng = ig;
function sg(i, t, e, n, s) {
  if (!i || !(e in i.wantedTiles) || !i.wantedTiles[e][t.getKey()])
    return Vr;
  const r = i.viewState.center, o = n[0] - r[0], a = n[1] - r[1];
  return 65536 * Math.log(s) + Math.sqrt(o * o + a * a) / s;
}
const Ht = {
  ANIMATING: 0,
  INTERACTING: 1
}, Ee = {
  CENTER: "center",
  RESOLUTION: "resolution",
  ROTATION: "rotation"
}, rg = 42, il = 256, Xn = {
  radians: 6370997 / (2 * Math.PI),
  degrees: 2 * Math.PI * 6370997 / 360,
  ft: 0.3048,
  m: 1,
  "us-ft": 1200 / 3937
};
class og {
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
    return this.metersPerUnit_ || Xn[this.units_];
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
const nl = og, Ws = 6378137, Pn = Math.PI * Ws, ag = [-Pn, -Pn, Pn, Pn], lg = [-180, -85, 180, 85], vr = Ws * Math.log(Math.tan(Math.PI / 2));
class gn extends nl {
  constructor(t) {
    super({
      code: t,
      units: "m",
      extent: ag,
      global: !0,
      worldExtent: lg,
      getPointResolution: function(e, n) {
        return e / Math.cosh(n[1] / Ws);
      }
    });
  }
}
const Eh = [
  new gn("EPSG:3857"),
  new gn("EPSG:102100"),
  new gn("EPSG:102113"),
  new gn("EPSG:900913"),
  new gn("http://www.opengis.net/def/crs/EPSG/0/3857"),
  new gn("http://www.opengis.net/gml/srs/epsg.xml#3857")
];
function hg(i, t, e) {
  const n = i.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = i.slice() : t = new Array(n));
  for (let s = 0; s < n; s += e) {
    t[s] = Pn * i[s] / 180;
    let r = Ws * Math.log(Math.tan(Math.PI * (+i[s + 1] + 90) / 360));
    r > vr ? r = vr : r < -vr && (r = -vr), t[s + 1] = r;
  }
  return t;
}
function cg(i, t, e) {
  const n = i.length;
  e = e > 1 ? e : 2, t === void 0 && (e > 2 ? t = i.slice() : t = new Array(n));
  for (let s = 0; s < n; s += e)
    t[s] = 180 * i[s] / Pn, t[s + 1] = 360 * Math.atan(Math.exp(i[s + 1] / Ws)) / Math.PI - 90;
  return t;
}
const ug = 6378137, bh = [-180, -90, 180, 90], dg = Math.PI * ug / 180;
class Fi extends nl {
  constructor(t, e) {
    super({
      code: t,
      units: "degrees",
      extent: bh,
      axisOrientation: e,
      global: !0,
      metersPerUnit: dg,
      worldExtent: bh
    });
  }
}
const Ph = [
  new Fi("CRS:84"),
  new Fi("EPSG:4326", "neu"),
  new Fi("urn:ogc:def:crs:OGC:1.3:CRS84"),
  new Fi("urn:ogc:def:crs:OGC:2:84"),
  new Fi("http://www.opengis.net/def/crs/OGC/1.3/CRS84"),
  new Fi("http://www.opengis.net/gml/srs/epsg.xml#4326", "neu"),
  new Fi("http://www.opengis.net/def/crs/EPSG/0/4326", "neu")
];
let pa = {};
function fg(i) {
  return pa[i] || pa[i.replace(/urn:(x-)?ogc:def:crs:EPSG:(.*:)?(\w+)$/, "EPSG:$3")] || null;
}
function gg(i, t) {
  pa[i] = t;
}
let In = {};
function Gn(i, t, e) {
  const n = i.getCode(), s = t.getCode();
  n in In || (In[n] = {}), In[n][s] = e;
}
function Bu(i, t) {
  let e;
  return i in In && t in In[i] && (e = In[i][t]), e;
}
const Wu = 63710088e-1;
function Sh(i, t, e) {
  e = e || Wu;
  const n = Vi(i[1]), s = Vi(t[1]), r = (s - n) / 2, o = Vi(t[0] - i[0]) / 2, a = Math.sin(r) * Math.sin(r) + Math.sin(o) * Math.sin(o) * Math.cos(n) * Math.cos(s);
  return 2 * e * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
function mg(i, t, e, n) {
  n = n || Wu;
  const s = Vi(i[1]), r = Vi(i[0]), o = t / n, a = Math.asin(
    Math.sin(s) * Math.cos(o) + Math.cos(s) * Math.sin(o) * Math.cos(e)
  ), l = r + Math.atan2(
    Math.sin(e) * Math.sin(o) * Math.cos(s),
    Math.cos(o) - Math.sin(s) * Math.sin(a)
  );
  return [ph(l), ph(a)];
}
let va = !0;
function Vu(i) {
  va = !(i === void 0 ? !0 : i);
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
function Yu(i) {
  gg(i.getCode(), i), Gn(i, i, sl);
}
function pg(i) {
  i.forEach(Yu);
}
function K(i) {
  return typeof i == "string" ? fg(i) : i || null;
}
function Yr(i, t, e, n) {
  i = K(i);
  let s;
  const r = i.getPointResolutionFunc();
  if (r) {
    if (s = r(t, e), n && n !== i.getUnits()) {
      const o = i.getMetersPerUnit();
      o && (s = s * o / Xn[n]);
    }
  } else {
    const o = i.getUnits();
    if (o == "degrees" && !n || n == "degrees")
      s = t;
    else {
      const a = Mo(
        i,
        K("EPSG:4326")
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
      const l = n ? Xn[n] : i.getMetersPerUnit();
      l !== void 0 && (s /= l);
    }
  }
  return s;
}
function ya(i) {
  pg(i), i.forEach(function(t) {
    i.forEach(function(e) {
      t !== e && Gn(t, e, sl);
    });
  });
}
function vg(i, t, e, n) {
  i.forEach(function(s) {
    t.forEach(function(r) {
      Gn(s, r, e), Gn(r, s, n);
    });
  });
}
function ol(i, t) {
  return i ? typeof i == "string" ? K(i) : i : K(t);
}
function _h(i) {
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
function yg(i, t, e, n) {
  const s = K(i), r = K(t);
  Gn(
    s,
    r,
    _h(e)
  ), Gn(
    r,
    s,
    _h(n)
  );
}
function xg(i, t) {
  return Vu(), Uu(
    i,
    "EPSG:4326",
    t !== void 0 ? t : "EPSG:3857"
  );
}
function Oe(i, t) {
  if (i === t)
    return !0;
  const e = i.getUnits() === t.getUnits();
  return (i.getCode() === t.getCode() || Mo(i, t) === sl) && e;
}
function Mo(i, t) {
  const e = i.getCode(), n = t.getCode();
  let s = Bu(e, n);
  return s || (s = rl), s;
}
function Ns(i, t) {
  const e = K(i), n = K(t);
  return Mo(e, n);
}
function Uu(i, t, e) {
  return Ns(t, e)(i, void 0, i.length);
}
function Ju(i, t, e, n) {
  const s = Ns(t, e);
  return w0(i, s, void 0, n);
}
function xa(i, t) {
  return i;
}
function Qe(i, t) {
  return va && !Xr(i, [0, 0]) && i[0] >= -180 && i[0] <= 180 && i[1] >= -90 && i[1] <= 90 && (va = !1, console.warn(
    "Call useGeographic() from ol/proj once to work with [longitude, latitude] coordinates."
  )), i;
}
function qu(i, t) {
  return i;
}
function Xi(i, t) {
  return i;
}
function Rh(i, t, e) {
  return function(n) {
    let s, r;
    if (i.canWrapX()) {
      const o = i.getExtent(), a = mt(o);
      n = n.slice(0), r = Du(n, i, a), r && (n[0] = n[0] - r * a), n[0] = Pt(n[0], o[0], o[2]), n[1] = Pt(n[1], o[1], o[3]), s = e(n);
    } else
      s = e(n);
    return r && t.canWrapX() && (s[0] += r * mt(t.getExtent())), s;
  };
}
function Mg() {
  ya(Eh), ya(Ph), vg(
    Ph,
    Eh,
    hg,
    cg
  );
}
Mg();
function Th(i, t, e) {
  return function(n, s, r, o, a) {
    if (!n)
      return;
    if (!s && !t)
      return n;
    const l = t ? 0 : r[0] * s, h = t ? 0 : r[1] * s, c = a ? a[0] : 0, u = a ? a[1] : 0;
    let d = i[0] + l / 2 + c, f = i[2] - l / 2 + c, g = i[1] + h / 2 + u, m = i[3] - h / 2 + u;
    d > f && (d = (f + d) / 2, f = d), g > m && (g = (m + g) / 2, m = g);
    let p = Pt(n[0], d, f), v = Pt(n[1], g, m);
    if (o && e && s) {
      const y = 30 * s;
      p += -y * Math.log(1 + Math.max(0, d - n[0]) / y) + y * Math.log(1 + Math.max(0, n[0] - f) / y), v += -y * Math.log(1 + Math.max(0, g - n[1]) / y) + y * Math.log(1 + Math.max(0, n[1] - m) / y);
    }
    return [p, v];
  };
}
function Cg(i) {
  return i;
}
function al(i, t, e, n) {
  const s = mt(t) / e[0], r = je(t) / e[1];
  return n ? Math.min(i, Math.max(s, r)) : Math.min(i, Math.min(s, r));
}
function ll(i, t, e) {
  let n = Math.min(i, t);
  const s = 50;
  return n *= Math.log(1 + s * Math.max(0, i / t - 1)) / s + 1, e && (n = Math.max(n, e), n /= Math.log(1 + s * Math.max(0, e / i - 1)) / s + 1), Pt(n, e / 2, t * 2);
}
function wg(i, t, e, n) {
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
        ) : Pt(s, h, c);
      const u = Math.min(c, s), d = Math.floor(Ua(i, u, r));
      return i[d] > c && d < i.length - 1 ? i[d + 1] : i[d];
    } else
      return;
  };
}
function Eg(i, t, e, n, s, r) {
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
        ) : Pt(o, e, c);
      const u = 1e-9, d = Math.ceil(
        Math.log(t / c) / Math.log(i) - u
      ), f = -a * (0.5 - u) + 0.5, g = Math.min(c, o), m = Math.floor(
        Math.log(t / g) / Math.log(i) + f
      ), p = Math.max(d, m), v = t / Math.pow(i, p);
      return Pt(v, e, c);
    } else
      return;
  };
}
function Lh(i, t, e, n, s) {
  return e = e !== void 0 ? e : !0, function(r, o, a, l) {
    if (r !== void 0) {
      const h = n ? al(
        i,
        n,
        a,
        s
      ) : i;
      return !e || !l ? Pt(r, t, h) : ll(
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
function Oh(i) {
  if (i !== void 0)
    return i;
}
function bg(i) {
  const t = 2 * Math.PI / i;
  return function(e, n) {
    if (n)
      return e;
    if (e !== void 0)
      return e = Math.floor(e / t + 0.5) * t, e;
  };
}
function Pg(i) {
  return i = i || Vi(5), function(t, e) {
    if (e)
      return t;
    if (t !== void 0)
      return Math.abs(t) <= i ? 0 : t;
  };
}
function Ku(i) {
  return Math.pow(i, 3);
}
function Qn(i) {
  return 1 - Ku(1 - i);
}
function Sg(i) {
  return 3 * i * i - 2 * i * i * i;
}
function _g(i) {
  return i;
}
function Yi(i, t, e, n, s, r) {
  r = r || [];
  let o = 0;
  for (let a = t; a < e; a += n) {
    const l = i[a], h = i[a + 1];
    r[o++] = s[0] * l + s[2] * h + s[4], r[o++] = s[1] * l + s[3] * h + s[5];
  }
  return r && r.length != o && (r.length = o), r;
}
function Qu(i, t, e, n, s, r, o) {
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
function Rg(i, t, e, n, s, r, o, a) {
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
function Tg(i, t, e, n, s, r, o) {
  o = o || [];
  let a = 0;
  for (let l = t; l < e; l += n) {
    o[a++] = i[l] + s, o[a++] = i[l + 1] + r;
    for (let h = l + 2; h < l + n; ++h)
      o[a++] = i[h];
  }
  return o && o.length != a && (o.length = a), o;
}
const Ah = Fe();
class Lg extends Ce {
  constructor() {
    super(), this.extent_ = fe(), this.extentRevision_ = -1, this.simplifiedGeometryMaxMinSquaredTolerance = 0, this.simplifiedGeometryRevision = 0, this.simplifyTransformedInternal = $f(function(t, e, n) {
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
    return B();
  }
  closestPointXY(t, e, n, s) {
    return B();
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
    return B();
  }
  getExtent(t) {
    if (this.extentRevision_ != this.getRevision()) {
      const e = this.computeExtent(this.extent_);
      (isNaN(e[0]) || isNaN(e[1])) && Bs(e), this.extentRevision_ = this.getRevision();
    }
    return M0(this.extent_, t);
  }
  rotate(t, e) {
    B();
  }
  scale(t, e, n) {
    B();
  }
  simplify(t) {
    return this.getSimplifiedGeometry(t * t);
  }
  getSimplifiedGeometry(t) {
    return B();
  }
  getType() {
    return B();
  }
  applyTransform(t) {
    B();
  }
  intersectsExtent(t) {
    return B();
  }
  translate(t, e) {
    B();
  }
  transform(t, e) {
    const n = K(t), s = n.getUnits() == "tile-pixels" ? function(r, o, a) {
      const l = n.getExtent(), h = n.getWorldExtent(), c = je(h) / je(l);
      return _i(
        Ah,
        h[0],
        h[3],
        c,
        -c,
        0,
        0,
        0
      ), Yi(
        r,
        0,
        r.length,
        a,
        Ah,
        o
      ), Ns(n, e)(
        r,
        o,
        a
      );
    } : Ns(n, e);
    return this.applyTransform(s), this;
  }
}
const $u = Lg;
class Og extends $u {
  constructor() {
    super(), this.layout = "XY", this.stride = 2, this.flatCoordinates = null;
  }
  computeExtent(t) {
    return Pu(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinates() {
    return B();
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
    this.stride = Ih(t), this.layout = t, this.flatCoordinates = e;
  }
  setCoordinates(t, e) {
    B();
  }
  setLayout(t, e, n) {
    let s;
    if (t)
      s = Ih(t);
    else {
      for (let r = 0; r < n; ++r)
        if (e.length === 0) {
          this.layout = "XY", this.stride = 2;
          return;
        } else
          e = e[0];
      s = e.length, t = Ag(s);
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
      Qu(
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
      Rg(
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
      Tg(
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
function Ag(i) {
  let t;
  return i == 2 ? t = "XY" : i == 3 ? t = "XYZ" : i == 4 && (t = "XYZM"), t;
}
function Ih(i) {
  let t;
  return i == "XY" ? t = 2 : i == "XYZ" || i == "XYM" ? t = 3 : i == "XYZM" && (t = 4), t;
}
function Ig(i, t, e) {
  const n = i.getFlatCoordinates();
  if (n) {
    const s = i.getStride();
    return Yi(
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
const on = Og;
function Nh(i, t, e, n, s, r, o) {
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
        o[f] = ti(
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
    const a = i[t], l = i[t + 1], h = Wi(r, o, a, l);
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
function Ng(i, t, e, n, s) {
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
    if (d = Wi(
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
    if (Nh(
      i,
      f - n,
      f,
      n,
      o,
      a,
      c
    ), d = Wi(o, a, c[0], c[1]), d < h) {
      for (h = d, u = 0; u < n; ++u)
        l[u] = c[u];
      l.length = n, f += n;
    } else
      f += n * Math.max(
        (Math.sqrt(d) - Math.sqrt(h)) / s | 0,
        1
      );
  if (r && (Nh(
    i,
    e - n,
    t,
    n,
    o,
    a,
    c
  ), d = Wi(o, a, c[0], c[1]), d < h)) {
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
function zg(i, t, e, n, s, r, o, a, l, h, c) {
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
function Fg(i, t, e, n) {
  for (let s = 0, r = e.length; s < r; ++s)
    i[t++] = e[s];
  return t;
}
function Co(i, t, e, n) {
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
    const l = Co(
      i,
      t,
      e[o],
      n
    );
    s[r++] = l, t = l;
  }
  return s.length = r, s;
}
function Dg(i, t, e, n, s) {
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
    const g = i[d], m = i[d + 1], p = i[u], v = i[u + 1];
    for (let y = d + n; y < u; y += n) {
      const x = i[y], M = i[y + 1], C = b0(x, M, g, m, p, v);
      C > f && (c = y, f = C);
    }
    f > s && (l[(c - t) / n] = 1, d + n < c && h.push(d, c), c + n < u && h.push(c, u));
  }
  for (let u = 0; u < a; ++u)
    l[u] && (r[o++] = i[t + u * n], r[o++] = i[t + u * n + 1]);
  return o;
}
function jg(i, t, e, n, s, r, o, a) {
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
function ji(i, t) {
  return t * Math.round(i / t);
}
function kg(i, t, e, n, s, r, o) {
  if (t == e)
    return o;
  let a = ji(i[t], s), l = ji(i[t + 1], s);
  t += n, r[o++] = a, r[o++] = l;
  let h, c;
  do
    if (h = ji(i[t], s), c = ji(i[t + 1], s), t += n, t == e)
      return r[o++] = h, r[o++] = c, o;
  while (h == a && c == l);
  for (; t < e; ) {
    const u = ji(i[t], s), d = ji(i[t + 1], s);
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
function td(i, t, e, n, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l];
    o = kg(
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
function Xg(i, t, e, n, s, r, o, a) {
  for (let l = 0, h = e.length; l < h; ++l) {
    const c = e[l], u = [];
    o = td(
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
function Ci(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = t; o < e; o += n)
    s[r++] = i.slice(o, o + n);
  return s.length = r, s;
}
function zs(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = Ci(
      i,
      t,
      l,
      n,
      s[r]
    ), t = l;
  }
  return s.length = r, s;
}
function Ma(i, t, e, n, s) {
  s = s !== void 0 ? s : [];
  let r = 0;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    s[r++] = l.length === 1 && l[0] === t ? [] : zs(
      i,
      t,
      l,
      n,
      s[r]
    ), t = l[l.length - 1];
  }
  return s.length = r, s;
}
function ed(i, t, e, n) {
  let s = 0, r = i[e - n], o = i[e - n + 1];
  for (; t < e; t += n) {
    const a = i[t], l = i[t + 1];
    s += o * a - r * l, r = a, o = l;
  }
  return s / 2;
}
function id(i, t, e, n) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += ed(i, t, a, n), t = a;
  }
  return s;
}
function Gg(i, t, e, n) {
  let s = 0;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    s += id(i, t, a, n), t = a[a.length - 1];
  }
  return s;
}
class Ur extends on {
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
    return new Ur(this.flatCoordinates.slice(), this.layout);
  }
  closestPointXY(t, e, n, s) {
    return s < rn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
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
    return ed(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinates() {
    return Ci(
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
    ), new Ur(e, "XY");
  }
  getType() {
    return "LinearRing";
  }
  intersectsExtent(t) {
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Co(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const Ca = Ur;
class pl extends on {
  constructor(t, e) {
    super(), this.setCoordinates(t, e);
  }
  clone() {
    const t = new pl(this.flatCoordinates.slice(), this.layout);
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    const r = this.flatCoordinates, o = Wi(
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
    return bu(this.flatCoordinates, t);
  }
  getType() {
    return "Point";
  }
  intersectsExtent(t) {
    return Ka(t, this.flatCoordinates[0], this.flatCoordinates[1]);
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 0), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Fg(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const oi = pl;
function Hg(i, t, e, n, s) {
  return !Ru(
    s,
    function(o) {
      return !Gi(
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
function Gi(i, t, e, n, s, r) {
  let o = 0, a = i[e - n], l = i[e - n + 1];
  for (; t < e; t += n) {
    const h = i[t], c = i[t + 1];
    l <= r ? c > r && (h - a) * (r - l) - (s - a) * (c - l) > 0 && o++ : c <= r && (h - a) * (r - l) - (s - a) * (c - l) < 0 && o--, a = h, l = c;
  }
  return o !== 0;
}
function vl(i, t, e, n, s, r) {
  if (e.length === 0 || !Gi(i, t, e[0], n, s, r))
    return !1;
  for (let o = 1, a = e.length; o < a; ++o)
    if (Gi(i, e[o - 1], e[o], n, s, r))
      return !1;
  return !0;
}
function Zg(i, t, e, n, s, r) {
  if (e.length === 0)
    return !1;
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    if (vl(i, t, l, n, s, r))
      return !0;
    t = l[l.length - 1];
  }
  return !1;
}
function nd(i, t, e, n, s, r, o) {
  let a, l, h, c, u, d, f;
  const g = s[r + 1], m = [];
  for (let y = 0, x = e.length; y < x; ++y) {
    const M = e[y];
    for (c = i[M - n], d = i[M - n + 1], a = t; a < M; a += n)
      u = i[a], f = i[a + 1], (g <= d && f <= g || d <= g && g <= f) && (h = (g - d) / (f - d) * (u - c) + c, m.push(h)), c = u, d = f;
  }
  let p = NaN, v = -1 / 0;
  for (m.sort(qi), c = m[0], a = 1, l = m.length; a < l; ++a) {
    u = m[a];
    const y = Math.abs(u - c);
    y > v && (h = (c + u) / 2, vl(i, t, e, n, h, g) && (p = h, v = y)), c = u;
  }
  return isNaN(p) && (p = s[r]), o ? (o.push(p, g, v), o) : [p, g, v];
}
function Bg(i, t, e, n, s) {
  let r = [];
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = nd(
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
function sd(i, t, e, n, s) {
  let r;
  for (t += n; t < e; t += n)
    if (r = s(
      i.slice(t - n, t),
      i.slice(t, t + n)
    ), r)
      return r;
  return !1;
}
function wo(i, t, e, n, s) {
  const r = _u(
    fe(),
    i,
    t,
    e,
    n
  );
  return ie(s, r) ? Mi(s, r) || r[0] >= s[0] && r[2] <= s[2] || r[1] >= s[1] && r[3] <= s[3] ? !0 : sd(
    i,
    t,
    e,
    n,
    function(o, a) {
      return C0(s, o, a);
    }
  ) : !1;
}
function Wg(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    if (wo(i, t, e[r], n, s))
      return !0;
    t = e[r];
  }
  return !1;
}
function rd(i, t, e, n, s) {
  return !!(wo(i, t, e, n, s) || Gi(
    i,
    t,
    e,
    n,
    s[0],
    s[1]
  ) || Gi(
    i,
    t,
    e,
    n,
    s[0],
    s[3]
  ) || Gi(
    i,
    t,
    e,
    n,
    s[2],
    s[1]
  ) || Gi(
    i,
    t,
    e,
    n,
    s[2],
    s[3]
  ));
}
function od(i, t, e, n, s) {
  if (!rd(i, t, e[0], n, s))
    return !1;
  if (e.length === 1)
    return !0;
  for (let r = 1, o = e.length; r < o; ++r)
    if (Hg(
      i,
      e[r - 1],
      e[r],
      n,
      s
    ) && !wo(
      i,
      e[r - 1],
      e[r],
      n,
      s
    ))
      return !1;
  return !0;
}
function Vg(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (od(i, t, a, n, s))
      return !0;
    t = a[a.length - 1];
  }
  return !1;
}
function Yg(i, t, e, n) {
  for (; t < e - n; ) {
    for (let s = 0; s < n; ++s) {
      const r = i[t + s];
      i[t + s] = i[e - n + s], i[e - n + s] = r;
    }
    t += n, e -= n;
  }
}
function ad(i, t, e, n) {
  let s = 0, r = i[e - n], o = i[e - n + 1];
  for (; t < e; t += n) {
    const a = i[t], l = i[t + 1];
    s += (a - r) * (l + o), r = a, o = l;
  }
  return s === 0 ? void 0 : s > 0;
}
function ld(i, t, e, n, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = ad(
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
function Ug(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r];
    if (!ld(i, t, a, n, s))
      return !1;
    a.length && (t = a[a.length - 1]);
  }
  return !0;
}
function wa(i, t, e, n, s) {
  s = s !== void 0 ? s : !1;
  for (let r = 0, o = e.length; r < o; ++r) {
    const a = e[r], l = ad(
      i,
      t,
      a,
      n
    );
    (r === 0 ? s && l || !s && !l : s && !l || !s && l) && Yg(i, t, a, n), t = a;
  }
  return t;
}
function zh(i, t, e, n, s) {
  for (let r = 0, o = e.length; r < o; ++r)
    t = wa(
      i,
      t,
      e[r],
      n,
      s
    );
  return t;
}
class Hn extends on {
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
    this.flatCoordinates ? qt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new Hn(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < rn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
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
    return vl(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return id(
      this.getOrientedFlatCoordinates(),
      0,
      this.ends_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), wa(e, 0, this.ends_, this.stride, t)) : e = this.flatCoordinates, zs(e, 0, this.ends_, this.stride);
  }
  getEnds() {
    return this.ends_;
  }
  getFlatInteriorPoint() {
    if (this.flatInteriorPointRevision_ != this.getRevision()) {
      const t = Ri(this.getExtent());
      this.flatInteriorPoint_ = nd(
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
    return new oi(this.getFlatInteriorPoint(), "XYM");
  }
  getLinearRingCount() {
    return this.ends_.length;
  }
  getLinearRing(t) {
    return t < 0 || this.ends_.length <= t ? null : new Ca(
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
      const l = n[o], h = new Ca(
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
      ld(t, 0, this.ends_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = wa(
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
    return e.length = td(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      Math.sqrt(t),
      e,
      0,
      n
    ), new Hn(e, "XY", n);
  }
  getType() {
    return "Polygon";
  }
  intersectsExtent(t) {
    return od(
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
const Zn = Hn;
function Jg(i, t, e, n) {
  e = e || 32;
  const s = [];
  for (let r = 0; r < e; ++r)
    qt(
      s,
      mg(i, t, 2 * Math.PI * r / e, n)
    );
  return s.push(s[0], s[1]), new Hn(s, "XY", [s.length]);
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
  return new Hn(r, "XY", [r.length]);
}
const Bo = 0;
class qg extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, t = Object.assign({}, t), this.hints_ = [0, 0], this.animations_ = [], this.updateAnimationKey_, this.projection_ = ol(t.projection, "EPSG:3857"), this.viewportSize_ = [100, 100], this.targetCenter_ = null, this.targetResolution_, this.targetRotation_, this.nextCenter_ = null, this.nextResolution_, this.nextRotation_, this.cancelAnchor_ = void 0, t.projection && Vu(), t.center && (t.center = Qe(t.center, this.projection_)), t.extent && (t.extent = Xi(t.extent, this.projection_)), this.applyOptions_(t);
  }
  applyOptions_(t) {
    const e = Object.assign({}, t);
    for (const a in Ee)
      delete e[a];
    this.setProperties(e, !0);
    const n = Qg(t);
    this.maxResolution_ = n.maxResolution, this.minResolution_ = n.minResolution, this.zoomFactor_ = n.zoomFactor, this.resolutions_ = t.resolutions, this.padding_ = t.padding, this.minZoom_ = n.minZoom;
    const s = Kg(t), r = n.constraint, o = $g(t);
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
      s.center && (s = Object.assign({}, s), s.center = Qe(
        s.center,
        this.getProjection()
      )), s.anchor && (s = Object.assign({}, s), s.anchor = Qe(
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
      n && yr(n, !0);
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
        easing: c.easing || Sg,
        callback: n
      };
      if (c.center && (u.sourceCenter = o, u.targetCenter = c.center.slice(), o = u.targetCenter), c.zoom !== void 0 ? (u.sourceResolution = a, u.targetResolution = this.getResolutionForZoom(c.zoom), a = u.targetResolution) : c.resolution && (u.sourceResolution = a, u.targetResolution = c.resolution, a = u.targetResolution), c.rotation !== void 0) {
        u.sourceRotation = l;
        const d = An(c.rotation - l + Math.PI, 2 * Math.PI) - Math.PI;
        u.targetRotation = l + d, l = u.targetRotation;
      }
      t1(u) ? u.complete = !0 : r += u.duration, h.push(u);
    }
    this.animations_.push(h), this.setHint(Ht.ANIMATING, 1), this.updateAnimations_();
  }
  getAnimating() {
    return this.hints_[Ht.ANIMATING] > 0;
  }
  getInteracting() {
    return this.hints_[Ht.INTERACTING] > 0;
  }
  cancelAnimations() {
    this.setHint(Ht.ANIMATING, -this.hints_[Ht.ANIMATING]);
    let t;
    for (let e = 0, n = this.animations_.length; e < n; ++e) {
      const s = this.animations_[e];
      if (s[0].callback && yr(s[0].callback, !1), !t)
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
          const p = d + u * (g - d), v = f + u * (m - f);
          this.targetCenter_ = [p, v];
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
        this.animations_[n] = null, this.setHint(Ht.ANIMATING, -1), this.nextCenter_ = null, this.nextResolution_ = NaN, this.nextRotation_ = NaN;
        const o = s[0].callback;
        o && yr(o, !0);
      }
    }
    this.animations_ = this.animations_.filter(Boolean), e && this.updateAnimationKey_ === void 0 && (this.updateAnimationKey_ = requestAnimationFrame(
      this.updateAnimations_.bind(this)
    ));
  }
  calculateCenterRotate(t, e) {
    let n;
    const s = this.getCenterInternal();
    return s !== void 0 && (n = [s[0] - e[0], s[1] - e[1]], tl(n, t - this.getRotation()), Nu(n, e)), n;
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
    return t && xa(t, this.getProjection());
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
    return qu(e, this.getProjection());
  }
  calculateExtentInternal(t) {
    t = t || this.getViewportSizeMinusPadding_();
    const e = this.getCenterInternal();
    Y(e, 1);
    const n = this.getResolution();
    Y(n !== void 0, 2);
    const s = this.getRotation();
    return Y(s !== void 0, 3), ua(e, n, s, t);
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
      Xi(t, this.getProjection()),
      e
    );
  }
  getResolutionForExtentInternal(t, e) {
    e = e || this.getViewportSizeMinusPadding_();
    const n = mt(t) / e[0], s = je(t) / e[1];
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
      s = Wo(
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
      const r = Ua(this.resolutions_, t, 1);
      e = r, n = this.resolutions_[r], r == this.resolutions_.length - 1 ? s = 2 : s = n / this.resolutions_[r + 1];
    } else
      n = this.maxResolution_, s = this.zoomFactor_;
    return e + Math.log(n / t) / Math.log(s);
  }
  getResolutionForZoom(t) {
    if (this.resolutions_) {
      if (this.resolutions_.length <= 1)
        return 0;
      const e = Pt(
        Math.floor(t),
        0,
        this.resolutions_.length - 2
      ), n = this.resolutions_[e] / this.resolutions_[e + 1];
      return this.resolutions_[e] / Math.pow(n, Pt(t - e, 0, 1));
    } else
      return this.maxResolution_ / Math.pow(this.zoomFactor_, t - this.minZoom_);
  }
  fit(t, e) {
    let n;
    if (Y(
      Array.isArray(t) || typeof t.getSimplifiedGeometry == "function",
      24
    ), Array.isArray(t)) {
      Y(!Qa(t), 25);
      const s = Xi(t, this.getProjection());
      n = Fh(s);
    } else if (t.getType() === "Circle") {
      const s = Xi(
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
    const f = d[0] * u - d[1] * c, g = d[1] * u + d[0] * c, m = this.getConstrainedCenter([f, g], l), p = e.callback ? e.callback : Ki;
    e.duration !== void 0 ? this.animateInternal(
      {
        resolution: l,
        center: m,
        duration: e.duration,
        easing: e.easing
      },
      p
    ) : (this.targetResolution_ = l, this.targetCenter_ = m, this.applyTargetState_(!1, !0), yr(p, !0));
  }
  centerOn(t, e, n) {
    this.centerOnInternal(
      Qe(t, this.getProjection()),
      e,
      n
    );
  }
  centerOnInternal(t, e, n) {
    this.setCenterInternal(
      Wo(
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
      const a = this.getViewportSizeMinusPadding_(-n), l = Wo(
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
    const e = xa(this.targetCenter_, this.getProjection());
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
    e = e && Qe(e, this.getProjection()), this.adjustResolutionInternal(t, e);
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
    e && (e = Qe(e, this.getProjection())), this.adjustRotationInternal(t, e);
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
      t && Qe(t, this.getProjection())
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
    this.get(Ee.ROTATION) !== s && this.set(Ee.ROTATION, s), this.get(Ee.RESOLUTION) !== o && (this.set(Ee.RESOLUTION, o), this.set("zoom", this.getZoom(), !0)), (!a || !this.get(Ee.CENTER) || !Xr(this.get(Ee.CENTER), a)) && this.set(Ee.CENTER, a), this.getAnimating() && !t && this.cancelAnimations(), this.cancelAnchor_ = void 0;
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
    n = n || (t === 0 ? this.cancelAnchor_ : void 0), this.cancelAnchor_ = void 0, (this.getResolution() !== a || this.getRotation() !== r || !this.getCenterInternal() || !Xr(this.getCenterInternal(), l)) && (this.getAnimating() && this.cancelAnimations(), this.animateInternal({
      rotation: r,
      center: l,
      resolution: a,
      duration: t,
      easing: Qn,
      anchor: n
    }));
  }
  beginInteraction() {
    this.resolveConstraints(0), this.setHint(Ht.INTERACTING, 1);
  }
  endInteraction(t, e, n) {
    n = n && Qe(n, this.getProjection()), this.endInteractionInternal(t, e, n);
  }
  endInteractionInternal(t, e, n) {
    this.setHint(Ht.INTERACTING, -1), this.resolveConstraints(t, e, n);
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
function yr(i, t) {
  setTimeout(function() {
    i(t);
  }, 0);
}
function Kg(i) {
  if (i.extent !== void 0) {
    const e = i.smoothExtentConstraint !== void 0 ? i.smoothExtentConstraint : !0;
    return Th(i.extent, i.constrainOnlyCenter, e);
  }
  const t = ol(i.projection, "EPSG:3857");
  if (i.multiWorld !== !0 && t.isGlobal()) {
    const e = t.getExtent().slice();
    return e[0] = -1 / 0, e[2] = 1 / 0, Th(e, !1, !1);
  }
  return Cg;
}
function Qg(i) {
  let t, e, n, o = i.minZoom !== void 0 ? i.minZoom : Bo, a = i.maxZoom !== void 0 ? i.maxZoom : 28;
  const l = i.zoomFactor !== void 0 ? i.zoomFactor : 2, h = i.multiWorld !== void 0 ? i.multiWorld : !1, c = i.smoothResolutionConstraint !== void 0 ? i.smoothResolutionConstraint : !0, u = i.showFullExtent !== void 0 ? i.showFullExtent : !1, d = ol(i.projection, "EPSG:3857"), f = d.getExtent();
  let g = i.constrainOnlyCenter, m = i.extent;
  if (!h && !m && d.isGlobal() && (g = !1, m = f), i.resolutions !== void 0) {
    const p = i.resolutions;
    e = p[o], n = p[a] !== void 0 ? p[a] : p[p.length - 1], i.constrainResolution ? t = wg(
      p,
      c,
      !g && m,
      u
    ) : t = Lh(
      e,
      n,
      c,
      !g && m,
      u
    );
  } else {
    const v = (f ? Math.max(mt(f), je(f)) : 360 * Xn.degrees / d.getMetersPerUnit()) / il / Math.pow(2, Bo), y = v / Math.pow(2, 28 - Bo);
    e = i.maxResolution, e !== void 0 ? o = 0 : e = v / Math.pow(l, o), n = i.minResolution, n === void 0 && (i.maxZoom !== void 0 ? i.maxResolution !== void 0 ? n = e / Math.pow(l, a) : n = v / Math.pow(l, a) : n = y), a = o + Math.floor(
      Math.log(e / n) / Math.log(l)
    ), n = e / Math.pow(l, a - o), i.constrainResolution ? t = Eg(
      l,
      e,
      n,
      c,
      !g && m,
      u
    ) : t = Lh(
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
function $g(i) {
  if (i.enableRotation !== void 0 ? i.enableRotation : !0) {
    const e = i.constrainRotation;
    return e === void 0 || e === !0 ? Pg() : e === !1 ? Oh : typeof e == "number" ? bg(e) : Oh;
  } else
    return hl;
}
function t1(i) {
  return !(i.sourceCenter && i.targetCenter && !Xr(i.sourceCenter, i.targetCenter) || i.sourceResolution !== i.targetResolution || i.sourceRotation !== i.targetRotation);
}
function Wo(i, t, e, n, s) {
  const r = Math.cos(-s);
  let o = Math.sin(-s), a = i[0] * r - i[1] * o, l = i[1] * r + i[0] * o;
  a += (t[0] / 2 - e[0]) * n, l += (e[1] - t[1] / 2) * n, o = -o;
  const h = a * r - l * o, c = l * r + a * o;
  return [h, c];
}
const ii = qg;
class e1 extends Ce {
  constructor(t) {
    super();
    const e = t.element;
    e && !t.target && !e.style.pointerEvents && (e.style.pointerEvents = "auto"), this.element = e || null, this.target_ = null, this.map_ = null, this.listenerKeys = [], t.render && (this.render = t.render), t.target && this.setTarget(t.target);
  }
  disposeInternal() {
    Hr(this.element), super.disposeInternal();
  }
  getMap() {
    return this.map_;
  }
  setMap(t) {
    this.map_ && Hr(this.element);
    for (let e = 0, n = this.listenerKeys.length; e < n; ++e)
      pt(this.listenerKeys[e]);
    this.listenerKeys.length = 0, this.map_ = t, t && ((this.target_ ? this.target_ : t.getOverlayContainerStopEvent()).appendChild(this.element), this.render !== Ki && this.listenerKeys.push(
      et(t, $e.POSTRENDER, this.render, this)
    ), t.render());
  }
  render(t) {
  }
  setTarget(t) {
    this.target_ = typeof t == "string" ? document.getElementById(t) : t;
  }
}
const Dt = e1;
class i1 extends Dt {
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
      V.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const h = e + " " + Kn + " " + yo + (this.collapsed_ && this.collapsible_ ? " " + Mh : "") + (this.collapsible_ ? "" : " ol-uncollapsible"), c = this.element;
    c.className = h, c.appendChild(this.toggleButton_), c.appendChild(this.ulElement_), this.renderedAttributions_ = [], this.renderedVisible_ = !0;
  }
  collectSourceAttributions_(t) {
    const e = {}, n = [];
    let s = !0;
    const r = t.layerStatesArray;
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      if (!$a(l, t.viewState))
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
    if (this.renderedVisible_ != n && (this.element.style.display = n ? "" : "none", this.renderedVisible_ = n), !sn(e, this.renderedAttributions_)) {
      Gu(this.ulElement_);
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
    this.element.classList.toggle(Mh), this.collapsed_ ? Gr(this.collapseLabel_, this.label_) : Gr(this.label_, this.collapseLabel_), this.collapsed_ = !this.collapsed_, this.toggleButton_.setAttribute("aria-expanded", String(!this.collapsed_));
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
const n1 = i1;
class s1 extends Dt {
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
      V.CLICK,
      this.handleClick_.bind(this),
      !1
    );
    const a = e + " " + Kn + " " + yo, l = this.element;
    l.className = a, l.appendChild(o), this.callResetNorth_ = t.resetNorth ? t.resetNorth : void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.autoHide_ = t.autoHide !== void 0 ? t.autoHide : !0, this.rotation_ = void 0, this.autoHide_ && this.element.classList.add(pr);
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
      easing: Qn
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
        const r = this.element.classList.contains(pr);
        !r && n === 0 ? this.element.classList.add(pr) : r && n !== 0 && this.element.classList.remove(pr);
      }
      this.label_.style.transform = s;
    }
    this.rotation_ = n;
  }
}
const r1 = s1;
class o1 extends Dt {
  constructor(t) {
    t = t || {}, super({
      element: document.createElement("div"),
      target: t.target
    });
    const e = t.className !== void 0 ? t.className : "ol-zoom", n = t.delta !== void 0 ? t.delta : 1, s = t.zoomInClassName !== void 0 ? t.zoomInClassName : e + "-in", r = t.zoomOutClassName !== void 0 ? t.zoomOutClassName : e + "-out", o = t.zoomInLabel !== void 0 ? t.zoomInLabel : "+", a = t.zoomOutLabel !== void 0 ? t.zoomOutLabel : "\u2013", l = t.zoomInTipLabel !== void 0 ? t.zoomInTipLabel : "Zoom in", h = t.zoomOutTipLabel !== void 0 ? t.zoomOutTipLabel : "Zoom out", c = document.createElement("button");
    c.className = s, c.setAttribute("type", "button"), c.title = l, c.appendChild(
      typeof o == "string" ? document.createTextNode(o) : o
    ), c.addEventListener(
      V.CLICK,
      this.handleClick_.bind(this, n),
      !1
    );
    const u = document.createElement("button");
    u.className = r, u.setAttribute("type", "button"), u.title = h, u.appendChild(
      typeof a == "string" ? document.createTextNode(a) : a
    ), u.addEventListener(
      V.CLICK,
      this.handleClick_.bind(this, -n),
      !1
    );
    const d = e + " " + Kn + " " + yo, f = this.element;
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
        easing: Qn
      })) : n.setZoom(r);
    }
  }
}
const hd = o1;
function a1(i) {
  i = i || {};
  const t = new Ie();
  return (i.zoom !== void 0 ? i.zoom : !0) && t.push(new hd(i.zoomOptions)), (i.rotate !== void 0 ? i.rotate : !0) && t.push(new r1(i.rotateOptions)), (i.attribution !== void 0 ? i.attribution : !0) && t.push(new n1(i.attributionOptions)), t;
}
const Dh = {
  ACTIVE: "active"
};
class l1 extends Ce {
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
function h1(i, t, e) {
  const n = i.getCenterInternal();
  if (n) {
    const s = [n[0] + t[0], n[1] + t[1]];
    i.animateInternal({
      duration: e !== void 0 ? e : 250,
      easing: _g,
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
    easing: Qn
  });
}
const Vs = l1;
class c1 extends Vs {
  constructor(t) {
    super(), t = t || {}, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == Et.DBLCLICK) {
      const n = t.originalEvent, s = t.map, r = t.coordinate, o = n.shiftKey ? -this.delta_ : this.delta_, a = s.getView();
      yl(a, o, r, this.duration_), n.preventDefault(), e = !0;
    }
    return !e;
  }
}
const u1 = c1;
class d1 extends Vs {
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
      if (t.type == Et.POINTERDRAG)
        this.handleDragEvent(t), t.originalEvent.preventDefault();
      else if (t.type == Et.POINTERUP) {
        const n = this.handleUpEvent(t);
        this.handlingDownUpSequence = n && this.targetPointers.length > 0;
      }
    } else if (t.type == Et.POINTERDOWN) {
      const n = this.handleDownEvent(t);
      this.handlingDownUpSequence = n, e = this.stopDown(n);
    } else
      t.type == Et.POINTERMOVE && this.handleMoveEvent(t);
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
function xl(i) {
  const t = i.length;
  let e = 0, n = 0;
  for (let s = 0; s < t; s++)
    e += i[s].clientX, n += i[s].clientY;
  return [e / t, n / t];
}
const Ys = d1;
function Ea(i) {
  const t = arguments;
  return function(e) {
    let n = !0;
    for (let s = 0, r = t.length; s < r && (n = n && t[s](e), !!n); ++s)
      ;
    return n;
  };
}
const f1 = function(i) {
  const t = i.originalEvent;
  return t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, g1 = function(i) {
  const t = i.map.getTargetElement(), e = i.map.getOwnerDocument().activeElement;
  return t.contains(e);
}, cd = function(i) {
  return i.map.getTargetElement().hasAttribute("tabindex") ? g1(i) : !0;
}, m1 = Ss, ud = function(i) {
  const t = i.originalEvent;
  return t.button == 0 && !(h0 && c0 && t.ctrlKey);
}, dd = function(i) {
  const t = i.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && !t.shiftKey;
}, p1 = function(i) {
  const t = i.originalEvent;
  return !t.altKey && !(t.metaKey || t.ctrlKey) && t.shiftKey;
}, fd = function(i) {
  const t = i.originalEvent, e = t.target.tagName;
  return e !== "INPUT" && e !== "SELECT" && e !== "TEXTAREA" && !t.target.isContentEditable;
}, Vo = function(i) {
  const t = i.originalEvent;
  return Y(t !== void 0, 56), t.pointerType == "mouse";
}, v1 = function(i) {
  const t = i.originalEvent;
  return Y(t !== void 0, 56), t.isPrimary && t.button === 0;
};
class y1 extends Ys {
  constructor(t) {
    super({
      stopDown: lo
    }), t = t || {}, this.kinetic_ = t.kinetic, this.lastCentroid = null, this.lastPointersCount_, this.panning_ = !1;
    const e = t.condition ? t.condition : Ea(dd, v1);
    this.condition_ = t.onFocusOnly ? Ea(cd, e) : e, this.noKinetic_ = !1;
  }
  handleDragEvent(t) {
    this.panning_ || (this.panning_ = !0, this.getMap().getView().beginInteraction());
    const e = this.targetPointers, n = xl(e);
    if (e.length == this.lastPointersCount_) {
      if (this.kinetic_ && this.kinetic_.update(n[0], n[1]), this.lastCentroid) {
        const s = [
          this.lastCentroid[0] - n[0],
          n[1] - this.lastCentroid[1]
        ], o = t.map.getView();
        zu(s, o.getResolution()), tl(s, o.getRotation()), o.adjustCenterInternal(s);
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
          easing: Qn
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
const x1 = y1;
class M1 extends Ys {
  constructor(t) {
    t = t || {}, super({
      stopDown: lo
    }), this.condition_ = t.condition ? t.condition : f1, this.lastAngle_ = void 0, this.duration_ = t.duration !== void 0 ? t.duration : 250;
  }
  handleDragEvent(t) {
    if (!Vo(t))
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
    return Vo(t) ? (t.map.getView().endInteraction(this.duration_), !1) : !0;
  }
  handleDownEvent(t) {
    return Vo(t) && ud(t) && this.condition_(t) ? (t.map.getView().beginInteraction(), this.lastAngle_ = void 0, !0) : !1;
  }
}
const C1 = M1;
class w1 extends Ya {
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
    s[4] = s[0].slice(), this.geometry_ ? this.geometry_.setCoordinates([s]) : this.geometry_ = new Zn([s]);
  }
  getGeometry() {
    return this.geometry_;
  }
}
const E1 = w1, xr = {
  BOXSTART: "boxstart",
  BOXDRAG: "boxdrag",
  BOXEND: "boxend",
  BOXCANCEL: "boxcancel"
};
class Yo extends Ge {
  constructor(t, e, n) {
    super(t), this.coordinate = e, this.mapBrowserEvent = n;
  }
}
class b1 extends Ys {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.box_ = new E1(t.className || "ol-dragbox"), this.minArea_ = t.minArea !== void 0 ? t.minArea : 64, t.onBoxEnd && (this.onBoxEnd = t.onBoxEnd), this.startPixel_ = null, this.condition_ = t.condition ? t.condition : ud, this.boxEndCondition_ = t.boxEndCondition ? t.boxEndCondition : this.defaultBoxEndCondition;
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
      new Yo(
        xr.BOXDRAG,
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
      new Yo(
        e ? xr.BOXEND : xr.BOXCANCEL,
        t.coordinate,
        t
      )
    ), !1;
  }
  handleDownEvent(t) {
    return this.condition_(t) ? (this.startPixel_ = t.pixel, this.box_.setMap(t.map), this.box_.setPixels(this.startPixel_, this.startPixel_), this.dispatchEvent(
      new Yo(
        xr.BOXSTART,
        t.coordinate,
        t
      )
    ), !0) : !1;
  }
  onBoxEnd(t) {
  }
}
const P1 = b1;
class S1 extends P1 {
  constructor(t) {
    t = t || {};
    const e = t.condition ? t.condition : p1;
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
      easing: Qn
    });
  }
}
const _1 = S1, Di = {
  LEFT: 37,
  UP: 38,
  RIGHT: 39,
  DOWN: 40
};
class R1 extends Vs {
  constructor(t) {
    super(), t = t || {}, this.defaultCondition_ = function(e) {
      return dd(e) && fd(e);
    }, this.condition_ = t.condition !== void 0 ? t.condition : this.defaultCondition_, this.duration_ = t.duration !== void 0 ? t.duration : 100, this.pixelDelta_ = t.pixelDelta !== void 0 ? t.pixelDelta : 128;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == V.KEYDOWN) {
      const n = t.originalEvent, s = n.keyCode;
      if (this.condition_(t) && (s == Di.DOWN || s == Di.LEFT || s == Di.RIGHT || s == Di.UP)) {
        const o = t.map.getView(), a = o.getResolution() * this.pixelDelta_;
        let l = 0, h = 0;
        s == Di.DOWN ? h = -a : s == Di.LEFT ? l = -a : s == Di.RIGHT ? l = a : h = a;
        const c = [l, h];
        tl(c, o.getRotation()), h1(o, c, this.duration_), n.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const T1 = R1;
class L1 extends Vs {
  constructor(t) {
    super(), t = t || {}, this.condition_ = t.condition ? t.condition : fd, this.delta_ = t.delta ? t.delta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 100;
  }
  handleEvent(t) {
    let e = !1;
    if (t.type == V.KEYDOWN || t.type == V.KEYPRESS) {
      const n = t.originalEvent, s = n.charCode;
      if (this.condition_(t) && (s == "+".charCodeAt(0) || s == "-".charCodeAt(0))) {
        const r = t.map, o = s == "+".charCodeAt(0) ? this.delta_ : -this.delta_, a = r.getView();
        yl(a, o, void 0, this.duration_), n.preventDefault(), e = !0;
      }
    }
    return !e;
  }
}
const O1 = L1;
class A1 {
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
const I1 = A1;
class N1 extends Vs {
  constructor(t) {
    t = t || {}, super(
      t
    ), this.totalDelta_ = 0, this.lastDelta_ = 0, this.maxDelta_ = t.maxDelta !== void 0 ? t.maxDelta : 1, this.duration_ = t.duration !== void 0 ? t.duration : 250, this.timeout_ = t.timeout !== void 0 ? t.timeout : 80, this.useAnchor_ = t.useAnchor !== void 0 ? t.useAnchor : !0, this.constrainResolution_ = t.constrainResolution !== void 0 ? t.constrainResolution : !1;
    const e = t.condition ? t.condition : m1;
    this.condition_ = t.onFocusOnly ? Ea(cd, e) : e, this.lastAnchor_ = null, this.startTime_ = void 0, this.timeoutId_, this.mode_ = void 0, this.trackpadEventGap_ = 400, this.trackpadTimeoutId_, this.deltaPerZoom_ = 300;
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
    if (!this.condition_(t) || t.type !== V.WHEEL)
      return !0;
    const n = t.map, s = t.originalEvent;
    s.preventDefault(), this.useAnchor_ && (this.lastAnchor_ = t.coordinate);
    let r;
    if (t.type == V.WHEEL && (r = s.deltaY, a0 && s.deltaMode === WheelEvent.DOM_DELTA_PIXEL && (r /= Mu), s.deltaMode === WheelEvent.DOM_DELTA_LINE && (r *= 40)), r === 0)
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
    let n = -Pt(
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
const z1 = N1;
class F1 extends Ys {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = lo), super(e), this.anchor_ = null, this.lastAngle_ = void 0, this.rotating_ = !1, this.rotationDelta_ = 0, this.threshold_ = t.threshold !== void 0 ? t.threshold : 0.3, this.duration_ = t.duration !== void 0 ? t.duration : 250;
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
    const l = o.getViewport().getBoundingClientRect(), h = xl(this.targetPointers);
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
const D1 = F1;
class j1 extends Ys {
  constructor(t) {
    t = t || {};
    const e = t;
    e.stopDown || (e.stopDown = lo), super(e), this.anchor_ = null, this.duration_ = t.duration !== void 0 ? t.duration : 400, this.lastDistance_ = void 0, this.lastScaleDelta_ = 1;
  }
  handleDragEvent(t) {
    let e = 1;
    const n = this.targetPointers[0], s = this.targetPointers[1], r = n.clientX - s.clientX, o = n.clientY - s.clientY, a = Math.sqrt(r * r + o * o);
    this.lastDistance_ !== void 0 && (e = this.lastDistance_ / a), this.lastDistance_ = a;
    const l = t.map, h = l.getView();
    e != 1 && (this.lastScaleDelta_ = e);
    const c = l.getViewport().getBoundingClientRect(), u = xl(this.targetPointers);
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
const k1 = j1;
function X1(i) {
  i = i || {};
  const t = new Ie(), e = new I1(-5e-3, 0.05, 100);
  return (i.altShiftDragRotate !== void 0 ? i.altShiftDragRotate : !0) && t.push(new C1()), (i.doubleClickZoom !== void 0 ? i.doubleClickZoom : !0) && t.push(
    new u1({
      delta: i.zoomDelta,
      duration: i.zoomDuration
    })
  ), (i.dragPan !== void 0 ? i.dragPan : !0) && t.push(
    new x1({
      onFocusOnly: i.onFocusOnly,
      kinetic: e
    })
  ), (i.pinchRotate !== void 0 ? i.pinchRotate : !0) && t.push(new D1()), (i.pinchZoom !== void 0 ? i.pinchZoom : !0) && t.push(
    new k1({
      duration: i.zoomDuration
    })
  ), (i.keyboard !== void 0 ? i.keyboard : !0) && (t.push(new T1()), t.push(
    new O1({
      delta: i.zoomDelta,
      duration: i.zoomDuration
    })
  )), (i.mouseWheelZoom !== void 0 ? i.mouseWheelZoom : !0) && t.push(
    new z1({
      onFocusOnly: i.onFocusOnly,
      duration: i.zoomDuration
    })
  ), (i.shiftDragZoom !== void 0 ? i.shiftDragZoom : !0) && t.push(
    new _1({
      duration: i.zoomDuration
    })
  ), t;
}
function jh(i) {
  return i[0] > 0 && i[1] > 0;
}
function G1(i, t, e) {
  return e === void 0 && (e = [0, 0]), e[0] = i[0] * t + 0.5 | 0, e[1] = i[1] * t + 0.5 | 0, e;
}
function ce(i, t) {
  return Array.isArray(i) ? i : (t === void 0 ? t = [i, i] : (t[0] = i, t[1] = i), t);
}
function gd(i) {
  if (i instanceof vo) {
    i.setMapInternal(null);
    return;
  }
  i instanceof xo && i.getLayers().forEach(gd);
}
function md(i, t) {
  if (i instanceof vo) {
    i.setMapInternal(t);
    return;
  }
  if (i instanceof xo) {
    const e = i.getLayers().getArray();
    for (let n = 0, s = e.length; n < s; ++n)
      md(e[n], t);
  }
}
class H1 extends Ce {
  constructor(t) {
    super(), t = t || {}, this.on, this.once, this.un;
    const e = Z1(t);
    this.renderComplete_, this.loaded_ = !0, this.boundHandleBrowserEvent_ = this.handleBrowserEvent.bind(this), this.maxTilesLoading_ = t.maxTilesLoading !== void 0 ? t.maxTilesLoading : 16, this.pixelRatio_ = t.pixelRatio !== void 0 ? t.pixelRatio : Mu, this.postRenderTimeoutHandle_, this.animationDelayKey_, this.animationDelay_ = this.animationDelay_.bind(this), this.coordinateToPixelTransform_ = Fe(), this.pixelToCoordinateTransform_ = Fe(), this.frameIndex_ = 0, this.frameState_ = null, this.previousExtent_ = null, this.viewPropertyListenerKey_ = null, this.viewChangeListenerKey_ = null, this.layerGroupPropertyListenerKeys_ = null, this.viewport_ = document.createElement("div"), this.viewport_.className = "ol-viewport" + ("ontouchstart" in window ? " ol-touch" : ""), this.viewport_.style.position = "relative", this.viewport_.style.overflow = "hidden", this.viewport_.style.width = "100%", this.viewport_.style.height = "100%", this.overlayContainer_ = document.createElement("div"), this.overlayContainer_.style.position = "absolute", this.overlayContainer_.style.zIndex = "0", this.overlayContainer_.style.width = "100%", this.overlayContainer_.style.height = "100%", this.overlayContainer_.style.pointerEvents = "none", this.overlayContainer_.className = "ol-overlaycontainer", this.viewport_.appendChild(this.overlayContainer_), this.overlayContainerStopEvent_ = document.createElement("div"), this.overlayContainerStopEvent_.style.position = "absolute", this.overlayContainerStopEvent_.style.zIndex = "0", this.overlayContainerStopEvent_.style.width = "100%", this.overlayContainerStopEvent_.style.height = "100%", this.overlayContainerStopEvent_.style.pointerEvents = "none", this.overlayContainerStopEvent_.className = "ol-overlaycontainer-stopevent", this.viewport_.appendChild(this.overlayContainerStopEvent_), this.mapBrowserEventHandler_ = null, this.moveTolerance_ = t.moveTolerance, this.keyboardEventTarget_ = e.keyboardEventTarget, this.targetChangeHandlerKeys_ = null, this.controls = e.controls || a1(), this.interactions = e.interactions || X1({
      onFocusOnly: !0
    }), this.overlays_ = e.overlays, this.overlayIdIndex_ = {}, this.renderer_ = null, this.postRenderFunctions_ = [], this.tileQueue_ = new ng(
      this.getTilePriority.bind(this),
      this.handleTileChange_.bind(this)
    ), this.addChangeListener(
      Nt.LAYERGROUP,
      this.handleLayerGroupChanged_
    ), this.addChangeListener(Nt.VIEW, this.handleViewChanged_), this.addChangeListener(Nt.SIZE, this.handleSizeChanged_), this.addChangeListener(Nt.TARGET, this.handleTargetChanged_), this.setProperties(e.values);
    const n = this;
    t.view && !(t.view instanceof ii) && t.view.then(function(s) {
      n.setView(new ii(s));
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
    md(t.layer, this);
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
    const r = n.hitTolerance !== void 0 ? n.hitTolerance : 0, o = n.layerFilter !== void 0 ? n.layerFilter : Ss, a = n.checkWrapped !== !1;
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
        s instanceof xo ? e(s.getLayers()) : t.push(s);
      });
    }
    return e(this.getLayers()), t;
  }
  hasFeatureAtPixel(t, e) {
    if (!this.frameState_ || !this.renderer_)
      return !1;
    const n = this.getCoordinateFromPixelInternal(t);
    e = e !== void 0 ? e : {};
    const s = e.layerFilter !== void 0 ? e.layerFilter : Ss, r = e.hitTolerance !== void 0 ? e.hitTolerance : 0, o = e.checkWrapped !== !1;
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
    return this.get(Nt.TARGET);
  }
  getTargetElement() {
    const t = this.getTarget();
    return t !== void 0 ? typeof t == "string" ? document.getElementById(t) : t : null;
  }
  getCoordinateFromPixel(t) {
    return xa(
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
    return this.get(Nt.LAYERGROUP);
  }
  setLayers(t) {
    const e = this.getLayerGroup();
    if (t instanceof Ie) {
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
    const e = Qe(
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
    return this.get(Nt.SIZE);
  }
  getView() {
    return this.get(Nt.VIEW);
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
    return sg(
      this.frameState_,
      t,
      e,
      n,
      s
    );
  }
  handleBrowserEvent(t, e) {
    e = e || t.type;
    const n = new vi(e, this, t);
    this.handleMapBrowserEvent(n);
  }
  handleMapBrowserEvent(t) {
    if (!this.frameState_)
      return;
    const e = t.originalEvent, n = e.type;
    if (n === ma.POINTERDOWN || n === V.WHEEL || n === V.KEYDOWN) {
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
        if (o[Ht.ANIMATING] || o[Ht.INTERACTING]) {
          const a = Date.now() - t.time > 8;
          s = a ? 0 : 8, r = a ? 0 : 2;
        }
      }
      e.getTilesLoading() < s && (e.reprioritize(), e.loadMoreTiles(s, r));
    }
    t && this.renderer_ && !t.animate && (this.renderComplete_ === !0 ? (this.hasListener(Ei.RENDERCOMPLETE) && this.renderer_.dispatchRenderEvent(
      Ei.RENDERCOMPLETE,
      t
    ), this.loaded_ === !1 && (this.loaded_ = !0, this.dispatchEvent(
      new Cn($e.LOADEND, this, t)
    ))) : this.loaded_ === !0 && (this.loaded_ = !1, this.dispatchEvent(
      new Cn($e.LOADSTART, this, t)
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
        V.CONTEXTMENU,
        this.boundHandleBrowserEvent_
      ), this.viewport_.removeEventListener(
        V.WHEEL,
        this.boundHandleBrowserEvent_
      ), this.mapBrowserEventHandler_.dispose(), this.mapBrowserEventHandler_ = null, Hr(this.viewport_);
    }
    const t = this.getTargetElement();
    if (!t)
      this.renderer_ && (clearTimeout(this.postRenderTimeoutHandle_), this.postRenderTimeoutHandle_ = void 0, this.postRenderFunctions_.length = 0, this.renderer_.dispose(), this.renderer_ = null), this.animationDelayKey_ && (cancelAnimationFrame(this.animationDelayKey_), this.animationDelayKey_ = void 0);
    else {
      t.appendChild(this.viewport_), this.renderer_ || (this.renderer_ = new J0(this)), this.mapBrowserEventHandler_ = new $0(
        this,
        this.moveTolerance_
      );
      for (const s in Et)
        this.mapBrowserEventHandler_.addEventListener(
          Et[s],
          this.handleMapBrowserEvent.bind(this)
        );
      this.viewport_.addEventListener(
        V.CONTEXTMENU,
        this.boundHandleBrowserEvent_,
        !1
      ), this.viewport_.addEventListener(
        V.WHEEL,
        this.boundHandleBrowserEvent_,
        Cu ? { passive: !1 } : !1
      );
      const e = this.getOwnerDocument().defaultView, n = this.keyboardEventTarget_ ? this.keyboardEventTarget_ : t;
      this.targetChangeHandlerKeys_ = [
        et(
          n,
          V.KEYDOWN,
          this.handleBrowserEvent,
          this
        ),
        et(
          n,
          V.KEYPRESS,
          this.handleBrowserEvent,
          this
        ),
        et(e, V.RESIZE, this.updateSize, this)
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
      Dn.PROPERTYCHANGE,
      this.handleViewPropertyChanged_,
      this
    ), this.viewChangeListenerKey_ = et(
      t,
      V.CHANGE,
      this.handleViewPropertyChanged_,
      this
    ), t.resolveConstraints(0)), this.render();
  }
  handleLayerGroupChanged_() {
    this.layerGroupPropertyListenerKeys_ && (this.layerGroupPropertyListenerKeys_.forEach(pt), this.layerGroupPropertyListenerKeys_ = null);
    const t = this.getLayerGroup();
    t && (this.handleLayerAdd_(new xi("addlayer", t)), this.layerGroupPropertyListenerKeys_ = [
      et(t, Dn.PROPERTYCHANGE, this.render, this),
      et(t, V.CHANGE, this.render, this),
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
    gd(t.layer);
  }
  removeOverlay(t) {
    return this.getOverlays().remove(t);
  }
  renderFrame_(t) {
    const e = this.getSize(), n = this.getView(), s = this.frameState_;
    let r = null;
    if (e !== void 0 && jh(e) && n && n.isDef()) {
      const o = n.getHints(
        this.frameState_ ? this.frameState_.viewHints : void 0
      ), a = n.getState();
      if (r = {
        animate: !1,
        coordinateToPixelTransform: this.coordinateToPixelTransform_,
        declutterTree: null,
        extent: ua(
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
        mapId: rt(this),
        renderTargets: {}
      }, a.nextCenter && a.nextResolution) {
        const l = isNaN(a.nextRotation) ? a.rotation : a.nextRotation;
        r.nextExtent = ua(
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
    ), s && (!this.previousExtent_ || !Qa(this.previousExtent_) && !_s(r.extent, this.previousExtent_)) && (this.dispatchEvent(
      new Cn($e.MOVESTART, this, s)
    ), this.previousExtent_ = Bs(this.previousExtent_)), this.previousExtent_ && !r.viewHints[Ht.ANIMATING] && !r.viewHints[Ht.INTERACTING] && !_s(r.extent, this.previousExtent_) && (this.dispatchEvent(
      new Cn($e.MOVEEND, this, r)
    ), Eu(r.extent, this.previousExtent_))), this.dispatchEvent(new Cn($e.POSTRENDER, this, r)), this.renderComplete_ = this.hasListener($e.LOADSTART) || this.hasListener($e.LOADEND) || this.hasListener(Ei.RENDERCOMPLETE) ? !this.tileQueue_.getTilesLoading() && !this.tileQueue_.getCount() && !this.getLoadingOrNotReady() : void 0, this.postRenderTimeoutHandle_ || (this.postRenderTimeoutHandle_ = setTimeout(() => {
      this.postRenderTimeoutHandle_ = void 0, this.handlePostRender();
    }, 0));
  }
  setLayerGroup(t) {
    const e = this.getLayerGroup();
    e && this.handleLayerRemove_(new xi("removelayer", e)), this.set(Nt.LAYERGROUP, t);
  }
  setSize(t) {
    this.set(Nt.SIZE, t);
  }
  setTarget(t) {
    this.set(Nt.TARGET, t);
  }
  setView(t) {
    if (!t || t instanceof ii) {
      this.set(Nt.VIEW, t);
      return;
    }
    this.set(Nt.VIEW, new ii());
    const e = this;
    t.then(function(n) {
      e.setView(new ii(n));
    });
  }
  updateSize() {
    const t = this.getTargetElement();
    let e;
    if (t) {
      const n = getComputedStyle(t), s = t.offsetWidth - parseFloat(n.borderLeftWidth) - parseFloat(n.paddingLeft) - parseFloat(n.paddingRight) - parseFloat(n.borderRightWidth), r = t.offsetHeight - parseFloat(n.borderTopWidth) - parseFloat(n.paddingTop) - parseFloat(n.paddingBottom) - parseFloat(n.borderBottomWidth);
      !isNaN(s) && !isNaN(r) && (e = [s, r], !jh(e) && !!(t.offsetWidth || t.offsetHeight || t.getClientRects().length) && console.warn(
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
function Z1(i) {
  let t = null;
  i.keyboardEventTarget !== void 0 && (t = typeof i.keyboardEventTarget == "string" ? document.getElementById(i.keyboardEventTarget) : i.keyboardEventTarget);
  const e = {}, n = i.layers && typeof i.layers.getLayers == "function" ? i.layers : new xo({
    layers: i.layers
  });
  e[Nt.LAYERGROUP] = n, e[Nt.TARGET] = i.target, e[Nt.VIEW] = i.view instanceof ii ? i.view : new ii();
  let s;
  i.controls !== void 0 && (Array.isArray(i.controls) ? s = new Ie(i.controls.slice()) : (Y(
    typeof i.controls.getArray == "function",
    47
  ), s = i.controls));
  let r;
  i.interactions !== void 0 && (Array.isArray(i.interactions) ? r = new Ie(i.interactions.slice()) : (Y(
    typeof i.interactions.getArray == "function",
    48
  ), r = i.interactions));
  let o;
  return i.overlays !== void 0 ? Array.isArray(i.overlays) ? o = new Ie(i.overlays.slice()) : (Y(
    typeof i.overlays.getArray == "function",
    49
  ), o = i.overlays) : o = new Ie(), {
    controls: s,
    interactions: r,
    keyboardEventTarget: t,
    overlays: o,
    values: e
  };
}
const B1 = H1;
class Ml extends Ce {
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
    const t = new Ml(this.hasProperties() ? this.getProperties() : null);
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
      V.CHANGE,
      this.handleGeometryChange_,
      this
    )), this.changed();
  }
  setGeometry(t) {
    this.set(this.geometryName_, t);
  }
  setStyle(t) {
    this.style_ = t, this.styleFunction_ = t ? W1(t) : void 0, this.changed();
  }
  setId(t) {
    this.id_ = t, this.changed();
  }
  setGeometryName(t) {
    this.removeChangeListener(this.geometryName_, this.handleGeometryChanged_), this.geometryName_ = t, this.addChangeListener(this.geometryName_, this.handleGeometryChanged_), this.handleGeometryChanged_();
  }
}
function W1(i) {
  if (typeof i == "function")
    return i;
  {
    let t;
    return Array.isArray(i) ? t = i : (Y(typeof i.getZIndex == "function", 41), t = [i]), function() {
      return t;
    };
  }
}
const an = Ml, xt = {
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
class V1 extends Ge {
  constructor(t) {
    super(V.ERROR), this.code = t.code, this.message = t.message;
  }
}
class Y1 extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, t = t || {}, this.position_ = null, this.transform_ = rl, this.watchId_ = void 0, this.addChangeListener(xt.PROJECTION, this.handleProjectionChanged_), this.addChangeListener(xt.TRACKING, this.handleTrackingChanged_), t.projection !== void 0 && this.setProjection(t.projection), t.trackingOptions !== void 0 && this.setTrackingOptions(t.trackingOptions), this.setTracking(t.tracking !== void 0 ? t.tracking : !1);
  }
  disposeInternal() {
    this.setTracking(!1), super.disposeInternal();
  }
  handleProjectionChanged_() {
    const t = this.getProjection();
    t && (this.transform_ = Mo(
      K("EPSG:4326"),
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
      e.heading === null ? void 0 : Vi(e.heading)
    ), this.position_ ? (this.position_[0] = e.longitude, this.position_[1] = e.latitude) : this.position_ = [e.longitude, e.latitude];
    const n = this.transform_(this.position_);
    this.set(xt.POSITION, n), this.set(xt.SPEED, e.speed === null ? void 0 : e.speed);
    const s = Jg(this.position_, e.accuracy);
    s.applyTransform(this.transform_), this.set(xt.ACCURACY_GEOMETRY, s), this.changed();
  }
  positionError_(t) {
    this.dispatchEvent(new V1(t));
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
    this.set(xt.PROJECTION, K(t));
  }
  setTracking(t) {
    this.set(xt.TRACKING, t);
  }
  setTrackingOptions(t) {
    this.set(xt.TRACKING_OPTIONS, t);
  }
}
const U1 = Y1;
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
const Ut = Cl;
function pd(i, t, e, n, s, r, o) {
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
      const v = i[p], y = i[p + 1];
      d += Math.sqrt((v - c) * (v - c) + (y - u) * (y - u)), f.push(d), c = v, u = y;
    }
    const g = s * d, m = qf(f, g);
    m < 0 ? (l = (g - f[-m - 2]) / (f[-m - 1] - f[-m - 2]), a = t + (-m - 2) * n) : a = t + m * n;
  }
  o = o > 1 ? o : 2, r = r || new Array(o);
  for (let c = 0; c < o; ++c)
    r[c] = a === void 0 ? NaN : l === void 0 ? i[a + c] : ti(i[a + c], i[a + n + c], l);
  return r;
}
function ba(i, t, e, n, s, r) {
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
      ti(
        i[(a - 1) * n + d],
        i[a * n + d],
        u
      )
    );
  return o.push(s), o;
}
function J1(i, t, e, n, s, r, o) {
  if (o)
    return ba(
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
        return ba(
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
function vd(i, t, e, n) {
  let s = i[t], r = i[t + 1], o = 0;
  for (let a = t + n; a < e; a += n) {
    const l = i[a], h = i[a + 1];
    o += Math.sqrt((l - s) * (l - s) + (h - r) * (h - r)), s = l, r = h;
  }
  return o;
}
class Jr extends on {
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
    this.flatCoordinates ? qt(this.flatCoordinates, t) : this.flatCoordinates = t.slice(), this.changed();
  }
  clone() {
    const t = new Jr(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < rn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
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
    return sd(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  getCoordinateAtM(t, e) {
    return this.layout != "XYM" && this.layout != "XYZM" ? null : (e = e !== void 0 ? e : !1, ba(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t,
      e
    ));
  }
  getCoordinates() {
    return Ci(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getCoordinateAt(t, e) {
    return pd(
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
    return vd(
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
    ), new Jr(e, "XY");
  }
  getType() {
    return "LineString";
  }
  intersectsExtent(t) {
    return wo(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Co(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const Fs = Jr;
class wl {
  constructor(t) {
    t = t || {}, this.color_ = t.color !== void 0 ? t.color : null, this.lineCap_ = t.lineCap, this.lineDash_ = t.lineDash !== void 0 ? t.lineDash : null, this.lineDashOffset_ = t.lineDashOffset, this.lineJoin_ = t.lineJoin, this.miterLimit_ = t.miterLimit, this.width_ = t.width;
  }
  clone() {
    const t = this.getColor();
    return new wl({
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
const Se = wl, Ot = {
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
    return B();
  }
  getImage(t) {
    return B();
  }
  getHitDetectionImage() {
    return B();
  }
  getPixelRatio(t) {
    return 1;
  }
  getImageState() {
    return B();
  }
  getImageSize() {
    return B();
  }
  getOrigin() {
    return B();
  }
  getSize() {
    return B();
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
    B();
  }
  load() {
    B();
  }
  unlistenImageChange(t) {
    B();
  }
}
const yd = El;
function Ne(i) {
  return Array.isArray(i) ? Au(i) : i;
}
class bl extends yd {
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
    const t = this.getScale(), e = new bl({
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
    return Ot.LOADED;
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
      const E = s;
      s = r, r = E;
    }
    const o = this.radius2_ === void 0 ? this.points_ : this.points_ * 2, a = 2 * Math.PI / o, l = r * Math.sin(a), h = Math.sqrt(r * r - l * l), c = s - h, u = Math.sqrt(l * l + c * c), d = u / l;
    if (t === "miter" && d <= n)
      return d * e;
    const f = e / 2 / d, g = e / 2 * (c / u), p = Math.sqrt((s + f) * (s + f) + g * g) - s;
    if (this.radius2_ === void 0 || t === "bevel")
      return p * 2;
    const v = s * Math.sin(a), y = Math.sqrt(s * s - v * v), x = r - y, C = Math.sqrt(v * v + x * x) / v;
    if (C <= n) {
      const E = C * e / 2 - r - s;
      return 2 * Math.max(p, E);
    }
    return p * 2;
  }
  createRenderOptions() {
    let t = kn, e = 0, n = null, s = 0, r, o = 0;
    this.stroke_ && (r = this.stroke_.getColor(), r === null && (r = Os), r = Ne(r), o = this.stroke_.getWidth(), o === void 0 && (o = Is), n = this.stroke_.getLineDash(), s = this.stroke_.getLineDashOffset(), t = this.stroke_.getLineJoin(), t === void 0 && (t = kn), e = this.stroke_.getMiterLimit(), e === void 0 && (e = Ls));
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
      s === null && (s = si), e.fillStyle = Ne(s), e.fill();
    }
    this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
  createHitDetectionCanvas_(t) {
    if (this.fill_) {
      let e = this.fill_.getColor(), n = 0;
      if (typeof e == "string" && (e = jr(e)), e === null ? n = 1 : Array.isArray(e) && (n = e.length === 4 ? e[3] : 1), n === 0) {
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
    e.translate(t.size / 2, t.size / 2), this.createPath_(e), e.fillStyle = si, e.fill(), this.stroke_ && (e.strokeStyle = t.strokeStyle, e.lineWidth = t.strokeWidth, t.lineDash && (e.setLineDash(t.lineDash), e.lineDashOffset = t.lineDashOffset), e.lineJoin = t.lineJoin, e.miterLimit = t.miterLimit, e.stroke());
  }
}
const xd = bl;
class Pl extends xd {
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
    const t = this.getScale(), e = new Pl({
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
const ni = Pl;
class Eo {
  constructor(t) {
    t = t || {}, this.geometry_ = null, this.geometryFunction_ = kh, t.geometry !== void 0 && this.setGeometry(t.geometry), this.fill_ = t.fill !== void 0 ? t.fill : null, this.image_ = t.image !== void 0 ? t.image : null, this.renderer_ = t.renderer !== void 0 ? t.renderer : null, this.hitDetectionRenderer_ = t.hitDetectionRenderer !== void 0 ? t.hitDetectionRenderer : null, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.text_ = t.text !== void 0 ? t.text : null, this.zIndex_ = t.zIndex;
  }
  clone() {
    let t = this.getGeometry();
    return t && typeof t == "object" && (t = t.clone()), new Eo({
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
    }) : this.geometryFunction_ = kh, this.geometry_ = t;
  }
  setZIndex(t) {
    this.zIndex_ = t;
  }
}
function q1(i) {
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
let Uo = null;
function K1(i, t) {
  if (!Uo) {
    const e = new Ut({
      color: "rgba(255,255,255,0.4)"
    }), n = new Se({
      color: "#3399CC",
      width: 1.25
    });
    Uo = [
      new Eo({
        image: new ni({
          fill: e,
          stroke: n,
          radius: 5
        }),
        fill: e,
        stroke: n
      })
    ];
  }
  return Uo;
}
function kh(i) {
  return i.getGeometry();
}
const Bt = Eo, Q1 = "#333";
class Sl {
  constructor(t) {
    t = t || {}, this.font_ = t.font, this.rotation_ = t.rotation, this.rotateWithView_ = t.rotateWithView, this.scale_ = t.scale, this.scaleArray_ = ce(t.scale !== void 0 ? t.scale : 1), this.text_ = t.text, this.textAlign_ = t.textAlign, this.justify_ = t.justify, this.textBaseline_ = t.textBaseline, this.fill_ = t.fill !== void 0 ? t.fill : new Ut({ color: Q1 }), this.maxAngle_ = t.maxAngle !== void 0 ? t.maxAngle : Math.PI / 4, this.placement_ = t.placement !== void 0 ? t.placement : "point", this.overflow_ = !!t.overflow, this.stroke_ = t.stroke !== void 0 ? t.stroke : null, this.offsetX_ = t.offsetX !== void 0 ? t.offsetX : 0, this.offsetY_ = t.offsetY !== void 0 ? t.offsetY : 0, this.backgroundFill_ = t.backgroundFill ? t.backgroundFill : null, this.backgroundStroke_ = t.backgroundStroke ? t.backgroundStroke : null, this.padding_ = t.padding === void 0 ? null : t.padding;
  }
  clone() {
    const t = this.getScale();
    return new Sl({
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
const Pa = Sl;
function $1(i, t, e, n, s) {
  Md(i, t, e || 0, n || i.length - 1, s || t2);
}
function Md(i, t, e, n, s) {
  for (; n > e; ) {
    if (n - e > 600) {
      var r = n - e + 1, o = t - e + 1, a = Math.log(r), l = 0.5 * Math.exp(2 * a / 3), h = 0.5 * Math.sqrt(a * l * (r - l) / r) * (o - r / 2 < 0 ? -1 : 1), c = Math.max(e, Math.floor(t - o * l / r + h)), u = Math.min(n, Math.floor(t + (r - o) * l / r + h));
      Md(i, t, c, u, s);
    }
    var d = i[t], f = e, g = n;
    for (hs(i, e, t), s(i[n], d) > 0 && hs(i, e, n); f < g; ) {
      for (hs(i, f, g), f++, g--; s(i[f], d) < 0; )
        f++;
      for (; s(i[g], d) > 0; )
        g--;
    }
    s(i[e], d) === 0 ? hs(i, e, g) : (g++, hs(i, g, n)), g <= t && (e = g + 1), t <= g && (n = g - 1);
  }
}
function hs(i, t, e) {
  var n = i[t];
  i[t] = i[e], i[e] = n;
}
function t2(i, t) {
  return i < t ? -1 : i > t ? 1 : 0;
}
class Cd {
  constructor(t = 9) {
    this._maxEntries = Math.max(4, t), this._minEntries = Math.max(2, Math.ceil(this._maxEntries * 0.4)), this.clear();
  }
  all() {
    return this._all(this.data, []);
  }
  search(t) {
    let e = this.data;
    const n = [];
    if (!Cr(t, e))
      return n;
    const s = this.toBBox, r = [];
    for (; e; ) {
      for (let o = 0; o < e.children.length; o++) {
        const a = e.children[o], l = e.leaf ? s(a) : a;
        Cr(t, l) && (e.leaf ? n.push(a) : qo(t, l) ? this._all(a, n) : r.push(a));
      }
      e = r.pop();
    }
    return n;
  }
  collides(t) {
    let e = this.data;
    if (!Cr(t, e))
      return !1;
    const n = [];
    for (; e; ) {
      for (let s = 0; s < e.children.length; s++) {
        const r = e.children[s], o = e.leaf ? this.toBBox(r) : r;
        if (Cr(t, o)) {
          if (e.leaf || qo(t, o))
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
    return this.data = wn([]), this;
  }
  remove(t, e) {
    if (!t)
      return this;
    let n = this.data;
    const s = this.toBBox(t), r = [], o = [];
    let a, l, h;
    for (; n || r.length; ) {
      if (n || (n = r.pop(), l = r[r.length - 1], a = o.pop(), h = !0), n.leaf) {
        const c = e2(t, n.children, e);
        if (c !== -1)
          return n.children.splice(c, 1), r.push(n), this._condense(r), this;
      }
      !h && !n.leaf && qo(n, s) ? (r.push(n), o.push(a), a = 0, l = n, n = n.children[0]) : l ? (a++, n = l.children[a], h = !1) : n = null;
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
      return a = wn(t.slice(e, n + 1)), mn(a, this.toBBox), a;
    s || (s = Math.ceil(Math.log(r) / Math.log(o)), o = Math.ceil(r / Math.pow(o, s - 1))), a = wn([]), a.leaf = !1, a.height = s;
    const l = Math.ceil(r / o), h = l * Math.ceil(Math.sqrt(o));
    Xh(t, e, n, h, this.compareMinX);
    for (let c = e; c <= n; c += h) {
      const u = Math.min(c + h - 1, n);
      Xh(t, c, u, l, this.compareMinY);
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
        const h = e.children[l], c = Jo(h), u = s2(t, h) - c;
        u < o ? (o = u, r = c < r ? c : r, a = h) : u === o && c < r && (r = c, a = h);
      }
      e = a || e.children[0];
    }
    return e;
  }
  _insert(t, e, n) {
    const s = n ? t : this.toBBox(t), r = [], o = this._chooseSubtree(s, this.data, e, r);
    for (o.children.push(t), gs(o, s); e >= 0 && r[e].children.length > this._maxEntries; )
      this._split(r, e), e--;
    this._adjustParentBBoxes(s, r, e);
  }
  _split(t, e) {
    const n = t[e], s = n.children.length, r = this._minEntries;
    this._chooseSplitAxis(n, r, s);
    const o = this._chooseSplitIndex(n, r, s), a = wn(n.children.splice(o, n.children.length - o));
    a.height = n.height, a.leaf = n.leaf, mn(n, this.toBBox), mn(a, this.toBBox), e ? t[e - 1].children.push(a) : this._splitRoot(n, a);
  }
  _splitRoot(t, e) {
    this.data = wn([t, e]), this.data.height = t.height + 1, this.data.leaf = !1, mn(this.data, this.toBBox);
  }
  _chooseSplitIndex(t, e, n) {
    let s, r = 1 / 0, o = 1 / 0;
    for (let a = e; a <= n - e; a++) {
      const l = fs(t, 0, a, this.toBBox), h = fs(t, a, n, this.toBBox), c = r2(l, h), u = Jo(l) + Jo(h);
      c < r ? (r = c, s = a, o = u < o ? u : o) : c === r && u < o && (o = u, s = a);
    }
    return s || n - e;
  }
  _chooseSplitAxis(t, e, n) {
    const s = t.leaf ? this.compareMinX : i2, r = t.leaf ? this.compareMinY : n2, o = this._allDistMargin(t, e, n, s), a = this._allDistMargin(t, e, n, r);
    o < a && t.children.sort(s);
  }
  _allDistMargin(t, e, n, s) {
    t.children.sort(s);
    const r = this.toBBox, o = fs(t, 0, e, r), a = fs(t, n - e, n, r);
    let l = Mr(o) + Mr(a);
    for (let h = e; h < n - e; h++) {
      const c = t.children[h];
      gs(o, t.leaf ? r(c) : c), l += Mr(o);
    }
    for (let h = n - e - 1; h >= e; h--) {
      const c = t.children[h];
      gs(a, t.leaf ? r(c) : c), l += Mr(a);
    }
    return l;
  }
  _adjustParentBBoxes(t, e, n) {
    for (let s = n; s >= 0; s--)
      gs(e[s], t);
  }
  _condense(t) {
    for (let e = t.length - 1, n; e >= 0; e--)
      t[e].children.length === 0 ? e > 0 ? (n = t[e - 1].children, n.splice(n.indexOf(t[e]), 1)) : this.clear() : mn(t[e], this.toBBox);
  }
}
function e2(i, t, e) {
  if (!e)
    return t.indexOf(i);
  for (let n = 0; n < t.length; n++)
    if (e(i, t[n]))
      return n;
  return -1;
}
function mn(i, t) {
  fs(i, 0, i.children.length, t, i);
}
function fs(i, t, e, n, s) {
  s || (s = wn(null)), s.minX = 1 / 0, s.minY = 1 / 0, s.maxX = -1 / 0, s.maxY = -1 / 0;
  for (let r = t; r < e; r++) {
    const o = i.children[r];
    gs(s, i.leaf ? n(o) : o);
  }
  return s;
}
function gs(i, t) {
  return i.minX = Math.min(i.minX, t.minX), i.minY = Math.min(i.minY, t.minY), i.maxX = Math.max(i.maxX, t.maxX), i.maxY = Math.max(i.maxY, t.maxY), i;
}
function i2(i, t) {
  return i.minX - t.minX;
}
function n2(i, t) {
  return i.minY - t.minY;
}
function Jo(i) {
  return (i.maxX - i.minX) * (i.maxY - i.minY);
}
function Mr(i) {
  return i.maxX - i.minX + (i.maxY - i.minY);
}
function s2(i, t) {
  return (Math.max(t.maxX, i.maxX) - Math.min(t.minX, i.minX)) * (Math.max(t.maxY, i.maxY) - Math.min(t.minY, i.minY));
}
function r2(i, t) {
  const e = Math.max(i.minX, t.minX), n = Math.max(i.minY, t.minY), s = Math.min(i.maxX, t.maxX), r = Math.min(i.maxY, t.maxY);
  return Math.max(0, s - e) * Math.max(0, r - n);
}
function qo(i, t) {
  return i.minX <= t.minX && i.minY <= t.minY && t.maxX <= i.maxX && t.maxY <= i.maxY;
}
function Cr(i, t) {
  return t.minX <= i.maxX && t.minY <= i.maxY && t.maxX >= i.minX && t.maxY >= i.minY;
}
function wn(i) {
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
function Xh(i, t, e, n, s) {
  const r = [t, e];
  for (; r.length; ) {
    if (e = r.pop(), t = r.pop(), e - t <= n)
      continue;
    const o = t + Math.ceil((e - t) / n / 2) * n;
    $1(i, o, t, e, s), r.push(t, o, o, e);
  }
}
function wd(i, t, e) {
  const n = i;
  let s = !0, r = !1, o = !1;
  const a = [
    Dr(n, V.LOAD, function() {
      o = !0, r || t();
    })
  ];
  return n.src && u0 ? (r = !0, n.decode().then(function() {
    s && t();
  }).catch(function(l) {
    s && (o ? t() : e());
  })) : a.push(Dr(n, V.ERROR, e)), function() {
    s = !1, a.forEach(pt);
  };
}
let cs = null;
class o2 extends ho {
  constructor(t, e, n, s, r, o) {
    super(), this.hitDetectionImage_ = null, this.image_ = t, this.crossOrigin_ = s, this.canvas_ = {}, this.color_ = o, this.unlisten_ = null, this.imageState_ = r, this.size_ = n, this.src_ = e, this.tainted_;
  }
  initializeImage_() {
    this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_);
  }
  isTainted_() {
    if (this.tainted_ === void 0 && this.imageState_ === Ot.LOADED) {
      cs || (cs = ge(1, 1)), cs.drawImage(this.image_, 0, 0);
      try {
        cs.getImageData(0, 0, 1, 1), this.tainted_ = !1;
      } catch {
        cs = null, this.tainted_ = !0;
      }
    }
    return this.tainted_ === !0;
  }
  dispatchChangeEvent_() {
    this.dispatchEvent(V.CHANGE);
  }
  handleImageError_() {
    this.imageState_ = Ot.ERROR, this.unlistenImage_(), this.dispatchChangeEvent_();
  }
  handleImageLoad_() {
    this.imageState_ = Ot.LOADED, this.size_ ? (this.image_.width = this.size_[0], this.image_.height = this.size_[1]) : this.size_ = [this.image_.width, this.image_.height], this.unlistenImage_(), this.dispatchChangeEvent_();
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
    if (this.imageState_ === Ot.IDLE) {
      this.image_ || this.initializeImage_(), this.imageState_ = Ot.LOADING;
      try {
        this.image_.src = this.src_;
      } catch {
        this.handleImageError_();
      }
      this.unlisten_ = wd(
        this.image_,
        this.handleImageLoad_.bind(this),
        this.handleImageError_.bind(this)
      );
    }
  }
  replaceColor_(t) {
    if (!this.color_ || this.canvas_[t] || this.imageState_ !== Ot.LOADED)
      return;
    const e = this.image_, n = document.createElement("canvas");
    n.width = Math.ceil(e.width * t), n.height = Math.ceil(e.height * t);
    const s = n.getContext("2d");
    s.scale(t, t), s.drawImage(e, 0, 0), s.globalCompositeOperation = "multiply", s.fillStyle = Ou(this.color_), s.fillRect(0, 0, n.width / t, n.height / t), s.globalCompositeOperation = "destination-in", s.drawImage(e, 0, 0), this.canvas_[t] = n;
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function a2(i, t, e, n, s, r) {
  let o = kr.get(t, n, r);
  return o || (o = new o2(i, t, e, n, s, r), kr.set(t, n, r, o)), o;
}
class _l extends yd {
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
    Y(!(a !== void 0 && o), 4), Y(!o || o && this.imgSize_, 5), (a === void 0 || a.length === 0) && o && (a = o.src || rt(o)), Y(a !== void 0 && a.length > 0, 6);
    const l = t.src !== void 0 ? Ot.IDLE : Ot.LOADED;
    this.color_ = t.color !== void 0 ? jr(t.color) : null, this.iconImage_ = a2(
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
    return new _l({
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
    this.iconImage_.addEventListener(V.CHANGE, t);
  }
  load() {
    this.iconImage_.load();
  }
  unlistenImageChange(t) {
    this.iconImage_.removeEventListener(V.CHANGE, t);
  }
}
const Ms = _l;
function Gh(i) {
  return new Bt({
    fill: Ds(i, ""),
    stroke: js(i, ""),
    text: l2(i),
    image: h2(i)
  });
}
function Ds(i, t) {
  const e = i[t + "fill-color"];
  if (!!e)
    return new Ut({ color: e });
}
function js(i, t) {
  const e = i[t + "stroke-width"], n = i[t + "stroke-color"];
  if (!(!e && !n))
    return new Se({
      width: e,
      color: n,
      lineCap: i[t + "stroke-line-cap"],
      lineJoin: i[t + "stroke-line-join"],
      lineDash: i[t + "stroke-line-dash"],
      lineDashOffset: i[t + "stroke-line-dash-offset"],
      miterLimit: i[t + "stroke-miter-limit"]
    });
}
function l2(i) {
  const t = i["text-value"];
  return t ? new Pa({
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
    fill: Ds(i, "text-"),
    backgroundFill: Ds(i, "text-background-"),
    stroke: js(i, "text-"),
    backgroundStroke: js(i, "text-background-")
  }) : void 0;
}
function h2(i) {
  const t = i["icon-src"], e = i["icon-img"];
  if (t || e)
    return new Ms({
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
    return new xd({
      points: n,
      fill: Ds(i, r),
      stroke: js(i, r),
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
    return new ni({
      radius: s,
      fill: Ds(i, r),
      stroke: js(i, r),
      displacement: i["circle-displacement"],
      scale: i["circle-scale"],
      rotation: i["circle-rotation"],
      rotateWithView: i["circle-rotate-with-view"],
      declutterMode: i["circle-declutter-mode"]
    });
  }
}
const Hh = {
  RENDER_ORDER: "renderOrder"
};
class c2 extends vo {
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
    return this.get(Hh.RENDER_ORDER);
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
    t.declutterTree || (t.declutterTree = new Cd(9)), this.getRenderer().renderDeclutter(t);
  }
  setRenderOrder(t) {
    this.set(Hh.RENDER_ORDER, t);
  }
  setStyle(t) {
    let e;
    if (t === void 0)
      e = K1;
    else if (t === null)
      e = null;
    else if (typeof t == "function")
      e = t;
    else if (t instanceof Bt)
      e = t;
    else if (Array.isArray(t)) {
      const n = t.length, s = new Array(n);
      for (let r = 0; r < n; ++r) {
        const o = t[r];
        o instanceof Bt ? s[r] = o : s[r] = Gh(o);
      }
      e = s;
    } else
      e = Gh(t);
    this.style_ = e, this.styleFunction_ = t === null ? void 0 : q1(this.style_), this.changed();
  }
}
const u2 = c2, Us = {
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
}, wr = [Us.FILL], wi = [Us.STROKE], Hi = [Us.BEGIN_PATH], Zh = [Us.CLOSE_PATH], Z = Us;
class d2 {
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
const Ed = d2;
class f2 extends Ed {
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
      s[0] = t[a], s[1] = t[a + 1], fo(n, s) && (r[o++] = s[0], r[o++] = s[1]);
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
      d[0] = t[g], d[1] = t[g + 1], p = ha(h, d), p !== m ? (f && (a[l++] = c, a[l++] = u, f = !1), a[l++] = d[0], a[l++] = d[1]) : p === zt.INTERSECTING ? (a[l++] = d[0], a[l++] = d[1], f = !1) : f = !0, c = d[0], u = d[1], m = p;
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
          Z.CUSTOM,
          a,
          u,
          t,
          n,
          Ma
        ]), this.hitDetectionInstructions.push([
          Z.CUSTOM,
          a,
          u,
          t,
          s || n,
          Ma
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
          Z.CUSTOM,
          a,
          c,
          t,
          n,
          zs
        ]), this.hitDetectionInstructions.push([
          Z.CUSTOM,
          a,
          c,
          t,
          s || n,
          zs
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
          Z.CUSTOM,
          a,
          h,
          t,
          n,
          Ci
        ]), this.hitDetectionInstructions.push([
          Z.CUSTOM,
          a,
          h,
          t,
          s || n,
          Ci
        ]);
        break;
      case "MultiPoint":
        l = t.getFlatCoordinates(), h = this.appendFlatPointCoordinates(l, o), h > a && (this.instructions.push([
          Z.CUSTOM,
          a,
          h,
          t,
          n,
          Ci
        ]), this.hitDetectionInstructions.push([
          Z.CUSTOM,
          a,
          h,
          t,
          s || n,
          Ci
        ]));
        break;
      case "Point":
        l = t.getFlatCoordinates(), this.coordinates.push(l[0], l[1]), h = this.coordinates.length, this.instructions.push([
          Z.CUSTOM,
          a,
          h,
          t,
          n
        ]), this.hitDetectionInstructions.push([
          Z.CUSTOM,
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
      Z.BEGIN_GEOMETRY,
      e,
      0,
      t
    ], this.instructions.push(this.beginGeometryInstruction1_), this.beginGeometryInstruction2_ = [
      Z.BEGIN_GEOMETRY,
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
      s = t[e], r = s[0], r == Z.END_GEOMETRY ? o = e : r == Z.BEGIN_GEOMETRY && (s[2] = e, Kf(this.hitDetectionInstructions, o, e), o = -1);
  }
  setFillStrokeStyle(t, e) {
    const n = this.state;
    if (t) {
      const s = t.getColor();
      n.fillStyle = Ne(
        s || si
      );
    } else
      n.fillStyle = void 0;
    if (e) {
      const s = e.getColor();
      n.strokeStyle = Ne(
        s || Os
      );
      const r = e.getLineCap();
      n.lineCap = r !== void 0 ? r : Zr;
      const o = e.getLineDash();
      n.lineDash = o ? o.slice() : Rs;
      const a = e.getLineDashOffset();
      n.lineDashOffset = a || Ts;
      const l = e.getLineJoin();
      n.lineJoin = l !== void 0 ? l : kn;
      const h = e.getWidth();
      n.lineWidth = h !== void 0 ? h : Is;
      const c = e.getMiterLimit();
      n.miterLimit = c !== void 0 ? c : Ls, n.lineWidth > this.maxLineWidth && (this.maxLineWidth = n.lineWidth, this.bufferedMaxExtent_ = null);
    } else
      n.strokeStyle = void 0, n.lineCap = void 0, n.lineDash = null, n.lineDashOffset = void 0, n.lineJoin = void 0, n.lineWidth = void 0, n.miterLimit = void 0;
  }
  createFill(t) {
    const e = t.fillStyle, n = [Z.SET_FILL_STYLE, e];
    return typeof e != "string" && n.push(!0), n;
  }
  applyStroke(t) {
    this.instructions.push(this.createStroke(t));
  }
  createStroke(t) {
    return [
      Z.SET_STROKE_STYLE,
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
    (t.currentStrokeStyle != n || t.currentLineCap != s || r != t.currentLineDash && !sn(t.currentLineDash, r) || t.currentLineDashOffset != o || t.currentLineJoin != a || t.currentLineWidth != l || t.currentMiterLimit != h) && (n !== void 0 && e.call(this, t), t.currentStrokeStyle = n, t.currentLineCap = s, t.currentLineDash = r, t.currentLineDashOffset = o, t.currentLineJoin = a, t.currentLineWidth = l, t.currentMiterLimit = h);
  }
  endGeometry(t) {
    this.beginGeometryInstruction1_[2] = this.instructions.length, this.beginGeometryInstruction1_ = null, this.beginGeometryInstruction2_[2] = this.hitDetectionInstructions.length, this.beginGeometryInstruction2_ = null;
    const e = [Z.END_GEOMETRY, t];
    this.instructions.push(e), this.hitDetectionInstructions.push(e);
  }
  getBufferedMaxExtent() {
    if (!this.bufferedMaxExtent_ && (this.bufferedMaxExtent_ = Eu(this.maxExtent), this.maxLineWidth > 0)) {
      const t = this.resolution * (this.maxLineWidth + 1) / 2;
      uo(this.bufferedMaxExtent_, t, this.bufferedMaxExtent_);
    }
    return this.bufferedMaxExtent_;
  }
}
const Js = f2;
class g2 extends Js {
  constructor(t, e, n, s) {
    super(t, e, n, s), this.hitDetectionImage_ = null, this.image_ = null, this.imagePixelRatio_ = void 0, this.anchorX_ = void 0, this.anchorY_ = void 0, this.height_ = void 0, this.opacity_ = void 0, this.originX_ = void 0, this.originY_ = void 0, this.rotateWithView_ = void 0, this.rotation_ = void 0, this.scale_ = void 0, this.width_ = void 0, this.declutterMode_ = void 0, this.declutterImageWithText_ = void 0;
  }
  drawPoint(t, e) {
    if (!this.image_)
      return;
    this.beginGeometry(t, e);
    const n = t.getFlatCoordinates(), s = t.getStride(), r = this.coordinates.length, o = this.appendFlatPointCoordinates(n, s);
    this.instructions.push([
      Z.DRAW_IMAGE,
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
      Z.DRAW_IMAGE,
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
      Z.DRAW_IMAGE,
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
      Z.DRAW_IMAGE,
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
const m2 = g2;
class p2 extends Js {
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
      Z.MOVE_TO_LINE_TO,
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
        Z.SET_STROKE_STYLE,
        n.strokeStyle,
        n.lineWidth,
        n.lineCap,
        n.lineJoin,
        n.miterLimit,
        Rs,
        Ts
      ],
      Hi
    );
    const o = t.getFlatCoordinates(), a = t.getStride();
    this.drawFlatCoordinates_(
      o,
      0,
      o.length,
      a
    ), this.hitDetectionInstructions.push(wi), this.endGeometry(e);
  }
  drawMultiLineString(t, e) {
    const n = this.state, s = n.strokeStyle, r = n.lineWidth;
    if (s === void 0 || r === void 0)
      return;
    this.updateStrokeStyle(n, this.applyStroke), this.beginGeometry(t, e), this.hitDetectionInstructions.push(
      [
        Z.SET_STROKE_STYLE,
        n.strokeStyle,
        n.lineWidth,
        n.lineCap,
        n.lineJoin,
        n.miterLimit,
        n.lineDash,
        n.lineDashOffset
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
    this.hitDetectionInstructions.push(wi), this.endGeometry(e);
  }
  finish() {
    const t = this.state;
    return t.lastStroke != null && t.lastStroke != this.coordinates.length && this.instructions.push(wi), this.reverseHitDetectionInstructions(), this.state = null, super.finish();
  }
  applyStroke(t) {
    t.lastStroke != null && t.lastStroke != this.coordinates.length && (this.instructions.push(wi), t.lastStroke = this.coordinates.length), t.lastStroke = 0, super.applyStroke(t), this.instructions.push(Hi);
  }
}
const v2 = p2;
class y2 extends Js {
  constructor(t, e, n, s) {
    super(t, e, n, s);
  }
  drawFlatCoordinatess_(t, e, n, s) {
    const r = this.state, o = r.fillStyle !== void 0, a = r.strokeStyle !== void 0, l = n.length;
    this.instructions.push(Hi), this.hitDetectionInstructions.push(Hi);
    for (let h = 0; h < l; ++h) {
      const c = n[h], u = this.coordinates.length, d = this.appendFlatLineCoordinates(
        t,
        e,
        c,
        s,
        !0,
        !a
      ), f = [
        Z.MOVE_TO_LINE_TO,
        u,
        d
      ];
      this.instructions.push(f), this.hitDetectionInstructions.push(f), a && (this.instructions.push(Zh), this.hitDetectionInstructions.push(Zh)), e = c;
    }
    return o && (this.instructions.push(wr), this.hitDetectionInstructions.push(wr)), a && (this.instructions.push(wi), this.hitDetectionInstructions.push(wi)), e;
  }
  drawCircle(t, e) {
    const n = this.state, s = n.fillStyle, r = n.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), n.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      Z.SET_FILL_STYLE,
      si
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      Z.SET_STROKE_STYLE,
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
    const h = [Z.CIRCLE, l];
    this.instructions.push(Hi, h), this.hitDetectionInstructions.push(Hi, h), n.fillStyle !== void 0 && (this.instructions.push(wr), this.hitDetectionInstructions.push(wr)), n.strokeStyle !== void 0 && (this.instructions.push(wi), this.hitDetectionInstructions.push(wi)), this.endGeometry(e);
  }
  drawPolygon(t, e) {
    const n = this.state, s = n.fillStyle, r = n.strokeStyle;
    if (s === void 0 && r === void 0)
      return;
    this.setFillStrokeStyles_(), this.beginGeometry(t, e), n.fillStyle !== void 0 && this.hitDetectionInstructions.push([
      Z.SET_FILL_STYLE,
      si
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      Z.SET_STROKE_STYLE,
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
      Z.SET_FILL_STYLE,
      si
    ]), n.strokeStyle !== void 0 && this.hitDetectionInstructions.push([
      Z.SET_STROKE_STYLE,
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
        e[n] = ji(e[n], t);
    }
    return super.finish();
  }
  setFillStrokeStyles_() {
    const t = this.state;
    t.fillStyle !== void 0 && this.updateFillStyle(t, this.createFill), t.strokeStyle !== void 0 && this.updateStrokeStyle(t, this.applyStroke);
  }
}
const Bh = y2;
function x2(i, t, e, n, s) {
  let r = e, o = e, a = 0, l = 0, h = e, c, u, d, f, g, m, p, v, y, x;
  for (u = e; u < n; u += s) {
    const M = t[u], C = t[u + 1];
    g !== void 0 && (y = M - g, x = C - m, f = Math.sqrt(y * y + x * x), p !== void 0 && (l += d, c = Math.acos((p * y + v * x) / (d * f)), c > i && (l > a && (a = l, r = h, o = u), l = 0, h = u - s)), d = f, p = y, v = x), g = M, m = C;
  }
  return l += f, l > a ? [h, u] : [r, o];
}
const Cs = {
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
class M2 extends Js {
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
        for (let p = 0, v = m.length; p < v; ++p)
          u.push(m[p][0]);
      }
      this.beginGeometry(t, e);
      const d = r.textAlign;
      let f = 0, g;
      for (let m = 0, p = u.length; m < p; ++m) {
        if (d == null) {
          const y = x2(
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
        const v = o.length;
        f = u[m], this.drawChars_(a, v), a = v;
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
          for (let v = 0, y = p.length; v < y; v += 3)
            r.overflow || u.push(p[v + 2] / this.resolution), h.push(p[v], p[v + 1]);
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
        u = u.filter((v, y) => {
          const x = o[(p + y) * 2] === h[y * c] && o[(p + y) * 2 + 1] === h[y * c + 1];
          return x || --p, x;
        });
      }
      this.saveTextStates_(), (r.backgroundFill || r.backgroundStroke) && (this.setFillStrokeStyle(
        r.backgroundFill,
        r.backgroundStroke
      ), r.backgroundFill && (this.updateFillStyle(this.state, this.createFill), this.hitDetectionInstructions.push(this.createFill(this.state))), r.backgroundStroke && (this.updateStrokeStyle(this.state, this.applyStroke), this.hitDetectionInstructions.push(this.createStroke(this.state)))), this.beginGeometry(t, e);
      let f = r.padding;
      if (f != ki && (r.scale[0] < 0 || r.scale[1] < 0)) {
        let p = r.padding[0], v = r.padding[1], y = r.padding[2], x = r.padding[3];
        r.scale[0] < 0 && (v = -v, x = -x), r.scale[1] < 0 && (p = -p, y = -y), f = [p, v, y, x];
      }
      const g = this.pixelRatio;
      this.instructions.push([
        Z.DRAW_IMAGE,
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
        Z.DRAW_IMAGE,
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
      textAlign: e.textAlign || As,
      justify: e.justify,
      textBaseline: e.textBaseline || Br,
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
    const l = this.pixelRatio, h = Cs[s.textBaseline], c = this.textOffsetY_ * l, u = this.text_, d = n ? n.lineWidth * Math.abs(s.scale[0]) / 2 : 0;
    this.instructions.push([
      Z.DRAW_CHARS,
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
      Z.DRAW_CHARS,
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
      o ? (s = this.textFillState_, s || (s = {}, this.textFillState_ = s), s.fillStyle = Ne(
        o.getColor() || si
      )) : (s = null, this.textFillState_ = s);
      const a = t.getStroke();
      if (!a)
        r = null, this.textStrokeState_ = r;
      else {
        r = this.textStrokeState_, r || (r = {}, this.textStrokeState_ = r);
        const g = a.getLineDash(), m = a.getLineDashOffset(), p = a.getWidth(), v = a.getMiterLimit();
        r.lineCap = a.getLineCap() || Zr, r.lineDash = g ? g.slice() : Rs, r.lineDashOffset = m === void 0 ? Ts : m, r.lineJoin = a.getLineJoin() || kn, r.lineWidth = p === void 0 ? Is : p, r.miterLimit = v === void 0 ? Ls : v, r.strokeStyle = Ne(
          a.getColor() || Os
        );
      }
      n = this.textState_;
      const l = t.getFont() || Hu;
      Z0(l);
      const h = t.getScaleArray();
      n.overflow = t.getOverflow(), n.font = l, n.maxAngle = t.getMaxAngle(), n.placement = t.getPlacement(), n.textAlign = t.getTextAlign(), n.justify = t.getJustify(), n.textBaseline = t.getTextBaseline() || Br, n.backgroundFill = t.getBackgroundFill(), n.backgroundStroke = t.getBackgroundStroke(), n.padding = t.getPadding() || ki, n.scale = h === void 0 ? [1, 1] : h;
      const c = t.getOffsetX(), u = t.getOffsetY(), d = t.getRotateWithView(), f = t.getRotation();
      this.text_ = t.getText() || "", this.textOffsetX_ = c === void 0 ? 0 : c, this.textOffsetY_ = u === void 0 ? 0 : u, this.textRotateWithView_ = d === void 0 ? !1 : d, this.textRotation_ = f === void 0 ? 0 : f, this.strokeKey_ = r ? (typeof r.strokeStyle == "string" ? r.strokeStyle : rt(r.strokeStyle)) + r.lineCap + r.lineDashOffset + "|" + r.lineWidth + r.lineJoin + r.miterLimit + "[" + r.lineDash.join() + "]" : "", this.textKey_ = n.font + n.scale + (n.textAlign || "?") + (n.justify || "?") + (n.textBaseline || "?"), this.fillKey_ = s ? typeof s.fillStyle == "string" ? s.fillStyle : "|" + rt(s.fillStyle) : "";
    }
    this.declutterImageWithText_ = e;
  }
}
const C2 = {
  Circle: Bh,
  Default: Js,
  Image: m2,
  LineString: v2,
  Polygon: Bh,
  Text: M2
};
class w2 {
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
      const o = C2[e];
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
const Wh = w2;
class E2 extends yu {
  constructor(t) {
    super(), this.ready = !0, this.boundHandleImageChange_ = this.handleImageChange_.bind(this), this.layer_ = t, this.declutterExecutorGroup = null;
  }
  getFeatures(t) {
    return B();
  }
  getData(t) {
    return null;
  }
  prepareFrame(t) {
    return B();
  }
  renderFrame(t, e) {
    return B();
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
    t.target.getState() === Ot.LOADED && this.renderIfReadyAndVisible();
  }
  loadImage(t) {
    let e = t.getState();
    return e != Ot.LOADED && e != Ot.ERROR && t.addEventListener(V.CHANGE, this.boundHandleImageChange_), e == Ot.IDLE && (t.load(), e = t.getState()), e == Ot.LOADED;
  }
  renderIfReadyAndVisible() {
    const t = this.getLayer();
    t && t.getVisible() && t.getSourceState() === "ready" && t.changed();
  }
  disposeInternal() {
    delete this.layer_, super.disposeInternal();
  }
}
const b2 = E2, Vh = [];
let En = null;
function P2() {
  const i = document.createElement("canvas");
  i.width = 1, i.height = 1, En = i.getContext("2d");
}
class S2 extends b2 {
  constructor(t) {
    super(t), this.container = null, this.renderedResolution, this.tempTransform = Fe(), this.pixelTransform = Fe(), this.inversePixelTransform = Fe(), this.context = null, this.containerReused = !1, this.pixelContext_ = null, this.frameState = null;
  }
  getImageData(t, e, n) {
    En || P2(), En.clearRect(0, 0, 1, 1);
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
    if (t && t.className === s && (!n || t && t.style.backgroundColor && sn(
      jr(t.style.backgroundColor),
      jr(n)
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
    const s = Ai(n), r = po(n), o = mo(n), a = go(n);
    Ft(e.coordinateToPixelTransform, s), Ft(e.coordinateToPixelTransform, r), Ft(e.coordinateToPixelTransform, o), Ft(e.coordinateToPixelTransform, a);
    const l = this.inversePixelTransform;
    Ft(l, s), Ft(l, r), Ft(l, o), Ft(l, a), t.save(), t.beginPath(), t.moveTo(Math.round(s[0]), Math.round(s[1])), t.lineTo(Math.round(r[0]), Math.round(r[1])), t.lineTo(Math.round(o[0]), Math.round(o[1])), t.lineTo(Math.round(a[0]), Math.round(a[1])), t.clip();
  }
  dispatchRenderEvent_(t, e, n) {
    const s = this.getLayer();
    if (s.hasListener(t)) {
      const r = new ju(
        t,
        this.inversePixelTransform,
        n,
        e
      );
      s.dispatchEvent(r);
    }
  }
  preRender(t, e) {
    this.frameState = e, this.dispatchRenderEvent_(Ei.PRERENDER, t, e);
  }
  postRender(t, e) {
    this.dispatchRenderEvent_(Ei.POSTRENDER, t, e);
  }
  getRenderTransform(t, e, n, s, r, o, a) {
    const l = r / 2, h = o / 2, c = s / e, u = -c, d = -t[0] + a, f = -t[1];
    return _i(
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
const bd = S2;
function _2(i, t, e, n, s, r, o, a, l, h, c, u) {
  let d = i[t], f = i[t + 1], g = 0, m = 0, p = 0, v = 0;
  function y() {
    g = d, m = f, t += n, d = i[t], f = i[t + 1], v += p, p = Math.sqrt((d - g) * (d - g) + (f - m) * (f - m));
  }
  do
    y();
  while (t < e - n && v + p < r);
  let x = p === 0 ? 0 : (r - v) / p;
  const M = ti(g, d, x), C = ti(m, f, x), E = t - n, b = v, S = r + a * l(h, s, c);
  for (; t < e - n && v + p < S; )
    y();
  x = p === 0 ? 0 : (S - v) / p;
  const O = ti(g, d, x), D = ti(m, f, x);
  let H;
  if (u) {
    const F = [M, C, O, D];
    Qu(F, 0, 4, 2, u, F, F), H = F[0] > F[2];
  } else
    H = M > O;
  const R = Math.PI, j = [], dt = E + n === t;
  t = E, p = 0, v = b, d = i[t], f = i[t + 1];
  let N;
  if (dt) {
    y(), N = Math.atan2(f - m, d - g), H && (N += N > 0 ? -R : R);
    const F = (O + M) / 2, L = (D + C) / 2;
    return j[0] = [F, L, (S - r) / 2, N, s], j;
  }
  s = s.replace(/\n/g, " ");
  for (let F = 0, L = s.length; F < L; ) {
    y();
    let $ = Math.atan2(f - m, d - g);
    if (H && ($ += $ > 0 ? -R : R), N !== void 0) {
      let at = $ - N;
      if (at += at > R ? -2 * R : at < -R ? 2 * R : 0, Math.abs(at) > o)
        return null;
    }
    N = $;
    const wt = F;
    let vt = 0;
    for (; F < L; ++F) {
      const at = H ? L - F - 1 : F, ft = a * l(h, s[at], c);
      if (t + n < e && v + p < r + vt + ft / 2)
        break;
      vt += ft;
    }
    if (F === wt)
      continue;
    const It = H ? s.substring(L - wt, L - F) : s.substring(wt, F);
    x = p === 0 ? 0 : (r + vt / 2 - v) / p;
    const _ = ti(g, d, x), ae = ti(m, f, x);
    j.push([_, ae, vt / 2, $, It]), r += vt;
  }
  return j;
}
const pn = fe(), fi = [], Ue = [], Je = [], gi = [];
function Yh(i) {
  return i[3].declutterBox;
}
const R2 = new RegExp(
  "[" + String.fromCharCode(1425) + "-" + String.fromCharCode(2303) + String.fromCharCode(64285) + "-" + String.fromCharCode(65023) + String.fromCharCode(65136) + "-" + String.fromCharCode(65276) + String.fromCharCode(67584) + "-" + String.fromCharCode(69631) + String.fromCharCode(124928) + "-" + String.fromCharCode(126975) + "]"
);
function Uh(i, t) {
  return (t === "start" || t === "end") && !R2.test(i) && (t = t === "start" ? "left" : "right"), Cs[t];
}
function T2(i, t, e) {
  return e > 0 && i.push(`
`, ""), i.push(t, ""), i;
}
class L2 {
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
    ], u = Array.isArray(t), d = l.justify ? Cs[l.justify] : Uh(
      Array.isArray(t) ? t[0] : t,
      l.textAlign || As
    ), f = s && o.lineWidth ? o.lineWidth : 0, g = u ? t : t.split(`
`).reduce(T2, []), { width: m, height: p, widths: v, heights: y, lineWidths: x } = W0(
      l,
      g
    ), M = m + f, C = [], E = (M + 2) * c[0], b = (p + f) * c[1], S = {
      width: E < 0 ? Math.floor(E) : Math.ceil(E),
      height: b < 0 ? Math.floor(b) : Math.ceil(b),
      contextInstructions: C
    };
    (c[0] != 1 || c[1] != 1) && C.push("scale", c), s && (C.push("strokeStyle", o.strokeStyle), C.push("lineWidth", f), C.push("lineCap", o.lineCap), C.push("lineJoin", o.lineJoin), C.push("miterLimit", o.miterLimit), C.push("setLineDash", [o.lineDash]), C.push("lineDashOffset", o.lineDashOffset)), n && C.push("fillStyle", a.fillStyle), C.push("textBaseline", "middle"), C.push("textAlign", "center");
    const O = 0.5 - d;
    let D = d * M + O * f;
    const H = [], R = [];
    let j = 0, dt = 0, N = 0, F = 0, L;
    for (let $ = 0, wt = g.length; $ < wt; $ += 2) {
      const vt = g[$];
      if (vt === `
`) {
        dt += j, j = 0, D = d * M + O * f, ++F;
        continue;
      }
      const It = g[$ + 1] || l.font;
      It !== L && (s && H.push("font", It), n && R.push("font", It), L = It), j = Math.max(j, y[N]);
      const _ = [
        vt,
        D + O * v[N] + d * (v[N] - x[F]),
        0.5 * (f + j) + dt
      ];
      D += v[N], s && H.push("strokeText", _), n && R.push("fillText", _), ++N;
    }
    return Array.prototype.push.apply(C, H), Array.prototype.push.apply(C, R), this.labels_[r] = S, S;
  }
  replayTextBackground_(t, e, n, s, r, o, a) {
    t.beginPath(), t.moveTo.apply(t, e), t.lineTo.apply(t, n), t.lineTo.apply(t, s), t.lineTo.apply(t, r), t.lineTo.apply(t, e), o && (this.alignFill_ = o[2], this.fill_(t)), a && (this.setStrokeStyle_(
      t,
      a
    ), t.stroke());
  }
  calculateImageOrLabelDimensions_(t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p) {
    a *= d[0], l *= d[1];
    let v = n - a, y = s - l;
    const x = r + h > t ? t - h : r, M = o + c > e ? e - c : o, C = g[3] + x * d[0] + g[1], E = g[0] + M * d[1] + g[2], b = v - g[3], S = y - g[0];
    (m || u !== 0) && (fi[0] = b, gi[0] = b, fi[1] = S, Ue[1] = S, Ue[0] = b + C, Je[0] = Ue[0], Je[1] = S + E, gi[1] = Je[1]);
    let O;
    return u !== 0 ? (O = _i(
      Fe(),
      n,
      s,
      1,
      1,
      u,
      -n,
      -s
    ), Ft(O, fi), Ft(O, Ue), Ft(O, Je), Ft(O, gi), Me(
      Math.min(fi[0], Ue[0], Je[0], gi[0]),
      Math.min(fi[1], Ue[1], Je[1], gi[1]),
      Math.max(fi[0], Ue[0], Je[0], gi[0]),
      Math.max(fi[1], Ue[1], Je[1], gi[1]),
      pn
    )) : Me(
      Math.min(b, b + C),
      Math.min(S, S + E),
      Math.max(b, b + C),
      Math.max(S, S + E),
      pn
    ), f && (v = Math.round(v), y = Math.round(y)), {
      drawImageX: v,
      drawImageY: y,
      drawImageW: x,
      drawImageH: M,
      originX: h,
      originY: c,
      declutterBox: {
        minX: pn[0],
        minY: pn[1],
        maxX: pn[2],
        maxY: pn[3],
        value: p
      },
      canvasTransform: O,
      scale: d
    };
  }
  replayImageOrLabel_(t, e, n, s, r, o, a) {
    const l = !!(o || a), h = s.declutterBox, c = t.canvas, u = a ? a[2] * s.scale[0] / 2 : 0;
    return h.minX - u <= c.width / e && h.maxX + u >= 0 && h.minY - u <= c.height / e && h.maxY + u >= 0 && (l && this.replayTextBackground_(
      t,
      fi,
      Ue,
      Je,
      gi,
      o,
      a
    ), V0(
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
    const r = this.textStates[e], o = this.createLabel(t, e, s, n), a = this.strokeStates[n], l = this.pixelRatio, h = Uh(
      Array.isArray(t) ? t[0] : t,
      r.textAlign || As
    ), c = Cs[r.textBaseline || Br], u = a && a.lineWidth ? a.lineWidth : 0, d = o.width / l - 2 * r.scale[0], f = h * d + 2 * (0.5 - h) * u, g = c * o.height / l + 2 * (0.5 - c) * u;
    return {
      label: o,
      anchorX: f,
      anchorY: g
    };
  }
  execute_(t, e, n, s, r, o, a, l) {
    let h;
    this.pixelCoordinates_ && sn(n, this.renderedTransform_) ? h = this.pixelCoordinates_ : (this.pixelCoordinates_ || (this.pixelCoordinates_ = []), h = Yi(
      this.coordinates,
      0,
      this.coordinates.length,
      2,
      n,
      this.pixelCoordinates_
    ), g0(this.renderedTransform_, n));
    let c = 0;
    const u = s.length;
    let d = 0, f, g, m, p, v, y, x, M, C, E, b, S, O = 0, D = 0, H = null, R = null;
    const j = this.coordinateCache_, dt = this.viewRotation_, N = Math.round(Math.atan2(-n[1], n[0]) * 1e12) / 1e12, F = {
      context: t,
      pixelRatio: this.pixelRatio,
      resolution: this.resolution,
      rotation: dt
    }, L = this.instructions != s || this.overlaps ? 0 : 200;
    let $, wt, vt, It;
    for (; c < u; ) {
      const _ = s[c];
      switch (_[0]) {
        case Z.BEGIN_GEOMETRY:
          $ = _[1], It = _[3], $.getGeometry() ? a !== void 0 && !ie(a, It.getExtent()) ? c = _[2] + 1 : ++c : c = _[2];
          break;
        case Z.BEGIN_PATH:
          O > L && (this.fill_(t), O = 0), D > L && (t.stroke(), D = 0), !O && !D && (t.beginPath(), p = NaN, v = NaN), ++c;
          break;
        case Z.CIRCLE:
          d = _[1];
          const at = h[d], ft = h[d + 1], hi = h[d + 2], Le = h[d + 3], kt = hi - at, Be = Le - ft, ln = Math.sqrt(kt * kt + Be * Be);
          t.moveTo(at + ln, ft), t.arc(at, ft, ln, 0, 2 * Math.PI, !0), ++c;
          break;
        case Z.CLOSE_PATH:
          t.closePath(), ++c;
          break;
        case Z.CUSTOM:
          d = _[1], f = _[2];
          const rr = _[3], hn = _[4], or = _.length == 6 ? _[5] : void 0;
          F.geometry = rr, F.feature = $, c in j || (j[c] = []);
          const ci = j[c];
          or ? or(h, d, f, 2, ci) : (ci[0] = h[d], ci[1] = h[d + 1], ci.length = 2), hn(ci, F), ++c;
          break;
        case Z.DRAW_IMAGE:
          d = _[1], f = _[2], M = _[3], g = _[4], m = _[5];
          let ss = _[6];
          const ui = _[7], ar = _[8], lr = _[9], hr = _[10];
          let cn = _[11];
          const Io = _[12];
          let Qt = _[13];
          const me = _[14], we = _[15];
          if (!M && _.length >= 20) {
            C = _[19], E = _[20], b = _[21], S = _[22];
            const le = this.drawLabelWithPointPlacement_(
              C,
              E,
              b,
              S
            );
            M = le.label, _[3] = M;
            const fn = _[23];
            g = (le.anchorX - fn) * this.pixelRatio, _[4] = g;
            const pe = _[24];
            m = (le.anchorY - pe) * this.pixelRatio, _[5] = m, ss = M.height, _[6] = ss, Qt = M.width, _[13] = Qt;
          }
          let We;
          _.length > 25 && (We = _[25]);
          let un, Ni, di;
          _.length > 17 ? (un = _[16], Ni = _[17], di = _[18]) : (un = ki, Ni = !1, di = !1), hr && N ? cn += dt : !hr && !N && (cn -= dt);
          let dn = 0;
          for (; d < f; d += 2) {
            if (We && We[dn++] < Qt / this.pixelRatio)
              continue;
            const le = this.calculateImageOrLabelDimensions_(
              M.width,
              M.height,
              h[d],
              h[d + 1],
              Qt,
              ss,
              g,
              m,
              ar,
              lr,
              cn,
              Io,
              r,
              un,
              Ni || di,
              $
            ), fn = [
              t,
              e,
              M,
              le,
              ui,
              Ni ? H : null,
              di ? R : null
            ];
            if (l) {
              if (me === "none")
                continue;
              if (me === "obstacle") {
                l.insert(le.declutterBox);
                continue;
              } else {
                let pe, Ve;
                if (we) {
                  const he = f - d;
                  if (!we[he]) {
                    we[he] = fn;
                    continue;
                  }
                  if (pe = we[he], delete we[he], Ve = Yh(pe), l.collides(Ve))
                    continue;
                }
                if (l.collides(le.declutterBox))
                  continue;
                pe && (l.insert(Ve), this.replayImageOrLabel_.apply(this, pe)), l.insert(le.declutterBox);
              }
            }
            this.replayImageOrLabel_.apply(this, fn);
          }
          ++c;
          break;
        case Z.DRAW_CHARS:
          const cr = _[1], Vt = _[2], No = _[3], Ff = _[4];
          S = _[5];
          const Df = _[6], ql = _[7], Kl = _[8];
          b = _[9];
          const zo = _[10];
          C = _[11], E = _[12];
          const Ql = [
            _[13],
            _[13]
          ], Fo = this.textStates[E], rs = Fo.font, os = [
            Fo.scale[0] * ql,
            Fo.scale[1] * ql
          ];
          let as;
          rs in this.widths_ ? as = this.widths_[rs] : (as = {}, this.widths_[rs] = as);
          const $l = vd(h, cr, Vt, 2), th = Math.abs(os[0]) * wh(rs, C, as);
          if (Ff || th <= $l) {
            const le = this.textStates[E].textAlign, fn = ($l - th) * Cs[le], pe = _2(
              h,
              cr,
              Vt,
              2,
              C,
              fn,
              Df,
              Math.abs(os[0]),
              wh,
              rs,
              as,
              N ? 0 : this.viewRotation_
            );
            t:
              if (pe) {
                const Ve = [];
                let he, ur, dr, $t, ve;
                if (b)
                  for (he = 0, ur = pe.length; he < ur; ++he) {
                    ve = pe[he], dr = ve[4], $t = this.createLabel(dr, E, "", b), g = ve[2] + (os[0] < 0 ? -zo : zo), m = No * $t.height + (0.5 - No) * 2 * zo * os[1] / os[0] - Kl;
                    const Ye = this.calculateImageOrLabelDimensions_(
                      $t.width,
                      $t.height,
                      ve[0],
                      ve[1],
                      $t.width,
                      $t.height,
                      g,
                      m,
                      0,
                      0,
                      ve[3],
                      Ql,
                      !1,
                      ki,
                      !1,
                      $
                    );
                    if (l && l.collides(Ye.declutterBox))
                      break t;
                    Ve.push([
                      t,
                      e,
                      $t,
                      Ye,
                      1,
                      null,
                      null
                    ]);
                  }
                if (S)
                  for (he = 0, ur = pe.length; he < ur; ++he) {
                    ve = pe[he], dr = ve[4], $t = this.createLabel(dr, E, S, ""), g = ve[2], m = No * $t.height - Kl;
                    const Ye = this.calculateImageOrLabelDimensions_(
                      $t.width,
                      $t.height,
                      ve[0],
                      ve[1],
                      $t.width,
                      $t.height,
                      g,
                      m,
                      0,
                      0,
                      ve[3],
                      Ql,
                      !1,
                      ki,
                      !1,
                      $
                    );
                    if (l && l.collides(Ye.declutterBox))
                      break t;
                    Ve.push([
                      t,
                      e,
                      $t,
                      Ye,
                      1,
                      null,
                      null
                    ]);
                  }
                l && l.load(Ve.map(Yh));
                for (let Ye = 0, jf = Ve.length; Ye < jf; ++Ye)
                  this.replayImageOrLabel_.apply(this, Ve[Ye]);
              }
          }
          ++c;
          break;
        case Z.END_GEOMETRY:
          if (o !== void 0) {
            $ = _[1];
            const le = o($, It);
            if (le)
              return le;
          }
          ++c;
          break;
        case Z.FILL:
          L ? O++ : this.fill_(t), ++c;
          break;
        case Z.MOVE_TO_LINE_TO:
          for (d = _[1], f = _[2], wt = h[d], vt = h[d + 1], y = wt + 0.5 | 0, x = vt + 0.5 | 0, (y !== p || x !== v) && (t.moveTo(wt, vt), p = y, v = x), d += 2; d < f; d += 2)
            wt = h[d], vt = h[d + 1], y = wt + 0.5 | 0, x = vt + 0.5 | 0, (d == f - 2 || y !== p || x !== v) && (t.lineTo(wt, vt), p = y, v = x);
          ++c;
          break;
        case Z.SET_FILL_STYLE:
          H = _, this.alignFill_ = _[2], O && (this.fill_(t), O = 0, D && (t.stroke(), D = 0)), t.fillStyle = _[1], ++c;
          break;
        case Z.SET_STROKE_STYLE:
          R = _, D && (t.stroke(), D = 0), this.setStrokeStyle_(t, _), ++c;
          break;
        case Z.STROKE:
          L ? D++ : t.stroke(), ++c;
          break;
        default:
          ++c;
          break;
      }
    }
    O && this.fill_(t), D && t.stroke();
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
const O2 = L2, Ko = ["Polygon", "Circle", "LineString", "Image", "Text", "Default"];
class A2 {
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
        n[r] = new O2(
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
    const a = s * 2 + 1, l = _i(
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
    this.renderBuffer_ !== void 0 && (u = fe(), ys(u, t), uo(
      u,
      e * (this.renderBuffer_ + s),
      u
    ));
    const d = I2(s);
    let f;
    function g(C, E) {
      const b = c.getImageData(
        0,
        0,
        a,
        a
      ).data;
      for (let S = 0, O = d.length; S < O; S++)
        if (b[d[S]] > 0) {
          if (!o || f !== "Image" && f !== "Text" || o.includes(C)) {
            const D = (d[S] - 3) / 4, H = s - D % a, R = s - (D / a | 0), j = r(C, E, H * H + R * R);
            if (j)
              return j;
          }
          c.clearRect(0, 0, a, a);
          break;
        }
    }
    const m = Object.keys(this.executorsByZIndex_).map(Number);
    m.sort(qi);
    let p, v, y, x, M;
    for (p = m.length - 1; p >= 0; --p) {
      const C = m[p].toString();
      for (y = this.executorsByZIndex_[C], v = Ko.length - 1; v >= 0; --v)
        if (f = Ko[v], x = y[f], x !== void 0 && (M = x.executeHitDetection(
          c,
          l,
          n,
          g,
          u
        ), M))
          return M;
    }
  }
  getClipCoords(t) {
    const e = this.maxExtent_;
    if (!e)
      return null;
    const n = e[0], s = e[1], r = e[2], o = e[3], a = [n, s, n, o, r, o, r, s];
    return Yi(a, 0, 8, 2, t, a), a;
  }
  isEmpty() {
    return jn(this.executorsByZIndex_);
  }
  execute(t, e, n, s, r, o, a) {
    const l = Object.keys(this.executorsByZIndex_).map(Number);
    l.sort(qi), this.maxExtent_ && (t.save(), this.clip(t, n)), o = o || Ko;
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
const Qo = {};
function I2(i) {
  if (Qo[i] !== void 0)
    return Qo[i];
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
  return Qo[i] = s, s;
}
const Jh = A2;
class N2 extends Ed {
  constructor(t, e, n, s, r, o, a) {
    super(), this.context_ = t, this.pixelRatio_ = e, this.extent_ = n, this.transform_ = s, this.viewRotation_ = r, this.squaredTolerance_ = o, this.userTransform_ = a, this.contextFillState_ = null, this.contextStrokeState_ = null, this.contextTextState_ = null, this.fillState_ = null, this.strokeState_ = null, this.image_ = null, this.imageAnchorX_ = 0, this.imageAnchorY_ = 0, this.imageHeight_ = 0, this.imageOpacity_ = 0, this.imageOriginX_ = 0, this.imageOriginY_ = 0, this.imageRotateWithView_ = !1, this.imageRotation_ = 0, this.imageScale_ = [0, 0], this.imageWidth_ = 0, this.text_ = "", this.textOffsetX_ = 0, this.textOffsetY_ = 0, this.textRotateWithView_ = !1, this.textRotation_ = 0, this.textScale_ = [0, 0], this.textFillState_ = null, this.textStrokeState_ = null, this.textState_ = null, this.pixelCoordinates_ = [], this.tmpLocalTransform_ = Fe();
  }
  drawImages_(t, e, n, s) {
    if (!this.image_)
      return;
    const r = Yi(
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
        _i(
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
    const r = Yi(
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
    const o = this.context_, a = Yi(
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
        const e = Ig(
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
    n ? (n.lineCap != t.lineCap && (n.lineCap = t.lineCap, e.lineCap = t.lineCap), sn(n.lineDash, t.lineDash) || e.setLineDash(
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
    const e = this.context_, n = this.contextTextState_, s = t.textAlign ? t.textAlign : As;
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
        fillStyle: Ne(
          n || si
        )
      };
    }
    if (!e)
      this.strokeState_ = null;
    else {
      const n = e.getColor(), s = e.getLineCap(), r = e.getLineDash(), o = e.getLineDashOffset(), a = e.getLineJoin(), l = e.getWidth(), h = e.getMiterLimit(), c = r || Rs;
      this.strokeState_ = {
        lineCap: s !== void 0 ? s : Zr,
        lineDash: this.pixelRatio_ === 1 ? c : c.map((u) => u * this.pixelRatio_),
        lineDashOffset: (o || Ts) * this.pixelRatio_,
        lineJoin: a !== void 0 ? a : kn,
        lineWidth: (l !== void 0 ? l : Is) * this.pixelRatio_,
        miterLimit: h !== void 0 ? h : Ls,
        strokeStyle: Ne(
          n || Os
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
          fillStyle: Ne(
            f || si
          )
        };
      }
      const n = t.getStroke();
      if (!n)
        this.textStrokeState_ = null;
      else {
        const f = n.getColor(), g = n.getLineCap(), m = n.getLineDash(), p = n.getLineDashOffset(), v = n.getLineJoin(), y = n.getWidth(), x = n.getMiterLimit();
        this.textStrokeState_ = {
          lineCap: g !== void 0 ? g : Zr,
          lineDash: m || Rs,
          lineDashOffset: p || Ts,
          lineJoin: v !== void 0 ? v : kn,
          lineWidth: y !== void 0 ? y : Is,
          miterLimit: x !== void 0 ? x : Ls,
          strokeStyle: Ne(
            f || Os
          )
        };
      }
      const s = t.getFont(), r = t.getOffsetX(), o = t.getOffsetY(), a = t.getRotateWithView(), l = t.getRotation(), h = t.getScaleArray(), c = t.getText(), u = t.getTextAlign(), d = t.getTextBaseline();
      this.textState_ = {
        font: s !== void 0 ? s : Hu,
        textAlign: u !== void 0 ? u : As,
        textBaseline: d !== void 0 ? d : Br
      }, this.text_ = c !== void 0 ? Array.isArray(c) ? c.reduce((f, g, m) => f += m % 2 ? " " : g, "") : c : "", this.textOffsetX_ = r !== void 0 ? this.pixelRatio_ * r : 0, this.textOffsetY_ = o !== void 0 ? this.pixelRatio_ * o : 0, this.textRotateWithView_ = a !== void 0 ? a : !1, this.textRotation_ = l !== void 0 ? l : 0, this.textScale_ = [
        this.pixelRatio_ * h[0],
        this.pixelRatio_ * h[1]
      ];
    }
  }
}
const Pd = N2, Ae = 0.5;
function z2(i, t, e, n, s, r, o) {
  const a = i[0] * Ae, l = i[1] * Ae, h = ge(a, l);
  h.imageSmoothingEnabled = !1;
  const c = h.canvas, u = new Pd(
    h,
    Ae,
    s,
    null,
    o
  ), d = e.length, f = Math.floor((256 * 256 * 256 - 1) / d), g = {};
  for (let p = 1; p <= d; ++p) {
    const v = e[p - 1], y = v.getStyleFunction() || n;
    if (!n)
      continue;
    let x = y(v, r);
    if (!x)
      continue;
    Array.isArray(x) || (x = [x]);
    const C = "#" + ("000000" + (p * f).toString(16)).slice(-6);
    for (let E = 0, b = x.length; E < b; ++E) {
      const S = x[E], O = S.getGeometryFunction()(v);
      if (!O || !ie(s, O.getExtent()))
        continue;
      const D = S.clone(), H = D.getFill();
      H && H.setColor(C);
      const R = D.getStroke();
      R && (R.setColor(C), R.setLineDash(null)), D.setText(void 0);
      const j = S.getImage();
      if (j && j.getOpacity() !== 0) {
        const F = j.getImageSize();
        if (!F)
          continue;
        const L = ge(
          F[0],
          F[1],
          void 0,
          { alpha: !1 }
        ), $ = L.canvas;
        L.fillStyle = C, L.fillRect(0, 0, $.width, $.height), D.setImage(
          new Ms({
            img: $,
            imgSize: F,
            anchor: j.getAnchor(),
            anchorXUnits: "pixels",
            anchorYUnits: "pixels",
            offset: j.getOrigin(),
            opacity: 1,
            size: j.getSize(),
            scale: j.getScale(),
            rotation: j.getRotation(),
            rotateWithView: j.getRotateWithView()
          })
        );
      }
      const dt = D.getZIndex() || 0;
      let N = g[dt];
      N || (N = {}, g[dt] = N, N.Polygon = [], N.Circle = [], N.LineString = [], N.Point = []), N[O.getType().replace("Multi", "")].push(
        O,
        D
      );
    }
  }
  const m = Object.keys(g).map(Number).sort(qi);
  for (let p = 0, v = m.length; p < v; ++p) {
    const y = g[m[p]];
    for (const x in y) {
      const M = y[x];
      for (let C = 0, E = M.length; C < E; C += 2) {
        u.setStyle(M[C + 1]);
        for (let b = 0, S = t.length; b < S; ++b)
          u.setTransform(t[b]), u.drawGeometry(M[C]);
      }
    }
  }
  return h.getImageData(0, 0, c.width, c.height);
}
function F2(i, t, e) {
  const n = [];
  if (e) {
    const s = Math.floor(Math.round(i[0]) * Ae), r = Math.floor(Math.round(i[1]) * Ae), o = (Pt(s, 0, e.width - 1) + Pt(r, 0, e.height - 1) * e.width) * 4, a = e.data[o], l = e.data[o + 1], c = e.data[o + 2] + 256 * (l + 256 * a), u = Math.floor((256 * 256 * 256 - 1) / t.length);
    c && c % u === 0 && n.push(t[c / u - 1]);
  }
  return n;
}
const D2 = 0.5, Sd = {
  Point: W2,
  LineString: H2,
  Polygon: Y2,
  MultiPoint: V2,
  MultiLineString: Z2,
  MultiPolygon: B2,
  GeometryCollection: G2,
  Circle: k2
};
function j2(i, t) {
  return parseInt(rt(i), 10) - parseInt(rt(t), 10);
}
function _d(i, t) {
  const e = Sa(i, t);
  return e * e;
}
function Sa(i, t) {
  return D2 * i / t;
}
function k2(i, t, e, n, s) {
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
function qh(i, t, e, n, s, r, o) {
  let a = !1;
  const l = e.getImage();
  if (l) {
    const h = l.getImageState();
    h == Ot.LOADED || h == Ot.ERROR ? l.unlistenImageChange(s) : (h == Ot.IDLE && l.load(), l.listenImageChange(s), a = !0);
  }
  return X2(
    i,
    t,
    e,
    n,
    r,
    o
  ), a;
}
function X2(i, t, e, n, s, r) {
  const o = e.getGeometryFunction()(t);
  if (!o)
    return;
  const a = o.simplifyTransformed(
    n,
    s
  );
  if (e.getRenderer())
    Rd(i, a, e, t);
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
function Rd(i, t, e, n) {
  if (t.getType() == "GeometryCollection") {
    const r = t.getGeometries();
    for (let o = 0, a = r.length; o < a; ++o)
      Rd(i, r[o], e, n);
    return;
  }
  i.getBuilder(e.getZIndex(), "Default").drawCustom(
    t,
    n,
    e.getRenderer(),
    e.getHitDetectionRenderer()
  );
}
function G2(i, t, e, n, s) {
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
function H2(i, t, e, n, s) {
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
function Z2(i, t, e, n, s) {
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
function B2(i, t, e, n, s) {
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
function W2(i, t, e, n, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != Ot.LOADED)
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
function V2(i, t, e, n, s) {
  const r = e.getImage(), o = e.getText();
  let a;
  if (r) {
    if (r.getImageState() != Ot.LOADED)
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
function Y2(i, t, e, n, s) {
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
class U2 extends bd {
  constructor(t) {
    super(t), this.boundHandleStyleImageChange_ = this.handleStyleImageChange_.bind(this), this.animatingOrInteracting_, this.hitDetectionImageData_ = null, this.renderedFeatures_ = null, this.renderedRevision_ = -1, this.renderedResolution_ = NaN, this.renderedExtent_ = fe(), this.wrappedRenderedExtent_ = fe(), this.renderedRotation_, this.renderedCenter_ = null, this.renderedProjection_ = null, this.renderedRenderOrder_ = null, this.replayGroup_ = null, this.replayGroupChanged = !0, this.declutterExecutorGroup = null, this.clipping = !0, this.compositionContext_ = null, this.opacity_ = 1;
  }
  renderWorlds(t, e, n) {
    const s = e.extent, r = e.viewState, o = r.center, a = r.resolution, l = r.projection, h = r.rotation, c = l.getExtent(), u = this.getLayer().getSource(), d = e.pixelRatio, f = e.viewHints, g = !(f[Ht.ANIMATING] || f[Ht.INTERACTING]), m = this.compositionContext_, p = Math.round(e.size[0] * d), v = Math.round(e.size[1] * d), y = u.getWrapX() && l.canWrapX(), x = y ? mt(c) : null, M = y ? Math.ceil((s[2] - c[2]) / x) + 1 : 1;
    let C = y ? Math.floor((s[0] - c[0]) / x) : 0;
    do {
      const E = this.getRenderTransform(
        o,
        a,
        h,
        d,
        p,
        v,
        C * x
      );
      t.execute(
        m,
        1,
        E,
        h,
        g,
        void 0,
        n
      );
    } while (++C < M);
  }
  setupCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = ge(
        this.context.canvas.width,
        this.context.canvas.height,
        Vh
      );
      this.compositionContext_ = t;
    } else
      this.compositionContext_ = this.context;
  }
  releaseCompositionContext_() {
    if (this.opacity_ !== 1) {
      const t = this.context.globalAlpha;
      this.context.globalAlpha = this.opacity_, this.context.drawImage(this.compositionContext_.canvas, 0, 0), this.context.globalAlpha = t, Xu(this.compositionContext_), Vh.push(this.compositionContext_.canvas), this.compositionContext_ = null;
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
    m0(this.pixelTransform, 1 / n, 1 / n), qa(this.inversePixelTransform, this.pixelTransform);
    const r = wu(this.pixelTransform);
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
      const m = Xi(s.extent);
      g = ie(m, t.extent), f = g && !Mi(m, t.extent), f && this.clipUnrotated(this.compositionContext_, t, m);
    }
    return g && this.renderWorlds(l, t), f && this.compositionContext_.restore(), this.releaseCompositionContext_(), this.postRender(o, t), this.renderedRotation_ !== d.rotation && (this.renderedRotation_ = d.rotation, this.hitDetectionImageData_ = null), this.container;
  }
  getFeatures(t) {
    return new Promise(
      function(e) {
        if (!this.hitDetectionImageData_ && !this.animatingOrInteracting_) {
          const n = [this.context.canvas.width, this.context.canvas.height];
          Ft(this.pixelTransform, n);
          const s = this.renderedCenter_, r = this.renderedResolution_, o = this.renderedRotation_, a = this.renderedProjection_, l = this.wrappedRenderedExtent_, h = this.getLayer(), c = [], u = n[0] * Ae, d = n[1] * Ae;
          c.push(
            this.getRenderTransform(
              s,
              r,
              o,
              Ae,
              u,
              d,
              0
            ).slice()
          );
          const f = h.getSource(), g = a.getExtent();
          if (f.getWrapX() && a.canWrapX() && !Mi(g, l)) {
            let m = l[0];
            const p = mt(g);
            let v = 0, y;
            for (; m < g[0]; )
              --v, y = p * v, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  Ae,
                  u,
                  d,
                  y
                ).slice()
              ), m += p;
            for (v = 0, m = l[2]; m > g[2]; )
              ++v, y = p * v, c.push(
                this.getRenderTransform(
                  s,
                  r,
                  o,
                  Ae,
                  u,
                  d,
                  y
                ).slice()
              ), m -= p;
          }
          this.hitDetectionImageData_ = z2(
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
          F2(t, this.renderedFeatures_, this.hitDetectionImageData_)
        );
      }.bind(this)
    );
  }
  forEachFeatureAtCoordinate(t, e, n, s, r) {
    if (!this.replayGroup_)
      return;
    const o = e.viewState.resolution, a = e.viewState.rotation, l = this.getLayer(), h = {}, c = function(f, g, m) {
      const p = rt(f), v = h[p];
      if (v) {
        if (v !== !0 && m < v.distanceSq) {
          if (m === 0)
            return h[p] = !0, r.splice(r.lastIndexOf(v), 1), s(f, l, g);
          v.geometry = g, v.distanceSq = m;
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
    const s = t.viewHints[Ht.ANIMATING], r = t.viewHints[Ht.INTERACTING], o = e.getUpdateWhileAnimating(), a = e.getUpdateWhileInteracting();
    if (this.ready && !o && s || !a && r)
      return this.animatingOrInteracting_ = !0, !0;
    this.animatingOrInteracting_ = !1;
    const l = t.extent, h = t.viewState, c = h.projection, u = h.resolution, d = t.pixelRatio, f = e.getRevision(), g = e.getRenderBuffer();
    let m = e.getRenderOrder();
    m === void 0 && (m = j2);
    const p = h.center.slice(), v = uo(
      l,
      g * u
    ), y = v.slice(), x = [v.slice()], M = c.getExtent();
    if (n.getWrapX() && c.canWrapX() && !Mi(M, t.extent)) {
      const N = mt(M), F = Math.max(mt(v) / 2, N);
      v[0] = M[0] - F, v[2] = M[2] + F, Fu(p, c);
      const L = Tu(x[0], c);
      L[0] < M[0] && L[2] < M[2] ? x.push([
        L[0] + N,
        L[1],
        L[2] + N,
        L[3]
      ]) : L[0] > M[0] && L[2] > M[2] && x.push([
        L[0] - N,
        L[1],
        L[2] - N,
        L[3]
      ]);
    }
    if (this.ready && this.renderedResolution_ == u && this.renderedRevision_ == f && this.renderedRenderOrder_ == m && Mi(this.wrappedRenderedExtent_, v))
      return sn(this.renderedExtent_, y) || (this.hitDetectionImageData_ = null, this.renderedExtent_ = y), this.renderedCenter_ = p, this.replayGroupChanged = !1, !0;
    this.replayGroup_ = null;
    const C = new Wh(
      Sa(u, d),
      v,
      u,
      d
    );
    let E;
    this.getLayer().getDeclutter() && (E = new Wh(
      Sa(u, d),
      v,
      u,
      d
    ));
    let b;
    for (let N = 0, F = x.length; N < F; ++N)
      n.loadFeatures(x[N], u, c);
    const S = _d(u, d);
    let O = !0;
    const D = function(N) {
      let F;
      const L = N.getStyleFunction() || e.getStyleFunction();
      if (L && (F = L(N, u)), F) {
        const $ = this.renderFeature(
          N,
          S,
          F,
          C,
          b,
          E
        );
        O = O && !$;
      }
    }.bind(this), H = qu(v), R = n.getFeaturesInExtent(H);
    m && R.sort(m);
    for (let N = 0, F = R.length; N < F; ++N)
      D(R[N]);
    this.renderedFeatures_ = R, this.ready = O;
    const j = C.finish(), dt = new Jh(
      v,
      u,
      d,
      n.getOverlaps(),
      j,
      e.getRenderBuffer()
    );
    return E && (this.declutterExecutorGroup = new Jh(
      v,
      u,
      d,
      n.getOverlaps(),
      E.finish(),
      e.getRenderBuffer()
    )), this.renderedResolution_ = u, this.renderedRevision_ = f, this.renderedRenderOrder_ = m, this.renderedExtent_ = y, this.wrappedRenderedExtent_ = v, this.renderedCenter_ = p, this.renderedProjection_ = c, this.replayGroup_ = dt, this.hitDetectionImageData_ = null, this.replayGroupChanged = !0, !0;
  }
  renderFeature(t, e, n, s, r, o) {
    if (!n)
      return !1;
    let a = !1;
    if (Array.isArray(n))
      for (let l = 0, h = n.length; l < h; ++l)
        a = qh(
          s,
          t,
          n[l],
          e,
          this.boundHandleStyleImageChange_,
          r,
          o
        ) || a;
    else
      a = qh(
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
const J2 = U2;
class q2 extends u2 {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new J2(this);
  }
}
const Bn = q2;
class K2 {
  constructor(t) {
    this.rbush_ = new Cd(t), this.items_ = {};
  }
  insert(t, e) {
    const n = {
      minX: t[0],
      minY: t[1],
      maxX: t[2],
      maxY: t[3],
      value: e
    };
    this.rbush_.insert(n), this.items_[rt(e)] = n;
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
      n[s] = l, this.items_[rt(a)] = l;
    }
    this.rbush_.load(n);
  }
  remove(t) {
    const e = rt(t), n = this.items_[e];
    return delete this.items_[e], this.rbush_.remove(n) !== null;
  }
  update(t, e) {
    const n = this.items_[rt(e)], s = [n.minX, n.minY, n.maxX, n.maxY];
    _s(s, t) || (this.remove(e), this.insert(t, e));
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
    return jn(this.items_);
  }
  clear() {
    this.rbush_.clear(), this.items_ = {};
  }
  getExtent(t) {
    const e = this.rbush_.toJSON();
    return Me(e.minX, e.minY, e.maxX, e.maxY, t);
  }
  concat(t) {
    this.rbush_.load(t.rbush_.all());
    for (const e in t.items_)
      this.items_[e] = t.items_[e];
  }
}
const Kh = K2;
class Q2 extends Ce {
  constructor(t) {
    super(), this.projection = K(t.projection), this.attributions_ = Qh(t.attributions), this.attributionsCollapsible_ = t.attributionsCollapsible !== void 0 ? t.attributionsCollapsible : !0, this.loading = !1, this.state_ = t.state !== void 0 ? t.state : "ready", this.wrapX_ = t.wrapX !== void 0 ? t.wrapX : !1, this.interpolate_ = !!t.interpolate, this.viewResolver = null, this.viewRejector = null;
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
    return B();
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
    this.attributions_ = Qh(t), this.changed();
  }
  setState(t) {
    this.state_ = t, this.changed();
  }
}
function Qh(i) {
  return i ? Array.isArray(i) ? function(t) {
    return i;
  } : typeof i == "function" ? i : function(t) {
    return [i];
  } : null;
}
const Td = Q2, be = {
  ADDFEATURE: "addfeature",
  CHANGEFEATURE: "changefeature",
  CLEAR: "clear",
  REMOVEFEATURE: "removefeature",
  FEATURESLOADSTART: "featuresloadstart",
  FEATURESLOADEND: "featuresloadend",
  FEATURESLOADERROR: "featuresloaderror"
};
function Ld(i, t) {
  return [[-1 / 0, -1 / 0, 1 / 0, 1 / 0]];
}
function $2(i, t) {
  return [i];
}
let tm = !1;
function em(i, t, e, n, s, r, o) {
  const a = new XMLHttpRequest();
  a.open(
    "GET",
    typeof i == "function" ? i(e, n, s) : i,
    !0
  ), t.getType() == "arraybuffer" && (a.responseType = "arraybuffer"), a.withCredentials = tm, a.onload = function(l) {
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
function $h(i, t) {
  return function(e, n, s, r, o) {
    const a = this;
    em(
      i,
      t,
      e,
      n,
      s,
      function(l, h) {
        a.addFeatures(l), r !== void 0 && r(l);
      },
      o || Ki
    );
  };
}
class mi extends Ge {
  constructor(t, e, n) {
    super(t), this.feature = e, this.features = n;
  }
}
class im extends Td {
  constructor(t) {
    t = t || {}, super({
      attributions: t.attributions,
      interpolate: !0,
      projection: void 0,
      state: "ready",
      wrapX: t.wrapX !== void 0 ? t.wrapX : !0
    }), this.on, this.once, this.un, this.loader_ = Ki, this.format_ = t.format, this.overlaps_ = t.overlaps === void 0 ? !0 : t.overlaps, this.url_ = t.url, t.loader !== void 0 ? this.loader_ = t.loader : this.url_ !== void 0 && (Y(this.format_, 7), this.loader_ = $h(
      this.url_,
      this.format_
    )), this.strategy_ = t.strategy !== void 0 ? t.strategy : Ld;
    const e = t.useSpatialIndex !== void 0 ? t.useSpatialIndex : !0;
    this.featuresRtree_ = e ? new Kh() : null, this.loadedExtentsRtree_ = new Kh(), this.loadingExtentsCount_ = 0, this.nullGeometryFeatures_ = {}, this.idIndex_ = {}, this.uidIndex_ = {}, this.featureChangeKeys_ = {}, this.featuresCollection_ = null;
    let n, s;
    Array.isArray(t.features) ? s = t.features : t.features && (n = t.features, s = n.getArray()), !e && n === void 0 && (n = new Ie(s)), s !== void 0 && this.addFeaturesInternal(s), n !== void 0 && this.bindFeaturesCollection_(n);
  }
  addFeature(t) {
    this.addFeatureInternal(t), this.changed();
  }
  addFeatureInternal(t) {
    const e = rt(t);
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
      new mi(be.ADDFEATURE, t)
    );
  }
  setupChangeEvents_(t, e) {
    this.featureChangeKeys_[t] = [
      et(e, V.CHANGE, this.handleFeatureChange_, this),
      et(
        e,
        Dn.PROPERTYCHANGE,
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
      const a = t[r], l = rt(a);
      this.addToIndex_(l, a) && n.push(a);
    }
    for (let r = 0, o = n.length; r < o; r++) {
      const a = n[r], l = rt(a);
      this.setupChangeEvents_(l, a);
      const h = a.getGeometry();
      if (h) {
        const c = h.getExtent();
        e.push(c), s.push(a);
      } else
        this.nullGeometryFeatures_[l] = a;
    }
    if (this.featuresRtree_ && this.featuresRtree_.load(e, s), this.hasListener(be.ADDFEATURE))
      for (let r = 0, o = n.length; r < o; r++)
        this.dispatchEvent(
          new mi(be.ADDFEATURE, n[r])
        );
  }
  bindFeaturesCollection_(t) {
    let e = !1;
    this.addEventListener(
      be.ADDFEATURE,
      function(n) {
        e || (e = !0, t.push(n.feature), e = !1);
      }
    ), this.addEventListener(
      be.REMOVEFEATURE,
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
    const e = new mi(be.CLEAR);
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
    return this.featuresCollection_ ? t = this.featuresCollection_.getArray().slice(0) : this.featuresRtree_ && (t = this.featuresRtree_.getAll(), jn(this.nullGeometryFeatures_) || qt(t, Object.values(this.nullGeometryFeatures_))), t;
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
      const s = E0(t, e);
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
    return e = e || Ss, this.featuresRtree_.forEachInExtent(
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
    const e = t.target, n = rt(e), s = e.getGeometry();
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
      new mi(be.CHANGEFEATURE, e)
    );
  }
  hasFeature(t) {
    const e = t.getId();
    return e !== void 0 ? e in this.idIndex_ : rt(t) in this.uidIndex_;
  }
  isEmpty() {
    return this.featuresRtree_ ? this.featuresRtree_.isEmpty() && jn(this.nullGeometryFeatures_) : this.featuresCollection_ ? this.featuresCollection_.getLength() === 0 : !0;
  }
  loadFeatures(t, e, n) {
    const s = this.loadedExtentsRtree_, r = this.strategy_(t, e, n);
    for (let o = 0, a = r.length; o < a; ++o) {
      const l = r[o];
      s.forEachInExtent(
        l,
        function(c) {
          return Mi(c.extent, l);
        }
      ) || (++this.loadingExtentsCount_, this.dispatchEvent(
        new mi(be.FEATURESLOADSTART)
      ), this.loader_.call(
        this,
        l,
        e,
        n,
        function(c) {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new mi(
              be.FEATURESLOADEND,
              void 0,
              c
            )
          );
        }.bind(this),
        function() {
          --this.loadingExtentsCount_, this.dispatchEvent(
            new mi(be.FEATURESLOADERROR)
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
      if (_s(s.extent, t))
        return n = s, !0;
    }), n && e.remove(n);
  }
  removeFeature(t) {
    if (!t)
      return;
    const e = rt(t);
    e in this.nullGeometryFeatures_ ? delete this.nullGeometryFeatures_[e] : this.featuresRtree_ && this.featuresRtree_.remove(t), this.removeFeatureInternal(t) && this.changed();
  }
  removeFeatureInternal(t) {
    const e = rt(t), n = this.featureChangeKeys_[e];
    if (!n)
      return;
    n.forEach(pt), delete this.featureChangeKeys_[e];
    const s = t.getId();
    return s !== void 0 && delete this.idIndex_[s.toString()], delete this.uidIndex_[e], this.dispatchEvent(
      new mi(be.REMOVEFEATURE, t)
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
    Y(this.format_, 7), this.url_ = t, this.setLoader($h(t, this.format_));
  }
}
const $n = im;
function nm(i) {
  if (!(i.context instanceof CanvasRenderingContext2D))
    throw new Error("Only works for render events from Canvas 2D layers");
  const t = i.inversePixelTransform[0], e = i.frameState, n = d0(
    i.inversePixelTransform.slice(),
    e.coordinateToPixelTransform
  ), s = _d(
    e.viewState.resolution,
    t
  );
  let r;
  return new Pd(
    i.context,
    t,
    e.extent,
    n,
    e.viewState.rotation,
    s,
    r
  );
}
class sm extends ho {
  constructor(t, e, n) {
    super(), n = n || {}, this.tileCoord = t, this.state = e, this.interimTile = null, this.key = "", this.transition_ = n.transition === void 0 ? 250 : n.transition, this.transitionStarts_ = {}, this.interpolate = !!n.interpolate;
  }
  changed() {
    this.dispatchEvent(V.CHANGE);
  }
  release() {
    this.state === X.ERROR && this.setState(X.EMPTY);
  }
  getKey() {
    return this.key + "/" + this.tileCoord;
  }
  getInterimTile() {
    if (!this.interimTile)
      return this;
    let t = this.interimTile;
    do {
      if (t.getState() == X.LOADED)
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
      if (t.getState() == X.LOADED) {
        t.interimTile = null;
        break;
      } else
        t.getState() == X.LOADING ? e = t : t.getState() == X.IDLE ? e.interimTile = t.interimTile : e = t;
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
    if (this.state !== X.ERROR && this.state > t)
      throw new Error("Tile load sequence violation");
    this.state = t, this.changed();
  }
  load() {
    B();
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
const Od = sm;
class rm extends Od {
  constructor(t, e, n, s, r, o) {
    super(t, e, o), this.crossOrigin_ = s, this.src_ = n, this.key = n, this.image_ = new Image(), s !== null && (this.image_.crossOrigin = s), this.unlisten_ = null, this.tileLoadFunction_ = r;
  }
  getImage() {
    return this.image_;
  }
  setImage(t) {
    this.image_ = t, this.state = X.LOADED, this.unlistenImage_(), this.changed();
  }
  handleImageError_() {
    this.state = X.ERROR, this.unlistenImage_(), this.image_ = om(), this.changed();
  }
  handleImageLoad_() {
    const t = this.image_;
    t.naturalWidth && t.naturalHeight ? this.state = X.LOADED : this.state = X.EMPTY, this.unlistenImage_(), this.changed();
  }
  load() {
    this.state == X.ERROR && (this.state = X.IDLE, this.image_ = new Image(), this.crossOrigin_ !== null && (this.image_.crossOrigin = this.crossOrigin_)), this.state == X.IDLE && (this.state = X.LOADING, this.changed(), this.tileLoadFunction_(this, this.src_), this.unlisten_ = wd(
      this.image_,
      this.handleImageLoad_.bind(this),
      this.handleImageError_.bind(this)
    ));
  }
  unlistenImage_() {
    this.unlisten_ && (this.unlisten_(), this.unlisten_ = null);
  }
}
function om() {
  const i = ge(1, 1);
  return i.fillStyle = "rgba(0,0,0,0)", i.fillRect(0, 0, 1, 1), i.canvas;
}
const Ad = rm, Gt = {
  ELEMENT: "element",
  MAP: "map",
  OFFSET: "offset",
  POSITION: "position",
  POSITIONING: "positioning"
};
class am extends Ce {
  constructor(t) {
    super(), this.on, this.once, this.un, this.options = t, this.id = t.id, this.insertFirst = t.insertFirst !== void 0 ? t.insertFirst : !0, this.stopEvent = t.stopEvent !== void 0 ? t.stopEvent : !0, this.element = document.createElement("div"), this.element.className = t.className !== void 0 ? t.className : "ol-overlay-container " + j0, this.element.style.position = "absolute", this.element.style.pointerEvents = "auto", this.autoPan = t.autoPan === !0 ? {} : t.autoPan || void 0, this.rendered = {
      transform_: "",
      visible: !0
    }, this.mapPostrenderListenerKey = null, this.addChangeListener(Gt.ELEMENT, this.handleElementChanged), this.addChangeListener(Gt.MAP, this.handleMapChanged), this.addChangeListener(Gt.OFFSET, this.handleOffsetChanged), this.addChangeListener(Gt.POSITION, this.handlePositionChanged), this.addChangeListener(Gt.POSITIONING, this.handlePositioningChanged), t.element !== void 0 && this.setElement(t.element), this.setOffset(t.offset !== void 0 ? t.offset : [0, 0]), this.setPositioning(t.positioning || "top-left"), t.position !== void 0 && this.setPosition(t.position);
  }
  getElement() {
    return this.get(Gt.ELEMENT);
  }
  getId() {
    return this.id;
  }
  getMap() {
    return this.get(Gt.MAP) || null;
  }
  getOffset() {
    return this.get(Gt.OFFSET);
  }
  getPosition() {
    return this.get(Gt.POSITION);
  }
  getPositioning() {
    return this.get(Gt.POSITIONING);
  }
  handleElementChanged() {
    Gu(this.element);
    const t = this.getElement();
    t && this.element.appendChild(t);
  }
  handleMapChanged() {
    this.mapPostrenderListenerKey && (Hr(this.element), pt(this.mapPostrenderListenerKey), this.mapPostrenderListenerKey = null);
    const t = this.getMap();
    if (t) {
      this.mapPostrenderListenerKey = et(
        t,
        $e.POSTRENDER,
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
    this.set(Gt.ELEMENT, t);
  }
  setMap(t) {
    this.set(Gt.MAP, t);
  }
  setOffset(t) {
    this.set(Gt.OFFSET, t);
  }
  setPosition(t) {
    this.set(Gt.POSITION, t);
  }
  performAutoPan() {
    this.autoPan && this.panIntoView(this.autoPan);
  }
  panIntoView(t) {
    const e = this.getMap();
    if (!e || !e.getTargetElement() || !this.get(Gt.POSITION))
      return;
    const n = this.getRect(e.getTargetElement(), e.getSize()), s = this.getElement(), r = this.getRect(s, [
      X0(s),
      G0(s)
    ]);
    t = t || {};
    const o = t.margin === void 0 ? 20 : t.margin;
    if (!Mi(n, r)) {
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
    this.set(Gt.POSITIONING, t);
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
const lm = am;
class hm {
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
const cm = hm;
function tc(i, t, e, n) {
  return n !== void 0 ? (n[0] = i, n[1] = t, n[2] = e, n) : [i, t, e];
}
function bo(i, t, e) {
  return i + "/" + t + "/" + e;
}
function Id(i) {
  return bo(i[0], i[1], i[2]);
}
function um(i) {
  return i.split("/").map(Number);
}
function dm(i) {
  return (i[1] << i[0]) + i[2];
}
function fm(i, t) {
  const e = i[0], n = i[1], s = i[2];
  if (t.getMinZoom() > e || e > t.getMaxZoom())
    return !1;
  const r = t.getFullTileRange(e);
  return r ? r.containsXY(n, s) : !0;
}
class gm extends cm {
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
    const t = this.peekFirstKey(), n = um(t)[0];
    this.forEach(
      function(s) {
        s.tileCoord[0] !== n && (this.remove(Id(s.tileCoord)), s.release());
      }.bind(this)
    );
  }
}
const Nd = gm;
class zd {
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
function vn(i, t, e, n, s) {
  return s !== void 0 ? (s.minX = i, s.maxX = t, s.minY = e, s.maxY = n, s) : new zd(i, t, e, n);
}
const Fd = zd, ec = [
  "fullscreenchange",
  "webkitfullscreenchange",
  "MSFullscreenChange"
], ic = {
  ENTERFULLSCREEN: "enterfullscreen",
  LEAVEFULLSCREEN: "leavefullscreen"
};
class mm extends Dt {
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
      V.CLICK,
      this.handleClick_.bind(this),
      !1
    ), this.setClassName_(this.button_, this.isInFullscreen_), this.element.className = `${this.cssClassName_} ${Kn} ${yo}`, this.element.appendChild(this.button_);
  }
  handleClick_(t) {
    t.preventDefault(), this.handleFullScreen_();
  }
  handleFullScreen_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = t.getOwnerDocument();
    if (!!nc(e))
      if (sc(e))
        vm(e);
      else {
        let n;
        this.source_ ? n = typeof this.source_ == "string" ? e.getElementById(this.source_) : this.source_ : n = t.getTargetElement(), this.keys_ ? pm(n) : Dd(n);
      }
  }
  handleFullScreenChange_() {
    const t = this.getMap();
    if (!t)
      return;
    const e = this.isInFullscreen_;
    this.isInFullscreen_ = sc(t.getOwnerDocument()), e !== this.isInFullscreen_ && (this.setClassName_(this.button_, this.isInFullscreen_), this.isInFullscreen_ ? (Gr(this.labelActiveNode_, this.labelNode_), this.dispatchEvent(ic.ENTERFULLSCREEN)) : (Gr(this.labelNode_, this.labelActiveNode_), this.dispatchEvent(ic.LEAVEFULLSCREEN)), t.updateSize());
  }
  setClassName_(t, e) {
    e ? (t.classList.remove(...this.inactiveClassName_), t.classList.add(...this.activeClassName_)) : (t.classList.remove(...this.activeClassName_), t.classList.add(...this.inactiveClassName_));
  }
  setMap(t) {
    const e = this.getMap();
    e && e.removeChangeListener(
      Nt.TARGET,
      this.boundHandleMapTargetChange_
    ), super.setMap(t), this.handleMapTargetChange_(), t && t.addChangeListener(
      Nt.TARGET,
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
      nc(n) ? this.element.classList.remove(xh) : this.element.classList.add(xh);
      for (let s = 0, r = ec.length; s < r; ++s)
        t.push(
          et(n, ec[s], this.handleFullScreenChange_, this)
        );
      this.handleFullScreenChange_();
    }
  }
}
function nc(i) {
  const t = i.body;
  return !!(t.webkitRequestFullscreen || t.requestFullscreen && i.fullscreenEnabled);
}
function sc(i) {
  return !!(i.webkitIsFullScreen || i.fullscreenElement);
}
function Dd(i) {
  i.requestFullscreen ? i.requestFullscreen() : i.webkitRequestFullscreen && i.webkitRequestFullscreen();
}
function pm(i) {
  i.webkitRequestFullscreen ? i.webkitRequestFullscreen() : Dd(i);
}
function vm(i) {
  i.exitFullscreen ? i.exitFullscreen() : i.webkitExitFullscreen && i.webkitExitFullscreen();
}
const ym = mm, $o = "units", xm = [1, 2, 5], us = 25.4 / 0.28;
class Mm extends Dt {
  constructor(t) {
    t = t || {};
    const e = document.createElement("div");
    e.style.pointerEvents = "none", super({
      element: e,
      render: t.render,
      target: t.target
    }), this.on, this.once, this.un;
    const n = t.className !== void 0 ? t.className : t.bar ? "ol-scale-bar" : "ol-scale-line";
    this.innerElement_ = document.createElement("div"), this.innerElement_.className = n + "-inner", this.element.className = n + " " + Kn, this.element.appendChild(this.innerElement_), this.viewState_ = null, this.minWidth_ = t.minWidth !== void 0 ? t.minWidth : 64, this.maxWidth_ = t.maxWidth, this.renderedVisible_ = !1, this.renderedWidth_ = void 0, this.renderedHTML_ = "", this.addChangeListener($o, this.handleUnitsChanged_), this.setUnits(t.units || "metric"), this.scaleBar_ = t.bar || !1, this.scaleBarSteps_ = t.steps || 4, this.scaleBarText_ = t.text || !1, this.dpi_ = t.dpi || void 0;
  }
  getUnits() {
    return this.get($o);
  }
  handleUnitsChanged_() {
    this.updateElement_();
  }
  setUnits(t) {
    this.set($o, t);
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
    let o = Yr(
      n,
      t.resolution,
      e,
      r
    );
    const a = this.minWidth_ * (this.dpi_ || us) / us, l = this.maxWidth_ !== void 0 ? this.maxWidth_ * (this.dpi_ || us) / us : void 0;
    let h = a * o, c = "";
    if (s == "degrees") {
      const x = Xn.degrees;
      h *= x, h < x / 60 ? (c = "\u2033", o *= 3600) : h < x ? (c = "\u2032", o *= 60) : c = "\xB0";
    } else
      s == "imperial" ? h < 0.9144 ? (c = "in", o /= 0.0254) : h < 1609.344 ? (c = "ft", o /= 0.3048) : (c = "mi", o /= 1609.344) : s == "nautical" ? (o /= 1852, c = "NM") : s == "metric" ? h < 1e-3 ? (c = "\u03BCm", o *= 1e6) : h < 1 ? (c = "mm", o *= 1e3) : h < 1e3 ? c = "m" : (c = "km", o /= 1e3) : s == "us" ? h < 0.9144 ? (c = "in", o *= 39.37) : h < 1609.344 ? (c = "ft", o /= 0.30480061) : (c = "mi", o /= 1609.3472) : Y(!1, 33);
    let u = 3 * Math.floor(Math.log(a * o) / Math.log(10)), d, f, g, m, p, v;
    for (; ; ) {
      g = Math.floor(u / 3);
      const x = Math.pow(10, g);
      if (d = xm[(u % 3 + 3) % 3] * x, f = Math.round(d / o), isNaN(f)) {
        this.element.style.display = "none", this.renderedVisible_ = !1;
        return;
      }
      if (l !== void 0 && f >= l) {
        d = m, f = p, g = v;
        break;
      } else if (f >= a)
        break;
      m = d, p = f, v = g, ++u;
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
    const t = Yr(
      this.viewState_.projection,
      this.viewState_.resolution,
      this.viewState_.center,
      "m"
    ), e = this.dpi_ || us, n = 1e3 / 25.4;
    return t * n * e;
  }
  render(t) {
    const e = t.frameState;
    e ? this.viewState_ = e.viewState : this.viewState_ = null, this.updateElement_();
  }
}
const Cm = Mm, wm = 0.5, Em = 10, rc = 0.25;
class bm {
  constructor(t, e, n, s, r, o) {
    this.sourceProj_ = t, this.targetProj_ = e;
    let a = {};
    const l = Ns(this.targetProj_, this.sourceProj_);
    this.transformInv_ = function(y) {
      const x = y[0] + "/" + y[1];
      return a[x] || (a[x] = l(y)), a[x];
    }, this.maxSourceExtent_ = s, this.errorThresholdSquared_ = r * r, this.triangles_ = [], this.wrapsXInSource_ = !1, this.canWrapXInSource_ = this.sourceProj_.canWrapX() && !!s && !!this.sourceProj_.getExtent() && mt(s) == mt(this.sourceProj_.getExtent()), this.sourceWorldWidth_ = this.sourceProj_.getExtent() ? mt(this.sourceProj_.getExtent()) : null, this.targetWorldWidth_ = this.targetProj_.getExtent() ? mt(this.targetProj_.getExtent()) : null;
    const h = Ai(n), c = po(n), u = mo(n), d = go(n), f = this.transformInv_(h), g = this.transformInv_(c), m = this.transformInv_(u), p = this.transformInv_(d), v = Em + (o ? Math.max(
      0,
      Math.ceil(
        Math.log2(
          ca(n) / (o * o * 256 * 256)
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
      v
    ), this.wrapsXInSource_) {
      let y = 1 / 0;
      this.triangles_.forEach(function(x, M, C) {
        y = Math.min(
          y,
          x.source[0][0],
          x.source[1][0],
          x.source[2][0]
        );
      }), this.triangles_.forEach(
        function(x) {
          if (Math.max(
            x.source[0][0],
            x.source[1][0],
            x.source[2][0]
          ) - y > this.sourceWorldWidth_ / 2) {
            const M = [
              [x.source[0][0], x.source[0][1]],
              [x.source[1][0], x.source[1][1]],
              [x.source[2][0], x.source[2][1]]
            ];
            M[0][0] - y > this.sourceWorldWidth_ / 2 && (M[0][0] -= this.sourceWorldWidth_), M[1][0] - y > this.sourceWorldWidth_ / 2 && (M[1][0] -= this.sourceWorldWidth_), M[2][0] - y > this.sourceWorldWidth_ / 2 && (M[2][0] -= this.sourceWorldWidth_);
            const C = Math.min(
              M[0][0],
              M[1][0],
              M[2][0]
            );
            Math.max(
              M[0][0],
              M[1][0],
              M[2][0]
            ) - C < this.sourceWorldWidth_ / 2 && (x.source = M);
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
    const c = la([r, o, a, l]), u = this.sourceWorldWidth_ ? mt(c) / this.sourceWorldWidth_ : null, d = this.sourceWorldWidth_, f = this.sourceProj_.canWrapX() && u > 0.5 && u < 1;
    let g = !1;
    if (h > 0) {
      if (this.targetProj_.isGlobal() && this.targetWorldWidth_) {
        const p = la([t, e, n, s]);
        g = mt(p) / this.targetWorldWidth_ > rc || g;
      }
      !f && this.sourceProj_.isGlobal() && u && (g = u > rc || g);
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
        const p = [(t[0] + n[0]) / 2, (t[1] + n[1]) / 2], v = this.transformInv_(p);
        let y;
        f ? y = (An(r[0], d) + An(a[0], d)) / 2 - An(v[0], d) : y = (r[0] + a[0]) / 2 - v[0];
        const x = (r[1] + a[1]) / 2 - v[1];
        g = y * y + x * x > this.errorThresholdSquared_;
      }
      if (g) {
        if (Math.abs(t[0] - n[0]) <= Math.abs(t[1] - n[1])) {
          const p = [(e[0] + n[0]) / 2, (e[1] + n[1]) / 2], v = this.transformInv_(p), y = [(s[0] + t[0]) / 2, (s[1] + t[1]) / 2], x = this.transformInv_(y);
          this.addQuad_(
            t,
            e,
            p,
            y,
            r,
            o,
            v,
            x,
            h - 1
          ), this.addQuad_(
            y,
            p,
            n,
            s,
            x,
            v,
            a,
            l,
            h - 1
          );
        } else {
          const p = [(t[0] + e[0]) / 2, (t[1] + e[1]) / 2], v = this.transformInv_(p), y = [(n[0] + s[0]) / 2, (n[1] + s[1]) / 2], x = this.transformInv_(y);
          this.addQuad_(
            t,
            p,
            y,
            s,
            r,
            v,
            x,
            l,
            h - 1
          ), this.addQuad_(
            p,
            e,
            n,
            y,
            v,
            o,
            a,
            x,
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
      ys(t, r[0]), ys(t, r[1]), ys(t, r[2]);
    }), t;
  }
  getTriangles() {
    return this.triangles_;
  }
}
const Pm = bm;
let ta;
const jd = [];
function oc(i, t, e, n, s) {
  i.beginPath(), i.moveTo(0, 0), i.lineTo(t, e), i.lineTo(n, s), i.closePath(), i.save(), i.clip(), i.fillRect(0, 0, Math.max(t, n) + 1, Math.max(e, s)), i.restore();
}
function ea(i, t) {
  return Math.abs(i[t * 4] - 210) > 2 || Math.abs(i[t * 4 + 3] - 0.75 * 255) > 2;
}
function Sm() {
  if (ta === void 0) {
    const i = document.createElement("canvas").getContext("2d");
    i.globalCompositeOperation = "lighter", i.fillStyle = "rgba(210, 0, 0, 0.75)", oc(i, 4, 5, 4, 0), oc(i, 4, 5, 0, 5);
    const t = i.getImageData(0, 0, 3, 3).data;
    ta = ea(t, 0) || ea(t, 4) || ea(t, 8);
  }
  return ta;
}
function ac(i, t, e, n) {
  const s = Uu(e, t, i);
  let r = Yr(
    t,
    n,
    e
  );
  const o = t.getMetersPerUnit();
  o !== void 0 && (r *= o);
  const a = i.getMetersPerUnit();
  a !== void 0 && (r /= a);
  const l = i.getExtent();
  if (!l || fo(l, s)) {
    const h = Yr(i, r, s) / r;
    isFinite(h) && h > 0 && (r /= h);
  }
  return r;
}
function _m(i, t, e, n) {
  const s = Ri(e);
  let r = ac(
    i,
    t,
    s,
    n
  );
  return (!isFinite(r) || r <= 0) && Ru(e, function(o) {
    return r = ac(
      i,
      t,
      o,
      n
    ), isFinite(r) && r > 0;
  }), r;
}
function Rm(i, t, e, n, s, r, o, a, l, h, c, u) {
  const d = ge(
    Math.round(e * i),
    Math.round(e * t),
    jd
  );
  if (u || (d.imageSmoothingEnabled = !1), l.length === 0)
    return d.canvas;
  d.scale(e, e);
  function f(M) {
    return Math.round(M * e) / e;
  }
  d.globalCompositeOperation = "lighter";
  const g = fe();
  l.forEach(function(M, C, E) {
    Su(g, M.extent);
  });
  const m = mt(g), p = je(g), v = ge(
    Math.round(e * m / n),
    Math.round(e * p / n)
  );
  u || (v.imageSmoothingEnabled = !1);
  const y = e / n;
  l.forEach(function(M, C, E) {
    const b = M.extent[0] - g[0], S = -(M.extent[3] - g[3]), O = mt(M.extent), D = je(M.extent);
    M.image.width > 0 && M.image.height > 0 && v.drawImage(
      M.image,
      h,
      h,
      M.image.width - 2 * h,
      M.image.height - 2 * h,
      b * y,
      S * y,
      O * y,
      D * y
    );
  });
  const x = Ai(o);
  return a.getTriangles().forEach(function(M, C, E) {
    const b = M.source, S = M.target;
    let O = b[0][0], D = b[0][1], H = b[1][0], R = b[1][1], j = b[2][0], dt = b[2][1];
    const N = f((S[0][0] - x[0]) / r), F = f(
      -(S[0][1] - x[1]) / r
    ), L = f((S[1][0] - x[0]) / r), $ = f(
      -(S[1][1] - x[1]) / r
    ), wt = f((S[2][0] - x[0]) / r), vt = f(
      -(S[2][1] - x[1]) / r
    ), It = O, _ = D;
    O = 0, D = 0, H -= It, R -= _, j -= It, dt -= _;
    const ae = [
      [H, R, 0, 0, L - N],
      [j, dt, 0, 0, wt - N],
      [0, 0, H, R, $ - F],
      [0, 0, j, dt, vt - F]
    ], at = P0(ae);
    if (!!at) {
      if (d.save(), d.beginPath(), Sm() || !u) {
        d.moveTo(L, $);
        const ft = 4, hi = N - L, Le = F - $;
        for (let kt = 0; kt < ft; kt++)
          d.lineTo(
            L + f((kt + 1) * hi / ft),
            $ + f(kt * Le / (ft - 1))
          ), kt != ft - 1 && d.lineTo(
            L + f((kt + 1) * hi / ft),
            $ + f((kt + 1) * Le / (ft - 1))
          );
        d.lineTo(wt, vt);
      } else
        d.moveTo(L, $), d.lineTo(N, F), d.lineTo(wt, vt);
      d.clip(), d.transform(
        at[0],
        at[2],
        at[1],
        at[3],
        N,
        F
      ), d.translate(
        g[0] - It,
        g[3] - _
      ), d.scale(
        n / e,
        -n / e
      ), d.drawImage(v.canvas, 0, 0), d.restore();
    }
  }), c && (d.save(), d.globalCompositeOperation = "source-over", d.strokeStyle = "black", d.lineWidth = 1, a.getTriangles().forEach(function(M, C, E) {
    const b = M.target, S = (b[0][0] - x[0]) / r, O = -(b[0][1] - x[1]) / r, D = (b[1][0] - x[0]) / r, H = -(b[1][1] - x[1]) / r, R = (b[2][0] - x[0]) / r, j = -(b[2][1] - x[1]) / r;
    d.beginPath(), d.moveTo(D, H), d.lineTo(S, O), d.lineTo(R, j), d.closePath(), d.stroke();
  }), d.restore()), d.canvas;
}
class Tm extends Od {
  constructor(t, e, n, s, r, o, a, l, h, c, u, d) {
    super(r, X.IDLE, { interpolate: !!d }), this.renderEdges_ = u !== void 0 ? u : !1, this.pixelRatio_ = a, this.gutter_ = l, this.canvas_ = null, this.sourceTileGrid_ = e, this.targetTileGrid_ = s, this.wrappedTileCoord_ = o || r, this.sourceTiles_ = [], this.sourcesListenerKeys_ = null, this.sourceZ_ = 0;
    const f = s.getTileCoordExtent(
      this.wrappedTileCoord_
    ), g = this.targetTileGrid_.getExtent();
    let m = this.sourceTileGrid_.getExtent();
    const p = g ? xs(f, g) : f;
    if (ca(p) === 0) {
      this.state = X.EMPTY;
      return;
    }
    const v = t.getExtent();
    v && (m ? m = xs(m, v) : m = v);
    const y = s.getResolution(
      this.wrappedTileCoord_[0]
    ), x = _m(
      t,
      n,
      p,
      y
    );
    if (!isFinite(x) || x <= 0) {
      this.state = X.EMPTY;
      return;
    }
    const M = c !== void 0 ? c : wm;
    if (this.triangulation_ = new Pm(
      t,
      n,
      p,
      m,
      x * M,
      y
    ), this.triangulation_.getTriangles().length === 0) {
      this.state = X.EMPTY;
      return;
    }
    this.sourceZ_ = e.getZForResolution(x);
    let C = this.triangulation_.calculateSourceExtent();
    if (m && (t.canWrapX() ? (C[1] = Pt(
      C[1],
      m[1],
      m[3]
    ), C[3] = Pt(
      C[3],
      m[1],
      m[3]
    )) : C = xs(C, m)), !ca(C))
      this.state = X.EMPTY;
    else {
      const E = e.getTileRangeForExtentAndZ(
        C,
        this.sourceZ_
      );
      for (let b = E.minX; b <= E.maxX; b++)
        for (let S = E.minY; S <= E.maxY; S++) {
          const O = h(this.sourceZ_, b, S, a);
          O && this.sourceTiles_.push(O);
        }
      this.sourceTiles_.length === 0 && (this.state = X.EMPTY);
    }
  }
  getImage() {
    return this.canvas_;
  }
  reproject_() {
    const t = [];
    if (this.sourceTiles_.forEach(
      function(e, n, s) {
        e && e.getState() == X.LOADED && t.push({
          extent: this.sourceTileGrid_.getTileCoordExtent(e.tileCoord),
          image: e.getImage()
        });
      }.bind(this)
    ), this.sourceTiles_.length = 0, t.length === 0)
      this.state = X.ERROR;
    else {
      const e = this.wrappedTileCoord_[0], n = this.targetTileGrid_.getTileSize(e), s = typeof n == "number" ? n : n[0], r = typeof n == "number" ? n : n[1], o = this.targetTileGrid_.getResolution(e), a = this.sourceTileGrid_.getResolution(
        this.sourceZ_
      ), l = this.targetTileGrid_.getTileCoordExtent(
        this.wrappedTileCoord_
      );
      this.canvas_ = Rm(
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
      ), this.state = X.LOADED;
    }
    this.changed();
  }
  load() {
    if (this.state == X.IDLE) {
      this.state = X.LOADING, this.changed();
      let t = 0;
      this.sourcesListenerKeys_ = [], this.sourceTiles_.forEach(
        function(e, n, s) {
          const r = e.getState();
          if (r == X.IDLE || r == X.LOADING) {
            t++;
            const o = et(
              e,
              V.CHANGE,
              function(a) {
                const l = e.getState();
                (l == X.LOADED || l == X.ERROR || l == X.EMPTY) && (pt(o), t--, t === 0 && (this.unlistenSources_(), this.reproject_()));
              },
              this
            );
            this.sourcesListenerKeys_.push(o);
          }
        }.bind(this)
      ), t === 0 ? setTimeout(this.reproject_.bind(this), 0) : this.sourceTiles_.forEach(function(e, n, s) {
        e.getState() == X.IDLE && e.load();
      });
    }
  }
  unlistenSources_() {
    this.sourcesListenerKeys_.forEach(pt), this.sourcesListenerKeys_ = null;
  }
  release() {
    this.canvas_ && (Xu(this.canvas_.getContext("2d")), jd.push(this.canvas_), this.canvas_ = null), super.release();
  }
}
const _a = Tm, ia = {
  TILELOADSTART: "tileloadstart",
  TILELOADEND: "tileloadend",
  TILELOADERROR: "tileloaderror"
}, Lm = [0, 0, 0], pi = 5;
class Om {
  constructor(t) {
    this.minZoom = t.minZoom !== void 0 ? t.minZoom : 0, this.resolutions_ = t.resolutions, Y(
      Qf(
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
    n !== void 0 && !this.origin_ && !this.origins_ && (this.origin_ = Ai(n)), Y(
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
      if (this.zoomFactor_ === 2 ? (o = Math.floor(o / 2), a = Math.floor(a / 2), r = vn(o, o, a, a, n)) : r = this.getTileRangeForExtentAndZ(
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
        return vn(
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
      return vn(
        r,
        o,
        r,
        o,
        n
      );
    if (this.zoomFactor_) {
      const l = Math.pow(this.zoomFactor_, e - s), h = Math.floor(r * l), c = Math.floor(o * l);
      if (e < s)
        return vn(h, h, c, c, n);
      const u = Math.floor(l * (r + 1)) - 1, d = Math.floor(l * (o + 1)) - 1;
      return vn(h, u, c, d, n);
    }
    const a = this.getTileCoordExtent(t, this.tmpExtent_);
    return this.getTileRangeForExtentAndZ(a, e, n);
  }
  getTileRangeExtent(t, e, n) {
    const s = this.getOrigin(t), r = this.getResolution(t), o = ce(this.getTileSize(t), this.tmpSize_), a = s[0] + e.minX * o[0] * r, l = s[0] + (e.maxX + 1) * o[0] * r, h = s[1] + e.minY * o[1] * r, c = s[1] + (e.maxY + 1) * o[1] * r;
    return Me(a, h, l, c, n);
  }
  getTileRangeForExtentAndZ(t, e, n) {
    const s = Lm;
    this.getTileCoordForXYAndZ_(t[0], t[3], e, !1, s);
    const r = s[1], o = s[2];
    return this.getTileCoordForXYAndZ_(t[2], t[1], e, !0, s), vn(
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
    return Me(o, a, l, h, e);
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
    return s ? (c = mr(c, pi) - 1, u = mr(u, pi) - 1) : (c = gr(c, pi), u = gr(u, pi)), tc(o, c, u, r);
  }
  getTileCoordForXYAndZ_(t, e, n, s, r) {
    const o = this.getOrigin(n), a = this.getResolution(n), l = ce(this.getTileSize(n), this.tmpSize_);
    let h = (t - o[0]) / a / l[0], c = (o[1] - e) / a / l[1];
    return s ? (h = mr(h, pi) - 1, c = mr(c, pi) - 1) : (h = gr(h, pi), c = gr(c, pi)), tc(n, h, c, r);
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
    const n = Ua(
      this.resolutions_,
      t,
      e || 0
    );
    return Pt(n, this.minZoom, this.maxZoom);
  }
  tileCoordIntersectsViewport(t, e) {
    return rd(
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
const kd = Om;
function Xd(i) {
  let t = i.getDefaultTileGrid();
  return t || (t = zm(i), i.setDefaultTileGrid(t)), t;
}
function Am(i, t, e) {
  const n = t[0], s = i.getTileCoordCenter(t), r = Gd(e);
  if (fo(r, s))
    return t;
  {
    const o = mt(r), a = Math.ceil(
      (r[0] - s[0]) / o
    );
    return s[0] += o * a, i.getTileCoordForCoordAndZ(s, n);
  }
}
function Im(i, t, e, n) {
  n = n !== void 0 ? n : "top-left";
  const s = Nm(i, t, e);
  return new kd({
    extent: i,
    origin: x0(i, n),
    resolutions: s,
    tileSize: e
  });
}
function Nm(i, t, e, n) {
  t = t !== void 0 ? t : rg, e = ce(e !== void 0 ? e : il);
  const s = je(i), r = mt(i);
  n = n > 0 ? n : Math.max(r / e[0], s / e[1]);
  const o = t + 1, a = new Array(o);
  for (let l = 0; l < o; ++l)
    a[l] = n / Math.pow(2, l);
  return a;
}
function zm(i, t, e, n) {
  const s = Gd(i);
  return Im(s, t, e, n);
}
function Gd(i) {
  i = K(i);
  let t = i.getExtent();
  if (!t) {
    const e = 180 * Xn.degrees / i.getMetersPerUnit();
    t = Me(-e, -e, e, e);
  }
  return t;
}
class Fm extends Td {
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
    this.tileGrid && ce(this.tileGrid.getTileSize(this.tileGrid.getMinZoom()), e), this.tileCache = new Nd(t.cacheSize || 0), this.tmpSize = [0, 0], this.key_ = t.key || "", this.tileOptions = {
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
        l = bo(e, c, u), h = !1, r.containsKey(l) && (a = r.get(l), h = a.getState() === X.LOADED, h && (h = s(a) !== !1)), h || (o = !1);
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
    return B();
  }
  getTileGrid() {
    return this.tileGrid;
  }
  getTileGridForProjection(t) {
    return this.tileGrid ? this.tileGrid : Xd(t);
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    return Y(
      e === null || Oe(e, t),
      68
    ), this.tileCache;
  }
  getTilePixelRatio(t) {
    return this.tilePixelRatio_;
  }
  getTilePixelSize(t, e, n) {
    const s = this.getTileGridForProjection(n), r = this.getTilePixelRatio(e), o = ce(s.getTileSize(t), this.tmpSize);
    return r == 1 ? o : G1(o, r, this.tmpSize);
  }
  getTileCoordForTileUrlFunction(t, e) {
    e = e !== void 0 ? e : this.getProjection();
    const n = this.getTileGridForProjection(e);
    return this.getWrapX() && e.isGlobal() && (t = Am(n, t, e)), fm(t, n) ? t : null;
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
class Dm extends Ge {
  constructor(t, e) {
    super(t), this.tile = e;
  }
}
const jm = Fm;
function km(i, t) {
  const e = /\{z\}/g, n = /\{x\}/g, s = /\{y\}/g, r = /\{-y\}/g;
  return function(o, a, l) {
    if (o)
      return i.replace(e, o[0].toString()).replace(n, o[1].toString()).replace(s, o[2].toString()).replace(r, function() {
        const h = o[0], c = t.getFullTileRange(h);
        return Y(c, 55), (c.getHeight() - o[2] - 1).toString();
      });
  };
}
function Xm(i, t) {
  const e = i.length, n = new Array(e);
  for (let s = 0; s < e; ++s)
    n[s] = km(i[s], t);
  return Ra(n);
}
function Ra(i) {
  return i.length === 1 ? i[0] : function(t, e, n) {
    if (t) {
      const s = dm(t), r = An(s, i.length);
      return i[r](t, e, n);
    } else
      return;
  };
}
function Hd(i) {
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
class Rl extends jm {
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
    }), this.generateTileUrlFunction_ = this.tileUrlFunction === Rl.prototype.tileUrlFunction, this.tileLoadFunction = t.tileLoadFunction, t.tileUrlFunction && (this.tileUrlFunction = t.tileUrlFunction), this.urls = null, t.urls ? this.setUrls(t.urls) : t.url && this.setUrl(t.url), this.tileLoadingKeys_ = {};
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
    const e = t.target, n = rt(e), s = e.getState();
    let r;
    s == X.LOADING ? (this.tileLoadingKeys_[n] = !0, r = ia.TILELOADSTART) : n in this.tileLoadingKeys_ && (delete this.tileLoadingKeys_[n], r = s == X.ERROR ? ia.TILELOADERROR : s == X.LOADED ? ia.TILELOADEND : void 0), r != null && this.dispatchEvent(new Dm(r, e));
  }
  setTileLoadFunction(t) {
    this.tileCache.clear(), this.tileLoadFunction = t, this.changed();
  }
  setTileUrlFunction(t, e) {
    this.tileUrlFunction = t, this.tileCache.pruneExceptNewestZ(), typeof e < "u" ? this.setKey(e) : this.changed();
  }
  setUrl(t) {
    const e = Hd(t);
    this.urls = e, this.setUrls(e);
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.generateTileUrlFunction_ ? this.setTileUrlFunction(Xm(t, this.tileGrid), e) : this.setKey(e);
  }
  tileUrlFunction(t, e, n) {
  }
  useTile(t, e, n) {
    const s = bo(t, e, n);
    this.tileCache.containsKey(s) && this.tileCache.get(s);
  }
}
const Gm = Rl;
class Hm extends Gm {
  constructor(t) {
    super({
      attributions: t.attributions,
      cacheSize: t.cacheSize,
      opaque: t.opaque,
      projection: t.projection,
      state: t.state,
      tileGrid: t.tileGrid,
      tileLoadFunction: t.tileLoadFunction ? t.tileLoadFunction : Zm,
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
    }), this.crossOrigin = t.crossOrigin !== void 0 ? t.crossOrigin : null, this.tileClass = t.tileClass !== void 0 ? t.tileClass : Ad, this.tileCacheForProjection = {}, this.tileGridForProjection = {}, this.reprojectionErrorThreshold_ = t.reprojectionErrorThreshold, this.renderReprojectionEdges_ = !1;
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
    return this.getProjection() && t && !Oe(this.getProjection(), t) ? 0 : this.getGutter();
  }
  getGutter() {
    return 0;
  }
  getKey() {
    let t = super.getKey();
    return this.getInterpolate() || (t += ":disable-interpolation"), t;
  }
  getOpaque(t) {
    return this.getProjection() && t && !Oe(this.getProjection(), t) ? !1 : super.getOpaque(t);
  }
  getTileGridForProjection(t) {
    const e = this.getProjection();
    if (this.tileGrid && (!e || Oe(e, t)))
      return this.tileGrid;
    {
      const n = rt(t);
      return n in this.tileGridForProjection || (this.tileGridForProjection[n] = Xd(t)), this.tileGridForProjection[n];
    }
  }
  getTileCacheForProjection(t) {
    const e = this.getProjection();
    if (!e || Oe(e, t))
      return this.tileCache;
    {
      const n = rt(t);
      return n in this.tileCacheForProjection || (this.tileCacheForProjection[n] = new Nd(
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
      h !== void 0 ? X.IDLE : X.EMPTY,
      h !== void 0 ? h : "",
      this.crossOrigin,
      this.tileLoadFunction,
      this.tileOptions
    );
    return c.key = o, c.addEventListener(V.CHANGE, this.handleTileChange.bind(this)), c;
  }
  getTile(t, e, n, s, r) {
    const o = this.getProjection();
    if (!o || !r || Oe(o, r))
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
      const c = Id(l);
      a.containsKey(c) && (h = a.get(c));
      const u = this.getKey();
      if (h && h.key == u)
        return h;
      {
        const d = this.getTileGridForProjection(o), f = this.getTileGridForProjection(r), g = this.getTileCoordForTileUrlFunction(
          l,
          r
        ), m = new _a(
          o,
          d,
          r,
          f,
          l,
          g,
          this.getTilePixelRatio(s),
          this.getGutter(),
          function(p, v, y, x) {
            return this.getTileInternal(p, v, y, x, o);
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
    const a = bo(t, e, n), l = this.getKey();
    if (!this.tileCache.containsKey(a))
      o = this.createTile_(t, e, n, s, r, l), this.tileCache.set(a, o);
    else if (o = this.tileCache.get(a), o.key != l) {
      const h = o;
      o = this.createTile_(t, e, n, s, r, l), h.getState() == X.IDLE ? o.interimTile = h.interimTile : o.interimTile = h, o.refreshInterimChain(), this.tileCache.replace(a, o);
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
    const n = K(t);
    if (n) {
      const s = rt(n);
      s in this.tileGridForProjection || (this.tileGridForProjection[s] = e);
    }
  }
  clear() {
    super.clear();
    for (const t in this.tileCacheForProjection)
      this.tileCacheForProjection[t].clear();
  }
}
function Zm(i, t) {
  i.getImage().src = t;
}
const Bm = Hm;
class Wm extends $n {
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
    this.source && this.source.removeEventListener(V.CHANGE, this.boundRefresh_), this.source = t, t && t.addEventListener(V.CHANGE, this.boundRefresh_), this.refresh();
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
      if (!(rt(a) in s)) {
        const l = this.geometryFunction(a);
        if (l) {
          const h = l.getCoordinates();
          bu(h, t), uo(t, e, t);
          const c = this.source.getFeaturesInExtent(t).filter(function(u) {
            const d = rt(u);
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
      l ? Nu(n, l.getCoordinates()) : t.splice(a, 1);
    }
    zu(n, 1 / t.length);
    const s = Ri(e), r = this.interpolationRatio, o = new oi([
      n[0] * (1 - r) + s[0] * r,
      n[1] * (1 - r) + s[1] * r
    ]);
    return this.createCustomCluster_ ? this.createCustomCluster_(o, t) : new an({
      geometry: o,
      features: t
    });
  }
}
const Vm = Wm;
function lc(i, t) {
  const e = [];
  Object.keys(t).forEach(function(s) {
    t[s] !== null && t[s] !== void 0 && e.push(s + "=" + encodeURIComponent(t[s]));
  });
  const n = e.join("&");
  return i = i.replace(/[?&]$/, ""), i += i.includes("?") ? "&" : "?", i + n;
}
const Er = {
  PRELOAD: "preload",
  USE_INTERIM_TILES_ON_ERROR: "useInterimTilesOnError"
};
class Ym extends vo {
  constructor(t) {
    t = t || {};
    const e = Object.assign({}, t);
    delete e.preload, delete e.useInterimTilesOnError, super(e), this.on, this.once, this.un, this.setPreload(t.preload !== void 0 ? t.preload : 0), this.setUseInterimTilesOnError(
      t.useInterimTilesOnError !== void 0 ? t.useInterimTilesOnError : !0
    );
  }
  getPreload() {
    return this.get(Er.PRELOAD);
  }
  setPreload(t) {
    this.set(Er.PRELOAD, t);
  }
  getUseInterimTilesOnError() {
    return this.get(Er.USE_INTERIM_TILES_ON_ERROR);
  }
  setUseInterimTilesOnError(t) {
    this.set(Er.USE_INTERIM_TILES_ON_ERROR, t);
  }
  getData(t) {
    return super.getData(t);
  }
}
const Um = Ym;
class Jm extends bd {
  constructor(t) {
    super(t), this.extentChanged = !0, this.renderedExtent_ = null, this.renderedPixelRatio, this.renderedProjection = null, this.renderedRevision, this.renderedTiles = [], this.newTiles_ = !1, this.tmpExtent = fe(), this.tmpTileRange_ = new Fd(0, 0, 0, 0);
  }
  isDrawableTile(t) {
    const e = this.getLayer(), n = t.getState(), s = e.getUseInterimTilesOnError();
    return n == X.LOADED || n == X.EMPTY || n == X.ERROR && !s;
  }
  getTile(t, e, n, s) {
    const r = s.pixelRatio, o = s.viewState.projection, a = this.getLayer();
    let h = a.getSource().getTile(t, e, n, r, o);
    return h.getState() == X.ERROR && a.getUseInterimTilesOnError() && a.getPreload() > 0 && (this.newTiles_ = !0), this.isDrawableTile(h) || (h = h.getInterimTile()), h;
  }
  getData(t) {
    const e = this.frameState;
    if (!e)
      return null;
    const n = this.getLayer(), s = Ft(
      e.pixelToCoordinateTransform,
      t.slice()
    ), r = n.getExtent();
    if (r && !fo(r, s))
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
      if (!(g instanceof Ad || g instanceof _a) || g instanceof _a && g.getState() === X.EMPTY)
        return null;
      if (g.getState() !== X.LOADED)
        continue;
      const m = c.getOrigin(d), p = ce(c.getTileSize(d)), v = c.getResolution(d), y = Math.floor(
        u * ((s[0] - m[0]) / v - f[1] * p[0])
      ), x = Math.floor(
        u * ((m[1] - s[1]) / v - f[2] * p[1])
      ), M = Math.round(
        u * h.getGutterForProjection(l.projection)
      );
      return this.getImageData(g.getImage(), y + M, x + M);
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
    const v = t.viewState.resolution, y = u.getTilePixelRatio(h), x = Math.round(mt(p) / v * h), M = Math.round(je(p) / v * h), C = n.extent && Xi(n.extent);
    C && (p = xs(
      p,
      Xi(n.extent)
    ));
    const E = m * x / 2 / y, b = m * M / 2 / y, S = [
      a[0] - E,
      a[1] - b,
      a[0] + E,
      a[1] + b
    ], O = f.getTileRangeForExtentAndZ(p, g), D = {};
    D[g] = {};
    const H = this.createLoadedTileFinder(
      u,
      r,
      D
    ), R = this.tmpExtent, j = this.tmpTileRange_;
    this.newTiles_ = !1;
    const dt = l ? da(
      s.center,
      v,
      l,
      t.size
    ) : void 0;
    for (let ae = O.minX; ae <= O.maxX; ++ae)
      for (let at = O.minY; at <= O.maxY; ++at) {
        if (l && !f.tileCoordIntersectsViewport([g, ae, at], dt))
          continue;
        const ft = this.getTile(g, ae, at, t);
        if (this.isDrawableTile(ft)) {
          const kt = rt(this);
          if (ft.getState() == X.LOADED) {
            D[g][ft.tileCoord.toString()] = ft;
            let Be = ft.inTransition(kt);
            Be && n.opacity !== 1 && (ft.endTransition(kt), Be = !1), !this.newTiles_ && (Be || !this.renderedTiles.includes(ft)) && (this.newTiles_ = !0);
          }
          if (ft.getAlpha(kt, t.time) === 1)
            continue;
        }
        const hi = f.getTileCoordChildTileRange(
          ft.tileCoord,
          j,
          R
        );
        let Le = !1;
        hi && (Le = H(g + 1, hi)), Le || f.forEachTileCoordParentTileRange(
          ft.tileCoord,
          H,
          j,
          R
        );
      }
    const N = m / o * h / y;
    _i(
      this.pixelTransform,
      t.size[0] / 2,
      t.size[1] / 2,
      1 / h,
      1 / h,
      l,
      -x / 2,
      -M / 2
    );
    const F = wu(this.pixelTransform);
    this.useContainer(e, F, this.getBackground(t));
    const L = this.context, $ = L.canvas;
    qa(this.inversePixelTransform, this.pixelTransform), _i(
      this.tempTransform,
      x / 2,
      M / 2,
      N,
      N,
      0,
      -x / 2,
      -M / 2
    ), $.width != x || $.height != M ? ($.width = x, $.height = M) : this.containerReused || L.clearRect(0, 0, x, M), C && this.clipUnrotated(L, t, C), u.getInterpolate() || (L.imageSmoothingEnabled = !1), this.preRender(L, t), this.renderedTiles.length = 0;
    let wt = Object.keys(D).map(Number);
    wt.sort(qi);
    let vt, It, _;
    n.opacity === 1 && (!this.containerReused || u.getOpaque(t.viewState.projection)) ? wt = wt.reverse() : (vt = [], It = []);
    for (let ae = wt.length - 1; ae >= 0; --ae) {
      const at = wt[ae], ft = u.getTilePixelSize(
        at,
        h,
        r
      ), Le = f.getResolution(at) / m, kt = ft[0] * Le * N, Be = ft[1] * Le * N, ln = f.getTileCoordForCoordAndZ(
        Ai(S),
        at
      ), rr = f.getTileCoordExtent(ln), hn = Ft(this.tempTransform, [
        y * (rr[0] - S[0]) / m,
        y * (S[3] - rr[3]) / m
      ]), or = y * u.getGutterForProjection(r), ci = D[at];
      for (const ss in ci) {
        const ui = ci[ss], ar = ui.tileCoord, lr = ln[1] - ar[1], hr = Math.round(hn[0] - (lr - 1) * kt), cn = ln[2] - ar[2], Io = Math.round(hn[1] - (cn - 1) * Be), Qt = Math.round(hn[0] - lr * kt), me = Math.round(hn[1] - cn * Be), we = hr - Qt, We = Io - me, un = g === at, Ni = un && ui.getAlpha(rt(this), t.time) !== 1;
        let di = !1;
        if (!Ni)
          if (vt) {
            _ = [Qt, me, Qt + we, me, Qt + we, me + We, Qt, me + We];
            for (let dn = 0, cr = vt.length; dn < cr; ++dn)
              if (g !== at && at < It[dn]) {
                const Vt = vt[dn];
                ie(
                  [Qt, me, Qt + we, me + We],
                  [Vt[0], Vt[3], Vt[4], Vt[7]]
                ) && (di || (L.save(), di = !0), L.beginPath(), L.moveTo(_[0], _[1]), L.lineTo(_[2], _[3]), L.lineTo(_[4], _[5]), L.lineTo(_[6], _[7]), L.moveTo(Vt[6], Vt[7]), L.lineTo(Vt[4], Vt[5]), L.lineTo(Vt[2], Vt[3]), L.lineTo(Vt[0], Vt[1]), L.clip());
              }
            vt.push(_), It.push(at);
          } else
            L.clearRect(Qt, me, we, We);
        this.drawTileImage(
          ui,
          t,
          Qt,
          me,
          we,
          We,
          or,
          un
        ), vt && !Ni ? (di && L.restore(), this.renderedTiles.unshift(ui)) : this.renderedTiles.push(ui), this.updateUsedTiles(t.usedTiles, u, ui);
      }
    }
    return this.renderedRevision = d, this.renderedResolution = m, this.extentChanged = !this.renderedExtent_ || !_s(this.renderedExtent_, S), this.renderedExtent_ = S, this.renderedPixelRatio = h, this.renderedProjection = r, this.manageTilePyramid(
      t,
      u,
      f,
      h,
      r,
      p,
      g,
      c.getPreload()
    ), this.scheduleExpireCache(t, u), this.postRender(L, t), n.extent && L.restore(), L.imageSmoothingEnabled = !0, F !== $.style.transform && ($.style.transform = F), this.container;
  }
  drawTileImage(t, e, n, s, r, o, a, l) {
    const h = this.getTileImage(t);
    if (!h)
      return;
    const c = rt(this), u = e.layerStatesArray[e.layerIndex], d = u.opacity * (l ? t.getAlpha(c, e.time) : 1), f = d !== this.context.globalAlpha;
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
        const a = rt(s);
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
    const s = rt(e);
    s in t || (t[s] = {}), t[s][n.getKey()] = !0;
  }
  manageTilePyramid(t, e, n, s, r, o, a, l, h) {
    const c = rt(e);
    c in t.wantedTiles || (t.wantedTiles[c] = {});
    const u = t.wantedTiles[c], d = t.tileQueue, f = n.getMinZoom(), g = t.viewState.rotation, m = g ? da(
      t.viewState.center,
      t.viewState.resolution,
      g,
      t.size
    ) : void 0;
    let p = 0, v, y, x, M, C, E;
    for (E = f; E <= a; ++E)
      for (y = n.getTileRangeForExtentAndZ(o, E, y), x = n.getResolution(E), M = y.minX; M <= y.maxX; ++M)
        for (C = y.minY; C <= y.maxY; ++C)
          g && !n.tileCoordIntersectsViewport([E, M, C], m) || (a - E <= l ? (++p, v = e.getTile(E, M, C, s, r), v.getState() == X.IDLE && (u[v.getKey()] = !0, d.isKeyQueued(v.getKey()) || d.enqueue([
            v,
            c,
            n.getTileCoordCenter(v.tileCoord),
            x
          ])), h !== void 0 && h(v)) : e.useTile(E, M, C, r));
    e.updateCacheSize(p, r);
  }
}
const qm = Jm;
class Km extends Um {
  constructor(t) {
    super(t);
  }
  createRenderer() {
    return new qm(this);
  }
}
const Qm = Km;
class $m extends kd {
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
function tp(i, t, e) {
  const n = [], s = [], r = [], o = [], a = [];
  e = e !== void 0 ? e : [];
  const l = "SupportedCRS", h = "TileMatrix", c = "Identifier", u = "ScaleDenominator", d = "TopLeftCorner", f = "TileWidth", g = "TileHeight", m = i[l], p = K(m), v = p.getMetersPerUnit(), y = p.getAxisOrientation().substr(0, 2) == "ne";
  return i[h].sort(function(x, M) {
    return M[u] - x[u];
  }), i[h].forEach(function(x) {
    let M;
    if (e.length > 0 ? M = e.find(function(C) {
      return x[c] == C[h] ? !0 : x[c].includes(":") ? !1 : i[c] + ":" + x[c] === C[h];
    }) : M = !0, M) {
      s.push(x[c]);
      const C = x[u] * 28e-5 / v, E = x[f], b = x[g];
      y ? r.push([
        x[d][1],
        x[d][0]
      ]) : r.push(x[d]), n.push(C), o.push(
        E == b ? E : [E, b]
      ), a.push([x.MatrixWidth, x.MatrixHeight]);
    }
  }), new $m({
    extent: t,
    origins: r,
    resolutions: n,
    matrixIds: s,
    tileSizes: o,
    sizes: a
  });
}
class ep extends Bm {
  constructor(t) {
    const e = t.requestEncoding !== void 0 ? t.requestEncoding : "KVP", n = t.tileGrid;
    let s = t.urls;
    s === void 0 && t.url !== void 0 && (s = Hd(t.url)), super({
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
    }), this.version_ = t.version !== void 0 ? t.version : "1.0.0", this.format_ = t.format !== void 0 ? t.format : "image/jpeg", this.dimensions_ = t.dimensions !== void 0 ? t.dimensions : {}, this.layer_ = t.layer, this.matrixSet_ = t.matrixSet, this.style_ = t.style, this.requestEncoding_ = e, this.setKey(this.getKeyForDimensions_()), s && s.length > 0 && (this.tileUrlFunction = Ra(
      s.map(this.createFromWMTSTemplate.bind(this))
    ));
  }
  setUrls(t) {
    this.urls = t;
    const e = t.join(`
`);
    this.setTileUrlFunction(
      Ra(
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
    }), t = e == "KVP" ? lc(t, n) : t.replace(/\{(\w+?)\}/g, function(o, a) {
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
        return e == "KVP" ? c = lc(c, h) : c = c.replace(/\{(\w+?)\}/g, function(u, d) {
          return h[d];
        }), c;
      } else
        return;
    };
  }
}
const ip = ep;
function np(i, t) {
  const n = i.Contents.Layer.find(function(R) {
    return R.Identifier == t.layer;
  });
  if (!n)
    return null;
  const s = i.Contents.TileMatrixSet;
  let r;
  n.TileMatrixSetLink.length > 1 ? "projection" in t ? r = n.TileMatrixSetLink.findIndex(function(R) {
    const dt = s.find(function(L) {
      return L.Identifier == R.TileMatrixSet;
    }).SupportedCRS, N = K(dt), F = K(t.projection);
    return N && F ? Oe(N, F) : dt == t.projection;
  }) : r = n.TileMatrixSetLink.findIndex(function(R) {
    return R.TileMatrixSet == t.matrixSet;
  }) : r = 0, r < 0 && (r = 0);
  const o = n.TileMatrixSetLink[r].TileMatrixSet, a = n.TileMatrixSetLink[r].TileMatrixSetLimits;
  let l = n.Format[0];
  "format" in t && (l = t.format), r = n.Style.findIndex(function(R) {
    return "style" in t ? R.Title == t.style : R.isDefault;
  }), r < 0 && (r = 0);
  const h = n.Style[r].Identifier, c = {};
  "Dimension" in n && n.Dimension.forEach(function(R, j, dt) {
    const N = R.Identifier;
    let F = R.Default;
    F === void 0 && (F = R.Value[0]), c[N] = F;
  });
  const d = i.Contents.TileMatrixSet.find(function(R) {
    return R.Identifier == o;
  });
  let f;
  const g = d.SupportedCRS;
  if (g && (f = K(g)), "projection" in t) {
    const R = K(t.projection);
    R && (!f || Oe(R, f)) && (f = R);
  }
  let m = !1;
  const p = f.getAxisOrientation().substr(0, 2) == "ne";
  let v = d.TileMatrix[0], y = {
    MinTileCol: 0,
    MinTileRow: 0,
    MaxTileCol: v.MatrixWidth - 1,
    MaxTileRow: v.MatrixHeight - 1
  };
  if (a) {
    y = a[a.length - 1];
    const R = d.TileMatrix.find(
      (j) => j.Identifier === y.TileMatrix || d.Identifier + ":" + j.Identifier === y.TileMatrix
    );
    R && (v = R);
  }
  const x = v.ScaleDenominator * 28e-5 / f.getMetersPerUnit(), M = p ? [v.TopLeftCorner[1], v.TopLeftCorner[0]] : v.TopLeftCorner, C = v.TileWidth * x, E = v.TileHeight * x;
  let b = d.BoundingBox;
  b && p && (b = [
    b[1],
    b[0],
    b[3],
    b[2]
  ]);
  let S = [
    M[0] + C * y.MinTileCol,
    M[1] - E * (1 + y.MaxTileRow),
    M[0] + C * (1 + y.MaxTileCol),
    M[1] - E * y.MinTileRow
  ];
  if (b !== void 0 && !Mi(b, S)) {
    const R = n.WGS84BoundingBox, j = K("EPSG:4326").getExtent();
    if (S = b, R)
      m = R[0] === j[0] && R[2] === j[2];
    else {
      const dt = Ju(
        b,
        d.SupportedCRS,
        "EPSG:4326"
      );
      m = dt[0] - 1e-10 <= j[0] && dt[2] + 1e-10 >= j[2];
    }
  }
  const O = tp(
    d,
    S,
    a
  ), D = [];
  let H = t.requestEncoding;
  if (H = H !== void 0 ? H : "", "OperationsMetadata" in i && "GetTile" in i.OperationsMetadata) {
    const R = i.OperationsMetadata.GetTile.DCP.HTTP.Get;
    for (let j = 0, dt = R.length; j < dt; ++j)
      if (R[j].Constraint) {
        const F = R[j].Constraint.find(function(L) {
          return L.name == "GetEncoding";
        }).AllowedValues.Value;
        if (H === "" && (H = F[0]), H === "KVP")
          F.includes("KVP") && D.push(R[j].href);
        else
          break;
      } else
        R[j].href && (H = "KVP", D.push(R[j].href));
  }
  return D.length === 0 && (H = "REST", n.ResourceURL.forEach(function(R) {
    R.resourceType === "tile" && (l = R.format, D.push(R.template));
  })), {
    urls: D,
    layer: t.layer,
    matrixSet: o,
    format: l,
    projection: f,
    requestEncoding: H,
    tileGrid: O,
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
      let n = e.dataProjection ? K(e.dataProjection) : this.readProjection(t);
      e.extent && n && n.getUnits() === "tile-pixels" && (n = K(n), n.setWorldExtent(e.extent)), e = {
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
    return B();
  }
  readFeature(t, e) {
    return B();
  }
  readFeatures(t, e) {
    return B();
  }
  readGeometry(t, e) {
    return B();
  }
  readProjection(t) {
    return B();
  }
  writeFeature(t, e) {
    return B();
  }
  writeFeatures(t, e) {
    return B();
  }
  writeGeometry(t, e) {
    return B();
  }
}
function qs(i, t, e) {
  const n = e ? K(e.featureProjection) : null, s = e ? K(e.dataProjection) : null;
  let r;
  if (n && s && !Oe(n, s) ? r = (t ? i.clone() : i).transform(
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
  const e = t ? K(t.featureProjection) : null, n = t ? K(t.dataProjection) : null;
  return e && n && !Oe(e, n) ? Ju(i, n, e) : i;
}
class qr extends on {
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
        l === 0 && (s = c.getLayout()), qt(o, c.getFlatCoordinates()), a.push(o.length);
      }
      this.setFlatCoordinates(s, o), this.ends_ = a;
    }
  }
  appendLineString(t) {
    this.flatCoordinates ? qt(this.flatCoordinates, t.getFlatCoordinates().slice()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.ends_.push(this.flatCoordinates.length), this.changed();
  }
  clone() {
    const t = new qr(
      this.flatCoordinates.slice(),
      this.layout,
      this.ends_.slice()
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    return s < rn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
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
    return this.layout != "XYM" && this.layout != "XYZM" || this.flatCoordinates.length === 0 ? null : (e = e !== void 0 ? e : !1, n = n !== void 0 ? n : !1, J1(
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
    return zs(
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
    return t < 0 || this.ends_.length <= t ? null : new Fs(
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
      const l = e[o], h = new Fs(
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
      const l = s[o], h = pd(
        e,
        n,
        l,
        r,
        0.5
      );
      qt(t, h), n = l;
    }
    return t;
  }
  getSimplifiedGeometryInternal(t) {
    const e = [], n = [];
    return e.length = jg(
      this.flatCoordinates,
      0,
      this.ends_,
      this.stride,
      t,
      e,
      0,
      n
    ), new qr(e, "XY", n);
  }
  getType() {
    return "MultiLineString";
  }
  intersectsExtent(t) {
    return Wg(
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
const Ll = qr;
class Ol extends on {
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
    this.flatCoordinates ? qt(this.flatCoordinates, t.getFlatCoordinates()) : this.flatCoordinates = t.getFlatCoordinates().slice(), this.changed();
  }
  clone() {
    const t = new Ol(
      this.flatCoordinates.slice(),
      this.layout
    );
    return t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    if (s < rn(this.getExtent(), t, e))
      return s;
    const r = this.flatCoordinates, o = this.stride;
    for (let a = 0, l = r.length; a < l; a += o) {
      const h = Wi(
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
    return Ci(
      this.flatCoordinates,
      0,
      this.flatCoordinates.length,
      this.stride
    );
  }
  getPoint(t) {
    const e = this.flatCoordinates ? this.flatCoordinates.length / this.stride : 0;
    return t < 0 || e <= t ? null : new oi(
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
      const a = new oi(t.slice(r, r + n), e);
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
      if (Ka(t, o, a))
        return !0;
    }
    return !1;
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 1), this.flatCoordinates || (this.flatCoordinates = []), this.flatCoordinates.length = Co(
      this.flatCoordinates,
      0,
      t,
      this.stride
    ), this.changed();
  }
}
const Po = Ol;
function sp(i, t, e, n) {
  const s = [];
  let r = fe();
  for (let o = 0, a = e.length; o < a; ++o) {
    const l = e[o];
    r = Pu(
      i,
      t,
      l[0],
      n
    ), s.push((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), t = l[l.length - 1];
  }
  return s;
}
class Kr extends on {
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
        qt(o, c.getFlatCoordinates()), a.push(d);
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
      qt(this.flatCoordinates, t.getFlatCoordinates()), e = t.getEnds().slice();
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
    return s < rn(this.getExtent(), t, e) ? s : (this.maxDeltaRevision_ != this.getRevision() && (this.maxDelta_ = Math.sqrt(
      Ng(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride,
        0
      )
    ), this.maxDeltaRevision_ = this.getRevision()), zg(
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
    return Zg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t,
      e
    );
  }
  getArea() {
    return Gg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride
    );
  }
  getCoordinates(t) {
    let e;
    return t !== void 0 ? (e = this.getOrientedFlatCoordinates().slice(), zh(
      e,
      0,
      this.endss_,
      this.stride,
      t
    )) : e = this.flatCoordinates, Ma(
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
      const t = sp(
        this.flatCoordinates,
        0,
        this.endss_,
        this.stride
      );
      this.flatInteriorPoints_ = Bg(
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
    return new Po(this.getFlatInteriorPoints().slice(), "XYM");
  }
  getOrientedFlatCoordinates() {
    if (this.orientedRevision_ != this.getRevision()) {
      const t = this.flatCoordinates;
      Ug(t, 0, this.endss_, this.stride) ? this.orientedFlatCoordinates_ = t : (this.orientedFlatCoordinates_ = t.slice(), this.orientedFlatCoordinates_.length = zh(
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
    return e.length = Xg(
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
    return new Zn(
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
      const c = new Zn(
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
    return Vg(
      this.getOrientedFlatCoordinates(),
      0,
      this.endss_,
      this.stride,
      t
    );
  }
  setCoordinates(t, e) {
    this.setLayout(e, t, 3), this.flatCoordinates || (this.flatCoordinates = []);
    const n = Dg(
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
class Qr extends $u {
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
          et(this.geometries_[t], V.CHANGE, this.changed, this)
        );
  }
  clone() {
    const t = new Qr(null);
    return t.setGeometries(this.geometries_), t.applyProperties(this), t;
  }
  closestPointXY(t, e, n, s) {
    if (s < rn(this.getExtent(), t, e))
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
    Bs(t);
    const e = this.geometries_;
    for (let n = 0, s = e.length; n < s; ++n)
      Su(t, e[n].getExtent());
    return t;
  }
  getGeometries() {
    return hc(this.geometries_);
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
      const r = new Qr(null);
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
    this.setGeometriesArray(hc(t));
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
function hc(i) {
  const t = [];
  for (let e = 0, n = i.length; e < n; ++e)
    t.push(i[e].clone());
  return t;
}
const Bd = Qr;
class rp extends Zd {
  constructor() {
    super();
  }
  getType() {
    return "json";
  }
  readFeature(t, e) {
    return this.readFeatureFromObject(
      br(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatures(t, e) {
    return this.readFeaturesFromObject(
      br(t),
      this.getReadOptions(t, e)
    );
  }
  readFeatureFromObject(t, e) {
    return B();
  }
  readFeaturesFromObject(t, e) {
    return B();
  }
  readGeometry(t, e) {
    return this.readGeometryFromObject(
      br(t),
      this.getReadOptions(t, e)
    );
  }
  readGeometryFromObject(t, e) {
    return B();
  }
  readProjection(t) {
    return this.readProjectionFromObject(br(t));
  }
  readProjectionFromObject(t) {
    return B();
  }
  writeFeature(t, e) {
    return JSON.stringify(this.writeFeatureObject(t, e));
  }
  writeFeatureObject(t, e) {
    return B();
  }
  writeFeatures(t, e) {
    return JSON.stringify(this.writeFeaturesObject(t, e));
  }
  writeFeaturesObject(t, e) {
    return B();
  }
  writeGeometry(t, e) {
    return JSON.stringify(this.writeGeometryObject(t, e));
  }
  writeGeometryObject(t, e) {
    return B();
  }
}
function br(i) {
  if (typeof i == "string") {
    const t = JSON.parse(i);
    return t || null;
  } else
    return i !== null ? i : null;
}
const op = rp;
class ap extends op {
  constructor(t) {
    t = t || {}, super(), this.dataProjection = K(
      t.dataProjection ? t.dataProjection : "EPSG:4326"
    ), t.featureProjection && (this.defaultFeatureProjection = K(t.featureProjection)), this.geometryName_ = t.geometryName, this.extractGeometryName_ = t.extractGeometryName, this.supportedMediaTypes = [
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
    const s = Ta(n.geometry, e), r = new an();
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
    return Ta(t, e);
  }
  readProjectionFromObject(t) {
    const e = t.crs;
    let n;
    return e ? e.type == "name" ? n = K(e.properties.name) : e.type === "EPSG" ? n = K("EPSG:" + e.properties.code) : Y(!1, 36) : n = this.dataProjection, n;
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
    return o && (n.geometry = La(o, e), delete r[t.getGeometryName()]), jn(r) || (n.properties = r), n;
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
    return La(t, this.adaptOptions(e));
  }
}
function Ta(i, t) {
  if (!i)
    return null;
  let e;
  switch (i.type) {
    case "Point": {
      e = hp(i);
      break;
    }
    case "LineString": {
      e = cp(
        i
      );
      break;
    }
    case "Polygon": {
      e = gp(i);
      break;
    }
    case "MultiPoint": {
      e = dp(
        i
      );
      break;
    }
    case "MultiLineString": {
      e = up(
        i
      );
      break;
    }
    case "MultiPolygon": {
      e = fp(
        i
      );
      break;
    }
    case "GeometryCollection": {
      e = lp(
        i
      );
      break;
    }
    default:
      throw new Error("Unsupported GeoJSON type: " + i.type);
  }
  return qs(e, !1, t);
}
function lp(i, t) {
  const e = i.geometries.map(
    function(n) {
      return Ta(n, t);
    }
  );
  return new Bd(e);
}
function hp(i) {
  return new oi(i.coordinates);
}
function cp(i) {
  return new Fs(i.coordinates);
}
function up(i) {
  return new Ll(i.coordinates);
}
function dp(i) {
  return new Po(i.coordinates);
}
function fp(i) {
  return new Al(i.coordinates);
}
function gp(i) {
  return new Zn(i.coordinates);
}
function La(i, t) {
  i = qs(i, !0, t);
  const e = i.getType();
  let n;
  switch (e) {
    case "Point": {
      n = Mp(i);
      break;
    }
    case "LineString": {
      n = pp(
        i
      );
      break;
    }
    case "Polygon": {
      n = Cp(
        i,
        t
      );
      break;
    }
    case "MultiPoint": {
      n = yp(
        i
      );
      break;
    }
    case "MultiLineString": {
      n = vp(
        i
      );
      break;
    }
    case "MultiPolygon": {
      n = xp(
        i,
        t
      );
      break;
    }
    case "GeometryCollection": {
      n = mp(
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
function mp(i, t) {
  return t = Object.assign({}, t), delete t.featureProjection, {
    type: "GeometryCollection",
    geometries: i.getGeometriesArray().map(function(n) {
      return La(n, t);
    })
  };
}
function pp(i, t) {
  return {
    type: "LineString",
    coordinates: i.getCoordinates()
  };
}
function vp(i, t) {
  return {
    type: "MultiLineString",
    coordinates: i.getCoordinates()
  };
}
function yp(i, t) {
  return {
    type: "MultiPoint",
    coordinates: i.getCoordinates()
  };
}
function xp(i, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "MultiPolygon",
    coordinates: i.getCoordinates(e)
  };
}
function Mp(i, t) {
  return {
    type: "Point",
    coordinates: i.getCoordinates()
  };
}
function Cp(i, t) {
  let e;
  return t && (e = t.rightHanded), {
    type: "Polygon",
    coordinates: i.getCoordinates(e)
  };
}
const Wd = ap;
class tt {
  static sendEvent(t, e) {
    dispatchEvent(new CustomEvent(t, { detail: e }));
  }
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Vd = { ATTRIBUTE: 1, CHILD: 2, PROPERTY: 3, BOOLEAN_ATTRIBUTE: 4, EVENT: 5, ELEMENT: 6 }, Il = (i) => (...t) => ({ _$litDirective$: i, values: t });
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
const { I: wp } = Wf, Pr = (i, t) => t === void 0 ? (i == null ? void 0 : i._$litType$) !== void 0 : (i == null ? void 0 : i._$litType$) === t, cc = () => document.createComment(""), uc = (i, t, e) => {
  var n;
  const s = i._$AA.parentNode, r = t === void 0 ? i._$AB : t._$AA;
  if (e === void 0) {
    const o = s.insertBefore(cc(), r), a = s.insertBefore(cc(), r);
    e = new wp(o, a, i, i.options);
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
}, Ep = {}, dc = (i, t = Ep) => i._$AH = t, fc = (i) => i._$AH, bp = (i) => {
  i._$AR();
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const zl = Il(class extends Nl {
  constructor(i) {
    super(i), this.et = /* @__PURE__ */ new WeakMap();
  }
  render(i) {
    return [i];
  }
  update(i, [t]) {
    if (Pr(this.it) && (!Pr(t) || this.it.strings !== t.strings)) {
      const e = fc(i).pop();
      let n = this.et.get(this.it.strings);
      if (n === void 0) {
        const s = document.createDocumentFragment();
        n = vu(Rt, s), n.setConnected(!1), this.et.set(this.it.strings, n);
      }
      dc(n, [e]), uc(n, void 0, e);
    }
    if (Pr(t)) {
      if (!Pr(this.it) || this.it.strings !== t.strings) {
        const e = this.et.get(t.strings);
        if (e !== void 0) {
          const n = fc(e).pop();
          bp(i), uc(i, void 0, n), dc(i, [n]);
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
class Oa extends Nl {
  constructor(t) {
    if (super(t), this.it = Rt, t.type !== Vd.CHILD)
      throw Error(this.constructor.directiveName + "() can only be used in child bindings");
  }
  render(t) {
    if (t === Rt || t == null)
      return this._t = void 0, this.it = t;
    if (t === Pi)
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
Oa.directiveName = "unsafeHTML", Oa.resultType = 1;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class Aa extends Oa {
}
Aa.directiveName = "unsafeSVG", Aa.resultType = 2;
const Re = Il(Aa);
class gt {
  constructor() {
    this.customDisplay = !1, this.targetBoxSize = "", this.selectedFeatures = [], this.currentItemId = -1, this.maxElement = -1;
  }
  static setTheme(t) {
    this.theme = t;
  }
  static getTheme() {
    return this.theme;
  }
  static setGeolocation(t) {
    this.geolocation = t;
  }
  static getGeolocation() {
    return this.geolocation;
  }
  setCustomDisplay(t) {
    this.customDisplay = t;
  }
  isCustomDisplay() {
    return this.customDisplay;
  }
  setTargetBoxSize(t) {
    this.targetBoxSize = t;
  }
  getTargetBoxSize() {
    return this.targetBoxSize;
  }
  setOptions(t) {
    this.options = t;
  }
  getOptions() {
    return this.options;
  }
  setMap(t) {
    this.map = t;
  }
  getMap() {
    return this.map;
  }
  addSelectedFeature(t, e, n) {
    this.selectedFeatures.push({
      id: e,
      type: n,
      feature: t
    });
  }
  removeSelectedFeature(t) {
    const e = this.selectedFeatures.findIndex((n) => n.id === t);
    e !== -1 && this.selectedFeatures.splice(e, 1);
  }
  removeLastSelectedFeature() {
    this.selectedFeatures.splice(-1);
  }
  removeAllSelectedFeatures() {
    this.selectedFeatures = [];
  }
  getSelectedFeature(t) {
    const e = this.selectedFeatures.findIndex((n) => n.id === t);
    return e !== -1 ? this.selectedFeatures[e].feature : void 0;
  }
  getCurrentFeatureType(t) {
    const e = this.selectedFeatures.findIndex((n) => n.id === t);
    return e !== -1 ? this.selectedFeatures[e].type : "";
  }
  unselectFeatures() {
    var t;
    (t = this.selectedFeatures.find((e) => e.feature.get("isSelected"))) == null || t.feature.set("isSelected", void 0);
  }
  getSelectedFeatures() {
    return this.selectedFeatures.map((t) => t.feature);
  }
  setBorderConstraint(t) {
    this.borderConstraint = t;
  }
  getBorderConstraint() {
    return this.borderConstraint;
  }
  setCurrentItemId(t) {
    this.currentItemId = t;
  }
  getCurrentItemId() {
    return this.currentItemId;
  }
  setMaxElement(t) {
    this.maxElement = t;
  }
  getMaxElement() {
    return this.maxElement;
  }
}
gt.theme = "";
const Pp = `@media only screen and (min-width: 351px) and (max-width: 995px){.box-element{left:calc(50% - 167px);width:calc(100% - 30px);max-width:302px}}@media only screen and (max-width: 350px){.box-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 996px){.box-element{left:calc((100% - (var(--select-box-width) + 30px)) / 2);width:calc(var(--select-box-width))}}.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color);font-family:sans-serif;display:flex;z-index:5}.box-text-container{width:calc(100% - 80px)}.box-icon-container{width:80px;display:flex}.box-element-title{display:flex}.box-element-title-text{width:900%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color);width:90%}.position-icon{display:flex;justify-content:flex-end;width:50%}.icon-container{width:36px;height:36px;background-color:var(--select-icon-background);border-radius:var(--icon-border-radius)}.icon-container>svg{display:block;margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size)!important;height:var(--svg-icon-size)!important}.icon-container>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
class Wt {
  static setEvent(t, e, n) {
    n.getView().on(t, e);
  }
  static unsetEvent(t, e, n) {
    n.getView().on(t, e);
  }
  static registerWindowListener(t, e, n, s) {
    window.addEventListener(t, () => {
      Wt.unsetEvent(e, n, s), Wt.setEvent(e, n, s);
    });
  }
  static registerBorderConstaintMapEvent(t, e, n, s) {
    s.border.url !== "" && Wt.registerWindowListener(
      "border-contraint-enabled",
      t,
      e,
      n
    ), Wt.setEvent(t, e, n);
  }
  static setCursorEvent(t) {
    t.on("movestart", () => {
      t.getViewport().style.cursor = "all-scroll";
    }), t.on("moveend", () => {
      t.getViewport().style.cursor = "default";
    });
  }
  static setResizeEvent(t, e, n) {
    const s = n.getSize();
    s && t.style.setProperty(e, s[0] * 0.33 + "px"), n.on("change:size", () => {
      const r = n.getSize();
      r && t.style.setProperty(e, r[0] * 0.33 + "px");
    });
  }
}
class Yd {
  static getAddressFromCoordinate(t) {
    return fetch(`https://api3.geo.admin.ch/rest/services/api/MapServer/identify?mapExtent=0,0,100,100&imageDisplay=100,100,100&tolerance=20&geometryType=esriGeometryPoint&geometry=${t[0]},${t[1]}&layers=all:ch.bfs.gebaeude_wohnungs_register&returnGeometry=false&sr=2056`).then((e) => e.json());
  }
}
class st {
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
st.info = `
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
st.warning = `
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
st.error = `
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
st.mapPin = `
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
st.mapPinClick = `
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
st.mapPinSelect = `
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
st.information = `
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
st.geolocation = `
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
st.rotation = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="North">
        <g class="icon">
          <path d="M12 27.2375L16.2375 23L20.475 27.2375" class="Vector"/>
          <path d="M12 18V7L20.5 18V7" class="Vector 3"/>
        </g>
      </g>
    </svg>
  `;
st.iconRecenter = `
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
st.iconRemoveSelection = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      <g class="RemoveSelection">
        <g class="icon">
          <path d="M16 28C22.627 28 28 22.627 28 16 28 9.373 22.627 4 16 4 9.373 4 4 9.373 4 16 4 22.627 9.373 28 16 28ZM20 12 12 20M20 20 12 12" class="Vector"/>
        </g>
      </g>
    </svg>
  `;
st.search = `
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
st.cross = `
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
st.stack = `
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
var Sp = Object.defineProperty, _p = Object.getOwnPropertyDescriptor, So = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? _p(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && Sp(t, e, s), s;
};
let Qi = class extends At {
  constructor(i) {
    super(), this.currentPosition = [0, 0], this._isRecenterButton = !0, this._currentPosition = "", this.store = i;
    const t = this.store.getMap(), e = this.store.getOptions();
    if (!t || !e)
      throw new Error("invalid map or options");
    Wt.registerBorderConstaintMapEvent("change:center", () => this.setCenterChange(), t, e), window.addEventListener("open-select-create-box", (n) => {
      Yd.getAddressFromCoordinate(n.detail).then((s) => {
        this._currentPosition = s.results.length > 0 ? `\xC0 proximit\xE9 de ${s.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
      }), this.setCenterChange();
    });
  }
  setCenterChange() {
    var t, e;
    const i = this.store.getSelectedFeature(this.store.getCurrentItemId());
    if (i) {
      const n = i.get("geom");
      this._isRecenterButton = n.intersectsExtent((e = this.store.getMap()) == null ? void 0 : e.getView().calculateExtent((t = this.store.getMap()) == null ? void 0 : t.getSize()));
    }
  }
  connectedCallback() {
    super.connectedCallback();
  }
  render() {
    var i;
    return Ct`
      <div class="information-box-${gt.getTheme()} box-element">
        <div class="box-text-container">
            <div class="box-element-title">
            <div class="box-element-title-text">${(i = this.store.getOptions()) == null ? void 0 : i.selectionTargetBoxMessage}</div>
            </div>
            <div class="box-element-content">${this._currentPosition}</div>
        </div>
        <div class="box-icon-container">
          <div class="position-icon">
          ${zl(
      this._isRecenterButton ? Ct`` : Ct`<div class="icon-container" @click="${this.recenter}">
                      ${Re(st.iconRecenter)}
                    </div>`
    )}
          </div>
          <div class="position-icon">
            <div class="icon-container" @click="${this.unselect}">
              ${Re(st.iconRemoveSelection)}
            </div>
          </div>
        </div>
      </div>
    `;
  }
  recenter() {
    tt.sendEvent("recenter-selected-element", void 0);
  }
  unselect() {
    var e;
    const i = this.store.getOptions();
    let t = "";
    switch ((i == null ? void 0 : i.mode.type) === "mix" ? t = this.store.getCurrentFeatureType(this.store.getCurrentItemId()) : t = (e = i == null ? void 0 : i.mode.type) != null ? e : "", t) {
      case "select":
        tt.sendEvent("icon-clicked", this.store.getCurrentItemId());
        break;
      case "create":
        tt.sendEvent("icon-removed", void 0);
        break;
    }
  }
};
Qi.styles = [yt(Pp)];
So([
  Te()
], Qi.prototype, "currentPosition", 2);
So([
  Lt()
], Qi.prototype, "_isRecenterButton", 2);
So([
  Lt()
], Qi.prototype, "_currentPosition", 2);
Qi = So([
  Kt("select-information-box-element")
], Qi);
class Fl extends Dt {
  constructor(t) {
    const e = new Qi(t);
    super({ element: e }), this.div = e;
    const n = t.getMap();
    if (!n)
      throw new Error("missing map");
    Wt.setResizeEvent(this.div, "--select-box-width", n);
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
class Rp {
  constructor() {
    this.clickImage = document.createElement("img"), this.clickImage.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(st.mapPinClick), this.selectImage = document.createElement("img"), this.selectImage.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(st.mapPinSelect);
  }
  clusterWithIcon(t) {
    const e = t.get("features").length;
    let n;
    return e === 1 && t.get("features")[0].get("isSelected") ? n = new Bt({
      zIndex: 1,
      image: new Ms({
        img: this.selectImage,
        imgSize: [42, 54],
        anchor: [0.52, 55],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && t.get("features")[0].get("isClick") ? n = new Bt({
      zIndex: 1,
      image: new Ms({
        img: this.clickImage,
        imgSize: [42, 54],
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : e === 1 && !t.get("features")[0].get("isClick") ? n = new Bt({
      zIndex: 1,
      image: new Ms({
        src: "data:image/svg+xml;charset=utf-8," + encodeURIComponent(st.mapPin),
        anchor: [0.5, 54],
        anchorXUnits: "fraction",
        anchorYUnits: "pixels"
      })
    }) : t.get("features").find((s) => s.get("isClick")) ? n = new Bt({
      image: new ni({
        radius: 15,
        stroke: new Se({
          color: "#fff"
        }),
        fill: new Ut({
          color: "#EF4444"
        })
      }),
      text: new Pa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Ut({
          color: "#fff"
        })
      })
    }) : n = new Bt({
      image: new ni({
        radius: 15,
        stroke: new Se({
          color: "#fff"
        }),
        fill: new Ut({
          color: "#334155"
        })
      }),
      text: new Pa({
        text: e.toString(),
        font: "14px sans-serif",
        fill: new Ut({
          color: "#fff"
        })
      })
    }), n;
  }
}
class Ud {
  static setCustomStyleWithouInfoBox(t) {
    var s, r;
    const e = t.getOptions();
    t.setCustomDisplay((r = (s = e == null ? void 0 : e.search) == null ? void 0 : s.displaySearch) != null ? r : !1);
    const n = e != null && e.search.displaySearch ? "small" : "no-box";
    t.setTargetBoxSize(n);
  }
}
const Ia = "http://www.w3.org/2001/XMLSchema-instance";
function J(i, t) {
  return Qd().createElementNS(i, t);
}
function $i(i, t) {
  return Jd(i, t, []).join("");
}
function Jd(i, t, e) {
  if (i.nodeType == Node.CDATA_SECTION_NODE || i.nodeType == Node.TEXT_NODE)
    t ? e.push(String(i.nodeValue).replace(/(\r\n|\r|\n)/g, "")) : e.push(i.nodeValue);
  else {
    let n;
    for (n = i.firstChild; n; n = n.nextSibling)
      Jd(n, t, e);
  }
  return e;
}
function Zi(i) {
  return "documentElement" in i;
}
function Tp(i, t, e) {
  return i.getAttributeNS(t, e) || "";
}
function Bi(i) {
  return new DOMParser().parseFromString(i, "application/xml");
}
function qd(i, t) {
  return function(e, n) {
    const s = i.call(
      t !== void 0 ? t : this,
      e,
      n
    );
    if (s !== void 0) {
      const r = n[n.length - 1];
      qt(r, s);
    }
  };
}
function W(i, t) {
  return function(e, n) {
    const s = i.call(
      t !== void 0 ? t : this,
      e,
      n
    );
    s !== void 0 && n[n.length - 1].push(s);
  };
}
function G(i, t) {
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
function I(i, t, e) {
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
function w(i, t) {
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
    return J(l, a);
  };
}
const Kd = de();
function ct(i, t, e) {
  e = e !== void 0 ? e : {};
  let n, s;
  for (n = 0, s = i.length; n < s; ++n)
    e[i[n]] = t;
  return e;
}
function Ui(i, t, e, n) {
  let s;
  for (s = t.firstElementChild; s; s = s.nextElementSibling) {
    const r = i[s.namespaceURI];
    if (r !== void 0) {
      const o = r[s.localName];
      o !== void 0 && o.call(n, s, e);
    }
  }
}
function k(i, t, e, n, s) {
  return n.push(i), Ui(t, e, n, s), n.pop();
}
function Lp(i, t, e, n, s, r) {
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
function bt(i, t, e, n, s, r, o) {
  return s.push(i), Lp(t, e, n, s, r, o), s.pop();
}
let na;
function Op() {
  return na === void 0 && typeof XMLSerializer < "u" && (na = new XMLSerializer()), na;
}
let sa;
function Qd() {
  return sa === void 0 && typeof document < "u" && (sa = document.implementation.createDocument("", "", null)), sa;
}
class Ap extends Zd {
  constructor() {
    super(), this.xmlSerializer_ = Op();
  }
  getType() {
    return "xml";
  }
  readFeature(t, e) {
    if (t)
      if (typeof t == "string") {
        const n = Bi(t);
        return this.readFeatureFromDocument(n, e);
      } else
        return Zi(t) ? this.readFeatureFromDocument(
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
        const n = Bi(t);
        return this.readFeaturesFromDocument(n, e);
      } else
        return Zi(t) ? this.readFeaturesFromDocument(
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
      s.nodeType == Node.ELEMENT_NODE && qt(
        n,
        this.readFeaturesFromNode(s, e)
      );
    return n;
  }
  readFeaturesFromNode(t, e) {
    return B();
  }
  readGeometry(t, e) {
    if (t)
      if (typeof t == "string") {
        const n = Bi(t);
        return this.readGeometryFromDocument(n, e);
      } else
        return Zi(t) ? this.readGeometryFromDocument(
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
        const e = Bi(t);
        return this.readProjectionFromDocument(e);
      } else
        return Zi(t) ? this.readProjectionFromDocument(t) : this.readProjectionFromNode(t);
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
const $d = Ap, ri = "http://www.opengis.net/gml", Ip = /^\s*$/;
class St extends $d {
  constructor(t) {
    super(), t = t || {}, this.featureType = t.featureType, this.featureNS = t.featureNS, this.srsName = t.srsName, this.schemaLocation = "", this.FEATURE_COLLECTION_PARSERS = {}, this.FEATURE_COLLECTION_PARSERS[this.namespace] = {
      featureMember: W(this.readFeaturesInternal),
      featureMembers: G(this.readFeaturesInternal)
    }, this.supportedMediaTypes = ["application/gml+xml"];
  }
  readFeaturesInternal(t, e) {
    const n = t.localName;
    let s = null;
    if (n == "FeatureCollection")
      s = k(
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
              let p = "", v = 0;
              const y = g.namespaceURI;
              for (const x in a) {
                if (a[x] === y) {
                  p = x;
                  break;
                }
                ++v;
              }
              p || (p = l + v, a[p] = y), o.push(p + ":" + m);
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
          (u[g].includes(":") ? u[g].split(":")[0] : h) === d && (f[u[g].split(":").pop()] = n == "featureMembers" ? W(this.readFeatureElement, this) : G(this.readFeatureElement, this));
        c[a[d]] = f;
      }
      n == "featureMember" || n == "member" ? s = k(void 0, c, t, e) : s = k([], c, t, e);
    }
    return s === null && (s = []), s;
  }
  readGeometryOrExtent(t, e) {
    const n = e[0];
    return n.srsName = t.firstElementChild.getAttribute("srsName"), n.srsDimension = t.firstElementChild.getAttribute("srsDimension"), k(
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
    return s ? qs(s, !1, n) : void 0;
  }
  readFeatureElementInternal(t, e, n) {
    let s;
    const r = {};
    for (let o = t.firstElementChild; o; o = o.nextElementSibling) {
      let a;
      const l = o.localName;
      o.childNodes.length === 0 || o.childNodes.length === 1 && (o.firstChild.nodeType === 3 || o.firstChild.nodeType === 4) ? (a = $i(o, !1), Ip.test(a) && (a = void 0)) : (n && (a = l === "boundedBy" ? this.readExtentElement(o, e) : this.readGeometryElement(o, e)), a ? l !== "boundedBy" && (s = l) : a = this.readFeatureElementInternal(o, e, !1));
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
      const o = new an(r);
      s && o.setGeometryName(s);
      const a = t.getAttribute("fid") || Tp(t, this.namespace, "id");
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
      return new oi(n, "XYZ");
  }
  readMultiPoint(t, e) {
    const n = k(
      [],
      this.MULTIPOINT_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Po(n);
  }
  readMultiLineString(t, e) {
    const n = k(
      [],
      this.MULTILINESTRING_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Ll(n);
  }
  readMultiPolygon(t, e) {
    const n = k(
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
    Ui(this.POINTMEMBER_PARSERS, t, e, this);
  }
  lineStringMemberParser(t, e) {
    Ui(this.LINESTRINGMEMBER_PARSERS, t, e, this);
  }
  polygonMemberParser(t, e) {
    Ui(this.POLYGONMEMBER_PARSERS, t, e, this);
  }
  readLineString(t, e) {
    const n = this.readFlatCoordinatesFromNode(t, e);
    if (n)
      return new Fs(n, "XYZ");
  }
  readFlatLinearRing(t, e) {
    const n = k(
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
      return new Ca(n, "XYZ");
  }
  readPolygon(t, e) {
    const n = k(
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
        qt(s, n[o]), r.push(s.length);
      return new Zn(s, "XYZ", r);
    } else
      return;
  }
  readFlatCoordinatesFromNode(t, e) {
    return k(
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
    return K(
      this.srsName ? this.srsName : t.firstElementChild.getAttribute("srsName")
    );
  }
}
St.prototype.namespace = ri;
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
    pointMember: W(St.prototype.pointMemberParser),
    pointMembers: W(St.prototype.pointMemberParser)
  }
};
St.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: W(
      St.prototype.lineStringMemberParser
    ),
    lineStringMembers: W(
      St.prototype.lineStringMemberParser
    )
  }
};
St.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml": {
    polygonMember: W(St.prototype.polygonMemberParser),
    polygonMembers: W(St.prototype.polygonMemberParser)
  }
};
St.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: W(St.prototype.readFlatCoordinatesFromNode)
  }
};
St.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: W(St.prototype.readLineString)
  }
};
St.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: W(St.prototype.readPolygon)
  }
};
St.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: G(St.prototype.readFlatLinearRing)
  }
};
const q = St;
function Np(i) {
  const t = $i(i, !1);
  return zp(t);
}
function zp(i) {
  const t = /^\s*([+\-]?\d*\.?\d+(?:e[+\-]?\d+)?)\s*$/i.exec(i);
  if (t)
    return parseFloat(t[1]);
}
function ne(i) {
  const t = $i(i, !1);
  return Sn(t);
}
function Sn(i) {
  const t = /^\s*(\d+)\s*$/.exec(i);
  if (t)
    return parseInt(t[1], 10);
}
function nt(i) {
  return $i(i, !1).trim();
}
function Tt(i, t) {
  i.appendChild(Qd().createTextNode(t));
}
const Fp = ri + " http://schemas.opengis.net/gml/2.1.2/feature.xsd", Dp = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class it extends q {
  constructor(t) {
    t = t || {}, super(t), this.FEATURE_COLLECTION_PARSERS[ri].featureMember = W(
      this.readFeaturesInternal
    ), this.schemaLocation = t.schemaLocation ? t.schemaLocation : Fp;
  }
  readFlatCoordinates(t, e) {
    const n = $i(t, !1).replace(/^\s*|\s*$/g, ""), r = e[0].srsName;
    let o = "enu";
    if (r) {
      const h = K(r);
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
    const n = k(
      [null],
      this.BOX_PARSERS_,
      t,
      e,
      this
    );
    return Me(
      n[1][0],
      n[1][1],
      n[1][3],
      n[1][4]
    );
  }
  innerBoundaryIsParser(t, e) {
    const n = k(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    n && e[e.length - 1].push(n);
  }
  outerBoundaryIsParser(t, e) {
    const n = k(
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
    return Array.isArray(t) ? n = "Envelope" : (n = t.getType(), n === "MultiPolygon" && r === !0 ? n = "MultiSurface" : n === "Polygon" && o === !0 ? n = "Surface" : n === "MultiLineString" && a === !0 && (n = "MultiCurve")), J("http://www.opengis.net/gml", n);
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
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = w(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = w(Tt)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, bt(
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
      const o = J(t.namespaceURI, "segments");
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
    bt(
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
    ) : o = qs(
      e,
      !0,
      s
    ), bt(
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
    const e = J(t, "coordinates");
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
    const s = J(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, n);
  }
  writeSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      bt(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        n,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = J(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, n);
    }
  }
  RING_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), J(
      r.namespaceURI,
      o !== void 0 ? "innerBoundaryIs" : "outerBoundaryIs"
    );
  }
  writeSurfacePatches_(t, e, n) {
    const s = J(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n);
  }
  writeRing(t, e, n) {
    const s = J(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, n);
  }
  getCoords_(t, e, n) {
    let s = "enu";
    e && (s = K(e).getAxisOrientation());
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
    bt(
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
    const s = J(t.namespaceURI, "Point");
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
    bt(
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
    bt(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      Kd,
      a,
      n,
      o,
      this
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1].node;
    return J(
      "http://www.opengis.net/gml",
      Dp[s.nodeName]
    );
  }
}
it.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    coordinates: G(it.prototype.readFlatCoordinates)
  }
};
it.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {
    innerBoundaryIs: it.prototype.innerBoundaryIsParser,
    outerBoundaryIs: it.prototype.outerBoundaryIsParser
  }
};
it.prototype.BOX_PARSERS_ = {
  "http://www.opengis.net/gml": {
    coordinates: W(it.prototype.readFlatCoordinates)
  }
};
it.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: G(q.prototype.readPoint),
    MultiPoint: G(q.prototype.readMultiPoint),
    LineString: G(q.prototype.readLineString),
    MultiLineString: G(q.prototype.readMultiLineString),
    LinearRing: G(q.prototype.readLinearRing),
    Polygon: G(q.prototype.readPolygon),
    MultiPolygon: G(q.prototype.readMultiPolygon),
    Box: G(it.prototype.readBox)
  }
};
it.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: w(it.prototype.writeCurveOrLineString),
    MultiCurve: w(it.prototype.writeMultiCurveOrLineString),
    Point: w(it.prototype.writePoint),
    MultiPoint: w(it.prototype.writeMultiPoint),
    LineString: w(it.prototype.writeCurveOrLineString),
    MultiLineString: w(
      it.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: w(it.prototype.writeLinearRing),
    Polygon: w(it.prototype.writeSurfaceOrPolygon),
    MultiPolygon: w(
      it.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: w(it.prototype.writeSurfaceOrPolygon),
    MultiSurface: w(
      it.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: w(it.prototype.writeEnvelope)
  }
};
it.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: w(
      it.prototype.writeLineStringOrCurveMember
    ),
    curveMember: w(
      it.prototype.writeLineStringOrCurveMember
    )
  }
};
it.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    outerBoundaryIs: w(it.prototype.writeRing),
    innerBoundaryIs: w(it.prototype.writeRing)
  }
};
it.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: w(it.prototype.writePointMember)
  }
};
it.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: w(
      it.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: w(
      it.prototype.writeSurfaceOrPolygonMember
    )
  }
};
it.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: w(Tt),
    upperCorner: w(Tt)
  }
};
const Ks = it, jp = ri + " http://schemas.opengis.net/gml/3.1.1/profiles/gmlsfProfile/1.0.0/gmlsf.xsd", kp = {
  MultiLineString: "lineStringMember",
  MultiCurve: "curveMember",
  MultiPolygon: "polygonMember",
  MultiSurface: "surfaceMember"
};
class z extends q {
  constructor(t) {
    t = t || {}, super(t), this.surface_ = t.surface !== void 0 ? t.surface : !1, this.curve_ = t.curve !== void 0 ? t.curve : !1, this.multiCurve_ = t.multiCurve !== void 0 ? t.multiCurve : !0, this.multiSurface_ = t.multiSurface !== void 0 ? t.multiSurface : !0, this.schemaLocation = t.schemaLocation ? t.schemaLocation : jp, this.hasZ = t.hasZ !== void 0 ? t.hasZ : !1;
  }
  readMultiCurve(t, e) {
    const n = k(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Ll(n);
  }
  readFlatCurveRing(t, e) {
    const n = k(
      [],
      this.MULTICURVE_PARSERS,
      t,
      e,
      this
    ), s = [];
    for (let r = 0, o = n.length; r < o; ++r)
      qt(s, n[r].getFlatCoordinates());
    return s;
  }
  readMultiSurface(t, e) {
    const n = k(
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
    Ui(this.CURVEMEMBER_PARSERS, t, e, this);
  }
  surfaceMemberParser(t, e) {
    Ui(this.SURFACEMEMBER_PARSERS, t, e, this);
  }
  readPatch(t, e) {
    return k(
      [null],
      this.PATCHES_PARSERS,
      t,
      e,
      this
    );
  }
  readSegment(t, e) {
    return k([], this.SEGMENTS_PARSERS, t, e, this);
  }
  readPolygonPatch(t, e) {
    return k(
      [null],
      this.FLAT_LINEAR_RINGS_PARSERS,
      t,
      e,
      this
    );
  }
  readLineStringSegment(t, e) {
    return k(
      [null],
      this.GEOMETRY_FLAT_COORDINATES_PARSERS,
      t,
      e,
      this
    );
  }
  interiorParser(t, e) {
    const n = k(
      void 0,
      this.RING_PARSERS,
      t,
      e,
      this
    );
    n && e[e.length - 1].push(n);
  }
  exteriorParser(t, e) {
    const n = k(
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
    const n = k(
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
        qt(s, n[o]), r.push(s.length);
      return new Zn(s, "XYZ", r);
    } else
      return;
  }
  readCurve(t, e) {
    const n = k(
      [null],
      this.CURVE_PARSERS,
      t,
      e,
      this
    );
    if (n)
      return new Fs(n, "XYZ");
  }
  readEnvelope(t, e) {
    const n = k(
      [null],
      this.ENVELOPE_PARSERS,
      t,
      e,
      this
    );
    return Me(
      n[1][0],
      n[1][1],
      n[2][0],
      n[2][1]
    );
  }
  readFlatPos(t, e) {
    let n = $i(t, !1);
    const s = /^\s*([+\-]?\d*\.?\d+(?:[eE][+\-]?\d+)?)\s*/, r = [];
    let o;
    for (; o = s.exec(n); )
      r.push(parseFloat(o[1])), n = n.substr(o[0].length);
    if (n !== "")
      return;
    const l = e[0].srsName;
    let h = "enu";
    if (l && (h = K(l).getAxisOrientation()), h === "neu") {
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
    const n = $i(t, !1).replace(/^\s*|\s*$/g, ""), s = e[0], r = s.srsName, o = s.srsDimension;
    let a = "enu";
    r && (a = K(r).getAxisOrientation());
    const l = n.split(/\s+/);
    let h = 2;
    t.getAttribute("srsDimension") ? h = Sn(t.getAttribute("srsDimension")) : t.getAttribute("dimension") ? h = Sn(t.getAttribute("dimension")) : t.parentNode.getAttribute("srsDimension") ? h = Sn(
      t.parentNode.getAttribute("srsDimension")
    ) : o && (h = Sn(o));
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
    a && (l = K(a).getAxisOrientation());
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
    e && (s = K(e).getAxisOrientation());
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
    const o = J(t.namespaceURI, "pos");
    t.appendChild(o), this.writePos_(o, e, n);
  }
  writeEnvelope(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = ["lowerCorner", "upperCorner"], a = [e[0] + " " + e[1], e[2] + " " + e[3]];
    bt(
      { node: t },
      this.ENVELOPE_SERIALIZERS,
      Kd,
      a,
      n,
      o,
      this
    );
  }
  writeLinearRing(t, e, n) {
    const r = n[n.length - 1].srsName;
    r && t.setAttribute("srsName", r);
    const o = J(t.namespaceURI, "posList");
    t.appendChild(o), this.writePosList_(o, e, n);
  }
  RING_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.node, o = s.exteriorWritten;
    return o === void 0 && (s.exteriorWritten = !0), J(
      r.namespaceURI,
      o !== void 0 ? "interior" : "exterior"
    );
  }
  writeSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName;
    if (t.nodeName !== "PolygonPatch" && o && t.setAttribute("srsName", o), t.nodeName === "Polygon" || t.nodeName === "PolygonPatch") {
      const a = e.getLinearRings();
      bt(
        { node: t, hasZ: r, srsName: o },
        this.RING_SERIALIZERS,
        this.RING_NODE_FACTORY_,
        a,
        n,
        void 0,
        this
      );
    } else if (t.nodeName === "Surface") {
      const a = J(t.namespaceURI, "patches");
      t.appendChild(a), this.writeSurfacePatches_(a, e, n);
    }
  }
  writeCurveOrLineString(t, e, n) {
    const r = n[n.length - 1].srsName;
    if (t.nodeName !== "LineStringSegment" && r && t.setAttribute("srsName", r), t.nodeName === "LineString" || t.nodeName === "LineStringSegment") {
      const o = J(t.namespaceURI, "posList");
      t.appendChild(o), this.writePosList_(o, e, n);
    } else if (t.nodeName === "Curve") {
      const o = J(t.namespaceURI, "segments");
      t.appendChild(o), this.writeCurveSegments_(o, e, n);
    }
  }
  writeMultiSurfaceOrPolygon(t, e, n) {
    const s = n[n.length - 1], r = s.hasZ, o = s.srsName, a = s.surface;
    o && t.setAttribute("srsName", o);
    const l = e.getPolygons();
    bt(
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
    bt(
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
    bt(
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
    const s = J(t.namespaceURI, "LinearRing");
    t.appendChild(s), this.writeLinearRing(s, e, n);
  }
  writeSurfaceOrPolygonMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n));
  }
  writePointMember(t, e, n) {
    const s = J(t.namespaceURI, "Point");
    t.appendChild(s), this.writePoint(s, e, n);
  }
  writeLineStringOrCurveMember(t, e, n) {
    const s = this.GEOMETRY_NODE_FACTORY_(e, n);
    s && (t.appendChild(s), this.writeCurveOrLineString(s, e, n));
  }
  writeSurfacePatches_(t, e, n) {
    const s = J(t.namespaceURI, "PolygonPatch");
    t.appendChild(s), this.writeSurfaceOrPolygon(s, e, n);
  }
  writeCurveSegments_(t, e, n) {
    const s = J(t.namespaceURI, "LineStringSegment");
    t.appendChild(s), this.writeCurveOrLineString(s, e, n);
  }
  writeGeometryElement(t, e, n) {
    const s = n[n.length - 1], r = Object.assign({}, s);
    r.node = t;
    let o;
    Array.isArray(e) ? o = Tl(
      e,
      s
    ) : o = qs(
      e,
      !0,
      s
    ), bt(
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
        f !== null && (l.push(d), h.push(f), d == a || typeof f.getSimplifiedGeometry == "function" ? d in r.serializers[o] || (r.serializers[o][d] = w(
          this.writeGeometryElement,
          this
        )) : d in r.serializers[o] || (r.serializers[o][d] = w(Tt)));
      }
    }
    const c = Object.assign({}, r);
    c.node = t, bt(
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
    a[o] = {}, a[o][r] = w(
      this.writeFeatureElement,
      this
    );
    const l = Object.assign({}, s);
    l.node = t, bt(
      l,
      a,
      de(r, o),
      e,
      n
    );
  }
  MULTIGEOMETRY_MEMBER_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1].node;
    return J(
      this.namespace,
      kp[s.nodeName]
    );
  }
  GEOMETRY_NODE_FACTORY_(t, e, n) {
    const s = e[e.length - 1], r = s.multiSurface, o = s.surface, a = s.curve, l = s.multiCurve;
    return Array.isArray(t) ? n = "Envelope" : (n = t.getType(), n === "MultiPolygon" && r === !0 ? n = "MultiSurface" : n === "Polygon" && o === !0 ? n = "Surface" : n === "LineString" && a === !0 ? n = "Curve" : n === "MultiLineString" && l === !0 && (n = "MultiCurve")), J(this.namespace, n);
  }
  writeGeometryNode(t, e) {
    e = this.adaptOptions(e);
    const n = J(this.namespace, "geom"), s = {
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
    const n = J(this.namespace, "featureMembers");
    n.setAttributeNS(
      Ia,
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
z.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml": {
    pos: G(z.prototype.readFlatPos),
    posList: G(z.prototype.readFlatPosList),
    coordinates: G(Ks.prototype.readFlatCoordinates)
  }
};
z.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml": {
    interior: z.prototype.interiorParser,
    exterior: z.prototype.exteriorParser
  }
};
z.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml": {
    Point: G(q.prototype.readPoint),
    MultiPoint: G(q.prototype.readMultiPoint),
    LineString: G(q.prototype.readLineString),
    MultiLineString: G(q.prototype.readMultiLineString),
    LinearRing: G(q.prototype.readLinearRing),
    Polygon: G(q.prototype.readPolygon),
    MultiPolygon: G(q.prototype.readMultiPolygon),
    Surface: G(z.prototype.readSurface),
    MultiSurface: G(z.prototype.readMultiSurface),
    Curve: G(z.prototype.readCurve),
    MultiCurve: G(z.prototype.readMultiCurve),
    Envelope: G(z.prototype.readEnvelope)
  }
};
z.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml": {
    curveMember: W(z.prototype.curveMemberParser),
    curveMembers: W(z.prototype.curveMemberParser)
  }
};
z.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: W(z.prototype.surfaceMemberParser),
    surfaceMembers: W(z.prototype.surfaceMemberParser)
  }
};
z.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    LineString: W(q.prototype.readLineString),
    Curve: W(z.prototype.readCurve)
  }
};
z.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml": {
    Polygon: W(q.prototype.readPolygon),
    Surface: W(z.prototype.readSurface)
  }
};
z.prototype.SURFACE_PARSERS = {
  "http://www.opengis.net/gml": {
    patches: G(z.prototype.readPatch)
  }
};
z.prototype.CURVE_PARSERS = {
  "http://www.opengis.net/gml": {
    segments: G(z.prototype.readSegment)
  }
};
z.prototype.ENVELOPE_PARSERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: W(z.prototype.readFlatPosList),
    upperCorner: W(z.prototype.readFlatPosList)
  }
};
z.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml": {
    PolygonPatch: G(z.prototype.readPolygonPatch)
  }
};
z.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml": {
    LineStringSegment: qd(
      z.prototype.readLineStringSegment
    )
  }
};
q.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml": {
    LinearRing: G(q.prototype.readFlatLinearRing),
    Ring: G(z.prototype.readFlatCurveRing)
  }
};
z.prototype.writeFeatures;
z.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    exterior: w(z.prototype.writeRing),
    interior: w(z.prototype.writeRing)
  }
};
z.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lowerCorner: w(Tt),
    upperCorner: w(Tt)
  }
};
z.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    surfaceMember: w(
      z.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: w(
      z.prototype.writeSurfaceOrPolygonMember
    )
  }
};
z.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    pointMember: w(z.prototype.writePointMember)
  }
};
z.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    lineStringMember: w(
      z.prototype.writeLineStringOrCurveMember
    ),
    curveMember: w(
      z.prototype.writeLineStringOrCurveMember
    )
  }
};
z.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml": {
    Curve: w(z.prototype.writeCurveOrLineString),
    MultiCurve: w(z.prototype.writeMultiCurveOrLineString),
    Point: w(z.prototype.writePoint),
    MultiPoint: w(z.prototype.writeMultiPoint),
    LineString: w(z.prototype.writeCurveOrLineString),
    MultiLineString: w(
      z.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: w(z.prototype.writeLinearRing),
    Polygon: w(z.prototype.writeSurfaceOrPolygon),
    MultiPolygon: w(
      z.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: w(z.prototype.writeSurfaceOrPolygon),
    MultiSurface: w(
      z.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: w(z.prototype.writeEnvelope)
  }
};
const Q = z;
class ot extends Q {
  constructor(t) {
    t = t || {}, super(t), this.schemaLocation = t.schemaLocation ? t.schemaLocation : this.namespace + " http://schemas.opengis.net/gml/3.2.1/gml.xsd";
  }
}
ot.prototype.namespace = "http://www.opengis.net/gml/3.2";
ot.prototype.GEOMETRY_FLAT_COORDINATES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pos: G(Q.prototype.readFlatPos),
    posList: G(Q.prototype.readFlatPosList),
    coordinates: G(Ks.prototype.readFlatCoordinates)
  }
};
ot.prototype.FLAT_LINEAR_RINGS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    interior: Q.prototype.interiorParser,
    exterior: Q.prototype.exteriorParser
  }
};
ot.prototype.GEOMETRY_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: G(q.prototype.readPoint),
    MultiPoint: G(q.prototype.readMultiPoint),
    LineString: G(q.prototype.readLineString),
    MultiLineString: G(q.prototype.readMultiLineString),
    LinearRing: G(q.prototype.readLinearRing),
    Polygon: G(q.prototype.readPolygon),
    MultiPolygon: G(q.prototype.readMultiPolygon),
    Surface: G(ot.prototype.readSurface),
    MultiSurface: G(Q.prototype.readMultiSurface),
    Curve: G(ot.prototype.readCurve),
    MultiCurve: G(Q.prototype.readMultiCurve),
    Envelope: G(ot.prototype.readEnvelope)
  }
};
ot.prototype.MULTICURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    curveMember: W(Q.prototype.curveMemberParser),
    curveMembers: W(Q.prototype.curveMemberParser)
  }
};
ot.prototype.MULTISURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: W(Q.prototype.surfaceMemberParser),
    surfaceMembers: W(Q.prototype.surfaceMemberParser)
  }
};
ot.prototype.CURVEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: W(q.prototype.readLineString),
    Curve: W(Q.prototype.readCurve)
  }
};
ot.prototype.SURFACEMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: W(q.prototype.readPolygon),
    Surface: W(Q.prototype.readSurface)
  }
};
ot.prototype.SURFACE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    patches: G(Q.prototype.readPatch)
  }
};
ot.prototype.CURVE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    segments: G(Q.prototype.readSegment)
  }
};
ot.prototype.ENVELOPE_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: W(Q.prototype.readFlatPosList),
    upperCorner: W(Q.prototype.readFlatPosList)
  }
};
ot.prototype.PATCHES_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    PolygonPatch: G(Q.prototype.readPolygonPatch)
  }
};
ot.prototype.SEGMENTS_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineStringSegment: qd(
      Q.prototype.readLineStringSegment
    )
  }
};
ot.prototype.MULTIPOINT_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: W(q.prototype.pointMemberParser),
    pointMembers: W(q.prototype.pointMemberParser)
  }
};
ot.prototype.MULTILINESTRING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: W(
      q.prototype.lineStringMemberParser
    ),
    lineStringMembers: W(
      q.prototype.lineStringMemberParser
    )
  }
};
ot.prototype.MULTIPOLYGON_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    polygonMember: W(q.prototype.polygonMemberParser),
    polygonMembers: W(q.prototype.polygonMemberParser)
  }
};
ot.prototype.POINTMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Point: W(q.prototype.readFlatCoordinatesFromNode)
  }
};
ot.prototype.LINESTRINGMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LineString: W(q.prototype.readLineString)
  }
};
ot.prototype.POLYGONMEMBER_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    Polygon: W(q.prototype.readPolygon)
  }
};
ot.prototype.RING_PARSERS = {
  "http://www.opengis.net/gml/3.2": {
    LinearRing: G(q.prototype.readFlatLinearRing),
    Ring: G(ot.prototype.readFlatCurveRing)
  }
};
ot.prototype.RING_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    exterior: w(Q.prototype.writeRing),
    interior: w(Q.prototype.writeRing)
  }
};
ot.prototype.ENVELOPE_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lowerCorner: w(Tt),
    upperCorner: w(Tt)
  }
};
ot.prototype.SURFACEORPOLYGONMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    surfaceMember: w(
      Q.prototype.writeSurfaceOrPolygonMember
    ),
    polygonMember: w(
      Q.prototype.writeSurfaceOrPolygonMember
    )
  }
};
ot.prototype.POINTMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    pointMember: w(Q.prototype.writePointMember)
  }
};
ot.prototype.LINESTRINGORCURVEMEMBER_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    lineStringMember: w(
      Q.prototype.writeLineStringOrCurveMember
    ),
    curveMember: w(
      Q.prototype.writeLineStringOrCurveMember
    )
  }
};
ot.prototype.GEOMETRY_SERIALIZERS = {
  "http://www.opengis.net/gml/3.2": {
    Curve: w(Q.prototype.writeCurveOrLineString),
    MultiCurve: w(Q.prototype.writeMultiCurveOrLineString),
    Point: w(ot.prototype.writePoint),
    MultiPoint: w(Q.prototype.writeMultiPoint),
    LineString: w(Q.prototype.writeCurveOrLineString),
    MultiLineString: w(
      Q.prototype.writeMultiCurveOrLineString
    ),
    LinearRing: w(Q.prototype.writeLinearRing),
    Polygon: w(Q.prototype.writeSurfaceOrPolygon),
    MultiPolygon: w(
      Q.prototype.writeMultiSurfaceOrPolygon
    ),
    Surface: w(Q.prototype.writeSurfaceOrPolygon),
    MultiSurface: w(
      Q.prototype.writeMultiSurfaceOrPolygon
    ),
    Envelope: w(Q.prototype.writeEnvelope)
  }
};
const Dl = ot;
class Xp {
  constructor(t) {
    this.tagName_ = t;
  }
  getTagName() {
    return this.tagName_;
  }
}
const tf = Xp;
class Gp extends tf {
  constructor(t, e) {
    super(t), this.conditions = e, Y(this.conditions.length >= 2, 57);
  }
}
const Hp = Gp;
class Zp extends Hp {
  constructor(t) {
    super("And", Array.prototype.slice.call(arguments));
  }
}
const Bp = Zp;
class Wp extends tf {
  constructor(t, e, n) {
    if (super("BBOX"), this.geometryName = t, this.extent = e, e.length !== 4)
      throw new Error(
        "Expected an extent with four values ([minX, minY, maxX, maxY])"
      );
    this.srsName = n;
  }
}
const Vp = Wp;
function Yp(i) {
  const t = [null].concat(Array.prototype.slice.call(arguments));
  return new (Function.prototype.bind.apply(Bp, t))();
}
function Up(i, t, e) {
  return new Vp(i, t, e);
}
const gc = {
  "http://www.opengis.net/gml": {
    boundedBy: I(
      q.prototype.readExtentElement,
      "bounds"
    )
  },
  "http://www.opengis.net/wfs/2.0": {
    member: W(q.prototype.readFeaturesInternal)
  }
}, Jp = {
  "http://www.opengis.net/wfs": {
    totalInserted: I(ne),
    totalUpdated: I(ne),
    totalDeleted: I(ne)
  },
  "http://www.opengis.net/wfs/2.0": {
    totalInserted: I(ne),
    totalUpdated: I(ne),
    totalDeleted: I(ne)
  }
}, qp = {
  "http://www.opengis.net/wfs": {
    TransactionSummary: I(
      pc,
      "transactionSummary"
    ),
    InsertResults: I(yc, "insertIds")
  },
  "http://www.opengis.net/wfs/2.0": {
    TransactionSummary: I(
      pc,
      "transactionSummary"
    ),
    InsertResults: I(yc, "insertIds")
  }
}, Kp = {
  "http://www.opengis.net/wfs": {
    PropertyName: w(Tt)
  },
  "http://www.opengis.net/wfs/2.0": {
    PropertyName: w(Tt)
  }
}, ef = {
  "http://www.opengis.net/wfs": {
    Insert: w(xc),
    Update: w(Cc),
    Delete: w(Mc),
    Property: w(wc),
    Native: w(Ec)
  },
  "http://www.opengis.net/wfs/2.0": {
    Insert: w(xc),
    Update: w(Cc),
    Delete: w(Mc),
    Property: w(wc),
    Native: w(Ec)
  }
}, nf = "feature", jl = "http://www.w3.org/2000/xmlns/", kl = {
  "2.0.0": "http://www.opengis.net/ogc/1.1",
  "1.1.0": "http://www.opengis.net/ogc",
  "1.0.0": "http://www.opengis.net/ogc"
}, Na = {
  "2.0.0": "http://www.opengis.net/wfs/2.0",
  "1.1.0": "http://www.opengis.net/wfs",
  "1.0.0": "http://www.opengis.net/wfs"
}, Xl = {
  "2.0.0": "http://www.opengis.net/fes/2.0",
  "1.1.0": "http://www.opengis.net/fes",
  "1.0.0": "http://www.opengis.net/fes"
}, mc = {
  "2.0.0": "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd",
  "1.1.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd",
  "1.0.0": "http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/wfs.xsd"
}, Gl = {
  "2.0.0": Dl,
  "1.1.0": Q,
  "1.0.0": Ks
}, Qp = "1.1.0";
class $p extends $d {
  constructor(t) {
    super(), t = t || {}, this.version_ = t.version ? t.version : Qp, this.featureType_ = t.featureType, this.featureNS_ = t.featureNS, this.gmlFormat_ = t.gmlFormat ? t.gmlFormat : new Gl[this.version_](), this.schemaLocation_ = t.schemaLocation ? t.schemaLocation : mc[this.version_];
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
    this.version_ === "2.0.0" ? r = gc : r = this.gmlFormat_.FEATURE_COLLECTION_PARSERS;
    let o = k(
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
        const e = Bi(t);
        return this.readTransactionResponseFromDocument(e);
      } else
        return Zi(t) ? this.readTransactionResponseFromDocument(
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
        const e = Bi(t);
        return this.readFeatureCollectionMetadataFromDocument(e);
      } else
        return Zi(t) ? this.readFeatureCollectionMetadataFromDocument(
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
    const e = {}, n = Sn(
      t.getAttribute("numberOfFeatures")
    );
    return e.numberOfFeatures = n, k(
      e,
      gc,
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
    return k(
      {},
      qp,
      t,
      []
    );
  }
  writeGetFeature(t) {
    const e = J(Na[this.version_], "GetFeature");
    e.setAttribute("service", "WFS"), e.setAttribute("version", this.version_), t.handle && e.setAttribute("handle", t.handle), t.outputFormat && e.setAttribute("outputFormat", t.outputFormat), t.maxFeatures !== void 0 && e.setAttribute("maxFeatures", String(t.maxFeatures)), t.resultType && e.setAttribute("resultType", t.resultType), t.startIndex !== void 0 && e.setAttribute("startIndex", String(t.startIndex)), t.count !== void 0 && e.setAttribute("count", String(t.count)), t.viewParams !== void 0 && e.setAttribute("viewParams", t.viewParams), e.setAttributeNS(
      Ia,
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
      }), Ic(
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
        }), Ic(e, [s.name], [n]);
      });
    return e;
  }
  combineBboxAndFilter(t, e, n, s) {
    const r = Up(t, e, n);
    return s ? Yp(s, r) : r;
  }
  writeTransaction(t, e, n, s) {
    const r = [], o = s.version ? s.version : this.version_, a = J(Na[o], "Transaction");
    a.setAttribute("service", "WFS"), a.setAttribute("version", o);
    let l;
    s && (l = s.gmlOptions ? s.gmlOptions : {}, s.handle && a.setAttribute("handle", s.handle)), a.setAttributeNS(
      Ia,
      "xsi:schemaLocation",
      mc[o]
    );
    const h = tv(a, l, o, s);
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
          return this.gmlFormat_.readGeometryElement(e, n), K(n.pop().srsName);
        }
    }
    return null;
  }
}
function tv(i, t, e, n) {
  const s = n.featurePrefix ? n.featurePrefix : nf;
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
  bt(
    n,
    ef,
    de(i),
    t,
    e
  );
}
function pc(i, t) {
  return k({}, Jp, i, t);
}
const ev = {
  "http://www.opengis.net/ogc": {
    FeatureId: W(function(i, t) {
      return i.getAttribute("fid");
    })
  },
  "http://www.opengis.net/ogc/1.1": {
    FeatureId: W(function(i, t) {
      return i.getAttribute("fid");
    })
  }
};
function vc(i, t) {
  Ui(ev, i, t);
}
const iv = {
  "http://www.opengis.net/wfs": {
    Feature: vc
  },
  "http://www.opengis.net/wfs/2.0": {
    Feature: vc
  }
};
function yc(i, t) {
  return k([], iv, i, t);
}
function xc(i, t, e) {
  const n = e[e.length - 1], s = n.featureType, r = n.featureNS, o = n.gmlVersion, a = J(r, s);
  i.appendChild(a), o === 2 ? Ks.prototype.writeFeatureElement(a, t, e) : o === 3 ? Q.prototype.writeFeatureElement(a, t, e) : Dl.prototype.writeFeatureElement(a, t, e);
}
function sf(i, t, e) {
  const s = e[e.length - 1].version, r = kl[s], o = J(r, "Filter"), a = J(r, "FeatureId");
  o.appendChild(a), a.setAttribute("fid", t), i.appendChild(o);
}
function Hl(i, t) {
  i = i || nf;
  const e = i + ":";
  return t.startsWith(e) ? t : e + t;
}
function Mc(i, t, e) {
  const n = e[e.length - 1];
  Y(t.getId() !== void 0, 26);
  const s = n.featureType, r = n.featurePrefix, o = n.featureNS, a = Hl(r, s);
  i.setAttribute("typeName", a), i.setAttributeNS(jl, "xmlns:" + r, o);
  const l = t.getId();
  l !== void 0 && sf(i, l, e);
}
function Cc(i, t, e) {
  const n = e[e.length - 1];
  Y(t.getId() !== void 0, 27);
  const s = n.version, r = n.featureType, o = n.featurePrefix, a = n.featureNS, l = Hl(o, r), h = t.getGeometryName();
  i.setAttribute("typeName", l), i.setAttributeNS(jl, "xmlns:" + o, a);
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
    bt(
      {
        version: s,
        gmlVersion: n.gmlVersion,
        node: i,
        hasZ: n.hasZ,
        srsName: n.srsName
      },
      ef,
      de("Property"),
      d,
      e
    ), sf(i, c, e);
  }
}
function wc(i, t, e) {
  const n = e[e.length - 1], s = n.version, r = Na[s], o = J(r, "Name"), a = n.gmlVersion;
  if (i.appendChild(o), Tt(o, t.name), t.value !== void 0 && t.value !== null) {
    const l = J(r, "Value");
    i.appendChild(l), t.value && typeof t.value.getSimplifiedGeometry == "function" ? a === 2 ? Ks.prototype.writeGeometryElement(l, t.value, e) : a === 3 ? Q.prototype.writeGeometryElement(l, t.value, e) : Dl.prototype.writeGeometryElement(l, t.value, e) : Tt(l, t.value);
  }
}
function Ec(i, t, e) {
  t.vendorId && i.setAttribute("vendorId", t.vendorId), t.safeToIgnore !== void 0 && i.setAttribute("safeToIgnore", String(t.safeToIgnore)), t.value !== void 0 && Tt(i, t.value);
}
const _o = {
  "http://www.opengis.net/wfs": {
    Query: w(bc)
  },
  "http://www.opengis.net/wfs/2.0": {
    Query: w(bc)
  },
  "http://www.opengis.net/ogc": {
    During: w(_c),
    And: w(_r),
    Or: w(_r),
    Not: w(Rc),
    BBOX: w(Pc),
    Contains: w(yi),
    Intersects: w(yi),
    Within: w(yi),
    DWithin: w(Sc),
    PropertyIsEqualTo: w(ye),
    PropertyIsNotEqualTo: w(ye),
    PropertyIsLessThan: w(ye),
    PropertyIsLessThanOrEqualTo: w(ye),
    PropertyIsGreaterThan: w(ye),
    PropertyIsGreaterThanOrEqualTo: w(ye),
    PropertyIsNull: w(Tc),
    PropertyIsBetween: w(Lc),
    PropertyIsLike: w(Oc)
  },
  "http://www.opengis.net/fes/2.0": {
    During: w(_c),
    And: w(_r),
    Or: w(_r),
    Not: w(Rc),
    BBOX: w(Pc),
    Contains: w(yi),
    Disjoint: w(yi),
    Intersects: w(yi),
    ResourceId: w(sv),
    Within: w(yi),
    DWithin: w(Sc),
    PropertyIsEqualTo: w(ye),
    PropertyIsNotEqualTo: w(ye),
    PropertyIsLessThan: w(ye),
    PropertyIsLessThanOrEqualTo: w(ye),
    PropertyIsGreaterThan: w(ye),
    PropertyIsGreaterThanOrEqualTo: w(ye),
    PropertyIsNull: w(Tc),
    PropertyIsBetween: w(Lc),
    PropertyIsLike: w(Oc)
  }
};
function bc(i, t, e) {
  const n = e[e.length - 1], s = n.version, r = n.featurePrefix, o = n.featureNS, a = n.propertyNames, l = n.srsName;
  let h;
  r ? h = Hl(r, t) : h = t;
  let c;
  s === "2.0.0" ? c = "typeNames" : c = "typeName", i.setAttribute(c, h), l && i.setAttribute("srsName", l), o && i.setAttributeNS(jl, "xmlns:" + r, o);
  const u = Object.assign({}, n);
  u.node = i, bt(
    u,
    Kp,
    de("PropertyName"),
    a,
    e
  );
  const d = n.filter;
  if (d) {
    const f = J(Ro(s), "Filter");
    i.appendChild(f), nv(f, d, e);
  }
}
function nv(i, t, e) {
  const n = e[e.length - 1], s = { node: i };
  Object.assign(s, { context: n }), bt(
    s,
    _o,
    de(t.getTagName()),
    [t],
    e
  );
}
function Pc(i, t, e) {
  const n = e[e.length - 1], r = n.context.version;
  n.srsName = t.srsName;
  const o = Gl[r];
  ts(r, i, t.geometryName), o.prototype.writeGeometryElement(i, t.extent, e);
}
function sv(i, t, e) {
  i.setAttribute("rid", t.rid);
}
function yi(i, t, e) {
  const n = e[e.length - 1], r = n.context.version;
  n.srsName = t.srsName;
  const o = Gl[r];
  ts(r, i, t.geometryName), o.prototype.writeGeometryElement(i, t.geometry, e);
}
function Sc(i, t, e) {
  const r = e[e.length - 1].context.version;
  yi(i, t, e);
  const o = J(Ro(r), "Distance");
  Tt(o, t.distance.toString()), r === "2.0.0" ? o.setAttribute("uom", t.unit) : o.setAttribute("units", t.unit), i.appendChild(o);
}
function _c(i, t, e) {
  const r = e[e.length - 1].context.version;
  $r(Xl[r], "ValueReference", i, t.propertyName);
  const o = J(ri, "TimePeriod");
  i.appendChild(o);
  const a = J(ri, "begin");
  o.appendChild(a), Ac(a, t.begin);
  const l = J(ri, "end");
  o.appendChild(l), Ac(l, t.end);
}
function _r(i, t, e) {
  const s = e[e.length - 1].context, r = { node: i };
  Object.assign(r, { context: s });
  const o = t.conditions;
  for (let a = 0, l = o.length; a < l; ++a) {
    const h = o[a];
    bt(
      r,
      _o,
      de(h.getTagName()),
      [h],
      e
    );
  }
}
function Rc(i, t, e) {
  const s = e[e.length - 1].context, r = { node: i };
  Object.assign(r, { context: s });
  const o = t.condition;
  bt(
    r,
    _o,
    de(o.getTagName()),
    [o],
    e
  );
}
function ye(i, t, e) {
  const r = e[e.length - 1].context.version;
  t.matchCase !== void 0 && i.setAttribute("matchCase", t.matchCase.toString()), ts(r, i, t.propertyName), to(r, i, "" + t.expression);
}
function Tc(i, t, e) {
  const r = e[e.length - 1].context.version;
  ts(r, i, t.propertyName);
}
function Lc(i, t, e) {
  const r = e[e.length - 1].context.version, o = Ro(r);
  ts(r, i, t.propertyName);
  const a = J(o, "LowerBoundary");
  i.appendChild(a), to(r, a, "" + t.lowerBoundary);
  const l = J(o, "UpperBoundary");
  i.appendChild(l), to(r, l, "" + t.upperBoundary);
}
function Oc(i, t, e) {
  const r = e[e.length - 1].context.version;
  i.setAttribute("wildCard", t.wildCard), i.setAttribute("singleChar", t.singleChar), i.setAttribute("escapeChar", t.escapeChar), t.matchCase !== void 0 && i.setAttribute("matchCase", t.matchCase.toString()), ts(r, i, t.propertyName), to(r, i, "" + t.pattern);
}
function $r(i, t, e, n) {
  const s = J(i, t);
  Tt(s, n), e.appendChild(s);
}
function to(i, t, e) {
  $r(Ro(i), "Literal", t, e);
}
function ts(i, t, e) {
  i === "2.0.0" ? $r(Xl[i], "ValueReference", t, e) : $r(kl[i], "PropertyName", t, e);
}
function Ac(i, t) {
  const e = J(ri, "TimeInstant");
  i.appendChild(e);
  const n = J(ri, "timePosition");
  e.appendChild(n), Tt(n, t);
}
function Ic(i, t, e) {
  const n = e[e.length - 1], s = Object.assign({}, n);
  s.node = i, bt(
    s,
    _o,
    de("Query"),
    t,
    e
  );
}
function Ro(i) {
  let t;
  return i === "2.0.0" ? t = Xl[i] : t = kl[i], t;
}
const rv = $p;
class rf {
  static getSource(t, e, n) {
    return new $n({
      format: new rv({
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
      strategy: n ? $2 : Ld
    });
  }
}
class Nc {
  constructor(t, e, n) {
    this.vectorLayer = new Bn(), this.store = n, this.states = e, this.renderUtils = t;
    const s = this.store.getMap(), r = this.store.getOptions();
    if (!r || !s)
      throw new Error("Missing map or options");
    this.options = r, this.map = s, this.control = new Fl(this.store), this.vectorLayer = new Bn(), this.vectorSource = rf.getSource(r.wfs.url, "", !1), this.vectorSource.on("featuresloadend", () => {
      this.renderUtils.setIsLoaded(!0);
    }), this.displayDataOnMap(s, this.vectorLayer, r, this.vectorSource), this.states.readonly || (s.on("click", (o) => {
      s.forEachFeatureAtPixel(o.pixel, (a) => {
        var l;
        a && ((l = a.getGeometry()) == null ? void 0 : l.getType()) === "Point" && (a.getProperties().features && a.getProperties().features.length === 1 ? (this.store.getSelectedFeature(a.getProperties().features[0].get("objectid")) === void 0 && this.store.addSelectedFeature(a.getProperties().features[0], a.getProperties().features[0].get("objectid"), "select"), tt.sendEvent("icon-clicked", a.getProperties().features[0].get("objectid"))) : this.control.hide());
      });
    }), window.addEventListener("recenter-selected-element", () => {
      var l;
      const o = this.store.getCurrentItemId(), a = (l = this.store.getSelectedFeature(o)) == null ? void 0 : l.get("geom").getCoordinates();
      s.getView().setCenter(a);
    })), r.mode.type === "mix" && window.addEventListener("remove-clicked", (o) => {
      var a;
      (a = this.vectorLayer.getSource()) == null || a.getFeatures().forEach((l) => {
        l.get("features").forEach((h) => {
          h.get("objectid") === o.detail && (this.removeItem(h), this.control.hide());
        });
      });
    });
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementSelectMode(this.vectorSource, t);
  }
  removeCurrentSelection() {
    var t;
    (t = this.vectorLayer.getSource()) == null || t.getFeatures().forEach((e) => {
      e.get("features").forEach((n) => {
        n.get("isClick") && this.setIconToDisplay(n, void 0);
      });
    });
  }
  setChangeResolution(t, e, n) {
    const s = t.getView().getZoom();
    s && s >= n.maxZoom ? e.setDistance(0) : e.setDistance(n.cluster.distance);
  }
  displayDataOnMap(t, e, n, s) {
    const r = new Vm({
      distance: n.cluster.distance,
      minDistance: n.cluster.minDistance,
      source: s
    }), o = new Rp();
    e.setSource(r), e.setStyle(function(a) {
      return o.clusterWithIcon(a);
    }), t.addLayer(e), this.control.disable(), this.states.readonly || (t.addControl(this.control), this.toogleDataSelection(e)), Wt.registerBorderConstaintMapEvent(
      "change:resolution",
      () => this.setChangeResolution(t, r, n),
      this.map,
      this.options
    );
  }
  setCurrentElement(t) {
    var e;
    (e = this.store.getSelectedFeature(this.store.getCurrentItemId())) == null || e.set("isSelected", void 0), this.store.setCurrentItemId(t.get("objectid"));
  }
  setIconToDisplay(t, e) {
    t.set("isClick", e), t.set("isSelected", e);
  }
  removeSelectedItem(t) {
    this.removeItem(t), this.control.hide(), tt.sendEvent("rule-validation", void 0), Ud.setCustomStyleWithouInfoBox(this.store);
  }
  removeItem(t) {
    this.setIconToDisplay(t, void 0), this.store.removeSelectedFeature(t.get("objectid"));
  }
  setInformationBox(t) {
    this.setIconToDisplay(t, !0), this.control.show(), tt.sendEvent("open-select-create-box", t.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select");
  }
  toogleDataSelection(t) {
    window.addEventListener("authorize-clicked", (e) => {
      var s, r;
      const n = this.store.getSelectedFeature(e.detail);
      if (n)
        if (n.get("isClick"))
          this.store.getMaxElement() === 1 || this.store.getCurrentItemId() === n.get("objectid") ? this.removeSelectedItem(n) : (this.setCurrentElement(n), n.set("isSelected", !0), tt.sendEvent("open-select-create-box", n.get("geom").getCoordinates()), this.control.show());
        else if (this.store.getMaxElement() === 1) {
          if (((s = this.store.getOptions()) == null ? void 0 : s.mode.type) === "mix") {
            const a = this.store.getSelectedFeatures();
            if (a && a.length >= 1 && this.store.getCurrentFeatureType(a[0].get("id")) === "create") {
              const h = a[0].get("id");
              tt.sendEvent("remove-created", h);
            }
          }
          (r = t.getSource()) == null || r.getFeatures().forEach((a) => {
            a.get("features").forEach((l) => {
              l.get("isClick") && (this.setIconToDisplay(l, void 0), this.store.removeSelectedFeature(l.get("objectid")));
            });
          }), this.store.setCurrentItemId(n.get("objectid")), tt.sendEvent("rule-validation", void 0), this.setInformationBox(n);
        } else
          this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement() ? (this.setCurrentElement(n), this.setInformationBox(n)) : this.removeItem(n);
      this.map.get("target").className = `${this.store.getTargetBoxSize()} ${gt.getTheme()}`;
    });
  }
}
class ov {
  read(t) {
    if (t)
      if (typeof t == "string") {
        const e = Bi(t);
        return this.readFromDocument(e);
      } else
        return Zi(t) ? this.readFromDocument(t) : this.readFromNode(t);
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
const of = ov, av = "http://www.w3.org/1999/xlink";
function Zl(i) {
  return i.getAttributeNS(av, "href");
}
const re = [null, "http://www.opengis.net/ows/1.1"], lv = ct(re, {
  ServiceIdentification: I(Iv),
  ServiceProvider: I(zv),
  OperationsMetadata: I(Ov)
});
class hv extends of {
  constructor() {
    super();
  }
  readFromNode(t) {
    const e = k({}, lv, t, []);
    return e || null;
  }
}
const cv = ct(re, {
  DeliveryPoint: I(nt),
  City: I(nt),
  AdministrativeArea: I(nt),
  PostalCode: I(nt),
  Country: I(nt),
  ElectronicMailAddress: I(nt)
}), uv = ct(re, {
  Value: ue(Fv)
}), dv = ct(re, {
  AllowedValues: I(bv)
}), fv = ct(re, {
  Phone: I(Av),
  Address: I(Ev)
}), gv = ct(re, {
  HTTP: I(Tv)
}), mv = ct(re, {
  Get: ue(Rv),
  Post: void 0
}), pv = ct(re, {
  DCP: I(_v)
}), vv = ct(re, {
  Operation: Lv
}), yv = ct(re, {
  Voice: I(nt),
  Facsimile: I(nt)
}), xv = ct(re, {
  Constraint: ue(Pv)
}), Mv = ct(re, {
  IndividualName: I(nt),
  PositionName: I(nt),
  ContactInfo: I(Sv)
}), Cv = ct(re, {
  Abstract: I(nt),
  AccessConstraints: I(nt),
  Fees: I(nt),
  Title: I(nt),
  ServiceTypeVersion: I(nt),
  ServiceType: I(nt)
}), wv = ct(re, {
  ProviderName: I(nt),
  ProviderSite: I(Zl),
  ServiceContact: I(Nv)
});
function Ev(i, t) {
  return k({}, cv, i, t);
}
function bv(i, t) {
  return k({}, uv, i, t);
}
function Pv(i, t) {
  const e = i.getAttribute("name");
  if (!!e)
    return k({ name: e }, dv, i, t);
}
function Sv(i, t) {
  return k({}, fv, i, t);
}
function _v(i, t) {
  return k({}, gv, i, t);
}
function Rv(i, t) {
  const e = Zl(i);
  if (!!e)
    return k(
      { href: e },
      xv,
      i,
      t
    );
}
function Tv(i, t) {
  return k({}, mv, i, t);
}
function Lv(i, t) {
  const e = i.getAttribute("name"), n = k({}, pv, i, t);
  if (!n)
    return;
  const s = t[t.length - 1];
  s[e] = n;
}
function Ov(i, t) {
  return k({}, vv, i, t);
}
function Av(i, t) {
  return k({}, yv, i, t);
}
function Iv(i, t) {
  return k({}, Cv, i, t);
}
function Nv(i, t) {
  return k({}, Mv, i, t);
}
function zv(i, t) {
  return k({}, wv, i, t);
}
function Fv(i, t) {
  return nt(i);
}
const Dv = hv, He = [null, "http://www.opengis.net/wmts/1.0"], es = [null, "http://www.opengis.net/ows/1.1"], jv = ct(He, {
  Contents: I(qv)
});
class kv extends of {
  constructor() {
    super(), this.owsParser_ = new Dv();
  }
  readFromNode(t) {
    let e = t.getAttribute("version");
    e && (e = e.trim());
    let n = this.owsParser_.readFromNode(t);
    return n ? (n.version = e, n = k(
      n,
      jv,
      t,
      []
    ), n || null) : null;
  }
}
const Xv = ct(He, {
  Layer: ue(Kv),
  TileMatrixSet: ue(Qv)
}), Gv = ct(
  He,
  {
    Style: ue($v),
    Format: ue(nt),
    TileMatrixSetLink: ue(t3),
    Dimension: ue(e3),
    ResourceURL: ue(i3)
  },
  ct(es, {
    Title: I(nt),
    Abstract: I(nt),
    WGS84BoundingBox: I(af),
    Identifier: I(nt)
  })
), Hv = ct(
  He,
  {
    LegendURL: ue(n3)
  },
  ct(es, {
    Title: I(nt),
    Identifier: I(nt)
  })
), Zv = ct(He, {
  TileMatrixSet: I(nt),
  TileMatrixSetLimits: I(r3)
}), Bv = ct(He, {
  TileMatrixLimits: W(o3)
}), Wv = ct(He, {
  TileMatrix: I(nt),
  MinTileRow: I(ne),
  MaxTileRow: I(ne),
  MinTileCol: I(ne),
  MaxTileCol: I(ne)
}), Vv = ct(
  He,
  {
    Default: I(nt),
    Value: ue(nt)
  },
  ct(es, {
    Identifier: I(nt)
  })
), Yv = ct(es, {
  LowerCorner: W(za),
  UpperCorner: W(za)
}), Uv = ct(
  He,
  {
    WellKnownScaleSet: I(nt),
    TileMatrix: ue(s3)
  },
  ct(es, {
    SupportedCRS: I(nt),
    Identifier: I(nt),
    BoundingBox: I(af)
  })
), Jv = ct(
  He,
  {
    TopLeftCorner: I(za),
    ScaleDenominator: I(Np),
    TileWidth: I(ne),
    TileHeight: I(ne),
    MatrixWidth: I(ne),
    MatrixHeight: I(ne)
  },
  ct(es, {
    Identifier: I(nt)
  })
);
function qv(i, t) {
  return k({}, Xv, i, t);
}
function Kv(i, t) {
  return k({}, Gv, i, t);
}
function Qv(i, t) {
  return k({}, Uv, i, t);
}
function $v(i, t) {
  const e = k({}, Hv, i, t);
  if (!e)
    return;
  const n = i.getAttribute("isDefault") === "true";
  return e.isDefault = n, e;
}
function t3(i, t) {
  return k({}, Zv, i, t);
}
function e3(i, t) {
  return k({}, Vv, i, t);
}
function i3(i, t) {
  const e = i.getAttribute("format"), n = i.getAttribute("template"), s = i.getAttribute("resourceType"), r = {};
  return e && (r.format = e), n && (r.template = n), s && (r.resourceType = s), r;
}
function af(i, t) {
  const e = k(
    [],
    Yv,
    i,
    t
  );
  if (e.length == 2)
    return la(e);
}
function n3(i, t) {
  const e = {};
  return e.format = i.getAttribute("format"), e.href = Zl(i), e;
}
function za(i, t) {
  const e = nt(i).split(/\s+/);
  if (!e || e.length != 2)
    return;
  const n = +e[0], s = +e[1];
  if (!(isNaN(n) || isNaN(s)))
    return [n, s];
}
function s3(i, t) {
  return k({}, Jv, i, t);
}
function r3(i, t) {
  return k([], Bv, i, t);
}
function o3(i, t) {
  return k({}, Wv, i, t);
}
const a3 = kv;
class l3 {
  constructor(t) {
    const e = new a3(), n = t.getOptions();
    if (!n)
      throw new Error("Missing options");
    const s = [];
    Promise.all(n.wmts.map((r) => {
      fetch(r.capability).then((o) => o.text()).then(function(o) {
        var c, u, d;
        const a = new Qm({
          opacity: 1
        }), l = e.read(o), h = np(l, {
          layer: r.layer,
          matrixSet: r.projection
        });
        h && (a.setSource(new ip(h)), a.setVisible(r.layer == n.wmts[0].layer), s.push(a), (c = t.getMap()) == null || c.getLayers().insertAt(0, a), t.getBorderConstraint() && a.setExtent((d = (u = t.getBorderConstraint()) == null ? void 0 : u.getSource()) == null ? void 0 : d.getExtent()), a.on("postrender", function(f) {
          var p, v;
          const g = nm(f), m = f.context;
          m && (m.globalCompositeOperation = "destination-in", (v = (p = t.getBorderConstraint()) == null ? void 0 : p.getSource()) == null || v.forEachFeature(function(y) {
            const x = new Bt({
              fill: new Ut({
                color: "white"
              })
            });
            g.drawFeature(y, x);
          }), m.globalCompositeOperation = "source-over");
        }));
      });
    })), n.border.url !== "" && window.addEventListener("border-contraint-enabled", () => {
      s.forEach((r) => {
        var o, a;
        return r.setExtent((a = (o = t.getBorderConstraint()) == null ? void 0 : o.getSource()) == null ? void 0 : a.getExtent());
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
const h3 = `:root,:host{--ol-background-color: white;--ol-accent-background-color: #F5F5F5;--ol-subtle-background-color: rgba(128, 128, 128, .25);--ol-partial-background-color: rgba(255, 255, 255, .75);--ol-foreground-color: #333333;--ol-subtle-foreground-color: #666666;--ol-brand-color: #00AAFF}.ol-box{box-sizing:border-box;border-radius:2px;border:1.5px solid var(--ol-background-color);background-color:var(--ol-partial-background-color)}.ol-mouse-position{top:8px;right:8px;position:absolute}.ol-scale-line{background:var(--ol-partial-background-color);border-radius:4px;bottom:8px;left:8px;padding:2px;position:absolute}.ol-scale-line-inner{border:1px solid var(--ol-subtle-foreground-color);border-top:none;color:var(--ol-foreground-color);font-size:10px;text-align:center;margin:1px;will-change:contents,width;transition:all .25s}.ol-scale-bar{position:absolute;bottom:8px;left:8px}.ol-scale-bar-inner{display:flex}.ol-scale-step-marker{width:1px;height:15px;background-color:var(--ol-foreground-color);float:right;z-index:10}.ol-scale-step-text{position:absolute;bottom:-5px;font-size:10px;z-index:11;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-text{position:absolute;font-size:12px;text-align:center;bottom:25px;color:var(--ol-foreground-color);text-shadow:-1.5px 0 var(--ol-partial-background-color),0 1.5px var(--ol-partial-background-color),1.5px 0 var(--ol-partial-background-color),0 -1.5px var(--ol-partial-background-color)}.ol-scale-singlebar{position:relative;height:10px;z-index:9;box-sizing:border-box;border:1px solid var(--ol-foreground-color)}.ol-scale-singlebar-even{background-color:var(--ol-subtle-foreground-color)}.ol-scale-singlebar-odd{background-color:var(--ol-background-color)}.ol-unsupported{display:none}.ol-viewport,.ol-unselectable{-webkit-touch-callout:none;-webkit-user-select:none;-moz-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}.ol-viewport canvas{all:unset}.ol-selectable{-webkit-touch-callout:default;-webkit-user-select:text;-moz-user-select:text;user-select:text}.ol-grabbing{cursor:-webkit-grabbing;cursor:-moz-grabbing;cursor:grabbing}.ol-grab{cursor:move;cursor:-webkit-grab;cursor:-moz-grab;cursor:grab}.ol-control{position:absolute;background-color:var(--ol-subtle-background-color);border-radius:4px}.ol-zoom{top:.5em;left:.5em}.ol-rotate{top:.5em;right:.5em;transition:opacity .25s linear,visibility 0s linear}.ol-rotate.ol-hidden{opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s linear .25s}.ol-zoom-extent{top:4.643em;left:.5em}.ol-full-screen{right:.5em;top:.5em}.ol-control button{display:block;margin:1px;padding:0;color:var(--ol-subtle-foreground-color);font-weight:700;text-decoration:none;font-size:inherit;text-align:center;height:1.375em;width:1.375em;line-height:.4em;background-color:var(--ol-background-color);border:none;border-radius:2px}.ol-control button::-moz-focus-inner{border:none;padding:0}.ol-zoom-extent button{line-height:1.4em}.ol-compass{display:block;font-weight:400;will-change:transform}.ol-touch .ol-control button{font-size:1.5em}.ol-touch .ol-zoom-extent{top:5.5em}.ol-control button:hover,.ol-control button:focus{text-decoration:none;outline:1px solid var(--ol-subtle-foreground-color);color:var(--ol-foreground-color)}.ol-zoom .ol-zoom-in{border-radius:2px 2px 0 0}.ol-zoom .ol-zoom-out{border-radius:0 0 2px 2px}.ol-attribution{text-align:right;bottom:.5em;right:.5em;max-width:calc(100% - 1.3em);display:flex;flex-flow:row-reverse;align-items:center}.ol-attribution a{color:var(--ol-subtle-foreground-color);text-decoration:none}.ol-attribution ul{margin:0;padding:1px .5em;color:var(--ol-foreground-color);text-shadow:0 0 2px var(--ol-background-color);font-size:12px}.ol-attribution li{display:inline;list-style:none}.ol-attribution li:not(:last-child):after{content:" "}.ol-attribution img{max-height:2em;max-width:inherit;vertical-align:middle}.ol-attribution button{flex-shrink:0}.ol-attribution.ol-collapsed ul{display:none}.ol-attribution:not(.ol-collapsed){background:var(--ol-partial-background-color)}.ol-attribution.ol-uncollapsible{bottom:0;right:0;border-radius:4px 0 0}.ol-attribution.ol-uncollapsible img{margin-top:-.2em;max-height:1.6em}.ol-attribution.ol-uncollapsible button{display:none}.ol-zoomslider{top:4.5em;left:.5em;height:200px}.ol-zoomslider button{position:relative;height:10px}.ol-touch .ol-zoomslider{top:5.5em}.ol-overviewmap{left:.5em;bottom:.5em}.ol-overviewmap.ol-uncollapsible{bottom:0;left:0;border-radius:0 4px 0 0}.ol-overviewmap .ol-overviewmap-map,.ol-overviewmap button{display:block}.ol-overviewmap .ol-overviewmap-map{border:1px solid var(--ol-subtle-foreground-color);height:150px;width:150px}.ol-overviewmap:not(.ol-collapsed) button{bottom:0;left:0;position:absolute}.ol-overviewmap.ol-collapsed .ol-overviewmap-map,.ol-overviewmap.ol-uncollapsible button{display:none}.ol-overviewmap:not(.ol-collapsed){background:var(--ol-subtle-background-color)}.ol-overviewmap-box{border:1.5px dotted var(--ol-subtle-foreground-color)}.ol-overviewmap .ol-overviewmap-box:hover{cursor:move}
`, c3 = `#map{width:100%;height:100%;background-color:#fff}.ol-layer{background-color:#80808020}.map-overlay{width:100vw;height:100vh;background-color:gray;opacity:.3}.overlay-index{z-index:10}
`, To = `.left-buttons-control-container{display:flex;position:absolute;width:var(--icon-width);flex-direction:column;left:var(--side-distance)}.right-buttons-control-container{display:flex;position:absolute;right:var(--side-distance);width:var(--icon-width);flex-direction:column}.ol-control{background-color:transparent}.ol-control button:hover{background-color:var(--control-background-color-hover);outline:none}.ol-control button:focus{background-color:var(--control-background-color-hover);outline:none}.ol-zoom{position:relative;top:0px;left:0px;margin-bottom:var(--top-distance)}.ol-zoom>.ol-zoom-in{margin-bottom:1px}.ol-full-screen{position:relative;width:var(--icon-width);top:0px;right:0px;margin-bottom:var(--top-distance)}.center-control,.information-control{margin-bottom:var(--top-distance)}.ol-zoom>button{margin:0}.ol-full-screen>button,.ol-full-screen-custom-small>button,.ol-full-screen-custom-medium>button,.ol-full-screen-custom-large>button{border-radius:var(--icon-border-radius);margin:0;cursor:pointer}.ol-control button{background-color:var(--control-background-color);width:var(--icon-width);height:var(--icon-height)}.ol-zoom-in,.ol-zoom-out,.information-control,.center-control,.rotation-control,.ol-full-screen-true,.ol-full-screen-false{z-index:0;position:relative;width:var(--icon-width);height:var(--icon-height);background-color:var(--control-background-color);border-radius:var(--icon-border-radius);cursor:pointer}.ol-zoom-in:hover,.ol-zoom-out:hover,.information-control:hover,.center-control:hover,.rotation-control:hover,.ol-full-screen-true:hover,.ol-full-screen-false:hover,.information-control:focus,.center-control:focus,.rotation-control:focus{background-color:var(--control-background-color-hover);outline:none}.ol-zoom-in{border-top-right-radius:var(--icon-border-radius);border-top-left-radius:var(--icon-border-radius)}.ol-zoom-out{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}.ol-zoom-in>div>svg,.ol-zoom-out>div>svg,.ol-full-screen-true>div>svg,.ol-full-screen-false>div>svg{width:var(--svg-icon-size);height:var(--svg-icon-size)}.ol-zoom-in>div>svg>g>.icon,.ol-zoom-out>div>svg>g>.icon,.ol-full-screen-true>div>svg>g>.icon,.ol-full-screen-false>div>svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}@media only screen and (min-width: 420px){.left-buttons-control-container,.right-buttons-control-container{top:var(--top-distance)}}@media only screen and (max-width: 419px){.left-buttons-control-container,.right-buttons-control-container{top:calc(calc(var(--top-distance) * 2) + var(--box-height))}}
`, lf = `.notification-element-info-light{--notification-background-color: #DBEAFE;--notification-stroke-color: #1D4ED8;--notification-text-color: #1D4ED8}.notification-element-info-dark{--notification-background-color: #2563EB;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-warning-light{--notification-background-color: #FEF3C7;--notification-stroke-color: #B45309;--notification-text-color: #B45309}.notification-element-warning-dark{--notification-background-color: #D97706;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}.notification-element-error-light{--notification-background-color: #FEE2E2;--notification-stroke-color: #B91C1C;--notification-text-color: #B91C1C}.notification-element-error-dark{--notification-background-color: #DC2626;--notification-stroke-color: #FFFFFF;--notification-text-color: #FFFFFF}@media only screen and (max-width: 350px){.notification-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 351px) and (max-width: 995px){.notification-element{left:calc((100% - 334px)/2);width:100%;max-width:302px}}@media only screen and (min-width: 996px){.notification-element{left:calc((100% - (var(--notification-width) + 30px)) / 2);width:var(--notification-width)}}.notification-element{position:absolute;bottom:10px;display:block;font-family:sans-serif;--icon-size: 32px;background-color:var(--notification-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);z-index:5;grid-template-columns:100%;grid-template-rows:100%}.notification-title>div>svg{display:block;width:var(--icon-size);height:var(--icon-size);padding-right:10px}.notification-icon-container{height:100%}.notification-title>div>svg>g>.icon{fill:none;stroke:var(--notification-stroke-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round}.notification-title{display:flex}.notification-title-text{font-weight:400;font-size:12px;line-height:15px;color:var(--notification-text-color)}
`;
var u3 = Object.defineProperty, d3 = Object.getOwnPropertyDescriptor, Qs = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? d3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && u3(t, e, s), s;
};
let tn = class extends At {
  constructor() {
    super(), this.type = "info", this.message = "", this.icon = "", this.theme = "";
  }
  firstUpdated() {
    switch (this.type) {
      case "info":
        this.icon = st.info, this.theme = `notification-element-info-${gt.getTheme()}`;
        break;
      case "warning":
        this.icon = st.warning, this.theme = `notification-element-warning-${gt.getTheme()}`;
        break;
      case "error":
        this.icon = st.error, this.theme = `notification-element-error-${gt.getTheme()}`;
        break;
    }
  }
  render() {
    return Ct`
      <div class="notification-element ${this.theme}">
        <div class="notification-title">
          <div class="notification-icon-container">
            ${Re(this.icon)}
          </div>
          <div class="notification-title-text">${this.message}</div>
        </div>
      </div>
    `;
  }
};
tn.styles = [yt(lf)];
Qs([
  Te()
], tn.prototype, "type", 2);
Qs([
  Te()
], tn.prototype, "message", 2);
Qs([
  Lt()
], tn.prototype, "icon", 2);
Qs([
  Lt()
], tn.prototype, "theme", 2);
tn = Qs([
  Kt("notification-box")
], tn);
class yn extends Dt {
  constructor(t, e) {
    const n = document.createElement(
      "notification-box"
    );
    n.type = t.type, n.message = t.message, super({ element: n }), this.ruleType = t.rule.type, this.div = n, Wt.setResizeEvent(this.div, "--notification-width", e);
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
class f3 {
  constructor() {
    this.geojsonFormat = new Wd();
  }
  convertToMultiPoint(t) {
    return new an({
      geometry: new Po([[t[0], t[1]]])
    });
  }
  formatGeometryCollection(t) {
    const e = new Bd(t);
    return this.geojsonFormat.writeGeometry(e, {
      decimals: 2
    });
  }
  formatFeatureCollection(t) {
    return this.geojsonFormat.writeFeatures(t, {
      decimals: 2
    });
  }
  generateGeometryCollection(t) {
    const e = [];
    return t.forEach((n) => {
      const s = n.getGeometry();
      if (s) {
        const r = s, o = this.convertToMultiPoint(
          r.getCoordinates()
        ).getGeometry();
        o && e.push(o);
      }
    }), this.formatGeometryCollection(e);
  }
  generateFeatureCollection(t, e) {
    const n = [];
    return t.forEach((s) => {
      const r = s.getGeometry();
      if (r) {
        const o = r, a = this.convertToMultiPoint(o.getCoordinates());
        if (a) {
          const l = s.get("objectid");
          l && e.getCurrentFeatureType(l) === "select" && a.set("objectid", l), n.push(a);
        }
      }
    }), this.formatFeatureCollection(n);
  }
  generateTargetGeometry(t, e) {
    var s;
    const n = this.convertToMultiPoint(t);
    if (n) {
      if (((s = e.getOptions()) == null ? void 0 : s.outputFormat) === "GeometryCollection") {
        const r = n.getGeometry();
        return r ? this.formatGeometryCollection([r]) : void 0;
      }
      return this.formatFeatureCollection([n]);
    }
  }
  generateExportData(t, e) {
    var n;
    return ((n = e.getOptions()) == null ? void 0 : n.outputFormat) === "GeometryCollection" ? this.generateGeometryCollection(t) : this.generateFeatureCollection(t, e);
  }
}
class g3 {
  constructor(t) {
    var s;
    if (this.validZoomConstraint = !0, this.validAreaConstraint = !0, this.validBorderContraint = !0, this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1, this.outputFormat = new f3(), !t)
      throw new Error("Missing store!");
    this.store = t;
    const e = this.store.getOptions();
    if (!e)
      throw new Error("Missing options!");
    this.options = e;
    const n = this.store.getMap();
    if (!n)
      throw new Error("Missing map!");
    switch (this.map = n, e.mode.type) {
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
        (s = this.map) == null || s.addControl(new yn({
          type: "error",
          message: "Veuillez s\xE9lectionner un mode de fonctionnement valide.",
          rule: {
            type: "NOT_VALID_MODE"
          }
        }, this.map));
    }
    this.setup(e.notifications), this.displayRightNotification();
  }
  displayRightNotification() {
    var t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p, v, y, x, M, C, E, b, S, O;
    this.validZoomConstraint ? this.validBorderContraint ? this.validAreaConstraint ? this.displayMaxElementConstraint ? ((p = this.zoomNotificationControl) == null || p.hide(), (v = this.inclusionNotificationControl) == null || v.hide(), (y = this.maxElementNotificationControl) == null || y.show(), (x = this.infosNotificationControl) == null || x.hide(), (M = this.borderContraintNotificationControl) == null || M.hide()) : ((C = this.zoomNotificationControl) == null || C.hide(), (E = this.inclusionNotificationControl) == null || E.hide(), (b = this.maxElementNotificationControl) == null || b.hide(), (S = this.infosNotificationControl) == null || S.show(), (O = this.borderContraintNotificationControl) == null || O.hide()) : ((u = this.zoomNotificationControl) == null || u.hide(), (d = this.inclusionNotificationControl) == null || d.show(), (f = this.maxElementNotificationControl) == null || f.hide(), (g = this.infosNotificationControl) == null || g.hide(), (m = this.borderContraintNotificationControl) == null || m.hide()) : ((o = this.zoomNotificationControl) == null || o.hide(), (a = this.inclusionNotificationControl) == null || a.hide(), (l = this.maxElementNotificationControl) == null || l.hide(), (h = this.infosNotificationControl) == null || h.hide(), (c = this.borderContraintNotificationControl) == null || c.show()) : ((t = this.zoomNotificationControl) == null || t.show(), (e = this.inclusionNotificationControl) == null || e.hide(), (n = this.maxElementNotificationControl) == null || n.hide(), (s = this.infosNotificationControl) == null || s.hide(), (r = this.borderContraintNotificationControl) == null || r.hide());
  }
  setupTargetMode() {
    window.addEventListener("current-center-position", (t) => {
      this.validZoomConstraint && this.validAreaConstraint && tt.sendEvent("position-selected", this.outputFormat.generateTargetGeometry(t.detail, this.store));
    });
  }
  iconClickedListener() {
    window.addEventListener("icon-clicked", (t) => {
      const e = this.store.getSelectedFeatures();
      this.validZoomConstraint && e.length > 0 && (this.checkMaxElementContraint(e), this.validMaxElementConstraint && tt.sendEvent("position-selected", this.outputFormat.generateExportData(e, this.store)), tt.sendEvent("authorize-clicked", t.detail)), this.displayRightNotification();
    });
  }
  setupSelectMode() {
    this.iconClickedListener(), this.ruleValidationListener();
  }
  iconCreatedListener() {
    window.addEventListener("icon-created", (t) => {
      const e = this.store.getSelectedFeatures();
      this.checkMaxElementContraint(e), this.checkIsInBorder(e), this.validZoomConstraint && this.validMaxElementConstraint && e.length > 0 && this.validBorderContraint ? (tt.sendEvent("position-selected", this.outputFormat.generateExportData(e, this.store)), tt.sendEvent("authorize-created", t.detail)) : tt.sendEvent("refused-created", t.detail), this.displayRightNotification();
    }), window.addEventListener("icon-removed", () => {
      tt.sendEvent("position-selected", void 0), tt.sendEvent("remove-created-icon", void 0);
    });
  }
  setupCreateMode() {
    this.iconCreatedListener(), this.ruleValidationListener();
  }
  ruleValidationListener() {
    window.addEventListener("rule-validation", () => {
      const t = this.store.getSelectedFeatures();
      this.checkMaxElementContraint(t), this.validZoomConstraint && this.validMaxElementConstraint && t.length > 0 ? tt.sendEvent("position-selected", this.outputFormat.generateExportData(t, this.store)) : tt.sendEvent("position-selected", void 0), this.displayRightNotification();
    });
  }
  setupMixMode() {
    this.iconClickedListener(), this.iconCreatedListener(), this.ruleValidationListener();
  }
  setup(t) {
    t.forEach((e) => {
      e.rule.type === "ZOOM_CONSTRAINT" && this.setupZoomContraint(e), e.rule.type === "AREA_CONSTRAINT" && this.setupInclusionAreaConstraint(e), e.rule.type === "MAX_SELECTION" && this.setupMaxSelectionConstraint(e), e.type === "info" && (this.infosNotificationControl = new yn(e, this.map), this.map.addControl(this.infosNotificationControl));
    }), this.options.border.url !== "" && (this.borderContraintNotificationControl = new yn({
      type: "warning",
      message: this.options.border.notification,
      rule: {
        type: "BORDER_CONSTRAINT"
      }
    }, this.map), this.borderContraintNotificationControl.hide(), this.map.addControl(this.borderContraintNotificationControl));
  }
  setupZoomContraint(t) {
    this.zoomNotificationControl = new yn(t, this.map), this.zoomNotificationControl.disable(), this.map.addControl(this.zoomNotificationControl), this.hasValidZoom(t) && (this.validZoomConstraint = !1), Wt.registerBorderConstaintMapEvent(
      "change:resolution",
      () => {
        this.checkZoomConstraint(t), this.displayRightNotification();
      },
      this.map,
      this.options
    );
  }
  setupInclusionAreaConstraint(t) {
    this.inclusionNotificationControl = new yn(t, this.map), this.inclusionNotificationControl.disable(), this.map.addControl(this.inclusionNotificationControl), window.addEventListener("inclusion-area-included", (e) => {
      this.checkInclusionAreaConstraint(e.detail, t.rule.couldBypass), this.displayRightNotification();
    });
  }
  setupMaxSelectionConstraint(t) {
    const e = t.rule.maxElement;
    e !== void 0 && this.store.setMaxElement(e), t.message = t.message.replace("{x}", `${e}`), this.maxElementNotificationControl = new yn(t, this.map), this.maxElementNotificationControl.disable(), this.map.addControl(this.maxElementNotificationControl);
  }
  hasValidZoom(t) {
    const e = this.map.getView().getZoom();
    return e && t.rule.minZoom && e < t.rule.minZoom;
  }
  checkZoomConstraint(t) {
    this.hasValidZoom(t) ? (this.validZoomConstraint = !1, tt.sendEvent("position-selected", void 0)) : (this.validZoomConstraint = !0, tt.sendEvent("rule-validation", void 0));
  }
  checkInclusionAreaConstraint(t, e) {
    t ? this.validAreaConstraint = !0 : e ? this.validAreaConstraint = !0 : (this.validAreaConstraint = !1, this.options.mode.type === "target" ? tt.sendEvent("position-selected", void 0) : setTimeout(() => {
      this.validAreaConstraint = !0, this.displayRightNotification();
    }, 2e3));
  }
  checkMaxElementContraint(t) {
    this.store.getMaxElement() >= 0 && (t.length >= this.store.getMaxElement() ? this.store.getMaxElement() === 1 && t.length === this.store.getMaxElement() ? (this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1) : t.length === this.store.getMaxElement() && !this.validMaxElementConstraint ? (this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !0) : t.length > this.store.getMaxElement() && (this.validMaxElementConstraint = !1, this.displayMaxElementConstraint = !0) : (this.validMaxElementConstraint = !0, this.displayMaxElementConstraint = !1));
  }
  checkIsInBorder(t) {
    var e, n, s;
    if (this.options.border.url !== "") {
      const o = t[t.length - 1].getGeometry();
      ((s = (n = (e = this.store.getBorderConstraint()) == null ? void 0 : e.getSource()) == null ? void 0 : n.getFeatures()[0].getGeometry()) == null ? void 0 : s.intersectsCoordinate(o.getCoordinates())) ? this.validBorderContraint = !0 : (this.validBorderContraint = !1, this.displayRightNotification(), setTimeout(() => {
        this.validBorderContraint = !0, this.displayRightNotification();
      }, 2e3));
    } else
      this.validBorderContraint = !0;
  }
}
const m3 = `:host>.no-box{--box-height: 0px;--top-distance: 10px}:host>.select{--box-height: 68px;--top-distance: 10px}:host>.large{--box-height: 79px;--top-distance: 10px}:host>.medium{--box-height: 64px;--top-distance: 10px}:host>.small{--box-height: 49px;--top-distance: 10px}:host>.light{--control-background-color: rgb(30 41 59 / 75%);--control-background-color-hover: rgb(30 41 59 / 100%);--control-icon-color: white;--information-box-background-color: white;--information-box-title-color: #1E293B;--information-cross-hover-color: rgb(30 41 59 / 75%);--information-box-text-color: #334155;--suggestion-box-text-color: #334155;--select-icon-background: #1E293B;--icon-border-color: #CBD5E1}:host>.dark{--control-background-color: rgb(255 255 255 / 75%);--control-background-color-hover: rgb(255 255 255 / 100%);--control-icon-color: #1E293B;--information-box-background-color: #1F2937;--information-box-title-color: #F3F4F6;--information-cross-hover-color: rgb(255 255 255 / 75%);--information-box-text-color: #9CA3AF;--suggestion-box-text-color: #F1F5F9;--select-icon-background: rgb(255,255,255, .75);--icon-border-color: #334155}:host>#map{--icon-width: 36px;--icon-height: 36px;--side-distance: 10px;--icon-border-radius: 4px;--box-border-radius: 4px;--svg-icon-size: 26px;--icon-stroke-width: 2px;font-family:sans-serif}
`, p3 = `@keyframes fadeIn{0%{opacity:0;visibility:inherit}to{opacity:1}}@keyframes fadeOut{0%{opacity:1}to{opacity:0;visibility:hidden}}.fade-in{animation:fadeIn .3s forwards}.fade-out{animation:fadeOut .3s forwards}.disabled{visibility:hidden}
`, v3 = `@media only screen and (min-width: 513px){.layer-container-position{right:55px;width:100%}}@media only screen and (min-width: 350px) and (max-width: 512px){.layer-container-position{left:calc(50% - 166px);width:100%}}@media only screen and (max-width: 350px){.layer-container-position{left:10px;width:calc(100% - 20px)}}.layer-container-position{z-index:1;max-width:332px;top:var(--top-distance);position:absolute}@media only screen and (min-width: 513px){.custom-popup-element-position{right:55px;width:100%}}@media only screen and (min-width: 350px) and (max-width: 512px){.custom-popup-element-position{left:calc(50% - 166px);width:100%}}@media only screen and (max-width: 350px){.custom-popup-element-position{left:10px;width:calc(100% - 20px)}}.custom-popup-element-position{font-family:sans-serif;position:absolute;top:10px;z-index:2;max-width:332px}
`;
class y3 {
  static webComponentOptions(t) {
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
    return t.zoom !== void 0 && (e.zoom = t.zoom), t.minZoom !== void 0 && (e.minZoom = t.minZoom), t.maxZoom !== void 0 && (e.maxZoom = t.maxZoom), t.interaction !== void 0 && (e.interaction = t.interaction), t.search !== void 0 && (e.search = t.search), t.defaultCenter !== void 0 && t.defaultCenter[0] !== null && (e.defaultCenter = t.defaultCenter), t.information !== void 0 && (e.information = t.information), t.notifications !== void 0 && t.notifications.length > 0 && (e.notifications = t.notifications), t.mode !== void 0 && (e.mode = t.mode), t.cluster !== void 0 && (e.cluster = t.cluster), t.geolocationInformation !== void 0 && (e.geolocationInformation = t.geolocationInformation), t.wfs !== void 0 && (e.wfs = t.wfs), t.wmts !== void 0 && (e.wmts = t.wmts), t.inclusionArea !== void 0 && (e.inclusionArea = t.inclusionArea), t.selectionTargetBoxMessage !== void 0 && (e.selectionTargetBoxMessage = t.selectionTargetBoxMessage), t.border !== void 0 && (e.border = t.border), t.outputFormat !== void 0 && (e.outputFormat = t.outputFormat), (e.mode.type == "select" || e.mode.type == "mix") && e.wfs.url == "" && console.error("Configuration error: There is no WFS url defined"), e;
  }
}
class x3 {
  static setupStyle() {
    return new Bt({
      stroke: new Se({
        color: "#C026D3",
        width: 1
      }),
      fill: new Ut({
        color: "rgb(191, 38, 211, 0.10)"
      })
    });
  }
}
class M3 {
  constructor(t) {
    var s;
    const e = t.getOptions();
    if (!e)
      throw new Error("Invalid store options");
    this.vectorSource = rf.getSource(e.inclusionArea.url, e.inclusionArea.filter, !0);
    const n = new Bn({
      source: this.vectorSource,
      style: x3.setupStyle()
    });
    (s = t.getMap()) == null || s.addLayer(n), e.mode.type === "target" && window.addEventListener("current-center-position", (r) => {
      this.couldCreate(r.detail);
    });
  }
  couldCreate(t) {
    var n;
    const e = this.vectorSource.getClosestFeatureToCoordinate(
      t
    );
    if (e && ((n = e.getGeometry()) == null ? void 0 : n.getType()) === "Polygon") {
      const s = e.getGeometry(), r = s == null ? void 0 : s.intersectsCoordinate(t);
      return tt.sendEvent("inclusion-area-included", r), r;
    }
    return !1;
  }
}
const Lo = `svg{margin-left:calc((var(--icon-width) - var(--svg-icon-size)) / 2);margin-top:calc((var(--icon-height) - var(--svg-icon-size)) / 2);width:var(--svg-icon-size);height:var(--svg-icon-size)}svg>g>.icon{fill:none;stroke:var(--control-icon-color);stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}
`;
var C3 = Object.defineProperty, w3 = Object.getOwnPropertyDescriptor, E3 = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? w3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && C3(t, e, s), s;
};
let Fa = class extends At {
  constructor() {
    super();
  }
  render() {
    return Ct`<div class="ol-unselectable ol-control center-control" tabindex="0">
                  <div>
                    <div class="control-${gt.getTheme()}">
                      ${Re(st.geolocation)}
                    </div>
                  </div>
                </div>
    `;
  }
};
Fa.styles = [yt(Lo), yt(To)];
Fa = E3([
  Kt("geolocation-control-button")
], Fa);
class b3 extends Dt {
  constructor(t) {
    const e = document.createElement("geolocation-control-button");
    super({
      element: e
    }), e.addEventListener("click", this.centerMap.bind(this), !1), this.setTarget(t);
  }
  centerMap() {
    const t = gt.getGeolocation();
    if (t) {
      const e = t.getPosition(), n = this.getMap();
      if (n) {
        const s = n.getView();
        e && s.setCenter(e);
      }
    }
  }
}
var P3 = Object.defineProperty, S3 = Object.getOwnPropertyDescriptor, _3 = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? S3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && P3(t, e, s), s;
};
let Da = class extends At {
  render() {
    return Ct`<div class="control-${gt.getTheme()}" tabindex="0">${Re(st.rotation)}</div>`;
  }
};
Da.styles = [yt(Lo)];
Da = _3([
  Kt("rotation-control-button")
], Da);
class zc extends Dt {
  constructor(t, e) {
    const n = document.createElement("div"), s = document.createElement("rotation-control-button");
    n.appendChild(s);
    const r = document.createElement("div");
    if (r.className = "rotation-control ", r.appendChild(n), super({
      element: r
    }), !e)
      throw new Error("Missing map!");
    this.map = e, n.addEventListener("click", this.resetRotation.bind(this), !1), this.setTarget(t);
  }
  resetRotation() {
    this.map.getView().setRotation(0);
  }
}
const R3 = `.custom-popup-element{background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:0 11px 11px;border-radius:var(--box-border-radius)}.custom-popup-element:after{content:"";width:var(--progress-width);height:4px;background:#008C6F;position:absolute;bottom:-1px;left:0;border-bottom-left-radius:4px;border-bottom-right-radius:var(--border-radius-right)}.custom-popup-title{display:flex;height:36px}.custom-popup-title-text{width:calc(100% - var(--svg-icon-size));font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color);align-items:center;display:flex}.custom-popup-title-svg-container{width:29px;height:36px;justify-content:flex-end;display:flex;align-items:center}.custom-popup-title-svg{width:10%;justify-content:flex-end;display:flex;fill:none;stroke:var(--information-box-title-color);stroke-width:2px;stroke-linejoin:round;stroke-linecap:round;cursor:pointer}.custom-popup-title-svg:hover{stroke:var(--information-cross-hover-color)}.custom-popup-content{width:calc(100% - var(--svg-icon-size));font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var T3 = Object.defineProperty, L3 = Object.getOwnPropertyDescriptor, Bl = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? L3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && T3(t, e, s), s;
};
let Wn = class extends At {
  constructor(i) {
    super(), this._width = 100, this._borderRadiusRight = 0, this.store = i;
    const t = i.getOptions();
    if (!t)
      throw new Error("Missing options");
    window.addEventListener("clear-information-box-interval", this.clear.bind(this), !0), window.addEventListener("open-information-box", () => {
      this._width = 100;
      const e = t.information.duration / 100;
      this.interval = setInterval(() => {
        this._width > 0 ? (this._width < 100 && (this._borderRadiusRight = 0), this._width--) : this.closeBox();
      }, e);
    });
  }
  render() {
    var i, t;
    return Ct`
      <div class="information-box-${gt.getTheme()} custom-popup-element" style="--progress-width: ${this._width}%; --border-radius-right: ${this._borderRadiusRight}px">
        <div class="custom-popup-title">
          <div class="custom-popup-title-text">${(i = this.store.getOptions()) == null ? void 0 : i.information.title}</div>
          <div class="custom-popup-title-svg-container">
            <div class="cross-div" @click="${this.closeBox}">
              ${Re(st.cross)}
            </div>
          </div>
        </div>
        <div class="custom-popup-content">${(t = this.store.getOptions()) == null ? void 0 : t.information.content}</div>
        <div class="custom-progress-element"></div>
      </div>`;
  }
  clear() {
    clearInterval(this.interval);
  }
  closeBox() {
    clearInterval(this.interval), tt.sendEvent("close-information-box", {});
  }
};
Wn.styles = [yt(R3)];
Bl([
  Lt()
], Wn.prototype, "_width", 2);
Bl([
  Lt()
], Wn.prototype, "_borderRadiusRight", 2);
Wn = Bl([
  Kt("information-box")
], Wn);
class O3 extends Dt {
  constructor(t) {
    const e = new Wn(t);
    super({ element: e }), this.div = e, this.div.classList.add("custom-popup-element-position");
  }
  show() {
    this.div.classList.remove("fade-out"), this.div.classList.add("fade-in");
  }
  hide() {
    this.div.classList.remove("fade-in"), this.div.classList.add("fade-out");
  }
}
var A3 = Object.defineProperty, I3 = Object.getOwnPropertyDescriptor, N3 = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? I3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && A3(t, e, s), s;
};
let ja = class extends At {
  constructor() {
    super();
  }
  render() {
    return Ct`<div class="information-control" tabindex="0">
                  <div>
                    <div class="control-${gt.getTheme()}">
                      ${Re(st.information)}
                    </div>
                  </div>
                </div>
    `;
  }
};
ja.styles = [yt(Lo), yt(To)];
ja = N3([
  Kt("information-control-button")
], ja);
class z3 extends Dt {
  constructor(t, e, n) {
    const s = document.createElement("information-control-button");
    super({
      element: s
    }), this.informationIsOpen = !0, s.addEventListener("click", this.toogleInformationBox.bind(this), !1), window.addEventListener("close-information-box", this.closeInformationBox.bind(this), !1), this.control = new O3(e), n.addControl(this.control), this.openInformationBox(), this.setTarget(t);
  }
  closeInformationBox() {
    tt.sendEvent("clear-information-box-interval", {}), this.control.hide(), this.informationIsOpen = !1;
  }
  openInformationBox() {
    this.control.show(), tt.sendEvent("open-information-box", {}), this.informationIsOpen = !0;
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
const Fc = Il(class extends Nl {
  constructor(i) {
    var t;
    if (super(i), i.type !== Vd.ATTRIBUTE || i.name !== "class" || ((t = i.strings) === null || t === void 0 ? void 0 : t.length) > 2)
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
    return Pi;
  }
});
class hf {
}
hf.baseMapIcon = "data:image/png;base64,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";
const cf = `.layer-container{font-family:sans-serif}.layer-title-container{border-radius:var(--icon-border-radius) var(--icon-border-radius) 0px 0px;border-bottom:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color)}.layer-text{width:calc(100% - 13px);height:36px;padding:0;font-weight:400;background-color:var(--information-box-background-color);font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color);margin:0 0 0 11px;align-items:center;display:flex}.layer-svg-container{width:29px;height:36px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-bottom-left-radius:var(--icon-border-radius);border-bottom-right-radius:var(--icon-border-radius)}li{height:64px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--information-box-text-color)}li>.image-container{width:56px;display:flex;align-items:center;justify-content:center;height:inherit;padding-right:9px}li>.image-container>img{width:46px;height:46px;border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color)}.selected-layer{border:2px solid #dc2626!important;border-radius:var(--icon-border-radius)}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var F3 = Object.defineProperty, D3 = Object.getOwnPropertyDescriptor, is = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? D3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && F3(t, e, s), s;
};
let Vn = class extends At {
  constructor() {
    super(...arguments), this._currentSelectedIndex = 0, this._wmts = [], this.wmts = "";
  }
  selectLayer(i, t) {
    tt.sendEvent("layer-selected", i), this._currentSelectedIndex = t;
  }
  updated(i) {
    i.has("wmts") && (this._wmts = JSON.parse(this.wmts));
  }
  render() {
    return Ct`
                <ul>
                  ${this._wmts.map(
      (i, t) => Ct`<li tabindex="0" @click=${() => this.selectLayer(i, t)}>
                          <div class="image-container">
                          ${zl(
        i.thumbnail && i.thumbnail.length > 0 ? Ct`
                            <img class=${Fc({ "selected-layer": this._currentSelectedIndex === t })} src="${i.thumbnail}"/>
                            ` : Ct`
                            <img class=${Fc({ "selected-layer": this._currentSelectedIndex === t })} src="${hf.baseMapIcon}"/>
                            `
      )}
                          </div>
                          <p>${i.name}</p>
                        </li>`
    )}
                </ul>
              `;
  }
};
Vn.styles = [yt(cf)];
is([
  Lt()
], Vn.prototype, "_currentSelectedIndex", 2);
is([
  Lt()
], Vn.prototype, "_wmts", 2);
is([
  Te()
], Vn.prototype, "wmts", 2);
Vn = is([
  Kt("layer-list")
], Vn);
let eo = class extends At {
  constructor() {
    super(...arguments), this.wmts = [];
  }
  render() {
    return Ct`<div class="layer-container">
                  <div class="layer-title-container">
                      <p class="layer-text">Affichage de la carte</p>
                      <div class="layer-svg-container">
                        <div class="cross-div" @click="${this.closeBox}">
                          ${Re(st.cross)}
                        </div>
                      </div>
                  </div>
                  <layer-list wmts=${JSON.stringify(this.wmts)}/>
              </div>`;
  }
  closeBox() {
    tt.sendEvent("layer-selection-closed", void 0);
  }
};
eo.styles = [yt(cf)];
is([
  Te()
], eo.prototype, "wmts", 2);
eo = is([
  Kt("layer-selection")
], eo);
class j3 extends Dt {
  constructor(t) {
    const e = document.createElement("layer-selection");
    e.wmts = t, super({ element: e }), this.element.classList.add("layer-container-position");
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
var k3 = Object.defineProperty, X3 = Object.getOwnPropertyDescriptor, G3 = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? X3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && k3(t, e, s), s;
};
let ka = class extends At {
  render() {
    return Ct`<div class="ol-unselectable ol-control center-control" tabindex="0">
                  <div>
                    <div class="control-${gt.getTheme()}">
                      ${Re(st.stack)}
                    </div>
                  </div>
                </div> `;
  }
};
ka.styles = [yt(Lo), yt(To)];
ka = G3([
  Kt("geo-layer-control-button")
], ka);
class H3 extends Dt {
  constructor(t, e, n) {
    const s = document.createElement(
      "geo-layer-control-button"
    );
    super({
      element: s
    }), this.isOpen = !1, this.layerSelection = new j3(n), this.layerSelection.disable(), e.addControl(this.layerSelection), s.addEventListener("click", () => {
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
class Dc extends Dt {
  constructor(t) {
    const e = document.createElement("div");
    e.className = t, super({
      element: e
    }), this.div = e;
  }
}
class Z3 {
  static setupIcon(t, e) {
    var l;
    const n = e.getOptions(), s = t.readonly, r = e.getMap();
    if (!r)
      throw new Error("Missing map!");
    const o = new Dc("left-buttons-control-container");
    r.addControl(o);
    const a = new Dc("right-buttons-control-container");
    r.addControl(a), s || r.addControl(new z3(a.div, e, r)), n != null && n.interaction.fullscreen && r.addControl(
      new ym({
        label: st.fullScreenLabel(),
        labelActive: st.fullScreenLabelActive(),
        className: "ol-full-screen",
        target: a.div
      })
    ), r.addControl(new H3(a.div, r, (l = n == null ? void 0 : n.wmts) != null ? l : [])), n != null && n.interaction.displayZoom && r.addControl(
      new hd({
        zoomInLabel: st.zoomInLabel(),
        zoomOutLabel: st.zoomOutLabel(),
        className: "ol-zoom",
        target: o.div
      })
    ), (n == null ? void 0 : n.interaction.enableCenterButton) && !s && r.addControl(new b3(o.div)), n != null && n.interaction.enableRotation && Wt.registerBorderConstaintMapEvent(
      "change:rotation",
      (h) => B3(r, h, o.div),
      r,
      n
    );
  }
}
function B3(i, t, e) {
  i.getControls().forEach((n) => {
    n instanceof zc && i.removeControl(n);
  }), t.target.getRotation() !== 0 && i.addControl(new zc(e, i));
}
var W3 = Object.defineProperty, V3 = Object.getOwnPropertyDescriptor, Y3 = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? V3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && W3(t, e, s), s;
};
class U3 {
  constructor(t) {
    var n;
    const e = t.getMap();
    if (!e)
      throw new Error("Invalid map!");
    e.getView().on("change:center", (s) => {
      tt.sendEvent("current-center-position", s.target.getCenter());
    }), ((n = t.getOptions()) == null ? void 0 : n.border.url) !== "" && Wt.registerWindowListener(
      "border-contraint-enabled",
      "change:center",
      (s) => {
        tt.sendEvent("current-center-position", s.target.getCenter());
      },
      e
    );
  }
}
let jc = class extends At {
  constructor() {
    super();
  }
  render() {
    return Ct`
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
jc = Y3([
  Kt("target-element")
], jc);
class J3 extends Dt {
  constructor(t) {
    const e = document.createElement("target-element");
    super({ element: e }), new U3(t);
  }
}
const q3 = `@media only screen and (min-width: 351px) and (max-width: 995px){.box-element{left:calc(50% - 167px);width:calc(100% - 30px);max-width:302px}}@media only screen and (max-width: 350px){.box-element{left:10px;width:calc(100% - 50px);max-width:302px}}@media only screen and (min-width: 996px){.box-element{left:calc((100% - (var(--target-box-width) + 30px)) / 2);width:calc(var(--target-box-width))}}.box-element{position:absolute;top:10px;background-color:var(--information-box-background-color);box-shadow:0 1px 4px #0003;padding:15px;border-radius:var(--box-border-radius);border:1px solid var(--information-box-background-color)}.box-element-title{display:flex}.box-element-title-text{width:90%;font-weight:600;font-size:14px;line-height:17px;color:var(--information-box-title-color)}.box-element-content{font-weight:400;font-size:12px;line-height:15px;color:var(--information-box-text-color)}
`;
var K3 = Object.defineProperty, Q3 = Object.getOwnPropertyDescriptor, $s = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? Q3(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && K3(t, e, s), s;
};
let Ti = class extends At {
  constructor(i) {
    super(), this.defaultPosition = [0, 0], this._currentPosition = "", this._reversePosition = "";
    const t = i.getOptions();
    if (!t)
      throw new Error("invalid options");
    this.options = t, this._lastPosition = this.defaultPosition;
    const e = 20;
    window.addEventListener("current-center-position", (n) => {
      var s, r;
      (s = this.options) != null && s.geolocationInformation.reverseLocation ? (Math.abs(this._lastPosition[0] - n.detail[0]) > e || Math.abs(this._lastPosition[1] - n.detail[1]) > e) && (this._lastPosition = n.detail, this.searchAddress(n.detail)) : this._reversePosition = "", this._currentPosition = (r = this.options) != null && r.geolocationInformation.currentLocation ? `${n.detail[0].toFixed(6)}, ${n.detail[1].toFixed(6)}` : "";
    });
  }
  connectedCallback() {
    super.connectedCallback();
  }
  searchAddress(i) {
    Yd.getAddressFromCoordinate(i).then((t) => {
      this._reversePosition = t.results.length > 0 ? `\xC0 proximit\xE9 de ${t.results[0].attributes.strname_deinr}` : "Aucune adresse proche reconnue";
    });
  }
  firstUpdated() {
    var i, t;
    (i = this.options) != null && i.geolocationInformation.reverseLocation ? this.searchAddress(this.defaultPosition) : this._reversePosition = "", this._currentPosition = (t = this.options) != null && t.geolocationInformation.currentLocation ? `${this.defaultPosition[0].toFixed(6)}, ${this.defaultPosition[1].toFixed(6)}` : "";
  }
  render() {
    var i;
    return Ct`
      <div class="information-box-${gt.getTheme()} box-element">
        <div class="box-element-title">
          <div class="box-element-title-text">${(i = this.options) == null ? void 0 : i.selectionTargetBoxMessage}</div>
        </div>
        <div class="box-element-content">${this._reversePosition}</div>
        <div class="box-element-content">${this._currentPosition}</div>
      </div>
    `;
  }
};
Ti.styles = [yt(q3)];
$s([
  Te()
], Ti.prototype, "defaultPosition", 2);
$s([
  Lt()
], Ti.prototype, "_currentPosition", 2);
$s([
  Lt()
], Ti.prototype, "_reversePosition", 2);
$s([
  Lt()
], Ti.prototype, "_lastPosition", 2);
Ti = $s([
  Kt("target-information-box-element")
], Ti);
class $3 extends Dt {
  constructor(t) {
    var s, r;
    const e = new Ti(t);
    e.defaultPosition = (r = (s = t.getOptions()) == null ? void 0 : s.defaultCenter) != null ? r : [], super({ element: e });
    const n = t.getMap();
    if (!n)
      throw new Error("invalid map");
    Wt.setResizeEvent(this.element, "--target-box-width", n);
  }
}
function ty(i) {
  i("EPSG:4326", "+title=WGS 84 (long/lat) +proj=longlat +ellps=WGS84 +datum=WGS84 +units=degrees"), i("EPSG:4269", "+title=NAD83 (long/lat) +proj=longlat +a=6378137.0 +b=6356752.31414036 +ellps=GRS80 +datum=NAD83 +units=degrees"), i("EPSG:3857", "+title=WGS 84 / Pseudo-Mercator +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"), i.WGS84 = i["EPSG:4326"], i["EPSG:3785"] = i["EPSG:3857"], i.GOOGLE = i["EPSG:3857"], i["EPSG:900913"] = i["EPSG:3857"], i["EPSG:102113"] = i["EPSG:3857"];
}
var en = 1, nn = 2, Or = 3, ey = 4, Xa = 5, kc = 6378137, iy = 6356752314e-3, Xc = 0.0066943799901413165, ws = 484813681109536e-20, P = Math.PI / 2, ny = 0.16666666666666666, sy = 0.04722222222222222, ry = 0.022156084656084655, T = 1e-10, Xt = 0.017453292519943295, ze = 57.29577951308232, lt = Math.PI / 4, ks = Math.PI * 2, _t = 3.14159265359, oe = {};
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
const oy = {
  ft: { to_meter: 0.3048 },
  "us-ft": { to_meter: 1200 / 3937 }
};
var Gc = /[\s_\-\/\(\)]/g;
function Li(i, t) {
  if (i[t])
    return i[t];
  for (var e = Object.keys(i), n = t.toLowerCase().replace(Gc, ""), s = -1, r, o; ++s < e.length; )
    if (r = e[s], o = r.toLowerCase().replace(Gc, ""), o === n)
      return i[r];
}
function Ga(i) {
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
      t.lat0 = a * Xt;
    },
    lat_1: function(a) {
      t.lat1 = a * Xt;
    },
    lat_2: function(a) {
      t.lat2 = a * Xt;
    },
    lat_ts: function(a) {
      t.lat_ts = a * Xt;
    },
    lon_0: function(a) {
      t.long0 = a * Xt;
    },
    lon_1: function(a) {
      t.long1 = a * Xt;
    },
    lon_2: function(a) {
      t.long2 = a * Xt;
    },
    alpha: function(a) {
      t.alpha = parseFloat(a) * Xt;
    },
    gamma: function(a) {
      t.rectified_grid_angle = parseFloat(a);
    },
    lonc: function(a) {
      t.longc = a * Xt;
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
      var l = Li(oy, a);
      l && (t.to_meter = l.to_meter);
    },
    from_greenwich: function(a) {
      t.from_greenwich = a * Xt;
    },
    pm: function(a) {
      var l = Li(oe, a);
      t.from_greenwich = (l || parseFloat(a)) * Xt;
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
var Xs = 1, uf = 2, df = 3, io = 4, ff = 5, Wl = -1, ay = /\s/, ly = /[A-Za-z]/, hy = /[A-Za-z84_]/, Oo = /[,\]]/, gf = /[\d\.E\-\+]/;
function li(i) {
  if (typeof i != "string")
    throw new Error("not a string");
  this.text = i.trim(), this.level = 0, this.place = 0, this.root = null, this.stack = [], this.currentObject = null, this.state = Xs;
}
li.prototype.readCharicter = function() {
  var i = this.text[this.place++];
  if (this.state !== io)
    for (; ay.test(i); ) {
      if (this.place >= this.text.length)
        return;
      i = this.text[this.place++];
    }
  switch (this.state) {
    case Xs:
      return this.neutral(i);
    case uf:
      return this.keyword(i);
    case io:
      return this.quoted(i);
    case ff:
      return this.afterquote(i);
    case df:
      return this.number(i);
    case Wl:
      return;
  }
};
li.prototype.afterquote = function(i) {
  if (i === '"') {
    this.word += '"', this.state = io;
    return;
  }
  if (Oo.test(i)) {
    this.word = this.word.trim(), this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in afterquote yet, index ' + this.place);
};
li.prototype.afterItem = function(i) {
  if (i === ",") {
    this.word !== null && this.currentObject.push(this.word), this.word = null, this.state = Xs;
    return;
  }
  if (i === "]") {
    this.level--, this.word !== null && (this.currentObject.push(this.word), this.word = null), this.state = Xs, this.currentObject = this.stack.pop(), this.currentObject || (this.state = Wl);
    return;
  }
};
li.prototype.number = function(i) {
  if (gf.test(i)) {
    this.word += i;
    return;
  }
  if (Oo.test(i)) {
    this.word = parseFloat(this.word), this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in number yet, index ' + this.place);
};
li.prototype.quoted = function(i) {
  if (i === '"') {
    this.state = ff;
    return;
  }
  this.word += i;
};
li.prototype.keyword = function(i) {
  if (hy.test(i)) {
    this.word += i;
    return;
  }
  if (i === "[") {
    var t = [];
    t.push(this.word), this.level++, this.root === null ? this.root = t : this.currentObject.push(t), this.stack.push(this.currentObject), this.currentObject = t, this.state = Xs;
    return;
  }
  if (Oo.test(i)) {
    this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in keyword yet, index ' + this.place);
};
li.prototype.neutral = function(i) {
  if (ly.test(i)) {
    this.word = i, this.state = uf;
    return;
  }
  if (i === '"') {
    this.word = "", this.state = io;
    return;
  }
  if (gf.test(i)) {
    this.word = i, this.state = df;
    return;
  }
  if (Oo.test(i)) {
    this.afterItem(i);
    return;
  }
  throw new Error(`havn't handled "` + i + '" in neutral yet, index ' + this.place);
};
li.prototype.output = function() {
  for (; this.place < this.text.length; )
    this.readCharicter();
  if (this.state === Wl)
    return this.root;
  throw new Error('unable to parse string "' + this.text + '". State is ' + this.state);
};
function cy(i) {
  var t = new li(i);
  return t.output();
}
function Hc(i, t, e) {
  Array.isArray(t) && (e.unshift(t), t = null);
  var n = t ? {} : i, s = e.reduce(function(r, o) {
    return _n(o, r), r;
  }, n);
  t && (i[t] = s);
}
function _n(i, t) {
  if (!Array.isArray(i)) {
    t[i] = !0;
    return;
  }
  var e = i.shift();
  if (e === "PARAMETER" && (e = i.shift()), i.length === 1) {
    if (Array.isArray(i[0])) {
      t[e] = {}, _n(i[0], t[e]);
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
      }, i.length === 3 && _n(i[2], t[e]);
      return;
    case "SPHEROID":
    case "ELLIPSOID":
      t[e] = {
        name: i[0],
        a: i[1],
        rf: i[2]
      }, i.length === 4 && _n(i[3], t[e]);
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
      i[0] = ["name", i[0]], Hc(t, e, i);
      return;
    default:
      for (n = -1; ++n < i.length; )
        if (!Array.isArray(i[n]))
          return _n(i, t[e]);
      return Hc(t, e, i);
  }
}
var uy = 0.017453292519943295;
function dy(i, t) {
  var e = t[0], n = t[1];
  !(e in i) && n in i && (i[e] = i[n], t.length === 3 && (i[e] = t[2](i[e])));
}
function qe(i) {
  return i * uy;
}
function fy(i) {
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
    return dy(i, h);
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
    ["lat0", "latitude_of_center", qe],
    ["longitude_of_center", "Longitude_Of_Center"],
    ["longitude_of_center", "Longitude_of_center"],
    ["longc", "longitude_of_center", qe],
    ["x0", "false_easting", o],
    ["y0", "false_northing", o],
    ["long0", "central_meridian", qe],
    ["lat0", "latitude_of_origin", qe],
    ["lat0", "standard_parallel_1", qe],
    ["lat1", "standard_parallel_1", qe],
    ["lat2", "standard_parallel_2", qe],
    ["azimuth", "Azimuth"],
    ["alpha", "azimuth", qe],
    ["srsCode", "name"]
  ];
  l.forEach(a), !i.long0 && i.longc && (i.projName === "Albers_Conic_Equal_Area" || i.projName === "Lambert_Azimuthal_Equal_Area") && (i.long0 = i.longc), !i.lat_ts && i.lat1 && (i.projName === "Stereographic_South_Pole" || i.projName === "Polar Stereographic (variant B)") && (i.lat0 = qe(i.lat1 > 0 ? 90 : -90), i.lat_ts = i.lat1);
}
function mf(i) {
  var t = cy(i), e = t.shift(), n = t.shift();
  t.unshift(["name", n]), t.unshift(["type", e]);
  var s = {};
  return _n(t, s), fy(s), s;
}
function Yt(i) {
  var t = this;
  if (arguments.length === 2) {
    var e = arguments[1];
    typeof e == "string" ? e.charAt(0) === "+" ? Yt[i] = Ga(arguments[1]) : Yt[i] = mf(arguments[1]) : Yt[i] = e;
  } else if (arguments.length === 1) {
    if (Array.isArray(i))
      return i.map(function(n) {
        Array.isArray(n) ? Yt.apply(t, n) : Yt(n);
      });
    if (typeof i == "string") {
      if (i in Yt)
        return Yt[i];
    } else
      "EPSG" in i ? Yt["EPSG:" + i.EPSG] = i : "ESRI" in i ? Yt["ESRI:" + i.ESRI] = i : "IAU2000" in i ? Yt["IAU2000:" + i.IAU2000] = i : console.log(i);
    return;
  }
}
ty(Yt);
function gy(i) {
  return typeof i == "string";
}
function my(i) {
  return i in Yt;
}
var py = ["PROJECTEDCRS", "PROJCRS", "GEOGCS", "GEOCCS", "PROJCS", "LOCAL_CS", "GEODCRS", "GEODETICCRS", "GEODETICDATUM", "ENGCRS", "ENGINEERINGCRS"];
function vy(i) {
  return py.some(function(t) {
    return i.indexOf(t) > -1;
  });
}
var yy = ["3857", "900913", "3785", "102113"];
function xy(i) {
  var t = Li(i, "authority");
  if (!!t) {
    var e = Li(t, "epsg");
    return e && yy.indexOf(e) > -1;
  }
}
function My(i) {
  var t = Li(i, "extension");
  if (!!t)
    return Li(t, "proj4");
}
function Cy(i) {
  return i[0] === "+";
}
function wy(i) {
  if (gy(i)) {
    if (my(i))
      return Yt[i];
    if (vy(i)) {
      var t = mf(i);
      if (xy(t))
        return Yt["EPSG:3857"];
      var e = My(t);
      return e ? Ga(e) : t;
    }
    if (Cy(i))
      return Ga(i);
  } else
    return i;
}
function Zc(i, t) {
  i = i || {};
  var e, n;
  if (!t)
    return i;
  for (n in t)
    e = t[n], e !== void 0 && (i[n] = e);
  return i;
}
function ke(i, t, e) {
  var n = i * t;
  return e / Math.sqrt(1 - n * n);
}
function tr(i) {
  return i < 0 ? -1 : 1;
}
function A(i) {
  return Math.abs(i) <= _t ? i : i - tr(i) * ks;
}
function _e(i, t, e) {
  var n = i * e, s = 0.5 * i;
  return n = Math.pow((1 - n) / (1 + n), s), Math.tan(0.5 * (P - t)) / n;
}
function Gs(i, t) {
  for (var e = 0.5 * i, n, s, r = P - 2 * Math.atan(t), o = 0; o <= 15; o++)
    if (n = i * Math.sin(r), s = P - 2 * Math.atan(t * Math.pow((1 - n) / (1 + n), e)) - r, r += s, Math.abs(s) <= 1e-10)
      return r;
  return -9999;
}
function Ey() {
  var i = this.b / this.a;
  this.es = 1 - i * i, "x0" in this || (this.x0 = 0), "y0" in this || (this.y0 = 0), this.e = Math.sqrt(this.es), this.lat_ts ? this.sphere ? this.k0 = Math.cos(this.lat_ts) : this.k0 = ke(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) : this.k0 || (this.k ? this.k0 = this.k : this.k0 = 1);
}
function by(i) {
  var t = i.x, e = i.y;
  if (e * ze > 90 && e * ze < -90 && t * ze > 180 && t * ze < -180)
    return null;
  var n, s;
  if (Math.abs(Math.abs(e) - P) <= T)
    return null;
  if (this.sphere)
    n = this.x0 + this.a * this.k0 * A(t - this.long0), s = this.y0 + this.a * this.k0 * Math.log(Math.tan(lt + 0.5 * e));
  else {
    var r = Math.sin(e), o = _e(this.e, e, r);
    n = this.x0 + this.a * this.k0 * A(t - this.long0), s = this.y0 - this.a * this.k0 * Math.log(o);
  }
  return i.x = n, i.y = s, i;
}
function Py(i) {
  var t = i.x - this.x0, e = i.y - this.y0, n, s;
  if (this.sphere)
    s = P - 2 * Math.atan(Math.exp(-e / (this.a * this.k0)));
  else {
    var r = Math.exp(-e / (this.a * this.k0));
    if (s = Gs(this.e, r), s === -9999)
      return null;
  }
  return n = A(this.long0 + t / (this.a * this.k0)), i.x = n, i.y = s, i;
}
var Sy = ["Mercator", "Popular Visualisation Pseudo Mercator", "Mercator_1SP", "Mercator_Auxiliary_Sphere", "merc"];
const _y = {
  init: Ey,
  forward: by,
  inverse: Py,
  names: Sy
};
function Ry() {
}
function Bc(i) {
  return i;
}
var Ty = ["longlat", "identity"];
const Ly = {
  init: Ry,
  forward: Bc,
  inverse: Bc,
  names: Ty
};
var Oy = [_y, Ly], Ar = {}, no = [];
function pf(i, t) {
  var e = no.length;
  return i.names ? (no[e] = i, i.names.forEach(function(n) {
    Ar[n.toLowerCase()] = e;
  }), this) : (console.log(t), !0);
}
function Ay(i) {
  if (!i)
    return !1;
  var t = i.toLowerCase();
  if (typeof Ar[t] < "u" && no[Ar[t]])
    return no[Ar[t]];
}
function Iy() {
  Oy.forEach(pf);
}
const Ny = {
  start: Iy,
  add: pf,
  get: Ay
};
var U = {};
U.MERIT = {
  a: 6378137,
  rf: 298.257,
  ellipseName: "MERIT 1983"
};
U.SGS85 = {
  a: 6378136,
  rf: 298.257,
  ellipseName: "Soviet Geodetic System 85"
};
U.GRS80 = {
  a: 6378137,
  rf: 298.257222101,
  ellipseName: "GRS 1980(IUGG, 1980)"
};
U.IAU76 = {
  a: 6378140,
  rf: 298.257,
  ellipseName: "IAU 1976"
};
U.airy = {
  a: 6377563396e-3,
  b: 635625691e-2,
  ellipseName: "Airy 1830"
};
U.APL4 = {
  a: 6378137,
  rf: 298.25,
  ellipseName: "Appl. Physics. 1965"
};
U.NWL9D = {
  a: 6378145,
  rf: 298.25,
  ellipseName: "Naval Weapons Lab., 1965"
};
U.mod_airy = {
  a: 6377340189e-3,
  b: 6356034446e-3,
  ellipseName: "Modified Airy"
};
U.andrae = {
  a: 637710443e-2,
  rf: 300,
  ellipseName: "Andrae 1876 (Den., Iclnd.)"
};
U.aust_SA = {
  a: 6378160,
  rf: 298.25,
  ellipseName: "Australian Natl & S. Amer. 1969"
};
U.GRS67 = {
  a: 6378160,
  rf: 298.247167427,
  ellipseName: "GRS 67(IUGG 1967)"
};
U.bessel = {
  a: 6377397155e-3,
  rf: 299.1528128,
  ellipseName: "Bessel 1841"
};
U.bess_nam = {
  a: 6377483865e-3,
  rf: 299.1528128,
  ellipseName: "Bessel 1841 (Namibia)"
};
U.clrk66 = {
  a: 63782064e-1,
  b: 63565838e-1,
  ellipseName: "Clarke 1866"
};
U.clrk80 = {
  a: 6378249145e-3,
  rf: 293.4663,
  ellipseName: "Clarke 1880 mod."
};
U.clrk58 = {
  a: 6378293645208759e-9,
  rf: 294.2606763692654,
  ellipseName: "Clarke 1858"
};
U.CPM = {
  a: 63757387e-1,
  rf: 334.29,
  ellipseName: "Comm. des Poids et Mesures 1799"
};
U.delmbr = {
  a: 6376428,
  rf: 311.5,
  ellipseName: "Delambre 1810 (Belgium)"
};
U.engelis = {
  a: 637813605e-2,
  rf: 298.2566,
  ellipseName: "Engelis 1985"
};
U.evrst30 = {
  a: 6377276345e-3,
  rf: 300.8017,
  ellipseName: "Everest 1830"
};
U.evrst48 = {
  a: 6377304063e-3,
  rf: 300.8017,
  ellipseName: "Everest 1948"
};
U.evrst56 = {
  a: 6377301243e-3,
  rf: 300.8017,
  ellipseName: "Everest 1956"
};
U.evrst69 = {
  a: 6377295664e-3,
  rf: 300.8017,
  ellipseName: "Everest 1969"
};
U.evrstSS = {
  a: 6377298556e-3,
  rf: 300.8017,
  ellipseName: "Everest (Sabah & Sarawak)"
};
U.fschr60 = {
  a: 6378166,
  rf: 298.3,
  ellipseName: "Fischer (Mercury Datum) 1960"
};
U.fschr60m = {
  a: 6378155,
  rf: 298.3,
  ellipseName: "Fischer 1960"
};
U.fschr68 = {
  a: 6378150,
  rf: 298.3,
  ellipseName: "Fischer 1968"
};
U.helmert = {
  a: 6378200,
  rf: 298.3,
  ellipseName: "Helmert 1906"
};
U.hough = {
  a: 6378270,
  rf: 297,
  ellipseName: "Hough"
};
U.intl = {
  a: 6378388,
  rf: 297,
  ellipseName: "International 1909 (Hayford)"
};
U.kaula = {
  a: 6378163,
  rf: 298.24,
  ellipseName: "Kaula 1961"
};
U.lerch = {
  a: 6378139,
  rf: 298.257,
  ellipseName: "Lerch 1979"
};
U.mprts = {
  a: 6397300,
  rf: 191,
  ellipseName: "Maupertius 1738"
};
U.new_intl = {
  a: 63781575e-1,
  b: 63567722e-1,
  ellipseName: "New International 1967"
};
U.plessis = {
  a: 6376523,
  rf: 6355863,
  ellipseName: "Plessis 1817 (France)"
};
U.krass = {
  a: 6378245,
  rf: 298.3,
  ellipseName: "Krassovsky, 1942"
};
U.SEasia = {
  a: 6378155,
  b: 63567733205e-4,
  ellipseName: "Southeast Asia"
};
U.walbeck = {
  a: 6376896,
  b: 63558348467e-4,
  ellipseName: "Walbeck"
};
U.WGS60 = {
  a: 6378165,
  rf: 298.3,
  ellipseName: "WGS 60"
};
U.WGS66 = {
  a: 6378145,
  rf: 298.25,
  ellipseName: "WGS 66"
};
U.WGS7 = {
  a: 6378135,
  rf: 298.26,
  ellipseName: "WGS 72"
};
var zy = U.WGS84 = {
  a: 6378137,
  rf: 298.257223563,
  ellipseName: "WGS 84"
};
U.sphere = {
  a: 6370997,
  b: 6370997,
  ellipseName: "Normal Sphere (r=6370997)"
};
function Fy(i, t, e, n) {
  var s = i * i, r = t * t, o = (s - r) / s, a = 0;
  n ? (i *= 1 - o * (ny + o * (sy + o * ry)), s = i * i, o = 0) : a = Math.sqrt(o);
  var l = (s - r) / r;
  return {
    es: o,
    e: a,
    ep2: l
  };
}
function Dy(i, t, e, n, s) {
  if (!i) {
    var r = Li(U, n);
    r || (r = zy), i = r.a, t = r.b, e = r.rf;
  }
  return e && !t && (t = (1 - 1 / e) * i), (e === 0 || Math.abs(i - t) < T) && (s = !0, t = i), {
    a: i,
    b: t,
    rf: e,
    sphere: s
  };
}
var jt = {};
jt.wgs84 = {
  towgs84: "0,0,0",
  ellipse: "WGS84",
  datumName: "WGS84"
};
jt.ch1903 = {
  towgs84: "674.374,15.056,405.346",
  ellipse: "bessel",
  datumName: "swiss"
};
jt.ggrs87 = {
  towgs84: "-199.87,74.79,246.62",
  ellipse: "GRS80",
  datumName: "Greek_Geodetic_Reference_System_1987"
};
jt.nad83 = {
  towgs84: "0,0,0",
  ellipse: "GRS80",
  datumName: "North_American_Datum_1983"
};
jt.nad27 = {
  nadgrids: "@conus,@alaska,@ntv2_0.gsb,@ntv1_can.dat",
  ellipse: "clrk66",
  datumName: "North_American_Datum_1927"
};
jt.potsdam = {
  towgs84: "598.1,73.7,418.2,0.202,0.045,-2.455,6.7",
  ellipse: "bessel",
  datumName: "Potsdam Rauenberg 1950 DHDN"
};
jt.carthage = {
  towgs84: "-263.0,6.0,431.0",
  ellipse: "clark80",
  datumName: "Carthage 1934 Tunisia"
};
jt.hermannskogel = {
  towgs84: "577.326,90.129,463.919,5.137,1.474,5.297,2.4232",
  ellipse: "bessel",
  datumName: "Hermannskogel"
};
jt.osni52 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "airy",
  datumName: "Irish National"
};
jt.ire65 = {
  towgs84: "482.530,-130.596,564.557,-1.042,-0.214,-0.631,8.15",
  ellipse: "mod_airy",
  datumName: "Ireland 1965"
};
jt.rassadiran = {
  towgs84: "-133.63,-157.5,-158.62",
  ellipse: "intl",
  datumName: "Rassadiran"
};
jt.nzgd49 = {
  towgs84: "59.47,-5.04,187.44,0.47,-0.1,1.024,-4.5993",
  ellipse: "intl",
  datumName: "New Zealand Geodetic Datum 1949"
};
jt.osgb36 = {
  towgs84: "446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894",
  ellipse: "airy",
  datumName: "Airy 1830"
};
jt.s_jtsk = {
  towgs84: "589,76,480",
  ellipse: "bessel",
  datumName: "S-JTSK (Ferro)"
};
jt.beduaram = {
  towgs84: "-106,-87,188",
  ellipse: "clrk80",
  datumName: "Beduaram"
};
jt.gunung_segara = {
  towgs84: "-403,684,41",
  ellipse: "bessel",
  datumName: "Gunung Segara Jakarta"
};
jt.rnb72 = {
  towgs84: "106.869,-52.2978,103.724,-0.33657,0.456955,-1.84218,1",
  ellipse: "intl",
  datumName: "Reseau National Belge 1972"
};
function jy(i, t, e, n, s, r, o) {
  var a = {};
  return i === void 0 || i === "none" ? a.datum_type = Xa : a.datum_type = ey, t && (a.datum_params = t.map(parseFloat), (a.datum_params[0] !== 0 || a.datum_params[1] !== 0 || a.datum_params[2] !== 0) && (a.datum_type = en), a.datum_params.length > 3 && (a.datum_params[3] !== 0 || a.datum_params[4] !== 0 || a.datum_params[5] !== 0 || a.datum_params[6] !== 0) && (a.datum_type = nn, a.datum_params[3] *= ws, a.datum_params[4] *= ws, a.datum_params[5] *= ws, a.datum_params[6] = a.datum_params[6] / 1e6 + 1)), o && (a.datum_type = Or, a.grids = o), a.a = e, a.b = n, a.es = s, a.ep2 = r, a;
}
var vf = {};
function ky(i, t) {
  var e = new DataView(t), n = Hy(e), s = Zy(e, n);
  s.nSubgrids > 1 && console.log("Only single NTv2 subgrids are currently supported, subsequent sub grids are ignored");
  var r = By(e, s, n), o = { header: s, subgrids: r };
  return vf[i] = o, o;
}
function Xy(i) {
  if (i === void 0)
    return null;
  var t = i.split(",");
  return t.map(Gy);
}
function Gy(i) {
  if (i.length === 0)
    return null;
  var t = i[0] === "@";
  return t && (i = i.slice(1)), i === "null" ? { name: "null", mandatory: !t, grid: null, isNull: !0 } : {
    name: i,
    mandatory: !t,
    grid: vf[i] || null,
    isNull: !1
  };
}
function Rn(i) {
  return i / 3600 * Math.PI / 180;
}
function Hy(i) {
  var t = i.getInt32(8, !1);
  return t === 11 ? !1 : (t = i.getInt32(8, !0), t !== 11 && console.warn("Failed to detect nadgrid endian-ness, defaulting to little-endian"), !0);
}
function Zy(i, t) {
  return {
    nFields: i.getInt32(8, t),
    nSubgridFields: i.getInt32(24, t),
    nSubgrids: i.getInt32(40, t),
    shiftType: Ha(i, 56, 56 + 8).trim(),
    fromSemiMajorAxis: i.getFloat64(120, t),
    fromSemiMinorAxis: i.getFloat64(136, t),
    toSemiMajorAxis: i.getFloat64(152, t),
    toSemiMinorAxis: i.getFloat64(168, t)
  };
}
function Ha(i, t, e) {
  return String.fromCharCode.apply(null, new Uint8Array(i.buffer.slice(t, e)));
}
function By(i, t, e) {
  for (var n = 176, s = [], r = 0; r < t.nSubgrids; r++) {
    var o = Vy(i, n, e), a = Yy(i, n, o, e), l = Math.round(
      1 + (o.upperLongitude - o.lowerLongitude) / o.longitudeInterval
    ), h = Math.round(
      1 + (o.upperLatitude - o.lowerLatitude) / o.latitudeInterval
    );
    s.push({
      ll: [Rn(o.lowerLongitude), Rn(o.lowerLatitude)],
      del: [Rn(o.longitudeInterval), Rn(o.latitudeInterval)],
      lim: [l, h],
      count: o.gridNodeCount,
      cvs: Wy(a)
    });
  }
  return s;
}
function Wy(i) {
  return i.map(function(t) {
    return [Rn(t.longitudeShift), Rn(t.latitudeShift)];
  });
}
function Vy(i, t, e) {
  return {
    name: Ha(i, t + 8, t + 16).trim(),
    parent: Ha(i, t + 24, t + 24 + 8).trim(),
    lowerLatitude: i.getFloat64(t + 72, e),
    upperLatitude: i.getFloat64(t + 88, e),
    lowerLongitude: i.getFloat64(t + 104, e),
    upperLongitude: i.getFloat64(t + 120, e),
    latitudeInterval: i.getFloat64(t + 136, e),
    longitudeInterval: i.getFloat64(t + 152, e),
    gridNodeCount: i.getInt32(t + 168, e)
  };
}
function Yy(i, t, e, n) {
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
  var e = wy(i);
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
    var s = Li(jt, e.datumCode);
    s && (e.datum_params = e.datum_params || (s.towgs84 ? s.towgs84.split(",") : null), e.ellps = s.ellipse, e.datumName = s.datumName ? s.datumName : e.datumCode);
  }
  e.k0 = e.k0 || 1, e.axis = e.axis || "enu", e.ellps = e.ellps || "wgs84", e.lat1 = e.lat1 || e.lat0;
  var r = Dy(e.a, e.b, e.rf, e.ellps, e.sphere), o = Fy(r.a, r.b, r.rf, e.R_A), a = Xy(e.nadgrids), l = e.datum || jy(
    e.datumCode,
    e.datum_params,
    r.a,
    r.b,
    o.es,
    o.ep2,
    a
  );
  Zc(this, e), Zc(this, n), this.a = r.a, this.b = r.b, this.rf = r.rf, this.sphere = r.sphere, this.es = o.es, this.e = o.e, this.ep2 = o.ep2, this.datum = l, this.init(), t(null, this);
}
De.projections = Ny;
De.projections.start();
function Uy(i, t) {
  return i.datum_type !== t.datum_type || i.a !== t.a || Math.abs(i.es - t.es) > 5e-11 ? !1 : i.datum_type === en ? i.datum_params[0] === t.datum_params[0] && i.datum_params[1] === t.datum_params[1] && i.datum_params[2] === t.datum_params[2] : i.datum_type === nn ? i.datum_params[0] === t.datum_params[0] && i.datum_params[1] === t.datum_params[1] && i.datum_params[2] === t.datum_params[2] && i.datum_params[3] === t.datum_params[3] && i.datum_params[4] === t.datum_params[4] && i.datum_params[5] === t.datum_params[5] && i.datum_params[6] === t.datum_params[6] : !0;
}
function yf(i, t, e) {
  var n = i.x, s = i.y, r = i.z ? i.z : 0, o, a, l, h;
  if (s < -P && s > -1.001 * P)
    s = -P;
  else if (s > P && s < 1.001 * P)
    s = P;
  else {
    if (s < -P)
      return { x: -1 / 0, y: -1 / 0, z: i.z };
    if (s > P)
      return { x: 1 / 0, y: 1 / 0, z: i.z };
  }
  return n > Math.PI && (n -= 2 * Math.PI), a = Math.sin(s), h = Math.cos(s), l = a * a, o = e / Math.sqrt(1 - t * l), {
    x: (o + r) * h * Math.cos(n),
    y: (o + r) * h * Math.sin(n),
    z: (o * (1 - t) + r) * a
  };
}
function xf(i, t, e, n) {
  var s = 1e-12, r = s * s, o = 30, a, l, h, c, u, d, f, g, m, p, v, y, x, M = i.x, C = i.y, E = i.z ? i.z : 0, b, S, O;
  if (a = Math.sqrt(M * M + C * C), l = Math.sqrt(M * M + C * C + E * E), a / e < s) {
    if (b = 0, l / e < s)
      return S = P, O = -n, {
        x: i.x,
        y: i.y,
        z: i.z
      };
  } else
    b = Math.atan2(C, M);
  h = E / l, c = a / l, u = 1 / Math.sqrt(1 - t * (2 - t) * c * c), g = c * (1 - t) * u, m = h * u, x = 0;
  do
    x++, f = e / Math.sqrt(1 - t * m * m), O = a * g + E * m - f * (1 - t * m * m), d = t * f / (f + O), u = 1 / Math.sqrt(1 - d * (2 - d) * c * c), p = c * (1 - d) * u, v = h * u, y = v * g - p * m, g = p, m = v;
  while (y * y > r && x < o);
  return S = Math.atan(v / Math.abs(p)), {
    x: b,
    y: S,
    z: O
  };
}
function Jy(i, t, e) {
  if (t === en)
    return {
      x: i.x + e[0],
      y: i.y + e[1],
      z: i.z + e[2]
    };
  if (t === nn) {
    var n = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6];
    return {
      x: h * (i.x - l * i.y + a * i.z) + n,
      y: h * (l * i.x + i.y - o * i.z) + s,
      z: h * (-a * i.x + o * i.y + i.z) + r
    };
  }
}
function qy(i, t, e) {
  if (t === en)
    return {
      x: i.x - e[0],
      y: i.y - e[1],
      z: i.z - e[2]
    };
  if (t === nn) {
    var n = e[0], s = e[1], r = e[2], o = e[3], a = e[4], l = e[5], h = e[6], c = (i.x - n) / h, u = (i.y - s) / h, d = (i.z - r) / h;
    return {
      x: c + l * u - a * d,
      y: -l * c + u + o * d,
      z: a * c - o * u + d
    };
  }
}
function Rr(i) {
  return i === en || i === nn;
}
function Ky(i, t, e) {
  if (Uy(i, t) || i.datum_type === Xa || t.datum_type === Xa)
    return e;
  var n = i.a, s = i.es;
  if (i.datum_type === Or) {
    var r = Wc(i, !1, e);
    if (r !== 0)
      return;
    n = kc, s = Xc;
  }
  var o = t.a, a = t.b, l = t.es;
  if (t.datum_type === Or && (o = kc, a = iy, l = Xc), s === l && n === o && !Rr(i.datum_type) && !Rr(t.datum_type))
    return e;
  if (e = yf(e, s, n), Rr(i.datum_type) && (e = Jy(e, i.datum_type, i.datum_params)), Rr(t.datum_type) && (e = qy(e, t.datum_type, t.datum_params)), e = xf(e, l, o, a), t.datum_type === Or) {
    var h = Wc(t, !0, e);
    if (h !== 0)
      return;
  }
  return e;
}
function Wc(i, t, e) {
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
    if (!(u > n.y || c > n.x || f < n.y || d < n.x) && (s = Qy(n, t, l), !isNaN(s.x)))
      break;
  }
  return isNaN(s.x) ? (console.log("Failed to find a grid shift table for location '" + -n.x * ze + " " + n.y * ze + " tried: '" + r + "'"), -1) : (e.x = -s.x, e.y = s.y, 0);
}
function Qy(i, t, e) {
  var n = { x: Number.NaN, y: Number.NaN };
  if (isNaN(i.x))
    return n;
  var s = { x: i.x, y: i.y };
  s.x -= e.ll[0], s.y -= e.ll[1], s.x = A(s.x - Math.PI) + Math.PI;
  var r = Vc(s, e);
  if (t) {
    if (isNaN(r.x))
      return n;
    r.x = s.x - r.x, r.y = s.y - r.y;
    var o = 9, a = 1e-12, l, h;
    do {
      if (h = Vc(r, e), isNaN(h.x)) {
        console.log("Inverse grid shift iteration failed, presumably at grid edge.  Using first approximation.");
        break;
      }
      l = { x: s.x - (h.x + r.x), y: s.y - (h.y + r.y) }, r.x += l.x, r.y += l.y;
    } while (o-- && Math.abs(l.x) > a && Math.abs(l.y) > a);
    if (o < 0)
      return console.log("Inverse grid shift iterator failed to converge."), n;
    n.x = A(r.x + e.ll[0]), n.y = r.y + e.ll[1];
  } else
    isNaN(r.x) || (n.x = i.x + r.x, n.y = i.y + r.y);
  return n;
}
function Vc(i, t) {
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
function Yc(i, t, e) {
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
function Mf(i) {
  var t = {
    x: i[0],
    y: i[1]
  };
  return i.length > 2 && (t.z = i[2]), i.length > 3 && (t.m = i[3]), t;
}
function $y(i) {
  Uc(i.x), Uc(i.y);
}
function Uc(i) {
  if (typeof Number.isFinite == "function") {
    if (Number.isFinite(i))
      return;
    throw new TypeError("coordinates must be finite numbers");
  }
  if (typeof i != "number" || i !== i || !isFinite(i))
    throw new TypeError("coordinates must be finite numbers");
}
function tx(i, t) {
  return (i.datum.datum_type === en || i.datum.datum_type === nn) && t.datumCode !== "WGS84" || (t.datum.datum_type === en || t.datum.datum_type === nn) && i.datumCode !== "WGS84";
}
function so(i, t, e, n) {
  var s;
  if (Array.isArray(e) && (e = Mf(e)), $y(e), i.datum && t.datum && tx(i, t) && (s = new De("WGS84"), e = so(i, s, e, n), i = s), n && i.axis !== "enu" && (e = Yc(i, !1, e)), i.projName === "longlat")
    e = {
      x: e.x * Xt,
      y: e.y * Xt,
      z: e.z || 0
    };
  else if (i.to_meter && (e = {
    x: e.x * i.to_meter,
    y: e.y * i.to_meter,
    z: e.z || 0
  }), e = i.inverse(e), !e)
    return;
  if (i.from_greenwich && (e.x += i.from_greenwich), e = Ky(i.datum, t.datum, e), !!e)
    return t.from_greenwich && (e = {
      x: e.x - t.from_greenwich,
      y: e.y,
      z: e.z || 0
    }), t.projName === "longlat" ? e = {
      x: e.x * ze,
      y: e.y * ze,
      z: e.z || 0
    } : (e = t.forward(e), t.to_meter && (e = {
      x: e.x / t.to_meter,
      y: e.y / t.to_meter,
      z: e.z || 0
    })), n && t.axis !== "enu" ? Yc(t, !0, e) : e;
}
var Jc = De("WGS84");
function ra(i, t, e, n) {
  var s, r, o;
  return Array.isArray(e) ? (s = so(i, t, e, n) || { x: NaN, y: NaN }, e.length > 2 ? typeof i.name < "u" && i.name === "geocent" || typeof t.name < "u" && t.name === "geocent" ? typeof s.z == "number" ? [s.x, s.y, s.z].concat(e.splice(3)) : [s.x, s.y, e[2]].concat(e.splice(3)) : [s.x, s.y].concat(e.splice(2)) : [s.x, s.y]) : (r = so(i, t, e, n), o = Object.keys(e), o.length === 2 || o.forEach(function(a) {
    if (typeof i.name < "u" && i.name === "geocent" || typeof t.name < "u" && t.name === "geocent") {
      if (a === "x" || a === "y" || a === "z")
        return;
    } else if (a === "x" || a === "y")
      return;
    r[a] = e[a];
  }), r);
}
function qc(i) {
  return i instanceof De ? i : i.oProj ? i.oProj : De(i);
}
function se(i, t, e) {
  i = qc(i);
  var n = !1, s;
  return typeof t > "u" ? (t = i, i = Jc, n = !0) : (typeof t.x < "u" || Array.isArray(t)) && (e = t, t = i, i = Jc, n = !0), t = qc(t), e ? ra(i, t, e) : (s = {
    forward: function(r, o) {
      return ra(i, t, r, o);
    },
    inverse: function(r, o) {
      return ra(t, i, r, o);
    }
  }, n && (s.oProj = t), s);
}
var Kc = 6, Cf = "AJSAJS", wf = "AFAFAF", Tn = 65, te = 73, xe = 79, ms = 86, ps = 90;
const ex = {
  forward: Ef,
  inverse: ix,
  toPoint: bf
};
function Ef(i, t) {
  return t = t || 5, rx(nx({
    lat: i[1],
    lon: i[0]
  }), t);
}
function ix(i) {
  var t = Vl(Sf(i.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat, t.lon, t.lat] : [t.left, t.bottom, t.right, t.top];
}
function bf(i) {
  var t = Vl(Sf(i.toUpperCase()));
  return t.lat && t.lon ? [t.lon, t.lat] : [(t.left + t.right) / 2, (t.top + t.bottom) / 2];
}
function oa(i) {
  return i * (Math.PI / 180);
}
function Qc(i) {
  return 180 * (i / Math.PI);
}
function nx(i) {
  var t = i.lat, e = i.lon, n = 6378137, s = 669438e-8, r = 0.9996, o, a, l, h, c, u, d, f = oa(t), g = oa(e), m, p;
  p = Math.floor((e + 180) / 6) + 1, e === 180 && (p = 60), t >= 56 && t < 64 && e >= 3 && e < 12 && (p = 32), t >= 72 && t < 84 && (e >= 0 && e < 9 ? p = 31 : e >= 9 && e < 21 ? p = 33 : e >= 21 && e < 33 ? p = 35 : e >= 33 && e < 42 && (p = 37)), o = (p - 1) * 6 - 180 + 3, m = oa(o), a = s / (1 - s), l = n / Math.sqrt(1 - s * Math.sin(f) * Math.sin(f)), h = Math.tan(f) * Math.tan(f), c = a * Math.cos(f) * Math.cos(f), u = Math.cos(f) * (g - m), d = n * ((1 - s / 4 - 3 * s * s / 64 - 5 * s * s * s / 256) * f - (3 * s / 8 + 3 * s * s / 32 + 45 * s * s * s / 1024) * Math.sin(2 * f) + (15 * s * s / 256 + 45 * s * s * s / 1024) * Math.sin(4 * f) - 35 * s * s * s / 3072 * Math.sin(6 * f));
  var v = r * l * (u + (1 - h + c) * u * u * u / 6 + (5 - 18 * h + h * h + 72 * c - 58 * a) * u * u * u * u * u / 120) + 5e5, y = r * (d + l * Math.tan(f) * (u * u / 2 + (5 - h + 9 * c + 4 * c * c) * u * u * u * u / 24 + (61 - 58 * h + h * h + 600 * c - 330 * a) * u * u * u * u * u * u / 720));
  return t < 0 && (y += 1e7), {
    northing: Math.round(y),
    easting: Math.round(v),
    zoneNumber: p,
    zoneLetter: sx(t)
  };
}
function Vl(i) {
  var t = i.northing, e = i.easting, n = i.zoneLetter, s = i.zoneNumber;
  if (s < 0 || s > 60)
    return null;
  var r = 0.9996, o = 6378137, a = 669438e-8, l, h = (1 - Math.sqrt(1 - a)) / (1 + Math.sqrt(1 - a)), c, u, d, f, g, m, p, v, y, x = e - 5e5, M = t;
  n < "N" && (M -= 1e7), p = (s - 1) * 6 - 180 + 3, l = a / (1 - a), m = M / r, v = m / (o * (1 - a / 4 - 3 * a * a / 64 - 5 * a * a * a / 256)), y = v + (3 * h / 2 - 27 * h * h * h / 32) * Math.sin(2 * v) + (21 * h * h / 16 - 55 * h * h * h * h / 32) * Math.sin(4 * v) + 151 * h * h * h / 96 * Math.sin(6 * v), c = o / Math.sqrt(1 - a * Math.sin(y) * Math.sin(y)), u = Math.tan(y) * Math.tan(y), d = l * Math.cos(y) * Math.cos(y), f = o * (1 - a) / Math.pow(1 - a * Math.sin(y) * Math.sin(y), 1.5), g = x / (c * r);
  var C = y - c * Math.tan(y) / f * (g * g / 2 - (5 + 3 * u + 10 * d - 4 * d * d - 9 * l) * g * g * g * g / 24 + (61 + 90 * u + 298 * d + 45 * u * u - 252 * l - 3 * d * d) * g * g * g * g * g * g / 720);
  C = Qc(C);
  var E = (g - (1 + 2 * u + d) * g * g * g / 6 + (5 - 2 * d + 28 * u - 3 * d * d + 8 * l + 24 * u * u) * g * g * g * g * g / 120) / Math.cos(y);
  E = p + Qc(E);
  var b;
  if (i.accuracy) {
    var S = Vl({
      northing: i.northing + i.accuracy,
      easting: i.easting + i.accuracy,
      zoneLetter: i.zoneLetter,
      zoneNumber: i.zoneNumber
    });
    b = {
      top: S.lat,
      right: S.lon,
      bottom: C,
      left: E
    };
  } else
    b = {
      lat: C,
      lon: E
    };
  return b;
}
function sx(i) {
  var t = "Z";
  return 84 >= i && i >= 72 ? t = "X" : 72 > i && i >= 64 ? t = "W" : 64 > i && i >= 56 ? t = "V" : 56 > i && i >= 48 ? t = "U" : 48 > i && i >= 40 ? t = "T" : 40 > i && i >= 32 ? t = "S" : 32 > i && i >= 24 ? t = "R" : 24 > i && i >= 16 ? t = "Q" : 16 > i && i >= 8 ? t = "P" : 8 > i && i >= 0 ? t = "N" : 0 > i && i >= -8 ? t = "M" : -8 > i && i >= -16 ? t = "L" : -16 > i && i >= -24 ? t = "K" : -24 > i && i >= -32 ? t = "J" : -32 > i && i >= -40 ? t = "H" : -40 > i && i >= -48 ? t = "G" : -48 > i && i >= -56 ? t = "F" : -56 > i && i >= -64 ? t = "E" : -64 > i && i >= -72 ? t = "D" : -72 > i && i >= -80 && (t = "C"), t;
}
function rx(i, t) {
  var e = "00000" + i.easting, n = "00000" + i.northing;
  return i.zoneNumber + i.zoneLetter + ox(i.easting, i.northing, i.zoneNumber) + e.substr(e.length - 5, t) + n.substr(n.length - 5, t);
}
function ox(i, t, e) {
  var n = Pf(e), s = Math.floor(i / 1e5), r = Math.floor(t / 1e5) % 20;
  return ax(s, r, n);
}
function Pf(i) {
  var t = i % Kc;
  return t === 0 && (t = Kc), t;
}
function ax(i, t, e) {
  var n = e - 1, s = Cf.charCodeAt(n), r = wf.charCodeAt(n), o = s + i - 1, a = r + t, l = !1;
  o > ps && (o = o - ps + Tn - 1, l = !0), (o === te || s < te && o > te || (o > te || s < te) && l) && o++, (o === xe || s < xe && o > xe || (o > xe || s < xe) && l) && (o++, o === te && o++), o > ps && (o = o - ps + Tn - 1), a > ms ? (a = a - ms + Tn - 1, l = !0) : l = !1, (a === te || r < te && a > te || (a > te || r < te) && l) && a++, (a === xe || r < xe && a > xe || (a > xe || r < xe) && l) && (a++, a === te && a++), a > ms && (a = a - ms + Tn - 1);
  var h = String.fromCharCode(o) + String.fromCharCode(a);
  return h;
}
function Sf(i) {
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
  for (var l = Pf(o), h = lx(e.charAt(0), l), c = hx(e.charAt(1), l); c < cx(a); )
    c += 2e6;
  var u = t - r;
  if (u % 2 !== 0)
    throw `MGRSPoint has to have an even number
of digits after the zone letter and two 100km letters - front
half for easting meters, second half for
northing meters` + i;
  var d = u / 2, f = 0, g = 0, m, p, v, y, x;
  return d > 0 && (m = 1e5 / Math.pow(10, d), p = i.substring(r, r + d), f = parseFloat(p) * m, v = i.substring(r + d), g = parseFloat(v) * m), y = f + h, x = g + c, {
    easting: y,
    northing: x,
    zoneLetter: a,
    zoneNumber: o,
    accuracy: m
  };
}
function lx(i, t) {
  for (var e = Cf.charCodeAt(t - 1), n = 1e5, s = !1; e !== i.charCodeAt(0); ) {
    if (e++, e === te && e++, e === xe && e++, e > ps) {
      if (s)
        throw "Bad character: " + i;
      e = Tn, s = !0;
    }
    n += 1e5;
  }
  return n;
}
function hx(i, t) {
  if (i > "V")
    throw "MGRSPoint given invalid Northing " + i;
  for (var e = wf.charCodeAt(t - 1), n = 0, s = !1; e !== i.charCodeAt(0); ) {
    if (e++, e === te && e++, e === xe && e++, e > ms) {
      if (s)
        throw "Bad character: " + i;
      e = Tn, s = !0;
    }
    n += 1e5;
  }
  return n;
}
function cx(i) {
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
function Yn(i, t, e) {
  if (!(this instanceof Yn))
    return new Yn(i, t, e);
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
Yn.fromMGRS = function(i) {
  return new Yn(bf(i));
};
Yn.prototype.toMGRS = function(i) {
  return Ef([this.x, this.y], i);
};
var ux = 1, dx = 0.25, $c = 0.046875, tu = 0.01953125, eu = 0.01068115234375, fx = 0.75, gx = 0.46875, mx = 0.013020833333333334, px = 0.007120768229166667, vx = 0.3645833333333333, yx = 0.005696614583333333, xx = 0.3076171875;
function _f(i) {
  var t = [];
  t[0] = ux - i * (dx + i * ($c + i * (tu + i * eu))), t[1] = i * (fx - i * ($c + i * (tu + i * eu)));
  var e = i * i;
  return t[2] = e * (gx - i * (mx + i * px)), e *= i, t[3] = e * (vx - i * yx), t[4] = e * i * xx, t;
}
function Ao(i, t, e, n) {
  return e *= t, t *= t, n[0] * i - e * (n[1] + t * (n[2] + t * (n[3] + t * n[4])));
}
var Mx = 20;
function Rf(i, t, e) {
  for (var n = 1 / (1 - t), s = i, r = Mx; r; --r) {
    var o = Math.sin(s), a = 1 - t * o * o;
    if (a = (Ao(s, o, Math.cos(s), e) - i) * (a * Math.sqrt(a)) * n, s -= a, Math.abs(a) < T)
      return s;
  }
  return s;
}
function Cx() {
  this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.es && (this.en = _f(this.es), this.ml0 = Ao(this.lat0, Math.sin(this.lat0), Math.cos(this.lat0), this.en));
}
function wx(i) {
  var t = i.x, e = i.y, n = A(t - this.long0), s, r, o, a = Math.sin(e), l = Math.cos(e);
  if (this.es) {
    var c = l * n, u = Math.pow(c, 2), d = this.ep2 * Math.pow(l, 2), f = Math.pow(d, 2), g = Math.abs(l) > T ? Math.tan(e) : 0, m = Math.pow(g, 2), p = Math.pow(m, 2);
    s = 1 - this.es * Math.pow(a, 2), c = c / Math.sqrt(s);
    var v = Ao(e, a, l, this.en);
    r = this.a * (this.k0 * c * (1 + u / 6 * (1 - m + d + u / 20 * (5 - 18 * m + p + 14 * d - 58 * m * d + u / 42 * (61 + 179 * p - p * m - 479 * m))))) + this.x0, o = this.a * (this.k0 * (v - this.ml0 + a * n * c / 2 * (1 + u / 12 * (5 - m + 9 * d + 4 * f + u / 30 * (61 + p - 58 * m + 270 * d - 330 * m * d + u / 56 * (1385 + 543 * p - p * m - 3111 * m)))))) + this.y0;
  } else {
    var h = l * Math.sin(n);
    if (Math.abs(Math.abs(h) - 1) < T)
      return 93;
    if (r = 0.5 * this.a * this.k0 * Math.log((1 + h) / (1 - h)) + this.x0, o = l * Math.cos(n) / Math.sqrt(1 - Math.pow(h, 2)), h = Math.abs(o), h >= 1) {
      if (h - 1 > T)
        return 93;
      o = 0;
    } else
      o = Math.acos(o);
    e < 0 && (o = -o), o = this.a * this.k0 * (o - this.lat0) + this.y0;
  }
  return i.x = r, i.y = o, i;
}
function Ex(i) {
  var t, e, n, s, r = (i.x - this.x0) * (1 / this.a), o = (i.y - this.y0) * (1 / this.a);
  if (this.es)
    if (t = this.ml0 + o / this.k0, e = Rf(t, this.es, this.en), Math.abs(e) < P) {
      var u = Math.sin(e), d = Math.cos(e), f = Math.abs(d) > T ? Math.tan(e) : 0, g = this.ep2 * Math.pow(d, 2), m = Math.pow(g, 2), p = Math.pow(f, 2), v = Math.pow(p, 2);
      t = 1 - this.es * Math.pow(u, 2);
      var y = r * Math.sqrt(t) / this.k0, x = Math.pow(y, 2);
      t = t * f, n = e - t * x / (1 - this.es) * 0.5 * (1 - x / 12 * (5 + 3 * p - 9 * g * p + g - 4 * m - x / 30 * (61 + 90 * p - 252 * g * p + 45 * v + 46 * g - x / 56 * (1385 + 3633 * p + 4095 * v + 1574 * v * p)))), s = A(this.long0 + y * (1 - x / 6 * (1 + 2 * p + g - x / 20 * (5 + 28 * p + 24 * v + 8 * g * p + 6 * g - x / 42 * (61 + 662 * p + 1320 * v + 720 * v * p)))) / d);
    } else
      n = P * tr(o), s = 0;
  else {
    var a = Math.exp(r / this.k0), l = 0.5 * (a - 1 / a), h = this.lat0 + o / this.k0, c = Math.cos(h);
    t = Math.sqrt((1 - Math.pow(c, 2)) / (1 + Math.pow(l, 2))), n = Math.asin(t), o < 0 && (n = -n), l === 0 && c === 0 ? s = 0 : s = A(Math.atan2(l, c) + this.long0);
  }
  return i.x = s, i.y = n, i;
}
var bx = ["Fast_Transverse_Mercator", "Fast Transverse Mercator"];
const Ir = {
  init: Cx,
  forward: wx,
  inverse: Ex,
  names: bx
};
function Tf(i) {
  var t = Math.exp(i);
  return t = (t - 1 / t) / 2, t;
}
function Pe(i, t) {
  i = Math.abs(i), t = Math.abs(t);
  var e = Math.max(i, t), n = Math.min(i, t) / (e || 1);
  return e * Math.sqrt(1 + Math.pow(n, 2));
}
function Px(i) {
  var t = 1 + i, e = t - 1;
  return e === 0 ? i : i * Math.log(t) / e;
}
function Sx(i) {
  var t = Math.abs(i);
  return t = Px(t * (1 + t / (Pe(1, t) + 1))), i < 0 ? -t : t;
}
function Yl(i, t) {
  for (var e = 2 * Math.cos(2 * t), n = i.length - 1, s = i[n], r = 0, o; --n >= 0; )
    o = -r + e * s + i[n], r = s, s = o;
  return t + o * Math.sin(2 * t);
}
function _x(i, t) {
  for (var e = 2 * Math.cos(t), n = i.length - 1, s = i[n], r = 0, o; --n >= 0; )
    o = -r + e * s + i[n], r = s, s = o;
  return Math.sin(t) * o;
}
function Rx(i) {
  var t = Math.exp(i);
  return t = (t + 1 / t) / 2, t;
}
function Lf(i, t, e) {
  for (var n = Math.sin(t), s = Math.cos(t), r = Tf(e), o = Rx(e), a = 2 * s * o, l = -2 * n * r, h = i.length - 1, c = i[h], u = 0, d = 0, f = 0, g, m; --h >= 0; )
    g = d, m = u, d = c, u = f, c = -g + a * d - l * u + i[h], f = -m + l * d + a * u;
  return a = n * o, l = s * r, [a * c - l * f, a * f + l * c];
}
function Tx() {
  if (!this.approx && (isNaN(this.es) || this.es <= 0))
    throw new Error('Incorrect elliptical usage. Try using the +approx option in the proj string, or PROJECTION["Fast_Transverse_Mercator"] in the WKT.');
  this.approx && (Ir.init.apply(this), this.forward = Ir.forward, this.inverse = Ir.inverse), this.x0 = this.x0 !== void 0 ? this.x0 : 0, this.y0 = this.y0 !== void 0 ? this.y0 : 0, this.long0 = this.long0 !== void 0 ? this.long0 : 0, this.lat0 = this.lat0 !== void 0 ? this.lat0 : 0, this.cgb = [], this.cbg = [], this.utg = [], this.gtu = [];
  var i = this.es / (1 + Math.sqrt(1 - this.es)), t = i / (2 - i), e = t;
  this.cgb[0] = t * (2 + t * (-2 / 3 + t * (-2 + t * (116 / 45 + t * (26 / 45 + t * (-2854 / 675)))))), this.cbg[0] = t * (-2 + t * (2 / 3 + t * (4 / 3 + t * (-82 / 45 + t * (32 / 45 + t * (4642 / 4725)))))), e = e * t, this.cgb[1] = e * (7 / 3 + t * (-8 / 5 + t * (-227 / 45 + t * (2704 / 315 + t * (2323 / 945))))), this.cbg[1] = e * (5 / 3 + t * (-16 / 15 + t * (-13 / 9 + t * (904 / 315 + t * (-1522 / 945))))), e = e * t, this.cgb[2] = e * (56 / 15 + t * (-136 / 35 + t * (-1262 / 105 + t * (73814 / 2835)))), this.cbg[2] = e * (-26 / 15 + t * (34 / 21 + t * (8 / 5 + t * (-12686 / 2835)))), e = e * t, this.cgb[3] = e * (4279 / 630 + t * (-332 / 35 + t * (-399572 / 14175))), this.cbg[3] = e * (1237 / 630 + t * (-12 / 5 + t * (-24832 / 14175))), e = e * t, this.cgb[4] = e * (4174 / 315 + t * (-144838 / 6237)), this.cbg[4] = e * (-734 / 315 + t * (109598 / 31185)), e = e * t, this.cgb[5] = e * (601676 / 22275), this.cbg[5] = e * (444337 / 155925), e = Math.pow(t, 2), this.Qn = this.k0 / (1 + t) * (1 + e * (1 / 4 + e * (1 / 64 + e / 256))), this.utg[0] = t * (-0.5 + t * (2 / 3 + t * (-37 / 96 + t * (1 / 360 + t * (81 / 512 + t * (-96199 / 604800)))))), this.gtu[0] = t * (0.5 + t * (-2 / 3 + t * (5 / 16 + t * (41 / 180 + t * (-127 / 288 + t * (7891 / 37800)))))), this.utg[1] = e * (-1 / 48 + t * (-1 / 15 + t * (437 / 1440 + t * (-46 / 105 + t * (1118711 / 3870720))))), this.gtu[1] = e * (13 / 48 + t * (-3 / 5 + t * (557 / 1440 + t * (281 / 630 + t * (-1983433 / 1935360))))), e = e * t, this.utg[2] = e * (-17 / 480 + t * (37 / 840 + t * (209 / 4480 + t * (-5569 / 90720)))), this.gtu[2] = e * (61 / 240 + t * (-103 / 140 + t * (15061 / 26880 + t * (167603 / 181440)))), e = e * t, this.utg[3] = e * (-4397 / 161280 + t * (11 / 504 + t * (830251 / 7257600))), this.gtu[3] = e * (49561 / 161280 + t * (-179 / 168 + t * (6601661 / 7257600))), e = e * t, this.utg[4] = e * (-4583 / 161280 + t * (108847 / 3991680)), this.gtu[4] = e * (34729 / 80640 + t * (-3418889 / 1995840)), e = e * t, this.utg[5] = e * (-20648693 / 638668800), this.gtu[5] = e * (212378941 / 319334400);
  var n = Yl(this.cbg, this.lat0);
  this.Zb = -this.Qn * (n + _x(this.gtu, 2 * n));
}
function Lx(i) {
  var t = A(i.x - this.long0), e = i.y;
  e = Yl(this.cbg, e);
  var n = Math.sin(e), s = Math.cos(e), r = Math.sin(t), o = Math.cos(t);
  e = Math.atan2(n, o * s), t = Math.atan2(r * s, Pe(n, s * o)), t = Sx(Math.tan(t));
  var a = Lf(this.gtu, 2 * e, 2 * t);
  e = e + a[0], t = t + a[1];
  var l, h;
  return Math.abs(t) <= 2.623395162778 ? (l = this.a * (this.Qn * t) + this.x0, h = this.a * (this.Qn * e + this.Zb) + this.y0) : (l = 1 / 0, h = 1 / 0), i.x = l, i.y = h, i;
}
function Ox(i) {
  var t = (i.x - this.x0) * (1 / this.a), e = (i.y - this.y0) * (1 / this.a);
  e = (e - this.Zb) / this.Qn, t = t / this.Qn;
  var n, s;
  if (Math.abs(t) <= 2.623395162778) {
    var r = Lf(this.utg, 2 * e, 2 * t);
    e = e + r[0], t = t + r[1], t = Math.atan(Tf(t));
    var o = Math.sin(e), a = Math.cos(e), l = Math.sin(t), h = Math.cos(t);
    e = Math.atan2(o * h, Pe(l, h * a)), t = Math.atan2(l, h * a), n = A(t + this.long0), s = Yl(this.cgb, e);
  } else
    n = 1 / 0, s = 1 / 0;
  return i.x = n, i.y = s, i;
}
var Ax = ["Extended_Transverse_Mercator", "Extended Transverse Mercator", "etmerc", "Transverse_Mercator", "Transverse Mercator", "tmerc"];
const Nr = {
  init: Tx,
  forward: Lx,
  inverse: Ox,
  names: Ax
};
function Ix(i, t) {
  if (i === void 0) {
    if (i = Math.floor((A(t) + Math.PI) * 30 / Math.PI) + 1, i < 0)
      return 0;
    if (i > 60)
      return 60;
  }
  return i;
}
var Nx = "etmerc";
function zx() {
  var i = Ix(this.zone, this.long0);
  if (i === void 0)
    throw new Error("unknown utm zone");
  this.lat0 = 0, this.long0 = (6 * Math.abs(i) - 183) * Xt, this.x0 = 5e5, this.y0 = this.utmSouth ? 1e7 : 0, this.k0 = 0.9996, Nr.init.apply(this), this.forward = Nr.forward, this.inverse = Nr.inverse;
}
var Fx = ["Universal Transverse Mercator System", "utm"];
const Dx = {
  init: zx,
  names: Fx,
  dependsOn: Nx
};
function Ul(i, t) {
  return Math.pow((1 - i) / (1 + i), t);
}
var jx = 20;
function kx() {
  var i = Math.sin(this.lat0), t = Math.cos(this.lat0);
  t *= t, this.rc = Math.sqrt(1 - this.es) / (1 - this.es * i * i), this.C = Math.sqrt(1 + this.es * t * t / (1 - this.es)), this.phic0 = Math.asin(i / this.C), this.ratexp = 0.5 * this.C * this.e, this.K = Math.tan(0.5 * this.phic0 + lt) / (Math.pow(Math.tan(0.5 * this.lat0 + lt), this.C) * Ul(this.e * i, this.ratexp));
}
function Xx(i) {
  var t = i.x, e = i.y;
  return i.y = 2 * Math.atan(this.K * Math.pow(Math.tan(0.5 * e + lt), this.C) * Ul(this.e * Math.sin(e), this.ratexp)) - P, i.x = this.C * t, i;
}
function Gx(i) {
  for (var t = 1e-14, e = i.x / this.C, n = i.y, s = Math.pow(Math.tan(0.5 * n + lt) / this.K, 1 / this.C), r = jx; r > 0 && (n = 2 * Math.atan(s * Ul(this.e * Math.sin(i.y), -0.5 * this.e)) - P, !(Math.abs(n - i.y) < t)); --r)
    i.y = n;
  return r ? (i.x = e, i.y = n, i) : null;
}
var Hx = ["gauss"];
const Jl = {
  init: kx,
  forward: Xx,
  inverse: Gx,
  names: Hx
};
function Zx() {
  Jl.init.apply(this), this.rc && (this.sinc0 = Math.sin(this.phic0), this.cosc0 = Math.cos(this.phic0), this.R2 = 2 * this.rc, this.title || (this.title = "Oblique Stereographic Alternative"));
}
function Bx(i) {
  var t, e, n, s;
  return i.x = A(i.x - this.long0), Jl.forward.apply(this, [i]), t = Math.sin(i.y), e = Math.cos(i.y), n = Math.cos(i.x), s = this.k0 * this.R2 / (1 + this.sinc0 * t + this.cosc0 * e * n), i.x = s * e * Math.sin(i.x), i.y = s * (this.cosc0 * t - this.sinc0 * e * n), i.x = this.a * i.x + this.x0, i.y = this.a * i.y + this.y0, i;
}
function Wx(i) {
  var t, e, n, s, r;
  if (i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, i.x /= this.k0, i.y /= this.k0, r = Math.sqrt(i.x * i.x + i.y * i.y)) {
    var o = 2 * Math.atan2(r, this.R2);
    t = Math.sin(o), e = Math.cos(o), s = Math.asin(e * this.sinc0 + i.y * t * this.cosc0 / r), n = Math.atan2(i.x * t, r * this.cosc0 * e - i.y * this.sinc0 * t);
  } else
    s = this.phic0, n = 0;
  return i.x = n, i.y = s, Jl.inverse.apply(this, [i]), i.x = A(i.x + this.long0), i;
}
var Vx = ["Stereographic_North_Pole", "Oblique_Stereographic", "Polar_Stereographic", "sterea", "Oblique Stereographic Alternative", "Double_Stereographic"];
const Yx = {
  init: Zx,
  forward: Bx,
  inverse: Wx,
  names: Vx
};
function Ux(i, t, e) {
  return t *= e, Math.tan(0.5 * (P + i)) * Math.pow((1 - t) / (1 + t), 0.5 * e);
}
function Jx() {
  this.coslat0 = Math.cos(this.lat0), this.sinlat0 = Math.sin(this.lat0), this.sphere ? this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= T && (this.k0 = 0.5 * (1 + tr(this.lat0) * Math.sin(this.lat_ts))) : (Math.abs(this.coslat0) <= T && (this.lat0 > 0 ? this.con = 1 : this.con = -1), this.cons = Math.sqrt(Math.pow(1 + this.e, 1 + this.e) * Math.pow(1 - this.e, 1 - this.e)), this.k0 === 1 && !isNaN(this.lat_ts) && Math.abs(this.coslat0) <= T && (this.k0 = 0.5 * this.cons * ke(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)) / _e(this.e, this.con * this.lat_ts, this.con * Math.sin(this.lat_ts))), this.ms1 = ke(this.e, this.sinlat0, this.coslat0), this.X0 = 2 * Math.atan(this.ssfn_(this.lat0, this.sinlat0, this.e)) - P, this.cosX0 = Math.cos(this.X0), this.sinX0 = Math.sin(this.X0));
}
function qx(i) {
  var t = i.x, e = i.y, n = Math.sin(e), s = Math.cos(e), r, o, a, l, h, c, u = A(t - this.long0);
  return Math.abs(Math.abs(t - this.long0) - Math.PI) <= T && Math.abs(e + this.lat0) <= T ? (i.x = NaN, i.y = NaN, i) : this.sphere ? (r = 2 * this.k0 / (1 + this.sinlat0 * n + this.coslat0 * s * Math.cos(u)), i.x = this.a * r * s * Math.sin(u) + this.x0, i.y = this.a * r * (this.coslat0 * n - this.sinlat0 * s * Math.cos(u)) + this.y0, i) : (o = 2 * Math.atan(this.ssfn_(e, n, this.e)) - P, l = Math.cos(o), a = Math.sin(o), Math.abs(this.coslat0) <= T ? (h = _e(this.e, e * this.con, this.con * n), c = 2 * this.a * this.k0 * h / this.cons, i.x = this.x0 + c * Math.sin(t - this.long0), i.y = this.y0 - this.con * c * Math.cos(t - this.long0), i) : (Math.abs(this.sinlat0) < T ? (r = 2 * this.a * this.k0 / (1 + l * Math.cos(u)), i.y = r * a) : (r = 2 * this.a * this.k0 * this.ms1 / (this.cosX0 * (1 + this.sinX0 * a + this.cosX0 * l * Math.cos(u))), i.y = r * (this.cosX0 * a - this.sinX0 * l * Math.cos(u)) + this.y0), i.x = r * l * Math.sin(u) + this.x0, i));
}
function Kx(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e, n, s, r, o = Math.sqrt(i.x * i.x + i.y * i.y);
  if (this.sphere) {
    var a = 2 * Math.atan(o / (2 * this.a * this.k0));
    return t = this.long0, e = this.lat0, o <= T ? (i.x = t, i.y = e, i) : (e = Math.asin(Math.cos(a) * this.sinlat0 + i.y * Math.sin(a) * this.coslat0 / o), Math.abs(this.coslat0) < T ? this.lat0 > 0 ? t = A(this.long0 + Math.atan2(i.x, -1 * i.y)) : t = A(this.long0 + Math.atan2(i.x, i.y)) : t = A(this.long0 + Math.atan2(i.x * Math.sin(a), o * this.coslat0 * Math.cos(a) - i.y * this.sinlat0 * Math.sin(a))), i.x = t, i.y = e, i);
  } else if (Math.abs(this.coslat0) <= T) {
    if (o <= T)
      return e = this.lat0, t = this.long0, i.x = t, i.y = e, i;
    i.x *= this.con, i.y *= this.con, n = o * this.cons / (2 * this.a * this.k0), e = this.con * Gs(this.e, n), t = this.con * A(this.con * this.long0 + Math.atan2(i.x, -1 * i.y));
  } else
    s = 2 * Math.atan(o * this.cosX0 / (2 * this.a * this.k0 * this.ms1)), t = this.long0, o <= T ? r = this.X0 : (r = Math.asin(Math.cos(s) * this.sinX0 + i.y * Math.sin(s) * this.cosX0 / o), t = A(this.long0 + Math.atan2(i.x * Math.sin(s), o * this.cosX0 * Math.cos(s) - i.y * this.sinX0 * Math.sin(s)))), e = -1 * Gs(this.e, Math.tan(0.5 * (P + r)));
  return i.x = t, i.y = e, i;
}
var Qx = ["stere", "Stereographic_South_Pole", "Polar Stereographic (variant B)"];
const $x = {
  init: Jx,
  forward: qx,
  inverse: Kx,
  names: Qx,
  ssfn_: Ux
};
function t9() {
  var i = this.lat0;
  this.lambda0 = this.long0;
  var t = Math.sin(i), e = this.a, n = this.rf, s = 1 / n, r = 2 * s - Math.pow(s, 2), o = this.e = Math.sqrt(r);
  this.R = this.k0 * e * Math.sqrt(1 - r) / (1 - r * Math.pow(t, 2)), this.alpha = Math.sqrt(1 + r / (1 - r) * Math.pow(Math.cos(i), 4)), this.b0 = Math.asin(t / this.alpha);
  var a = Math.log(Math.tan(Math.PI / 4 + this.b0 / 2)), l = Math.log(Math.tan(Math.PI / 4 + i / 2)), h = Math.log((1 + o * t) / (1 - o * t));
  this.K = a - this.alpha * l + this.alpha * o / 2 * h;
}
function e9(i) {
  var t = Math.log(Math.tan(Math.PI / 4 - i.y / 2)), e = this.e / 2 * Math.log((1 + this.e * Math.sin(i.y)) / (1 - this.e * Math.sin(i.y))), n = -this.alpha * (t + e) + this.K, s = 2 * (Math.atan(Math.exp(n)) - Math.PI / 4), r = this.alpha * (i.x - this.lambda0), o = Math.atan(Math.sin(r) / (Math.sin(this.b0) * Math.tan(s) + Math.cos(this.b0) * Math.cos(r))), a = Math.asin(Math.cos(this.b0) * Math.sin(s) - Math.sin(this.b0) * Math.cos(s) * Math.cos(r));
  return i.y = this.R / 2 * Math.log((1 + Math.sin(a)) / (1 - Math.sin(a))) + this.y0, i.x = this.R * o + this.x0, i;
}
function i9(i) {
  for (var t = i.x - this.x0, e = i.y - this.y0, n = t / this.R, s = 2 * (Math.atan(Math.exp(e / this.R)) - Math.PI / 4), r = Math.asin(Math.cos(this.b0) * Math.sin(s) + Math.sin(this.b0) * Math.cos(s) * Math.cos(n)), o = Math.atan(Math.sin(n) / (Math.cos(this.b0) * Math.cos(n) - Math.sin(this.b0) * Math.tan(s))), a = this.lambda0 + o / this.alpha, l = 0, h = r, c = -1e3, u = 0; Math.abs(h - c) > 1e-7; ) {
    if (++u > 20)
      return;
    l = 1 / this.alpha * (Math.log(Math.tan(Math.PI / 4 + r / 2)) - this.K) + this.e * Math.log(Math.tan(Math.PI / 4 + Math.asin(this.e * Math.sin(h)) / 2)), c = h, h = 2 * Math.atan(Math.exp(l)) - Math.PI / 2;
  }
  return i.x = a, i.y = h, i;
}
var n9 = ["somerc"];
const s9 = {
  init: t9,
  forward: e9,
  inverse: i9,
  names: n9
};
var bn = 1e-7;
function r9(i) {
  var t = ["Hotine_Oblique_Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin"], e = typeof i.PROJECTION == "object" ? Object.keys(i.PROJECTION)[0] : i.PROJECTION;
  return "no_uoff" in i || "no_off" in i || t.indexOf(e) !== -1;
}
function o9() {
  var i, t, e, n, s, r, o, a, l, h, c = 0, u, d = 0, f = 0, g = 0, m = 0, p = 0, v = 0;
  this.no_off = r9(this), this.no_rot = "no_rot" in this;
  var y = !1;
  "alpha" in this && (y = !0);
  var x = !1;
  if ("rectified_grid_angle" in this && (x = !0), y && (v = this.alpha), x && (c = this.rectified_grid_angle * Xt), y || x)
    d = this.longc;
  else if (f = this.long1, m = this.lat1, g = this.long2, p = this.lat2, Math.abs(m - p) <= bn || (i = Math.abs(m)) <= bn || Math.abs(i - P) <= bn || Math.abs(Math.abs(this.lat0) - P) <= bn || Math.abs(Math.abs(p) - P) <= bn)
    throw new Error();
  var M = 1 - this.es;
  t = Math.sqrt(M), Math.abs(this.lat0) > T ? (a = Math.sin(this.lat0), e = Math.cos(this.lat0), i = 1 - this.es * a * a, this.B = e * e, this.B = Math.sqrt(1 + this.es * this.B * this.B / M), this.A = this.B * this.k0 * t / i, n = this.B * t / (e * Math.sqrt(i)), s = n * n - 1, s <= 0 ? s = 0 : (s = Math.sqrt(s), this.lat0 < 0 && (s = -s)), this.E = s += n, this.E *= Math.pow(_e(this.e, this.lat0, a), this.B)) : (this.B = 1 / t, this.A = this.k0, this.E = n = s = 1), y || x ? (y ? (u = Math.asin(Math.sin(v) / n), x || (c = v)) : (u = c, v = Math.asin(n * Math.sin(u))), this.lam0 = d - Math.asin(0.5 * (s - 1 / s) * Math.tan(u)) / this.B) : (r = Math.pow(_e(this.e, m, Math.sin(m)), this.B), o = Math.pow(_e(this.e, p, Math.sin(p)), this.B), s = this.E / r, l = (o - r) / (o + r), h = this.E * this.E, h = (h - o * r) / (h + o * r), i = f - g, i < -Math.pi ? g -= ks : i > Math.pi && (g += ks), this.lam0 = A(0.5 * (f + g) - Math.atan(h * Math.tan(0.5 * this.B * (f - g)) / l) / this.B), u = Math.atan(2 * Math.sin(this.B * A(f - this.lam0)) / (s - 1 / s)), c = v = Math.asin(n * Math.sin(u))), this.singam = Math.sin(u), this.cosgam = Math.cos(u), this.sinrot = Math.sin(c), this.cosrot = Math.cos(c), this.rB = 1 / this.B, this.ArB = this.A * this.rB, this.BrA = 1 / this.ArB, this.A * this.B, this.no_off ? this.u_0 = 0 : (this.u_0 = Math.abs(this.ArB * Math.atan(Math.sqrt(n * n - 1) / Math.cos(v))), this.lat0 < 0 && (this.u_0 = -this.u_0)), s = 0.5 * u, this.v_pole_n = this.ArB * Math.log(Math.tan(lt - s)), this.v_pole_s = this.ArB * Math.log(Math.tan(lt + s));
}
function a9(i) {
  var t = {}, e, n, s, r, o, a, l, h;
  if (i.x = i.x - this.lam0, Math.abs(Math.abs(i.y) - P) > T) {
    if (o = this.E / Math.pow(_e(this.e, i.y, Math.sin(i.y)), this.B), a = 1 / o, e = 0.5 * (o - a), n = 0.5 * (o + a), r = Math.sin(this.B * i.x), s = (e * this.singam - r * this.cosgam) / n, Math.abs(Math.abs(s) - 1) < T)
      throw new Error();
    h = 0.5 * this.ArB * Math.log((1 - s) / (1 + s)), a = Math.cos(this.B * i.x), Math.abs(a) < bn ? l = this.A * i.x : l = this.ArB * Math.atan2(e * this.cosgam + r * this.singam, a);
  } else
    h = i.y > 0 ? this.v_pole_n : this.v_pole_s, l = this.ArB * i.y;
  return this.no_rot ? (t.x = l, t.y = h) : (l -= this.u_0, t.x = h * this.cosrot + l * this.sinrot, t.y = l * this.cosrot - h * this.sinrot), t.x = this.a * t.x + this.x0, t.y = this.a * t.y + this.y0, t;
}
function l9(i) {
  var t, e, n, s, r, o, a, l = {};
  if (i.x = (i.x - this.x0) * (1 / this.a), i.y = (i.y - this.y0) * (1 / this.a), this.no_rot ? (e = i.y, t = i.x) : (e = i.x * this.cosrot - i.y * this.sinrot, t = i.y * this.cosrot + i.x * this.sinrot + this.u_0), n = Math.exp(-this.BrA * e), s = 0.5 * (n - 1 / n), r = 0.5 * (n + 1 / n), o = Math.sin(this.BrA * t), a = (o * this.cosgam + s * this.singam) / r, Math.abs(Math.abs(a) - 1) < T)
    l.x = 0, l.y = a < 0 ? -P : P;
  else {
    if (l.y = this.E / Math.sqrt((1 + a) / (1 - a)), l.y = Gs(this.e, Math.pow(l.y, 1 / this.B)), l.y === 1 / 0)
      throw new Error();
    l.x = -this.rB * Math.atan2(s * this.cosgam - o * this.singam, Math.cos(this.BrA * t));
  }
  return l.x += this.lam0, l;
}
var h9 = ["Hotine_Oblique_Mercator", "Hotine Oblique Mercator", "Hotine_Oblique_Mercator_Azimuth_Natural_Origin", "Hotine_Oblique_Mercator_Two_Point_Natural_Origin", "Hotine_Oblique_Mercator_Azimuth_Center", "Oblique_Mercator", "omerc"];
const c9 = {
  init: o9,
  forward: a9,
  inverse: l9,
  names: h9
};
function u9() {
  if (this.lat2 || (this.lat2 = this.lat1), this.k0 || (this.k0 = 1), this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, !(Math.abs(this.lat1 + this.lat2) < T)) {
    var i = this.b / this.a;
    this.e = Math.sqrt(1 - i * i);
    var t = Math.sin(this.lat1), e = Math.cos(this.lat1), n = ke(this.e, t, e), s = _e(this.e, this.lat1, t), r = Math.sin(this.lat2), o = Math.cos(this.lat2), a = ke(this.e, r, o), l = _e(this.e, this.lat2, r), h = _e(this.e, this.lat0, Math.sin(this.lat0));
    Math.abs(this.lat1 - this.lat2) > T ? this.ns = Math.log(n / a) / Math.log(s / l) : this.ns = t, isNaN(this.ns) && (this.ns = t), this.f0 = n / (this.ns * Math.pow(s, this.ns)), this.rh = this.a * this.f0 * Math.pow(h, this.ns), this.title || (this.title = "Lambert Conformal Conic");
  }
}
function d9(i) {
  var t = i.x, e = i.y;
  Math.abs(2 * Math.abs(e) - Math.PI) <= T && (e = tr(e) * (P - 2 * T));
  var n = Math.abs(Math.abs(e) - P), s, r;
  if (n > T)
    s = _e(this.e, e, Math.sin(e)), r = this.a * this.f0 * Math.pow(s, this.ns);
  else {
    if (n = e * this.ns, n <= 0)
      return null;
    r = 0;
  }
  var o = this.ns * A(t - this.long0);
  return i.x = this.k0 * (r * Math.sin(o)) + this.x0, i.y = this.k0 * (this.rh - r * Math.cos(o)) + this.y0, i;
}
function f9(i) {
  var t, e, n, s, r, o = (i.x - this.x0) / this.k0, a = this.rh - (i.y - this.y0) / this.k0;
  this.ns > 0 ? (t = Math.sqrt(o * o + a * a), e = 1) : (t = -Math.sqrt(o * o + a * a), e = -1);
  var l = 0;
  if (t !== 0 && (l = Math.atan2(e * o, e * a)), t !== 0 || this.ns > 0) {
    if (e = 1 / this.ns, n = Math.pow(t / (this.a * this.f0), e), s = Gs(this.e, n), s === -9999)
      return null;
  } else
    s = -P;
  return r = A(l / this.ns + this.long0), i.x = r, i.y = s, i;
}
var g9 = [
  "Lambert Tangential Conformal Conic Projection",
  "Lambert_Conformal_Conic",
  "Lambert_Conformal_Conic_1SP",
  "Lambert_Conformal_Conic_2SP",
  "lcc",
  "Lambert Conic Conformal (1SP)",
  "Lambert Conic Conformal (2SP)"
];
const m9 = {
  init: u9,
  forward: d9,
  inverse: f9,
  names: g9
};
function p9() {
  this.a = 6377397155e-3, this.es = 0.006674372230614, this.e = Math.sqrt(this.es), this.lat0 || (this.lat0 = 0.863937979737193), this.long0 || (this.long0 = 0.7417649320975901 - 0.308341501185665), this.k0 || (this.k0 = 0.9999), this.s45 = 0.785398163397448, this.s90 = 2 * this.s45, this.fi0 = this.lat0, this.e2 = this.es, this.e = Math.sqrt(this.e2), this.alfa = Math.sqrt(1 + this.e2 * Math.pow(Math.cos(this.fi0), 4) / (1 - this.e2)), this.uq = 1.04216856380474, this.u0 = Math.asin(Math.sin(this.fi0) / this.alfa), this.g = Math.pow((1 + this.e * Math.sin(this.fi0)) / (1 - this.e * Math.sin(this.fi0)), this.alfa * this.e / 2), this.k = Math.tan(this.u0 / 2 + this.s45) / Math.pow(Math.tan(this.fi0 / 2 + this.s45), this.alfa) * this.g, this.k1 = this.k0, this.n0 = this.a * Math.sqrt(1 - this.e2) / (1 - this.e2 * Math.pow(Math.sin(this.fi0), 2)), this.s0 = 1.37008346281555, this.n = Math.sin(this.s0), this.ro0 = this.k1 * this.n0 / Math.tan(this.s0), this.ad = this.s90 - this.uq;
}
function v9(i) {
  var t, e, n, s, r, o, a, l = i.x, h = i.y, c = A(l - this.long0);
  return t = Math.pow((1 + this.e * Math.sin(h)) / (1 - this.e * Math.sin(h)), this.alfa * this.e / 2), e = 2 * (Math.atan(this.k * Math.pow(Math.tan(h / 2 + this.s45), this.alfa) / t) - this.s45), n = -c * this.alfa, s = Math.asin(Math.cos(this.ad) * Math.sin(e) + Math.sin(this.ad) * Math.cos(e) * Math.cos(n)), r = Math.asin(Math.cos(e) * Math.sin(n) / Math.cos(s)), o = this.n * r, a = this.ro0 * Math.pow(Math.tan(this.s0 / 2 + this.s45), this.n) / Math.pow(Math.tan(s / 2 + this.s45), this.n), i.y = a * Math.cos(o) / 1, i.x = a * Math.sin(o) / 1, this.czech || (i.y *= -1, i.x *= -1), i;
}
function y9(i) {
  var t, e, n, s, r, o, a, l, h = i.x;
  i.x = i.y, i.y = h, this.czech || (i.y *= -1, i.x *= -1), o = Math.sqrt(i.x * i.x + i.y * i.y), r = Math.atan2(i.y, i.x), s = r / Math.sin(this.s0), n = 2 * (Math.atan(Math.pow(this.ro0 / o, 1 / this.n) * Math.tan(this.s0 / 2 + this.s45)) - this.s45), t = Math.asin(Math.cos(this.ad) * Math.sin(n) - Math.sin(this.ad) * Math.cos(n) * Math.cos(s)), e = Math.asin(Math.cos(n) * Math.sin(s) / Math.cos(t)), i.x = this.long0 - e / this.alfa, a = t, l = 0;
  var c = 0;
  do
    i.y = 2 * (Math.atan(Math.pow(this.k, -1 / this.alfa) * Math.pow(Math.tan(t / 2 + this.s45), 1 / this.alfa) * Math.pow((1 + this.e * Math.sin(a)) / (1 - this.e * Math.sin(a)), this.e / 2)) - this.s45), Math.abs(a - i.y) < 1e-10 && (l = 1), a = i.y, c += 1;
  while (l === 0 && c < 15);
  return c >= 15 ? null : i;
}
var x9 = ["Krovak", "krovak"];
const M9 = {
  init: p9,
  forward: v9,
  inverse: y9,
  names: x9
};
function Jt(i, t, e, n, s) {
  return i * s - t * Math.sin(2 * s) + e * Math.sin(4 * s) - n * Math.sin(6 * s);
}
function er(i) {
  return 1 - 0.25 * i * (1 + i / 16 * (3 + 1.25 * i));
}
function ir(i) {
  return 0.375 * i * (1 + 0.25 * i * (1 + 0.46875 * i));
}
function nr(i) {
  return 0.05859375 * i * i * (1 + 0.75 * i);
}
function sr(i) {
  return i * i * i * (35 / 3072);
}
function Un(i, t, e) {
  var n = t * e;
  return i / Math.sqrt(1 - n * n);
}
function ns(i) {
  return Math.abs(i) < P ? i : i - tr(i) * Math.PI;
}
function ro(i, t, e, n, s) {
  var r, o;
  r = i / t;
  for (var a = 0; a < 15; a++)
    if (o = (i - (t * r - e * Math.sin(2 * r) + n * Math.sin(4 * r) - s * Math.sin(6 * r))) / (t - 2 * e * Math.cos(2 * r) + 4 * n * Math.cos(4 * r) - 6 * s * Math.cos(6 * r)), r += o, Math.abs(o) <= 1e-10)
      return r;
  return NaN;
}
function C9() {
  this.sphere || (this.e0 = er(this.es), this.e1 = ir(this.es), this.e2 = nr(this.es), this.e3 = sr(this.es), this.ml0 = this.a * Jt(this.e0, this.e1, this.e2, this.e3, this.lat0));
}
function w9(i) {
  var t, e, n = i.x, s = i.y;
  if (n = A(n - this.long0), this.sphere)
    t = this.a * Math.asin(Math.cos(s) * Math.sin(n)), e = this.a * (Math.atan2(Math.tan(s), Math.cos(n)) - this.lat0);
  else {
    var r = Math.sin(s), o = Math.cos(s), a = Un(this.a, this.e, r), l = Math.tan(s) * Math.tan(s), h = n * Math.cos(s), c = h * h, u = this.es * o * o / (1 - this.es), d = this.a * Jt(this.e0, this.e1, this.e2, this.e3, s);
    t = a * h * (1 - c * l * (1 / 6 - (8 - l + 8 * u) * c / 120)), e = d - this.ml0 + a * r / o * c * (0.5 + (5 - l + 6 * u) * c / 24);
  }
  return i.x = t + this.x0, i.y = e + this.y0, i;
}
function E9(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = i.x / this.a, e = i.y / this.a, n, s;
  if (this.sphere) {
    var r = e + this.lat0;
    n = Math.asin(Math.sin(r) * Math.cos(t)), s = Math.atan2(Math.tan(t), Math.cos(r));
  } else {
    var o = this.ml0 / this.a + e, a = ro(o, this.e0, this.e1, this.e2, this.e3);
    if (Math.abs(Math.abs(a) - P) <= T)
      return i.x = this.long0, i.y = P, e < 0 && (i.y *= -1), i;
    var l = Un(this.a, this.e, Math.sin(a)), h = l * l * l / this.a / this.a * (1 - this.es), c = Math.pow(Math.tan(a), 2), u = t * this.a / l, d = u * u;
    n = a - l * Math.tan(a) / h * u * u * (0.5 - (1 + 3 * c) * u * u / 24), s = u * (1 - d * (c / 3 + (1 + 3 * c) * c * d / 15)) / Math.cos(a);
  }
  return i.x = A(s + this.long0), i.y = ns(n), i;
}
var b9 = ["Cassini", "Cassini_Soldner", "cass"];
const P9 = {
  init: C9,
  forward: w9,
  inverse: E9,
  names: b9
};
function bi(i, t) {
  var e;
  return i > 1e-7 ? (e = i * t, (1 - i * i) * (t / (1 - e * e) - 0.5 / i * Math.log((1 - e) / (1 + e)))) : 2 * t;
}
var S9 = 1, _9 = 2, R9 = 3, T9 = 4;
function L9() {
  var i = Math.abs(this.lat0);
  if (Math.abs(i - P) < T ? this.mode = this.lat0 < 0 ? this.S_POLE : this.N_POLE : Math.abs(i) < T ? this.mode = this.EQUIT : this.mode = this.OBLIQ, this.es > 0) {
    var t;
    switch (this.qp = bi(this.e, 1), this.mmf = 0.5 / (1 - this.es), this.apa = k9(this.es), this.mode) {
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
        this.rq = Math.sqrt(0.5 * this.qp), t = Math.sin(this.lat0), this.sinb1 = bi(this.e, t) / this.qp, this.cosb1 = Math.sqrt(1 - this.sinb1 * this.sinb1), this.dd = Math.cos(this.lat0) / (Math.sqrt(1 - this.es * t * t) * this.rq * this.cosb1), this.ymf = (this.xmf = this.rq) / this.dd, this.xmf *= this.dd;
        break;
    }
  } else
    this.mode === this.OBLIQ && (this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0));
}
function O9(i) {
  var t, e, n, s, r, o, a, l, h, c, u = i.x, d = i.y;
  if (u = A(u - this.long0), this.sphere) {
    if (r = Math.sin(d), c = Math.cos(d), n = Math.cos(u), this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (e = this.mode === this.EQUIT ? 1 + c * n : 1 + this.sinph0 * r + this.cosph0 * c * n, e <= T)
        return null;
      e = Math.sqrt(2 / e), t = e * c * Math.sin(u), e *= this.mode === this.EQUIT ? r : this.cosph0 * r - this.sinph0 * c * n;
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (n = -n), Math.abs(d + this.lat0) < T)
        return null;
      e = lt - d * 0.5, e = 2 * (this.mode === this.S_POLE ? Math.cos(e) : Math.sin(e)), t = e * Math.sin(u), e *= n;
    }
  } else {
    switch (a = 0, l = 0, h = 0, n = Math.cos(u), s = Math.sin(u), r = Math.sin(d), o = bi(this.e, r), (this.mode === this.OBLIQ || this.mode === this.EQUIT) && (a = o / this.qp, l = Math.sqrt(1 - a * a)), this.mode) {
      case this.OBLIQ:
        h = 1 + this.sinb1 * a + this.cosb1 * l * n;
        break;
      case this.EQUIT:
        h = 1 + l * n;
        break;
      case this.N_POLE:
        h = P + d, o = this.qp - o;
        break;
      case this.S_POLE:
        h = d - P, o = this.qp + o;
        break;
    }
    if (Math.abs(h) < T)
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
function A9(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = i.x / this.a, e = i.y / this.a, n, s, r, o, a, l, h;
  if (this.sphere) {
    var c = 0, u, d = 0;
    if (u = Math.sqrt(t * t + e * e), s = u * 0.5, s > 1)
      return null;
    switch (s = 2 * Math.asin(s), (this.mode === this.OBLIQ || this.mode === this.EQUIT) && (d = Math.sin(s), c = Math.cos(s)), this.mode) {
      case this.EQUIT:
        s = Math.abs(u) <= T ? 0 : Math.asin(e * d / u), t *= d, e = c * u;
        break;
      case this.OBLIQ:
        s = Math.abs(u) <= T ? this.lat0 : Math.asin(c * this.sinph0 + e * d * this.cosph0 / u), t *= d * this.cosph0, e = (c - Math.sin(s) * this.sinph0) * u;
        break;
      case this.N_POLE:
        e = -e, s = P - s;
        break;
      case this.S_POLE:
        s -= P;
        break;
    }
    n = e === 0 && (this.mode === this.EQUIT || this.mode === this.OBLIQ) ? 0 : Math.atan2(t, e);
  } else {
    if (h = 0, this.mode === this.OBLIQ || this.mode === this.EQUIT) {
      if (t /= this.dd, e *= this.dd, l = Math.sqrt(t * t + e * e), l < T)
        return i.x = this.long0, i.y = this.lat0, i;
      o = 2 * Math.asin(0.5 * l / this.rq), r = Math.cos(o), t *= o = Math.sin(o), this.mode === this.OBLIQ ? (h = r * this.sinb1 + e * o * this.cosb1 / l, a = this.qp * h, e = l * this.cosb1 * r - e * this.sinb1 * o) : (h = e * o / l, a = this.qp * h, e = l * r);
    } else if (this.mode === this.N_POLE || this.mode === this.S_POLE) {
      if (this.mode === this.N_POLE && (e = -e), a = t * t + e * e, !a)
        return i.x = this.long0, i.y = this.lat0, i;
      h = 1 - a / this.qp, this.mode === this.S_POLE && (h = -h);
    }
    n = Math.atan2(t, e), s = X9(Math.asin(h), this.apa);
  }
  return i.x = A(this.long0 + n), i.y = s, i;
}
var I9 = 0.3333333333333333, N9 = 0.17222222222222222, z9 = 0.10257936507936508, F9 = 0.06388888888888888, D9 = 0.0664021164021164, j9 = 0.016415012942191543;
function k9(i) {
  var t, e = [];
  return e[0] = i * I9, t = i * i, e[0] += t * N9, e[1] = t * F9, t *= i, e[0] += t * z9, e[1] += t * D9, e[2] = t * j9, e;
}
function X9(i, t) {
  var e = i + i;
  return i + t[0] * Math.sin(e) + t[1] * Math.sin(e + e) + t[2] * Math.sin(e + e + e);
}
var G9 = ["Lambert Azimuthal Equal Area", "Lambert_Azimuthal_Equal_Area", "laea"];
const H9 = {
  init: L9,
  forward: O9,
  inverse: A9,
  names: G9,
  S_POLE: S9,
  N_POLE: _9,
  EQUIT: R9,
  OBLIQ: T9
};
function Oi(i) {
  return Math.abs(i) > 1 && (i = i > 1 ? 1 : -1), Math.asin(i);
}
function Z9() {
  Math.abs(this.lat1 + this.lat2) < T || (this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e3 = Math.sqrt(this.es), this.sin_po = Math.sin(this.lat1), this.cos_po = Math.cos(this.lat1), this.t1 = this.sin_po, this.con = this.sin_po, this.ms1 = ke(this.e3, this.sin_po, this.cos_po), this.qs1 = bi(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat2), this.cos_po = Math.cos(this.lat2), this.t2 = this.sin_po, this.ms2 = ke(this.e3, this.sin_po, this.cos_po), this.qs2 = bi(this.e3, this.sin_po, this.cos_po), this.sin_po = Math.sin(this.lat0), this.cos_po = Math.cos(this.lat0), this.t3 = this.sin_po, this.qs0 = bi(this.e3, this.sin_po, this.cos_po), Math.abs(this.lat1 - this.lat2) > T ? this.ns0 = (this.ms1 * this.ms1 - this.ms2 * this.ms2) / (this.qs2 - this.qs1) : this.ns0 = this.con, this.c = this.ms1 * this.ms1 + this.ns0 * this.qs1, this.rh = this.a * Math.sqrt(this.c - this.ns0 * this.qs0) / this.ns0);
}
function B9(i) {
  var t = i.x, e = i.y;
  this.sin_phi = Math.sin(e), this.cos_phi = Math.cos(e);
  var n = bi(this.e3, this.sin_phi, this.cos_phi), s = this.a * Math.sqrt(this.c - this.ns0 * n) / this.ns0, r = this.ns0 * A(t - this.long0), o = s * Math.sin(r) + this.x0, a = this.rh - s * Math.cos(r) + this.y0;
  return i.x = o, i.y = a, i;
}
function W9(i) {
  var t, e, n, s, r, o;
  return i.x -= this.x0, i.y = this.rh - i.y + this.y0, this.ns0 >= 0 ? (t = Math.sqrt(i.x * i.x + i.y * i.y), n = 1) : (t = -Math.sqrt(i.x * i.x + i.y * i.y), n = -1), s = 0, t !== 0 && (s = Math.atan2(n * i.x, n * i.y)), n = t * this.ns0 / this.a, this.sphere ? o = Math.asin((this.c - n * n) / (2 * this.ns0)) : (e = (this.c - n * n) / this.ns0, o = this.phi1z(this.e3, e)), r = A(s / this.ns0 + this.long0), i.x = r, i.y = o, i;
}
function V9(i, t) {
  var e, n, s, r, o, a = Oi(0.5 * t);
  if (i < T)
    return a;
  for (var l = i * i, h = 1; h <= 25; h++)
    if (e = Math.sin(a), n = Math.cos(a), s = i * e, r = 1 - s * s, o = 0.5 * r * r / n * (t / (1 - l) - e / r + 0.5 / i * Math.log((1 - s) / (1 + s))), a = a + o, Math.abs(o) <= 1e-7)
      return a;
  return null;
}
var Y9 = ["Albers_Conic_Equal_Area", "Albers", "aea"];
const U9 = {
  init: Z9,
  forward: B9,
  inverse: W9,
  names: Y9,
  phi1z: V9
};
function J9() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0), this.infinity_dist = 1e3 * this.a, this.rc = 1;
}
function q9(i) {
  var t, e, n, s, r, o, a, l, h = i.x, c = i.y;
  return n = A(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(n), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, o > 0 || Math.abs(o) <= T ? (a = this.x0 + this.a * r * e * Math.sin(n) / o, l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s) / o) : (a = this.x0 + this.infinity_dist * e * Math.sin(n), l = this.y0 + this.infinity_dist * (this.cos_p14 * t - this.sin_p14 * e * s)), i.x = a, i.y = l, i;
}
function K9(i) {
  var t, e, n, s, r, o;
  return i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, i.x /= this.k0, i.y /= this.k0, (t = Math.sqrt(i.x * i.x + i.y * i.y)) ? (s = Math.atan2(t, this.rc), e = Math.sin(s), n = Math.cos(s), o = Oi(n * this.sin_p14 + i.y * e * this.cos_p14 / t), r = Math.atan2(i.x * e, t * this.cos_p14 * n - i.y * this.sin_p14 * e), r = A(this.long0 + r)) : (o = this.phic0, r = 0), i.x = r, i.y = o, i;
}
var Q9 = ["gnom"];
const $9 = {
  init: J9,
  forward: q9,
  inverse: K9,
  names: Q9
};
function t4(i, t) {
  var e = 1 - (1 - i * i) / (2 * i) * Math.log((1 - i) / (1 + i));
  if (Math.abs(Math.abs(t) - e) < 1e-6)
    return t < 0 ? -1 * P : P;
  for (var n = Math.asin(0.5 * t), s, r, o, a, l = 0; l < 30; l++)
    if (r = Math.sin(n), o = Math.cos(n), a = i * r, s = Math.pow(1 - a * a, 2) / (2 * o) * (t / (1 - i * i) - r / (1 - a * a) + 0.5 / i * Math.log((1 - a) / (1 + a))), n += s, Math.abs(s) <= 1e-10)
      return n;
  return NaN;
}
function e4() {
  this.sphere || (this.k0 = ke(this.e, Math.sin(this.lat_ts), Math.cos(this.lat_ts)));
}
function i4(i) {
  var t = i.x, e = i.y, n, s, r = A(t - this.long0);
  if (this.sphere)
    n = this.x0 + this.a * r * Math.cos(this.lat_ts), s = this.y0 + this.a * Math.sin(e) / Math.cos(this.lat_ts);
  else {
    var o = bi(this.e, Math.sin(e));
    n = this.x0 + this.a * this.k0 * r, s = this.y0 + this.a * o * 0.5 / this.k0;
  }
  return i.x = n, i.y = s, i;
}
function n4(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e;
  return this.sphere ? (t = A(this.long0 + i.x / this.a / Math.cos(this.lat_ts)), e = Math.asin(i.y / this.a * Math.cos(this.lat_ts))) : (e = t4(this.e, 2 * i.y * this.k0 / this.a), t = A(this.long0 + i.x / (this.a * this.k0))), i.x = t, i.y = e, i;
}
var s4 = ["cea"];
const r4 = {
  init: e4,
  forward: i4,
  inverse: n4,
  names: s4
};
function o4() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Equidistant Cylindrical (Plate Carre)", this.rc = Math.cos(this.lat_ts);
}
function a4(i) {
  var t = i.x, e = i.y, n = A(t - this.long0), s = ns(e - this.lat0);
  return i.x = this.x0 + this.a * n * this.rc, i.y = this.y0 + this.a * s, i;
}
function l4(i) {
  var t = i.x, e = i.y;
  return i.x = A(this.long0 + (t - this.x0) / (this.a * this.rc)), i.y = ns(this.lat0 + (e - this.y0) / this.a), i;
}
var h4 = ["Equirectangular", "Equidistant_Cylindrical", "eqc"];
const c4 = {
  init: o4,
  forward: a4,
  inverse: l4,
  names: h4
};
var iu = 20;
function u4() {
  this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = er(this.es), this.e1 = ir(this.es), this.e2 = nr(this.es), this.e3 = sr(this.es), this.ml0 = this.a * Jt(this.e0, this.e1, this.e2, this.e3, this.lat0);
}
function d4(i) {
  var t = i.x, e = i.y, n, s, r, o = A(t - this.long0);
  if (r = o * Math.sin(e), this.sphere)
    Math.abs(e) <= T ? (n = this.a * o, s = -1 * this.a * this.lat0) : (n = this.a * Math.sin(r) / Math.tan(e), s = this.a * (ns(e - this.lat0) + (1 - Math.cos(r)) / Math.tan(e)));
  else if (Math.abs(e) <= T)
    n = this.a * o, s = -1 * this.ml0;
  else {
    var a = Un(this.a, this.e, Math.sin(e)) / Math.tan(e);
    n = a * Math.sin(r), s = this.a * Jt(this.e0, this.e1, this.e2, this.e3, e) - this.ml0 + a * (1 - Math.cos(r));
  }
  return i.x = n + this.x0, i.y = s + this.y0, i;
}
function f4(i) {
  var t, e, n, s, r, o, a, l, h;
  if (n = i.x - this.x0, s = i.y - this.y0, this.sphere)
    if (Math.abs(s + this.a * this.lat0) <= T)
      t = A(n / this.a + this.long0), e = 0;
    else {
      o = this.lat0 + s / this.a, a = n * n / this.a / this.a + o * o, l = o;
      var c;
      for (r = iu; r; --r)
        if (c = Math.tan(l), h = -1 * (o * (l * c + 1) - l - 0.5 * (l * l + a) * c) / ((l - o) / c - 1), l += h, Math.abs(h) <= T) {
          e = l;
          break;
        }
      t = A(this.long0 + Math.asin(n * Math.tan(l) / this.a) / Math.sin(e));
    }
  else if (Math.abs(s + this.ml0) <= T)
    e = 0, t = A(this.long0 + n / this.a);
  else {
    o = (this.ml0 + s) / this.a, a = n * n / this.a / this.a + o * o, l = o;
    var u, d, f, g, m;
    for (r = iu; r; --r)
      if (m = this.e * Math.sin(l), u = Math.sqrt(1 - m * m) * Math.tan(l), d = this.a * Jt(this.e0, this.e1, this.e2, this.e3, l), f = this.e0 - 2 * this.e1 * Math.cos(2 * l) + 4 * this.e2 * Math.cos(4 * l) - 6 * this.e3 * Math.cos(6 * l), g = d / this.a, h = (o * (u * g + 1) - g - 0.5 * u * (g * g + a)) / (this.es * Math.sin(2 * l) * (g * g + a - 2 * o * g) / (4 * u) + (o - g) * (u * f - 2 / Math.sin(2 * l)) - f), l -= h, Math.abs(h) <= T) {
        e = l;
        break;
      }
    u = Math.sqrt(1 - this.es * Math.pow(Math.sin(e), 2)) * Math.tan(e), t = A(this.long0 + Math.asin(n * u / this.a) / Math.sin(e));
  }
  return i.x = t, i.y = e, i;
}
var g4 = ["Polyconic", "poly"];
const m4 = {
  init: u4,
  forward: d4,
  inverse: f4,
  names: g4
};
function p4() {
  this.A = [], this.A[1] = 0.6399175073, this.A[2] = -0.1358797613, this.A[3] = 0.063294409, this.A[4] = -0.02526853, this.A[5] = 0.0117879, this.A[6] = -55161e-7, this.A[7] = 26906e-7, this.A[8] = -1333e-6, this.A[9] = 67e-5, this.A[10] = -34e-5, this.B_re = [], this.B_im = [], this.B_re[1] = 0.7557853228, this.B_im[1] = 0, this.B_re[2] = 0.249204646, this.B_im[2] = 3371507e-9, this.B_re[3] = -1541739e-9, this.B_im[3] = 0.04105856, this.B_re[4] = -0.10162907, this.B_im[4] = 0.01727609, this.B_re[5] = -0.26623489, this.B_im[5] = -0.36249218, this.B_re[6] = -0.6870983, this.B_im[6] = -1.1651967, this.C_re = [], this.C_im = [], this.C_re[1] = 1.3231270439, this.C_im[1] = 0, this.C_re[2] = -0.577245789, this.C_im[2] = -7809598e-9, this.C_re[3] = 0.508307513, this.C_im[3] = -0.112208952, this.C_re[4] = -0.15094762, this.C_im[4] = 0.18200602, this.C_re[5] = 1.01418179, this.C_im[5] = 1.64497696, this.C_re[6] = 1.9660549, this.C_im[6] = 2.5127645, this.D = [], this.D[1] = 1.5627014243, this.D[2] = 0.5185406398, this.D[3] = -0.03333098, this.D[4] = -0.1052906, this.D[5] = -0.0368594, this.D[6] = 7317e-6, this.D[7] = 0.0122, this.D[8] = 394e-5, this.D[9] = -13e-4;
}
function v4(i) {
  var t, e = i.x, n = i.y, s = n - this.lat0, r = e - this.long0, o = s / ws * 1e-5, a = r, l = 1, h = 0;
  for (t = 1; t <= 10; t++)
    l = l * o, h = h + this.A[t] * l;
  var c = h, u = a, d = 1, f = 0, g, m, p = 0, v = 0;
  for (t = 1; t <= 6; t++)
    g = d * c - f * u, m = f * c + d * u, d = g, f = m, p = p + this.B_re[t] * d - this.B_im[t] * f, v = v + this.B_im[t] * d + this.B_re[t] * f;
  return i.x = v * this.a + this.x0, i.y = p * this.a + this.y0, i;
}
function y4(i) {
  var t, e = i.x, n = i.y, s = e - this.x0, r = n - this.y0, o = r / this.a, a = s / this.a, l = 1, h = 0, c, u, d = 0, f = 0;
  for (t = 1; t <= 6; t++)
    c = l * o - h * a, u = h * o + l * a, l = c, h = u, d = d + this.C_re[t] * l - this.C_im[t] * h, f = f + this.C_im[t] * l + this.C_re[t] * h;
  for (var g = 0; g < this.iterations; g++) {
    var m = d, p = f, v, y, x = o, M = a;
    for (t = 2; t <= 6; t++)
      v = m * d - p * f, y = p * d + m * f, m = v, p = y, x = x + (t - 1) * (this.B_re[t] * m - this.B_im[t] * p), M = M + (t - 1) * (this.B_im[t] * m + this.B_re[t] * p);
    m = 1, p = 0;
    var C = this.B_re[1], E = this.B_im[1];
    for (t = 2; t <= 6; t++)
      v = m * d - p * f, y = p * d + m * f, m = v, p = y, C = C + t * (this.B_re[t] * m - this.B_im[t] * p), E = E + t * (this.B_im[t] * m + this.B_re[t] * p);
    var b = C * C + E * E;
    d = (x * C + M * E) / b, f = (M * C - x * E) / b;
  }
  var S = d, O = f, D = 1, H = 0;
  for (t = 1; t <= 9; t++)
    D = D * S, H = H + this.D[t] * D;
  var R = this.lat0 + H * ws * 1e5, j = this.long0 + O;
  return i.x = j, i.y = R, i;
}
var x4 = ["New_Zealand_Map_Grid", "nzmg"];
const M4 = {
  init: p4,
  forward: v4,
  inverse: y4,
  names: x4
};
function C4() {
}
function w4(i) {
  var t = i.x, e = i.y, n = A(t - this.long0), s = this.x0 + this.a * n, r = this.y0 + this.a * Math.log(Math.tan(Math.PI / 4 + e / 2.5)) * 1.25;
  return i.x = s, i.y = r, i;
}
function E4(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t = A(this.long0 + i.x / this.a), e = 2.5 * (Math.atan(Math.exp(0.8 * i.y / this.a)) - Math.PI / 4);
  return i.x = t, i.y = e, i;
}
var b4 = ["Miller_Cylindrical", "mill"];
const P4 = {
  init: C4,
  forward: w4,
  inverse: E4,
  names: b4
};
var S4 = 20;
function _4() {
  this.sphere ? (this.n = 1, this.m = 0, this.es = 0, this.C_y = Math.sqrt((this.m + 1) / this.n), this.C_x = this.C_y / (this.m + 1)) : this.en = _f(this.es);
}
function R4(i) {
  var t, e, n = i.x, s = i.y;
  if (n = A(n - this.long0), this.sphere) {
    if (!this.m)
      s = this.n !== 1 ? Math.asin(this.n * Math.sin(s)) : s;
    else
      for (var r = this.n * Math.sin(s), o = S4; o; --o) {
        var a = (this.m * s + Math.sin(s) - r) / (this.m + Math.cos(s));
        if (s -= a, Math.abs(a) < T)
          break;
      }
    t = this.a * this.C_x * n * (this.m + Math.cos(s)), e = this.a * this.C_y * s;
  } else {
    var l = Math.sin(s), h = Math.cos(s);
    e = this.a * Ao(s, l, h, this.en), t = this.a * n * h / Math.sqrt(1 - this.es * l * l);
  }
  return i.x = t, i.y = e, i;
}
function T4(i) {
  var t, e, n, s;
  return i.x -= this.x0, n = i.x / this.a, i.y -= this.y0, t = i.y / this.a, this.sphere ? (t /= this.C_y, n = n / (this.C_x * (this.m + Math.cos(t))), this.m ? t = Oi((this.m * t + Math.sin(t)) / this.n) : this.n !== 1 && (t = Oi(Math.sin(t) / this.n)), n = A(n + this.long0), t = ns(t)) : (t = Rf(i.y / this.a, this.es, this.en), s = Math.abs(t), s < P ? (s = Math.sin(t), e = this.long0 + i.x * Math.sqrt(1 - this.es * s * s) / (this.a * Math.cos(t)), n = A(e)) : s - T < P && (n = this.long0)), i.x = n, i.y = t, i;
}
var L4 = ["Sinusoidal", "sinu"];
const O4 = {
  init: _4,
  forward: R4,
  inverse: T4,
  names: L4
};
function A4() {
}
function I4(i) {
  for (var t = i.x, e = i.y, n = A(t - this.long0), s = e, r = Math.PI * Math.sin(e); ; ) {
    var o = -(s + Math.sin(s) - r) / (1 + Math.cos(s));
    if (s += o, Math.abs(o) < T)
      break;
  }
  s /= 2, Math.PI / 2 - Math.abs(e) < T && (n = 0);
  var a = 0.900316316158 * this.a * n * Math.cos(s) + this.x0, l = 1.4142135623731 * this.a * Math.sin(s) + this.y0;
  return i.x = a, i.y = l, i;
}
function N4(i) {
  var t, e;
  i.x -= this.x0, i.y -= this.y0, e = i.y / (1.4142135623731 * this.a), Math.abs(e) > 0.999999999999 && (e = 0.999999999999), t = Math.asin(e);
  var n = A(this.long0 + i.x / (0.900316316158 * this.a * Math.cos(t)));
  n < -Math.PI && (n = -Math.PI), n > Math.PI && (n = Math.PI), e = (2 * t + Math.sin(2 * t)) / Math.PI, Math.abs(e) > 1 && (e = 1);
  var s = Math.asin(e);
  return i.x = n, i.y = s, i;
}
var z4 = ["Mollweide", "moll"];
const F4 = {
  init: A4,
  forward: I4,
  inverse: N4,
  names: z4
};
function D4() {
  Math.abs(this.lat1 + this.lat2) < T || (this.lat2 = this.lat2 || this.lat1, this.temp = this.b / this.a, this.es = 1 - Math.pow(this.temp, 2), this.e = Math.sqrt(this.es), this.e0 = er(this.es), this.e1 = ir(this.es), this.e2 = nr(this.es), this.e3 = sr(this.es), this.sinphi = Math.sin(this.lat1), this.cosphi = Math.cos(this.lat1), this.ms1 = ke(this.e, this.sinphi, this.cosphi), this.ml1 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat1), Math.abs(this.lat1 - this.lat2) < T ? this.ns = this.sinphi : (this.sinphi = Math.sin(this.lat2), this.cosphi = Math.cos(this.lat2), this.ms2 = ke(this.e, this.sinphi, this.cosphi), this.ml2 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat2), this.ns = (this.ms1 - this.ms2) / (this.ml2 - this.ml1)), this.g = this.ml1 + this.ms1 / this.ns, this.ml0 = Jt(this.e0, this.e1, this.e2, this.e3, this.lat0), this.rh = this.a * (this.g - this.ml0));
}
function j4(i) {
  var t = i.x, e = i.y, n;
  if (this.sphere)
    n = this.a * (this.g - e);
  else {
    var s = Jt(this.e0, this.e1, this.e2, this.e3, e);
    n = this.a * (this.g - s);
  }
  var r = this.ns * A(t - this.long0), o = this.x0 + n * Math.sin(r), a = this.y0 + this.rh - n * Math.cos(r);
  return i.x = o, i.y = a, i;
}
function k4(i) {
  i.x -= this.x0, i.y = this.rh - i.y + this.y0;
  var t, e, n, s;
  this.ns >= 0 ? (e = Math.sqrt(i.x * i.x + i.y * i.y), t = 1) : (e = -Math.sqrt(i.x * i.x + i.y * i.y), t = -1);
  var r = 0;
  if (e !== 0 && (r = Math.atan2(t * i.x, t * i.y)), this.sphere)
    return s = A(this.long0 + r / this.ns), n = ns(this.g - e / this.a), i.x = s, i.y = n, i;
  var o = this.g - e / this.a;
  return n = ro(o, this.e0, this.e1, this.e2, this.e3), s = A(this.long0 + r / this.ns), i.x = s, i.y = n, i;
}
var X4 = ["Equidistant_Conic", "eqdc"];
const G4 = {
  init: D4,
  forward: j4,
  inverse: k4,
  names: X4
};
function H4() {
  this.R = this.a;
}
function Z4(i) {
  var t = i.x, e = i.y, n = A(t - this.long0), s, r;
  Math.abs(e) <= T && (s = this.x0 + this.R * n, r = this.y0);
  var o = Oi(2 * Math.abs(e / Math.PI));
  (Math.abs(n) <= T || Math.abs(Math.abs(e) - P) <= T) && (s = this.x0, e >= 0 ? r = this.y0 + Math.PI * this.R * Math.tan(0.5 * o) : r = this.y0 + Math.PI * this.R * -Math.tan(0.5 * o));
  var a = 0.5 * Math.abs(Math.PI / n - n / Math.PI), l = a * a, h = Math.sin(o), c = Math.cos(o), u = c / (h + c - 1), d = u * u, f = u * (2 / h - 1), g = f * f, m = Math.PI * this.R * (a * (u - g) + Math.sqrt(l * (u - g) * (u - g) - (g + l) * (d - g))) / (g + l);
  n < 0 && (m = -m), s = this.x0 + m;
  var p = l + u;
  return m = Math.PI * this.R * (f * p - a * Math.sqrt((g + l) * (l + 1) - p * p)) / (g + l), e >= 0 ? r = this.y0 + m : r = this.y0 - m, i.x = s, i.y = r, i;
}
function B4(i) {
  var t, e, n, s, r, o, a, l, h, c, u, d, f;
  return i.x -= this.x0, i.y -= this.y0, u = Math.PI * this.R, n = i.x / u, s = i.y / u, r = n * n + s * s, o = -Math.abs(s) * (1 + r), a = o - 2 * s * s + n * n, l = -2 * o + 1 + 2 * s * s + r * r, f = s * s / l + (2 * a * a * a / l / l / l - 9 * o * a / l / l) / 27, h = (o - a * a / 3 / l) / l, c = 2 * Math.sqrt(-h / 3), u = 3 * f / h / c, Math.abs(u) > 1 && (u >= 0 ? u = 1 : u = -1), d = Math.acos(u) / 3, i.y >= 0 ? e = (-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI : e = -(-c * Math.cos(d + Math.PI / 3) - a / 3 / l) * Math.PI, Math.abs(n) < T ? t = this.long0 : t = A(this.long0 + Math.PI * (r - 1 + Math.sqrt(1 + 2 * (n * n - s * s) + r * r)) / 2 / n), i.x = t, i.y = e, i;
}
var W4 = ["Van_der_Grinten_I", "VanDerGrinten", "vandg"];
const V4 = {
  init: H4,
  forward: Z4,
  inverse: B4,
  names: W4
};
function Y4() {
  this.sin_p12 = Math.sin(this.lat0), this.cos_p12 = Math.cos(this.lat0);
}
function U4(i) {
  var t = i.x, e = i.y, n = Math.sin(i.y), s = Math.cos(i.y), r = A(t - this.long0), o, a, l, h, c, u, d, f, g, m, p, v, y, x, M, C, E, b, S, O, D, H, R;
  return this.sphere ? Math.abs(this.sin_p12 - 1) <= T ? (i.x = this.x0 + this.a * (P - e) * Math.sin(r), i.y = this.y0 - this.a * (P - e) * Math.cos(r), i) : Math.abs(this.sin_p12 + 1) <= T ? (i.x = this.x0 + this.a * (P + e) * Math.sin(r), i.y = this.y0 + this.a * (P + e) * Math.cos(r), i) : (b = this.sin_p12 * n + this.cos_p12 * s * Math.cos(r), C = Math.acos(b), E = C ? C / Math.sin(C) : 1, i.x = this.x0 + this.a * E * s * Math.sin(r), i.y = this.y0 + this.a * E * (this.cos_p12 * n - this.sin_p12 * s * Math.cos(r)), i) : (o = er(this.es), a = ir(this.es), l = nr(this.es), h = sr(this.es), Math.abs(this.sin_p12 - 1) <= T ? (c = this.a * Jt(o, a, l, h, P), u = this.a * Jt(o, a, l, h, e), i.x = this.x0 + (c - u) * Math.sin(r), i.y = this.y0 - (c - u) * Math.cos(r), i) : Math.abs(this.sin_p12 + 1) <= T ? (c = this.a * Jt(o, a, l, h, P), u = this.a * Jt(o, a, l, h, e), i.x = this.x0 + (c + u) * Math.sin(r), i.y = this.y0 + (c + u) * Math.cos(r), i) : (d = n / s, f = Un(this.a, this.e, this.sin_p12), g = Un(this.a, this.e, n), m = Math.atan((1 - this.es) * d + this.es * f * this.sin_p12 / (g * s)), p = Math.atan2(Math.sin(r), this.cos_p12 * Math.tan(m) - this.sin_p12 * Math.cos(r)), p === 0 ? S = Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : Math.abs(Math.abs(p) - Math.PI) <= T ? S = -Math.asin(this.cos_p12 * Math.sin(m) - this.sin_p12 * Math.cos(m)) : S = Math.asin(Math.sin(r) * Math.cos(m) / Math.sin(p)), v = this.e * this.sin_p12 / Math.sqrt(1 - this.es), y = this.e * this.cos_p12 * Math.cos(p) / Math.sqrt(1 - this.es), x = v * y, M = y * y, O = S * S, D = O * S, H = D * S, R = H * S, C = f * S * (1 - O * M * (1 - M) / 6 + D / 8 * x * (1 - 2 * M) + H / 120 * (M * (4 - 7 * M) - 3 * v * v * (1 - 7 * M)) - R / 48 * x), i.x = this.x0 + C * Math.sin(p), i.y = this.y0 + C * Math.cos(p), i));
}
function J4(i) {
  i.x -= this.x0, i.y -= this.y0;
  var t, e, n, s, r, o, a, l, h, c, u, d, f, g, m, p, v, y, x, M, C, E, b, S;
  return this.sphere ? (t = Math.sqrt(i.x * i.x + i.y * i.y), t > 2 * P * this.a ? void 0 : (e = t / this.a, n = Math.sin(e), s = Math.cos(e), r = this.long0, Math.abs(t) <= T ? o = this.lat0 : (o = Oi(s * this.sin_p12 + i.y * n * this.cos_p12 / t), a = Math.abs(this.lat0) - P, Math.abs(a) <= T ? this.lat0 >= 0 ? r = A(this.long0 + Math.atan2(i.x, -i.y)) : r = A(this.long0 - Math.atan2(-i.x, i.y)) : r = A(this.long0 + Math.atan2(i.x * n, t * this.cos_p12 * s - i.y * this.sin_p12 * n))), i.x = r, i.y = o, i)) : (l = er(this.es), h = ir(this.es), c = nr(this.es), u = sr(this.es), Math.abs(this.sin_p12 - 1) <= T ? (d = this.a * Jt(l, h, c, u, P), t = Math.sqrt(i.x * i.x + i.y * i.y), f = d - t, o = ro(f / this.a, l, h, c, u), r = A(this.long0 + Math.atan2(i.x, -1 * i.y)), i.x = r, i.y = o, i) : Math.abs(this.sin_p12 + 1) <= T ? (d = this.a * Jt(l, h, c, u, P), t = Math.sqrt(i.x * i.x + i.y * i.y), f = t - d, o = ro(f / this.a, l, h, c, u), r = A(this.long0 + Math.atan2(i.x, i.y)), i.x = r, i.y = o, i) : (t = Math.sqrt(i.x * i.x + i.y * i.y), p = Math.atan2(i.x, i.y), g = Un(this.a, this.e, this.sin_p12), v = Math.cos(p), y = this.e * this.cos_p12 * v, x = -y * y / (1 - this.es), M = 3 * this.es * (1 - x) * this.sin_p12 * this.cos_p12 * v / (1 - this.es), C = t / g, E = C - x * (1 + x) * Math.pow(C, 3) / 6 - M * (1 + 3 * x) * Math.pow(C, 4) / 24, b = 1 - x * E * E / 2 - C * E * E * E / 6, m = Math.asin(this.sin_p12 * Math.cos(E) + this.cos_p12 * Math.sin(E) * v), r = A(this.long0 + Math.asin(Math.sin(p) * Math.sin(E) / Math.cos(m))), S = Math.sin(m), o = Math.atan2((S - this.es * b * this.sin_p12) * Math.tan(m), S * (1 - this.es)), i.x = r, i.y = o, i));
}
var q4 = ["Azimuthal_Equidistant", "aeqd"];
const K4 = {
  init: Y4,
  forward: U4,
  inverse: J4,
  names: q4
};
function Q4() {
  this.sin_p14 = Math.sin(this.lat0), this.cos_p14 = Math.cos(this.lat0);
}
function $4(i) {
  var t, e, n, s, r, o, a, l, h = i.x, c = i.y;
  return n = A(h - this.long0), t = Math.sin(c), e = Math.cos(c), s = Math.cos(n), o = this.sin_p14 * t + this.cos_p14 * e * s, r = 1, (o > 0 || Math.abs(o) <= T) && (a = this.a * r * e * Math.sin(n), l = this.y0 + this.a * r * (this.cos_p14 * t - this.sin_p14 * e * s)), i.x = a, i.y = l, i;
}
function tM(i) {
  var t, e, n, s, r, o, a;
  return i.x -= this.x0, i.y -= this.y0, t = Math.sqrt(i.x * i.x + i.y * i.y), e = Oi(t / this.a), n = Math.sin(e), s = Math.cos(e), o = this.long0, Math.abs(t) <= T ? (a = this.lat0, i.x = o, i.y = a, i) : (a = Oi(s * this.sin_p14 + i.y * n * this.cos_p14 / t), r = Math.abs(this.lat0) - P, Math.abs(r) <= T ? (this.lat0 >= 0 ? o = A(this.long0 + Math.atan2(i.x, -i.y)) : o = A(this.long0 - Math.atan2(-i.x, i.y)), i.x = o, i.y = a, i) : (o = A(this.long0 + Math.atan2(i.x * n, t * this.cos_p14 * s - i.y * this.sin_p14 * n)), i.x = o, i.y = a, i));
}
var eM = ["ortho"];
const iM = {
  init: Q4,
  forward: $4,
  inverse: tM,
  names: eM
};
var Mt = {
  FRONT: 1,
  RIGHT: 2,
  BACK: 3,
  LEFT: 4,
  TOP: 5,
  BOTTOM: 6
}, ht = {
  AREA_0: 1,
  AREA_1: 2,
  AREA_2: 3,
  AREA_3: 4
};
function nM() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.lat0 = this.lat0 || 0, this.long0 = this.long0 || 0, this.lat_ts = this.lat_ts || 0, this.title = this.title || "Quadrilateralized Spherical Cube", this.lat0 >= P - lt / 2 ? this.face = Mt.TOP : this.lat0 <= -(P - lt / 2) ? this.face = Mt.BOTTOM : Math.abs(this.long0) <= lt ? this.face = Mt.FRONT : Math.abs(this.long0) <= P + lt ? this.face = this.long0 > 0 ? Mt.RIGHT : Mt.LEFT : this.face = Mt.BACK, this.es !== 0 && (this.one_minus_f = 1 - (this.a - this.b) / this.a, this.one_minus_f_squared = this.one_minus_f * this.one_minus_f);
}
function sM(i) {
  var t = { x: 0, y: 0 }, e, n, s, r, o, a, l = { value: 0 };
  if (i.x -= this.long0, this.es !== 0 ? e = Math.atan(this.one_minus_f_squared * Math.tan(i.y)) : e = i.y, n = i.x, this.face === Mt.TOP)
    r = P - e, n >= lt && n <= P + lt ? (l.value = ht.AREA_0, s = n - P) : n > P + lt || n <= -(P + lt) ? (l.value = ht.AREA_1, s = n > 0 ? n - _t : n + _t) : n > -(P + lt) && n <= -lt ? (l.value = ht.AREA_2, s = n + P) : (l.value = ht.AREA_3, s = n);
  else if (this.face === Mt.BOTTOM)
    r = P + e, n >= lt && n <= P + lt ? (l.value = ht.AREA_0, s = -n + P) : n < lt && n >= -lt ? (l.value = ht.AREA_1, s = -n) : n < -lt && n >= -(P + lt) ? (l.value = ht.AREA_2, s = -n - P) : (l.value = ht.AREA_3, s = n > 0 ? -n + _t : -n - _t);
  else {
    var h, c, u, d, f, g, m;
    this.face === Mt.RIGHT ? n = Nn(n, +P) : this.face === Mt.BACK ? n = Nn(n, +_t) : this.face === Mt.LEFT && (n = Nn(n, -P)), d = Math.sin(e), f = Math.cos(e), g = Math.sin(n), m = Math.cos(n), h = f * m, c = f * g, u = d, this.face === Mt.FRONT ? (r = Math.acos(h), s = Tr(r, u, c, l)) : this.face === Mt.RIGHT ? (r = Math.acos(c), s = Tr(r, u, -h, l)) : this.face === Mt.BACK ? (r = Math.acos(-h), s = Tr(r, u, -c, l)) : this.face === Mt.LEFT ? (r = Math.acos(-c), s = Tr(r, u, h, l)) : (r = s = 0, l.value = ht.AREA_0);
  }
  return a = Math.atan(12 / _t * (s + Math.acos(Math.sin(s) * Math.cos(lt)) - P)), o = Math.sqrt((1 - Math.cos(r)) / (Math.cos(a) * Math.cos(a)) / (1 - Math.cos(Math.atan(1 / Math.cos(s))))), l.value === ht.AREA_1 ? a += P : l.value === ht.AREA_2 ? a += _t : l.value === ht.AREA_3 && (a += 1.5 * _t), t.x = o * Math.cos(a), t.y = o * Math.sin(a), t.x = t.x * this.a + this.x0, t.y = t.y * this.a + this.y0, i.x = t.x, i.y = t.y, i;
}
function rM(i) {
  var t = { lam: 0, phi: 0 }, e, n, s, r, o, a, l, h, c, u = { value: 0 };
  if (i.x = (i.x - this.x0) / this.a, i.y = (i.y - this.y0) / this.a, n = Math.atan(Math.sqrt(i.x * i.x + i.y * i.y)), e = Math.atan2(i.y, i.x), i.x >= 0 && i.x >= Math.abs(i.y) ? u.value = ht.AREA_0 : i.y >= 0 && i.y >= Math.abs(i.x) ? (u.value = ht.AREA_1, e -= P) : i.x < 0 && -i.x >= Math.abs(i.y) ? (u.value = ht.AREA_2, e = e < 0 ? e + _t : e - _t) : (u.value = ht.AREA_3, e += P), c = _t / 12 * Math.tan(e), o = Math.sin(c) / (Math.cos(c) - 1 / Math.sqrt(2)), a = Math.atan(o), s = Math.cos(e), r = Math.tan(n), l = 1 - s * s * r * r * (1 - Math.cos(Math.atan(1 / Math.cos(a)))), l < -1 ? l = -1 : l > 1 && (l = 1), this.face === Mt.TOP)
    h = Math.acos(l), t.phi = P - h, u.value === ht.AREA_0 ? t.lam = a + P : u.value === ht.AREA_1 ? t.lam = a < 0 ? a + _t : a - _t : u.value === ht.AREA_2 ? t.lam = a - P : t.lam = a;
  else if (this.face === Mt.BOTTOM)
    h = Math.acos(l), t.phi = h - P, u.value === ht.AREA_0 ? t.lam = -a + P : u.value === ht.AREA_1 ? t.lam = -a : u.value === ht.AREA_2 ? t.lam = -a - P : t.lam = a < 0 ? -a - _t : -a + _t;
  else {
    var d, f, g;
    d = l, c = d * d, c >= 1 ? g = 0 : g = Math.sqrt(1 - c) * Math.sin(a), c += g * g, c >= 1 ? f = 0 : f = Math.sqrt(1 - c), u.value === ht.AREA_1 ? (c = f, f = -g, g = c) : u.value === ht.AREA_2 ? (f = -f, g = -g) : u.value === ht.AREA_3 && (c = f, f = g, g = -c), this.face === Mt.RIGHT ? (c = d, d = -f, f = c) : this.face === Mt.BACK ? (d = -d, f = -f) : this.face === Mt.LEFT && (c = d, d = f, f = -c), t.phi = Math.acos(-g) - P, t.lam = Math.atan2(f, d), this.face === Mt.RIGHT ? t.lam = Nn(t.lam, -P) : this.face === Mt.BACK ? t.lam = Nn(t.lam, -_t) : this.face === Mt.LEFT && (t.lam = Nn(t.lam, +P));
  }
  if (this.es !== 0) {
    var m, p, v;
    m = t.phi < 0 ? 1 : 0, p = Math.tan(t.phi), v = this.b / Math.sqrt(p * p + this.one_minus_f_squared), t.phi = Math.atan(Math.sqrt(this.a * this.a - v * v) / (this.one_minus_f * v)), m && (t.phi = -t.phi);
  }
  return t.lam += this.long0, i.x = t.lam, i.y = t.phi, i;
}
function Tr(i, t, e, n) {
  var s;
  return i < T ? (n.value = ht.AREA_0, s = 0) : (s = Math.atan2(t, e), Math.abs(s) <= lt ? n.value = ht.AREA_0 : s > lt && s <= P + lt ? (n.value = ht.AREA_1, s -= P) : s > P + lt || s <= -(P + lt) ? (n.value = ht.AREA_2, s = s >= 0 ? s - _t : s + _t) : (n.value = ht.AREA_3, s += P)), s;
}
function Nn(i, t) {
  var e = i + t;
  return e < -_t ? e += ks : e > +_t && (e -= ks), e;
}
var oM = ["Quadrilateralized Spherical Cube", "Quadrilateralized_Spherical_Cube", "qsc"];
const aM = {
  init: nM,
  forward: sM,
  inverse: rM,
  names: oM
};
var Za = [
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
], vs = [
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
], Of = 0.8487, Af = 1.3523, If = ze / 5, lM = 1 / If, Ln = 18, oo = function(i, t) {
  return i[0] + t * (i[1] + t * (i[2] + t * i[3]));
}, hM = function(i, t) {
  return i[1] + t * (2 * i[2] + t * 3 * i[3]);
};
function cM(i, t, e, n) {
  for (var s = t; n; --n) {
    var r = i(s);
    if (s -= r, Math.abs(r) < e)
      break;
  }
  return s;
}
function uM() {
  this.x0 = this.x0 || 0, this.y0 = this.y0 || 0, this.long0 = this.long0 || 0, this.es = 0, this.title = this.title || "Robinson";
}
function dM(i) {
  var t = A(i.x - this.long0), e = Math.abs(i.y), n = Math.floor(e * If);
  n < 0 ? n = 0 : n >= Ln && (n = Ln - 1), e = ze * (e - lM * n);
  var s = {
    x: oo(Za[n], e) * t,
    y: oo(vs[n], e)
  };
  return i.y < 0 && (s.y = -s.y), s.x = s.x * this.a * Of + this.x0, s.y = s.y * this.a * Af + this.y0, s;
}
function fM(i) {
  var t = {
    x: (i.x - this.x0) / (this.a * Of),
    y: Math.abs(i.y - this.y0) / (this.a * Af)
  };
  if (t.y >= 1)
    t.x /= Za[Ln][0], t.y = i.y < 0 ? -P : P;
  else {
    var e = Math.floor(t.y * Ln);
    for (e < 0 ? e = 0 : e >= Ln && (e = Ln - 1); ; )
      if (vs[e][0] > t.y)
        --e;
      else if (vs[e + 1][0] <= t.y)
        ++e;
      else
        break;
    var n = vs[e], s = 5 * (t.y - n[0]) / (vs[e + 1][0] - n[0]);
    s = cM(function(r) {
      return (oo(n, r) - t.y) / hM(n, r);
    }, s, T, 100), t.x /= oo(Za[e], s), t.y = (5 * e + s) * Xt, i.y < 0 && (t.y = -t.y);
  }
  return t.x = A(t.x + this.long0), t;
}
var gM = ["Robinson", "robin"];
const mM = {
  init: uM,
  forward: dM,
  inverse: fM,
  names: gM
};
function pM() {
  this.name = "geocent";
}
function vM(i) {
  var t = yf(i, this.es, this.a);
  return t;
}
function yM(i) {
  var t = xf(i, this.es, this.a, this.b);
  return t;
}
var xM = ["Geocentric", "geocentric", "geocent", "Geocent"];
const MM = {
  init: pM,
  forward: vM,
  inverse: yM,
  names: xM
};
var Zt = {
  N_POLE: 0,
  S_POLE: 1,
  EQUIT: 2,
  OBLIQ: 3
}, ds = {
  h: { def: 1e5, num: !0 },
  azi: { def: 0, num: !0, degrees: !0 },
  tilt: { def: 0, num: !0, degrees: !0 },
  long0: { def: 0, num: !0 },
  lat0: { def: 0, num: !0 }
};
function CM() {
  if (Object.keys(ds).forEach(function(e) {
    if (typeof this[e] > "u")
      this[e] = ds[e].def;
    else {
      if (ds[e].num && isNaN(this[e]))
        throw new Error("Invalid parameter value, must be numeric " + e + " = " + this[e]);
      ds[e].num && (this[e] = parseFloat(this[e]));
    }
    ds[e].degrees && (this[e] = this[e] * Xt);
  }.bind(this)), Math.abs(Math.abs(this.lat0) - P) < T ? this.mode = this.lat0 < 0 ? Zt.S_POLE : Zt.N_POLE : Math.abs(this.lat0) < T ? this.mode = Zt.EQUIT : (this.mode = Zt.OBLIQ, this.sinph0 = Math.sin(this.lat0), this.cosph0 = Math.cos(this.lat0)), this.pn1 = this.h / this.a, this.pn1 <= 0 || this.pn1 > 1e10)
    throw new Error("Invalid height");
  this.p = 1 + this.pn1, this.rp = 1 / this.p, this.h1 = 1 / this.pn1, this.pfact = (this.p + 1) * this.h1, this.es = 0;
  var i = this.tilt, t = this.azi;
  this.cg = Math.cos(t), this.sg = Math.sin(t), this.cw = Math.cos(i), this.sw = Math.sin(i);
}
function wM(i) {
  i.x -= this.long0;
  var t = Math.sin(i.y), e = Math.cos(i.y), n = Math.cos(i.x), s, r;
  switch (this.mode) {
    case Zt.OBLIQ:
      r = this.sinph0 * t + this.cosph0 * e * n;
      break;
    case Zt.EQUIT:
      r = e * n;
      break;
    case Zt.S_POLE:
      r = -t;
      break;
    case Zt.N_POLE:
      r = t;
      break;
  }
  switch (r = this.pn1 / (this.p - r), s = r * e * Math.sin(i.x), this.mode) {
    case Zt.OBLIQ:
      r *= this.cosph0 * t - this.sinph0 * e * n;
      break;
    case Zt.EQUIT:
      r *= t;
      break;
    case Zt.N_POLE:
      r *= -(e * n);
      break;
    case Zt.S_POLE:
      r *= e * n;
      break;
  }
  var o, a;
  return o = r * this.cg + s * this.sg, a = 1 / (o * this.sw * this.h1 + this.cw), s = (s * this.cg - r * this.sg) * this.cw * a, r = o * a, i.x = s * this.a, i.y = r * this.a, i;
}
function EM(i) {
  i.x /= this.a, i.y /= this.a;
  var t = { x: i.x, y: i.y }, e, n, s;
  s = 1 / (this.pn1 - i.y * this.sw), e = this.pn1 * i.x * s, n = this.pn1 * i.y * this.cw * s, i.x = e * this.cg + n * this.sg, i.y = n * this.cg - e * this.sg;
  var r = Pe(i.x, i.y);
  if (Math.abs(r) < T)
    t.x = 0, t.y = i.y;
  else {
    var o, a;
    switch (a = 1 - r * r * this.pfact, a = (this.p - Math.sqrt(a)) / (this.pn1 / r + r / this.pn1), o = Math.sqrt(1 - a * a), this.mode) {
      case Zt.OBLIQ:
        t.y = Math.asin(o * this.sinph0 + i.y * a * this.cosph0 / r), i.y = (o - this.sinph0 * Math.sin(t.y)) * r, i.x *= a * this.cosph0;
        break;
      case Zt.EQUIT:
        t.y = Math.asin(i.y * a / r), i.y = o * r, i.x *= a;
        break;
      case Zt.N_POLE:
        t.y = Math.asin(o), i.y = -i.y;
        break;
      case Zt.S_POLE:
        t.y = -Math.asin(o);
        break;
    }
    t.x = Math.atan2(i.x, i.y);
  }
  return i.x = t.x + this.long0, i.y = t.y, i;
}
var bM = ["Tilted_Perspective", "tpers"];
const PM = {
  init: CM,
  forward: wM,
  inverse: EM,
  names: bM
};
function SM() {
  if (this.flip_axis = this.sweep === "x" ? 1 : 0, this.h = Number(this.h), this.radius_g_1 = this.h / this.a, this.radius_g_1 <= 0 || this.radius_g_1 > 1e10)
    throw new Error();
  if (this.radius_g = 1 + this.radius_g_1, this.C = this.radius_g * this.radius_g - 1, this.es !== 0) {
    var i = 1 - this.es, t = 1 / i;
    this.radius_p = Math.sqrt(i), this.radius_p2 = i, this.radius_p_inv2 = t, this.shape = "ellipse";
  } else
    this.radius_p = 1, this.radius_p2 = 1, this.radius_p_inv2 = 1, this.shape = "sphere";
  this.title || (this.title = "Geostationary Satellite View");
}
function _M(i) {
  var t = i.x, e = i.y, n, s, r, o;
  if (t = t - this.long0, this.shape === "ellipse") {
    e = Math.atan(this.radius_p2 * Math.tan(e));
    var a = this.radius_p / Pe(this.radius_p * Math.cos(e), Math.sin(e));
    if (s = a * Math.cos(t) * Math.cos(e), r = a * Math.sin(t) * Math.cos(e), o = a * Math.sin(e), (this.radius_g - s) * s - r * r - o * o * this.radius_p_inv2 < 0)
      return i.x = Number.NaN, i.y = Number.NaN, i;
    n = this.radius_g - s, this.flip_axis ? (i.x = this.radius_g_1 * Math.atan(r / Pe(o, n)), i.y = this.radius_g_1 * Math.atan(o / n)) : (i.x = this.radius_g_1 * Math.atan(r / n), i.y = this.radius_g_1 * Math.atan(o / Pe(r, n)));
  } else
    this.shape === "sphere" && (n = Math.cos(e), s = Math.cos(t) * n, r = Math.sin(t) * n, o = Math.sin(e), n = this.radius_g - s, this.flip_axis ? (i.x = this.radius_g_1 * Math.atan(r / Pe(o, n)), i.y = this.radius_g_1 * Math.atan(o / n)) : (i.x = this.radius_g_1 * Math.atan(r / n), i.y = this.radius_g_1 * Math.atan(o / Pe(r, n))));
  return i.x = i.x * this.a, i.y = i.y * this.a, i;
}
function RM(i) {
  var t = -1, e = 0, n = 0, s, r, o, a;
  if (i.x = i.x / this.a, i.y = i.y / this.a, this.shape === "ellipse") {
    this.flip_axis ? (n = Math.tan(i.y / this.radius_g_1), e = Math.tan(i.x / this.radius_g_1) * Pe(1, n)) : (e = Math.tan(i.x / this.radius_g_1), n = Math.tan(i.y / this.radius_g_1) * Pe(1, e));
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
var TM = ["Geostationary Satellite View", "Geostationary_Satellite", "geos"];
const LM = {
  init: SM,
  forward: _M,
  inverse: RM,
  names: TM
};
function OM(i) {
  i.Proj.projections.add(Ir), i.Proj.projections.add(Nr), i.Proj.projections.add(Dx), i.Proj.projections.add(Yx), i.Proj.projections.add($x), i.Proj.projections.add(s9), i.Proj.projections.add(c9), i.Proj.projections.add(m9), i.Proj.projections.add(M9), i.Proj.projections.add(P9), i.Proj.projections.add(H9), i.Proj.projections.add(U9), i.Proj.projections.add($9), i.Proj.projections.add(r4), i.Proj.projections.add(c4), i.Proj.projections.add(m4), i.Proj.projections.add(M4), i.Proj.projections.add(P4), i.Proj.projections.add(O4), i.Proj.projections.add(F4), i.Proj.projections.add(G4), i.Proj.projections.add(V4), i.Proj.projections.add(K4), i.Proj.projections.add(iM), i.Proj.projections.add(aM), i.Proj.projections.add(mM), i.Proj.projections.add(MM), i.Proj.projections.add(PM), i.Proj.projections.add(LM);
}
se.defaultDatum = "WGS84";
se.Proj = De;
se.WGS84 = new se.Proj("WGS84");
se.Point = Yn;
se.toPoint = Mf;
se.defs = Yt;
se.nadgrid = ky;
se.transform = so;
se.mgrs = ex;
se.version = "__VERSION__";
OM(se);
function AM(i) {
  const t = Object.keys(i.defs), e = t.length;
  let n, s;
  for (n = 0; n < e; ++n) {
    const r = t[n];
    if (!K(r)) {
      const o = i.defs(r);
      let a = o.units;
      !a && o.projName === "longlat" && (a = "degrees"), Yu(
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
    const r = t[n], o = K(r);
    for (s = 0; s < e; ++s) {
      const a = t[s], l = K(a);
      if (!Bu(r, a))
        if (i.defs[r] === i.defs[a])
          ya([o, l]);
        else {
          const h = i(r, a);
          yg(
            o,
            l,
            Rh(o, l, h.forward),
            Rh(l, o, h.inverse)
          );
        }
    }
  }
}
class nu {
  constructor(t, e, n, s, r) {
    var a;
    this.store = r, this.states = s, this.inclusionArea = e, this.renderUtils = n;
    const o = this.store.getMap();
    if (!o)
      throw new Error("Missing map");
    this.map = o, this.control = new Fl(this.store), this.vectorSource = new $n(), this.setupMapForCreation(o, this.vectorSource), this.states.readonly || (window.addEventListener("authorize-created", (l) => {
      this.createElement(this.vectorSource, l);
    }), window.addEventListener("refused-created", () => {
      this.store.removeLastSelectedFeature(), this.store.getMaxElement() === 1 && this.previousElement && this.store.addSelectedFeature(this.previousElement, this.previousElement.get("id"), "create"), tt.sendEvent("rule-validation", void 0);
    }), window.addEventListener("remove-created-icon", () => {
      this.deleteElement(this.vectorSource);
    }), window.addEventListener("recenter-selected-element", () => {
      var c;
      const l = this.store.getCurrentItemId(), h = (c = this.store.getSelectedFeature(l)) == null ? void 0 : c.get("geom").getCoordinates();
      o.getView().setCenter(h);
    }), ((a = this.store.getOptions()) == null ? void 0 : a.mode.type) === "mix" && window.addEventListener("remove-created", (l) => {
      this.vectorSource.getFeatures().forEach((h) => {
        h.get("id") === l.detail && this.remove(this.vectorSource, h);
      });
    }), this.addLongClickEvent(t, o), o.on("click", (l) => {
      o.forEachFeatureAtPixel(l.pixel, (h) => {
        var c, u;
        h && ((c = h.getGeometry()) == null ? void 0 : c.getType()) === "Point" && h.get("id") && (this.store.unselectFeatures(), this.store.setCurrentItemId(h.get("id")), (u = this.store.getSelectedFeature(h.get("id"))) == null || u.set("isSelected", !0), tt.sendEvent("open-select-create-box", h.get("geom").getCoordinates()), this.control.show());
      });
    }));
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementCreateTargetMode(this.vectorSource, t);
  }
  removeCurrentSelection() {
    this.vectorSource.getFeatures().forEach((t) => this.vectorSource.removeFeature(t));
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
    }), t.addFeature(s), this.control.show(), tt.sendEvent("open-select-create-box", s.get("geom").getCoordinates()), this.store.setCustomDisplay(!0), this.store.setTargetBoxSize("select")), this.map.get("target").className = `${this.store.getTargetBoxSize()} ${gt.getTheme()}`;
  }
  remove(t, e) {
    t.removeFeature(e), this.control.hide(), this.store.removeSelectedFeature(e.get("id"));
  }
  deleteElement(t) {
    const e = this.store.getSelectedFeature(this.store.getCurrentItemId());
    e && (this.remove(t, e), tt.sendEvent("rule-validation", void 0), Ud.setCustomStyleWithouInfoBox(this.store)), this.map.get("target").className = `${this.store.getTargetBoxSize()} ${gt.getTheme()}`;
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
    var r;
    if (!this.states.readonly) {
      const o = s.getBoundingClientRect(), a = n.getCoordinateFromPixel([t - o.left - document.documentElement.scrollLeft, e - o.top - document.documentElement.scrollTop]), l = new oi(a), h = new an({
        geom: l,
        id: Number(`${Math.round(a[0])}${Math.round(a[1])}`),
        isSelected: !0
      });
      if (h.setGeometryName("geom"), this.inclusionArea && !this.inclusionArea.couldCreate(l.getCoordinates()))
        return;
      if (this.store.getMaxElement() === 1) {
        if (((r = this.store.getOptions()) == null ? void 0 : r.mode.type) === "mix") {
          const u = this.store.getSelectedFeatures();
          if (u && u.length === 1 && this.store.getCurrentFeatureType(u[0].get("objectid")) === "select") {
            const f = u[0].get("objectid");
            tt.sendEvent("remove-clicked", f);
          }
        }
        const c = this.store.getSelectedFeatures();
        c.length > 0 && (this.store.removeSelectedFeature(c[0].get("id")), this.previousElement = c[0]);
      }
      (this.store.getMaxElement() === -1 || this.store.getSelectedFeatures().length <= this.store.getMaxElement()) && (this.store.addSelectedFeature(h, h.get("id"), "create"), tt.sendEvent("icon-created", h.get("id")));
    }
  }
  moveAnalyzer(t, e, n) {
    return Math.abs(e - t[0]) > 10 || Math.abs(n - t[1]) > 10;
  }
  clearCreationTimeout(t) {
    clearTimeout(t), t = void 0;
  }
}
const Nf = `@media only screen and (min-width: 351px) and (max-width: 995px){.search-container{left:calc((100% - 334px)/2);width:100%;max-width:332px}}@media only screen and (max-width: 350px){.search-container{left:10px;width:calc(100% - 20px);max-width:332px}}@media only screen and (min-width: 996px){.search-container{left:calc((100% - (var(--search-width) + 30px)) / 2);width:calc(var(--search-width) + 30px)}}.search-container{position:absolute;top:var(--top-distance);z-index:0}.search-input-container{border-radius:var(--icon-border-radius);border:1px solid var(--icon-border-color);display:flex;background-color:var(--information-box-background-color);margin-bottom:1px}.search-input{width:calc(100% - 13px);height:44px;border:none;outline:none;padding:0 0 0 11px;font-size:14px;background-color:var(--information-box-background-color);color:var(--suggestion-box-text-color);font-family:sans-serif}.search-svg-container{width:29px;height:44px;margin-right:11px;display:flex;align-items:center}ul{margin-top:0;list-style-type:none;background-color:var(--information-box-background-color);padding-left:0;border-radius:var(--icon-border-radius)}ul>:first-child{border-top-right-radius:var(--icon-border-radius);border-top-left-radius:var(--icon-border-radius)}li{height:40px;border-bottom:1px solid var(--icon-border-color);padding-left:11px;font-size:12px;display:flex;align-items:center;justify-content:start;color:var(--suggestion-box-text-color);font-family:sans-serif;cursor:pointer}ul>:last-child{border-bottom-right-radius:var(--icon-border-radius);border-bottom-left-radius:var(--icon-border-radius)}li:hover,li:focus{background-color:var(--icon-border-color)}svg{width:var(--svg-icon-size);height:var(--svg-icon-size);stroke:var(--information-box-title-color)}svg:hover{stroke:var(--information-cross-hover-color)}svg>g>.icon{fill:none;stroke-width:var(--icon-stroke-width);stroke-linejoin:round;stroke-linecap:round}.cross-div{width:var(--svg-icon-size);height:var(--svg-icon-size);cursor:pointer}
`;
var IM = Object.defineProperty, NM = Object.getOwnPropertyDescriptor, Ze = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? NM(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && IM(t, e, s), s;
};
let Jn = class extends At {
  constructor() {
    super(...arguments), this._results = [];
  }
  firstUpdated() {
    var i;
    (i = this.map) == null || i.addEventListener("click", () => {
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
    var e;
    (e = this.map) == null || e.getView().setCenter(xg([i[0], i[1]], "EPSG:2056")), this._results = [], tt.sendEvent("address_selected", t);
  }
  render() {
    return Ct`
                <ul>
                  ${this._results.map(
      (i) => Ct`<li tabindex="0" @click=${() => this.selectAddress(i.coordinate, i.address)}>${i.address}</li>`
    )}
                </ul>
              `;
  }
};
Jn.styles = [yt(Nf)];
Ze([
  Te({ type: Object })
], Jn.prototype, "locations", 2);
Ze([
  Te({ type: Object })
], Jn.prototype, "map", 2);
Ze([
  Lt()
], Jn.prototype, "_results", 2);
Jn = Ze([
  Kt("location-list")
], Jn);
let ai = class extends At {
  constructor(i) {
    super(), this.results = {}, this._hasSearch = !1, this._hasSelected = !1, this.store = i;
    const t = i.getMap();
    if (!t)
      throw new Error("Missing map!");
    this.map = t, window.addEventListener("address_selected", (e) => {
      this.inputElement.value = e.detail, this._hasSearch = !1, this._hasSelected = !0;
    });
  }
  firstUpdated() {
    this.locationElements.map = this.map, this.inputElement.oninput = () => {
      if (this.inputElement.value.length > 1) {
        this._hasSearch = !0;
        const i = this.store.getOptions();
        if (!i)
          return;
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
    return Ct`<div class="search-container">
                    <div class="search-input-container">
                        <input id="search" type="text" class="search-input">
                        <div class="search-svg-container">
                        ${zl(
      this._hasSearch || this._hasSelected ? Ct`<div class="cross-div" @click="${this.clear}">
                                        ${Re(st.cross)}
                                    </div>` : Ct`${Re(st.search)}`
    )}
                        </div>
                    </div>
                    <location-list id="location-result" locations='${JSON.stringify(this.results)}'/>
                </div>`;
  }
};
ai.styles = [yt(Nf)];
Ze([
  Va("#search")
], ai.prototype, "inputElement", 2);
Ze([
  Va("#location-result")
], ai.prototype, "locationElements", 2);
Ze([
  Lt()
], ai.prototype, "results", 2);
Ze([
  Lt()
], ai.prototype, "_hasSearch", 2);
Ze([
  Lt()
], ai.prototype, "_hasSelected", 2);
ai = Ze([
  Kt("search-location")
], ai);
class zM extends Dt {
  constructor(t, e) {
    const n = new ai(t);
    super({ element: n }), this.div = n, Wt.setResizeEvent(this.div, "--search-width", e);
  }
}
class FM {
  constructor(t) {
    var r;
    const e = new Bt({
      fill: new Ut({
        color: "#ffffff00"
      }),
      stroke: new Se({
        color: "#dddddd",
        width: 5
      })
    }), n = t.getOptions();
    if (!n)
      throw new Error("Missing options");
    const s = new Bn({
      source: new $n({
        url: () => n.border.url,
        format: new Wd()
      }),
      zIndex: 9999,
      style: e,
      opacity: 0.9
    });
    s.on("change", () => {
      var a, l;
      const o = (a = s.getSource()) == null ? void 0 : a.getExtent();
      if (o) {
        const h = t.getOptions();
        if (!h)
          throw new Error("Missing options");
        (l = t.getMap()) == null || l.setView(new ii({
          extent: o,
          projection: "EPSG:2056",
          center: h.defaultCenter,
          zoom: h.zoom,
          minZoom: h.minZoom,
          maxZoom: h.maxZoom,
          enableRotation: h.interaction.enableRotation,
          constrainOnlyCenter: !0
        }));
      }
      t.setBorderConstraint(s), tt.sendEvent("border-contraint-enabled", void 0);
    }), (r = t.getMap()) == null || r.addLayer(s);
  }
}
class DM {
  constructor(t) {
    var n, s;
    this.vectorLayer = new Bn(), this.vectorSource = new $n(), this.map = t;
    const e = gt.getGeolocation();
    if (e) {
      const r = new an();
      r.setStyle(
        new Bt({
          image: new ni({
            radius: 6,
            fill: new Ut({
              color: "#3399CC"
            }),
            stroke: new Se({
              color: "#fff",
              width: 2
            })
          })
        })
      ), e.on("change:position", function() {
        const o = e.getPosition();
        r.setGeometry(
          o ? new oi(o) : void 0
        );
      }), (n = this.vectorSource) == null || n.addFeature(r), this.vectorLayer.setSource(this.vectorSource), (s = this.map) == null || s.addLayer(this.vectorLayer);
    }
  }
  removeMarker() {
    var t;
    (t = this.map) == null || t.removeLayer(this.vectorLayer);
  }
}
const jM = `.loader-element{position:absolute;top:calc(50% - 52px);background-color:var(--information-box-background-color);box-shadow:#0003 0 1px 4px;padding:15px;border-radius:10px;border:1px solid var(--information-box-background-color);z-index:10;max-width:302px;width:100%;left:calc(50% - 167px)}.loader-text{display:flex;justify-content:center;margin-top:10px;color:var(--information-box-title-color)}.loader-container{display:flex;justify-content:center}.loader{width:48px;height:48px;border:4px solid #008c6f;border-bottom-color:transparent;border-radius:50%;display:inline-block;box-sizing:border-box;animation:rotation 1s linear infinite}@keyframes rotation{0%{transform:rotate(0)}to{transform:rotate(360deg)}}
`;
var kM = Object.defineProperty, XM = Object.getOwnPropertyDescriptor, zf = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? XM(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && kM(t, e, s), s;
};
let ao = class extends At {
  constructor(i) {
    super(), this.message = "", this.message = i;
  }
  render() {
    return Ct`
      <div class="loader-element" style="pointer-events: auto;">
        <div class="loader-container">
          <span class="loader"></span>
        </div>
        <div class="loader-text">${this.message}</div>
      </div>
    `;
  }
};
ao.styles = [yt(jM)];
zf([
  Lt()
], ao.prototype, "message", 2);
ao = zf([
  Kt("loader-box")
], ao);
class GM extends Dt {
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
class HM {
  removeLoaderBox() {
    this.loaderBox.hide();
  }
  chromeBasePermissionAnalyzer() {
    const t = gt.getGeolocation();
    navigator.permissions.query({ name: "geolocation" }).then((e) => {
      e.state === "denied" && (t == null || t.setTracking(!1), this.denied()), e.state === "prompt" && this.openInfo(), e.state === "granted" && this.granted(), e.onchange = () => {
        var n;
        e.state === "denied" && (t == null || t.setTracking(!1), this.denied()), e.state === "prompt" && (this.openInfo(), t == null || t.setTracking(!0), (n = this.marker) == null || n.removeMarker()), e.state === "granted" && (t == null || t.setTracking(!0), this.granted());
      };
    });
  }
  granted() {
    this.removeLoaderBox(), this.map.removeOverlay(this.overlay), this.marker = new DM(this.map);
  }
  denied() {
    var t;
    this.removeLoaderBox(), this.map.removeOverlay(this.overlay), (t = this.marker) == null || t.removeMarker();
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
    this.map.addOverlay(this.overlay), this.loaderBox.show(), this.getLocation();
  }
  checkGeolocation() {
    const t = gt.getGeolocation();
    navigator.userAgent.match(/Chrome\/\d+/) !== null ? this.chromeBasePermissionAnalyzer() : navigator.userAgent.match(/(iPad)/) && navigator.userAgent.match(/AppleWebKit/) ? navigator.geolocation.getCurrentPosition(
      () => this.granted(),
      () => this.denied()
    ) : (navigator.permissions.query({ name: "geolocation" }).then((e) => {
      e.state === "denied" && this.denied(), e.state === "prompt" && this.openInfo(), e.state === "granted" && this.granted();
    }), t == null || t.on("error", () => {
      this.denied();
    }), t == null || t.on("change:position", () => {
      this.granted();
    }));
  }
  constructor(t) {
    if (!t)
      throw new Error("Missing map!");
    this.map = t;
    const e = gt.getGeolocation();
    e == null || e.setTracking(!0);
    const n = document.createElement("div");
    n.classList.add("map-overlay");
    const s = this.map.getView().calculateExtent(this.map.getSize());
    this.overlay = new lm({ element: n, position: Ai(s), className: "ol-overlay-container ol-selectable overlay-index" }), this.loaderBox = new GM("Chargement des donn\xE9es GPS"), this.map.addControl(this.loaderBox), this.checkGeolocation();
  }
}
class su {
  static getStates(t) {
    const e = {
      readonly: !1,
      currentSelections: []
    };
    return t && (t.readonly && (e.readonly = t.readonly), t.currentSelections && t.currentSelections.length > 0 && (e.currentSelections = t.currentSelections)), e;
  }
}
class ZM {
  constructor(t) {
    this.vectorSource = new $n(), this.renderUtils = t, this.renderUtils.setupAndLoadLayer(this.vectorSource);
  }
  renderCurrentSelection(t) {
    this.renderUtils.displayCurrentElementCreateTargetMode(this.vectorSource, t);
  }
  removeCurrentSelection() {
    this.vectorSource.getFeatures().forEach((t) => this.vectorSource.removeFeature(t));
  }
}
class ru {
  static setupCircles(t, e) {
    let n = [];
    return t.get("isSelected") ? n = [
      new Bt({
        zIndex: 1,
        image: new ni({
          radius: 2 * e,
          stroke: new Se({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Ut({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Bt({
        zIndex: 2,
        image: new ni({
          radius: e > 8 ? 4 : 0.2 * e,
          stroke: new Se({
            color: "#FFFFFF",
            width: 3
          }),
          fill: new Ut({
            color: "#DC2626"
          })
        })
      })
    ] : n = [
      new Bt({
        zIndex: 1,
        image: new ni({
          radius: 2 * e,
          stroke: new Se({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Ut({
            color: "rgb(239, 68, 68, 0.75)"
          })
        })
      }),
      new Bt({
        zIndex: 2,
        image: new ni({
          radius: e > 8 ? 4 : 0.2 * e,
          stroke: new Se({
            color: "#FFFFFF",
            width: 1
          }),
          fill: new Ut({
            color: "#DC2626"
          })
        })
      })
    ], n;
  }
}
class BM {
  constructor(t) {
    this.vectorIsLoaded = !1, this.store = t;
  }
  setIsLoaded(t) {
    this.vectorIsLoaded = t;
  }
  getDefaultZoomFactor() {
    var e;
    let t = ((e = this.store.getMap()) == null ? void 0 : e.getView().getZoom()) || 1;
    return t > 1 && (t = t / 2), t;
  }
  setChangeResolution(t, e) {
    var a;
    const n = this.store.getOptions(), s = ((a = n == null ? void 0 : n.notifications.find((l) => l.rule.type === "ZOOM_CONSTRAINT")) == null ? void 0 : a.rule.minZoom) || (n == null ? void 0 : n.zoom), r = t.getView().getZoom(), o = t.getView().getResolution();
    r && o && s && r > s && e.setStyle(function(l) {
      return ru.setupCircles(l, r / o);
    });
  }
  setupAndLoadLayer(t) {
    const e = new Bn({
      source: t,
      visible: !0
    });
    e.setStyle((r) => ru.setupCircles(r, this.getDefaultZoomFactor()));
    const n = this.store.getMap();
    if (!n)
      return;
    n == null || n.addLayer(e);
    const s = this.store.getOptions();
    !s || Wt.registerBorderConstaintMapEvent(
      "change:resolution",
      () => this.setChangeResolution(n, e),
      n,
      s
    );
  }
  generateFeaturePointFromCoordinate(t) {
    const e = t, n = new oi(e), s = new an({
      geom: n,
      id: Number(`${Math.round(e[0])}${Math.round(e[1])}`),
      isSelected: !1
    });
    return s.setGeometryName("geom"), s;
  }
  displayCurrentElementCreateTargetMode(t, e) {
    t.getFeatures().forEach((n) => t.removeFeature(n)), e.currentSelections.length > 0 && e.currentSelections.forEach((n) => {
      const s = this.generateFeaturePointFromCoordinate(n);
      e.readonly || this.store.addSelectedFeature(s, s.get("id"), "create"), t.addFeature(s);
    });
  }
  loadSelectMode(t, e) {
    const n = [];
    return e.currentSelections && e.currentSelections.length > 0 && (t.getFeatures().forEach((s) => {
      s.get("isClick") && s.set("isClick", !1);
    }), e.currentSelections.forEach((s) => {
      t.getFeatures().forEach((r) => {
        const o = r.get("geom").getCoordinates();
        o[0].toFixed(2) == s[0] && o[1].toFixed(2) == s[1] && (n.push(s), r.set("isClick", !0), e.readonly || this.store.addSelectedFeature(r, r.get("objectid"), "select"));
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
    t && e && (this.vectorIsLoaded ? this.loadMixMode(t, e, n) : t.on("featuresloadend", () => {
      this.loadMixMode(t, e, n), this.vectorIsLoaded = !0;
    }));
  }
}
var WM = Object.defineProperty, VM = Object.getOwnPropertyDescriptor, Ii = (i, t, e, n) => {
  for (var s = n > 1 ? void 0 : n ? VM(t, e) : t, r = i.length - 1, o; r >= 0; r--)
    (o = i[r]) && (s = (n ? o(t, e, s) : o(s)) || s);
  return n && s && WM(t, e, s), s;
};
let Xe = class extends At {
  constructor() {
    super(), this.modeControllers = [], this.inclusionArea = void 0, this.options = {}, this.states = {}, this.store = new gt(), this.renderUtils = new BM(this.store);
  }
  connectedCallback() {
    super.connectedCallback();
  }
  setupTheme(i) {
    i.darkMode ? gt.setTheme("dark") : i.lightMode || window.matchMedia("(prefers-color-scheme: light)").matches ? gt.setTheme("light") : window.matchMedia("(prefers-color-scheme: dark)").matches ? gt.setTheme("dark") : gt.setTheme("light");
  }
  setupCustomDisplay(i) {
    i.mode.type === "target" ? (this.store.setCustomDisplay(i.geolocationInformation.displayBox), this.setupTargetBoxSize(i.geolocationInformation)) : i.search.displaySearch ? (this.store.setTargetBoxSize("small"), this.store.setCustomDisplay(!0)) : (this.store.setTargetBoxSize("no-box"), this.store.setCustomDisplay(!1));
  }
  setupTargetBoxSize(i) {
    i.currentLocation && i.reverseLocation ? this.store.setTargetBoxSize("large") : i.currentLocation || i.reverseLocation ? this.store.setTargetBoxSize("medium") : this.store.setTargetBoxSize("small");
  }
  firstUpdated() {
    const i = y3.webComponentOptions(this.options);
    this.store.setOptions(i);
    const t = su.getStates(this.states);
    if (!i)
      return;
    const e = t.readonly;
    this.setupTheme(i), this.setupCustomDisplay(i), se.defs("EPSG:2056", "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"), AM(se), this.view = new ii({
      projection: "EPSG:2056",
      center: i.defaultCenter,
      zoom: i.zoom,
      minZoom: i.minZoom,
      maxZoom: i.maxZoom,
      enableRotation: i.interaction.enableRotation
    });
    const n = new B1({
      target: this.mapElement,
      controls: [],
      layers: [],
      view: this.view
    });
    this.store.setMap(n), Z3.setupIcon(t, this.store), i.interaction.enableGeolocation && !e && (gt.setGeolocation(new U1({
      trackingOptions: {
        enableHighAccuracy: !0
      },
      projection: this.view.getProjection()
    })), new HM(n)), i.search.displaySearch && i.mode.type !== "target" && !e && n.addControl(new zM(this.store, n)), i.mode.type === "target" && (this.modeControllers.push(new ZM(this.renderUtils)), e || (n.addControl(new J3(this.store)), i.geolocationInformation.displayBox && n.addControl(
      new $3(this.store)
    ))), i.wmts.length > 0 && new l3(this.store), i.interaction.displayScaleLine && n.addControl(new Cm({ units: "metric" })), i.border.url !== "" && new FM(this.store), i.inclusionArea.url !== "" && (this.inclusionArea = new M3(this.store)), i.mode.type === "select" && i.wfs.url != "" && this.modeControllers.push(new Nc(this.renderUtils, t, this.store)), i.mode.type === "create" && this.modeControllers.push(new nu(this.mapElement, this.inclusionArea, this.renderUtils, t, this.store)), i.mode.type === "mix" && i.wfs.url != "" && (this.modeControllers.push(new Nc(this.renderUtils, t, this.store)), this.modeControllers.push(new nu(this.mapElement, this.inclusionArea, this.renderUtils, t, this.store))), e || new g3(this.store), Wt.setCursorEvent(n);
  }
  updated(i) {
    var t, e, n, s, r, o, a, l;
    if (i.has("states") && this.states) {
      const h = su.getStates(this.states);
      if (h.currentSelections.length > 0) {
        switch ((t = this.store.getOptions()) == null ? void 0 : t.mode.type) {
          case "target":
            (e = this.modeControllers[0]) == null || e.renderCurrentSelection(h);
            break;
          case "select":
            (n = this.modeControllers[0]) == null || n.renderCurrentSelection(h);
            break;
          case "create":
            (s = this.modeControllers[0]) == null || s.renderCurrentSelection(h);
            break;
          case "mix":
            this.renderUtils.displayMixMode((r = this.modeControllers[0]) == null ? void 0 : r.vectorSource, (o = this.modeControllers[1]) == null ? void 0 : o.vectorSource, h);
            break;
        }
        (a = this.store.getMap()) == null || a.updateSize();
      } else
        this.modeControllers.forEach((c) => c.removeCurrentSelection()), this.store.removeAllSelectedFeatures(), (l = this.store.getMap()) == null || l.getControls().forEach((c) => {
          c instanceof Fl && c.disable();
        });
    }
  }
  render() {
    return Ct`
    <div id="map" class="${this.store.getTargetBoxSize()} ${gt.getTheme()}">
    </div>
    `;
  }
};
Xe.styles = [yt(h3), yt(c3), yt(To), yt(lf), yt(m3), yt(p3), yt(v3)];
Ii([
  Va("#map")
], Xe.prototype, "mapElement", 2);
Ii([
  Lt()
], Xe.prototype, "view", 2);
Ii([
  Lt()
], Xe.prototype, "modeControllers", 2);
Ii([
  Lt()
], Xe.prototype, "renderUtils", 2);
Ii([
  Lt()
], Xe.prototype, "inclusionArea", 2);
Ii([
  Te({ type: Object, attribute: "options" })
], Xe.prototype, "options", 2);
Ii([
  Te({ type: Object, attribute: "states" })
], Xe.prototype, "states", 2);
Xe = Ii([
  Kt("openlayers-element")
], Xe);
export {
  Xe as OpenLayersElement
};
