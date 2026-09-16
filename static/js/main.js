/* ================================================================
   Uni-Connect — igloo.inc-inspired JS
   Custom cursor · Split text · Magnetic buttons · Scroll reveals
   ================================================================ */

(function () {
  "use strict";

  /* ── CUSTOM CURSOR ── */
  const dot = document.querySelector(".cursor-dot");
  const ring = document.querySelector(".cursor-ring");

  if (dot && ring && window.innerWidth > 768) {
    let mx = 0,
      my = 0,
      rx = 0,
      ry = 0;

    document.addEventListener("mousemove", (e) => {
      mx = e.clientX;
      my = e.clientY;
      gsap.to(dot, { x: mx, y: my, duration: 0.08, ease: "none" });
    });

    gsap.ticker.add(() => {
      rx += (mx - rx) * 0.11;
      ry += (my - ry) * 0.11;
      gsap.set(ring, { x: rx, y: ry });
    });

    // Hover state on interactive elements
    const hoverEls =
      "a, button, .btn, .dept-card, .pin-card, .thread-card, [data-vote-url], [data-bookmark-url]";
    document.querySelectorAll(hoverEls).forEach((el) => {
      el.addEventListener("mouseenter", () =>
        document.body.classList.add("cursor-hover"),
      );
      el.addEventListener("mouseleave", () =>
        document.body.classList.remove("cursor-hover"),
      );
    });

    document.addEventListener("mouseleave", () => {
      gsap.to([dot, ring], { opacity: 0, duration: 0.3 });
    });
    document.addEventListener("mouseenter", () => {
      gsap.to([dot, ring], { opacity: 1, duration: 0.3 });
    });
  }

  /* ── MAGNETIC BUTTONS ── */
  function initMagnetic() {
    document
      .querySelectorAll(".btn-primary-glow, .btn-outline-glass")
      .forEach((btn) => {
        btn.addEventListener("mousemove", (e) => {
          const rect = btn.getBoundingClientRect();
          const cx = rect.left + rect.width / 2;
          const cy = rect.top + rect.height / 2;
          const dx = (e.clientX - cx) * 0.38;
          const dy = (e.clientY - cy) * 0.38;
          gsap.to(btn, { x: dx, y: dy, duration: 0.4, ease: "power2.out" });
        });
        btn.addEventListener("mouseleave", () => {
          gsap.to(btn, {
            x: 0,
            y: 0,
            duration: 0.5,
            ease: "elastic.out(1,0.5)",
          });
        });
      });
  }
  initMagnetic();

  /* ── SPLIT TEXT (manual, no plugin) ── */
  function splitWords(el) {
    const text = el.textContent;
    el.innerHTML = "";
    text.split(" ").forEach((word, i) => {
      const wrap = document.createElement("span");
      wrap.className = "split-word-wrap";
      const inner = document.createElement("span");
      inner.className = "split-word";
      inner.textContent = i === 0 ? word : " " + word;
      wrap.appendChild(inner);
      el.appendChild(wrap);
    });
    return el.querySelectorAll(".split-word");
  }

  function splitChars(el) {
    const words = el.textContent.split(" ");
    el.innerHTML = "";
    const chars = [];
    words.forEach((word, wi) => {
      const wordWrap = document.createElement("span");
      wordWrap.style.display = "inline-block";
      word.split("").forEach((char) => {
        const wrap = document.createElement("span");
        wrap.style.overflow = "hidden";
        wrap.style.display = "inline-block";
        const inner = document.createElement("span");
        inner.style.display = "inline-block";
        inner.textContent = char;
        wrap.appendChild(inner);
        wordWrap.appendChild(wrap);
        chars.push(inner);
      });
      el.appendChild(wordWrap);
      if (wi < words.length - 1) el.appendChild(document.createTextNode(" "));
    });
    return chars;
  }

  /* ── HERO — pin cards only (text is CSS animated) ── */
  function initHero() {
    // Pin cards cascade after CSS animations clear
    const pins = gsap.utils.toArray(".pin-card");
    if (pins.length) {
      gsap.from(pins, {
        opacity: 0,
        y: 60,
        scale: 0.9,
        duration: 0.9,
        delay: 1.55,
        stagger: { amount: 0.6 },
        ease: "back.out(1.2)",
      });
    }

    // Stat number counter
    setTimeout(() => {
      document.querySelectorAll(".stat-number[data-count]").forEach((el) => {
        const target = parseInt(el.getAttribute("data-count"), 10);
        if (isNaN(target) || target === 0) return;
        let start = 0;
        const step = target / 55;
        const tick = setInterval(() => {
          start = Math.min(start + step, target);
          el.textContent = Math.round(start);
          if (start >= target) clearInterval(tick);
        }, 22);
      });
    }, 1600);
  }
  initHero();

  /* ── SCROLL REVEALS ── */
  gsap.registerPlugin(ScrollTrigger);

  function initScrollReveals() {
    // Section labels + display headings
    document.querySelectorAll(".section-label, .reveal-label").forEach((el) => {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: "top 88%" },
        opacity: 0,
        y: 18,
        duration: 0.7,
        ease: "power3.out",
      });
    });

    document.querySelectorAll(".display-heading[data-split]").forEach((el) => {
      const words = splitWords(el);
      gsap.from(words, {
        scrollTrigger: { trigger: el, start: "top 85%" },
        y: "100%",
        opacity: 0,
        duration: 0.8,
        stagger: 0.06,
        ease: "power4.out",
      });
    });

    // Reveal elements with data-reveal attribute
    document.querySelectorAll("[data-reveal]").forEach((el, i) => {
      const delay = parseFloat(el.getAttribute("data-reveal-delay") || 0);
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: "top 85%" },
        opacity: 0,
        y: 40,
        duration: 0.85,
        delay,
        ease: "power3.out",
      });
    });

    // Feature cards
    const featureCards = gsap.utils.toArray(".feature-card-igloo");
    if (featureCards.length) {
      gsap.from(featureCards, {
        scrollTrigger: { trigger: featureCards[0], start: "top 80%" },
        opacity: 0,
        y: 50,
        scale: 0.96,
        duration: 0.9,
        stagger: { amount: 0.5 },
        ease: "power3.out",
      });
    }

    // Dept cards
    const deptCards = gsap.utils.toArray(".dept-card");
    if (deptCards.length) {
      gsap.from(deptCards, {
        scrollTrigger: {
          trigger: deptCards[0].closest(".row") || deptCards[0],
          start: "top 82%",
        },
        opacity: 0,
        y: 36,
        scale: 0.96,
        duration: 0.75,
        stagger: { amount: 0.5, from: "start" },
        ease: "power2.out",
      });
    }

    // Thread cards on list page
    gsap.utils.toArray(".thread-card").forEach((card, i) => {
      gsap.from(card, {
        scrollTrigger: { trigger: card, start: "top 90%" },
        opacity: 0,
        x: -20,
        duration: 0.55,
        delay: i < 5 ? i * 0.06 : 0,
        ease: "power2.out",
      });
    });

    // Generic reveal sections
    gsap.utils.toArray(".reveal-section").forEach((section) => {
      gsap.from(section.querySelectorAll(".reveal-el"), {
        scrollTrigger: { trigger: section, start: "top 80%" },
        opacity: 0,
        y: 30,
        duration: 0.7,
        stagger: 0.1,
        ease: "power2.out",
      });
    });

    // Section lines
    gsap.utils.toArray(".section-line").forEach((line) => {
      gsap.from(line, {
        scrollTrigger: { trigger: line, start: "top 90%" },
        scaleX: 0,
        transformOrigin: "left",
        duration: 1.2,
        ease: "power3.out",
      });
    });

    // Marquee: if present, no extra animation needed
  }
  initScrollReveals();

  /* ── PARALLAX (hero background orbs) ── */
  window.addEventListener("scroll", () => {
    const sy = window.scrollY;
    document.querySelectorAll(".ambient-orb").forEach((orb, i) => {
      const factor = i % 2 === 0 ? 0.12 : -0.08;
      orb.style.transform = `translateY(${sy * factor}px)`;
    });
  });

  /* ── TILT ON CARDS ── */
  function initTilt() {
    document.querySelectorAll(".tilt-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const cx = (e.clientX - rect.left) / rect.width - 0.5;
        const cy = (e.clientY - rect.top) / rect.height - 0.5;
        gsap.to(card, {
          rotationY: cx * 14,
          rotationX: -cy * 14,
          duration: 0.4,
          ease: "power2.out",
          transformPerspective: 1000,
        });
      });
      card.addEventListener("mouseleave", () => {
        gsap.to(card, {
          rotationY: 0,
          rotationX: 0,
          duration: 0.6,
          ease: "elastic.out(1, 0.5)",
        });
      });
    });
  }
  initTilt();

  /* ── VOTE HANDLER ── */
  document.addEventListener("click", function (e) {
    const voteBtn = e.target.closest("[data-vote-url]");
    if (!voteBtn) return;
    e.preventDefault();
    fetch(voteBtn.getAttribute("data-vote-url"), {
      method: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((r) => r.json())
      .then((data) => {
        const counter = voteBtn.querySelector(".vote-count");
        if (counter) counter.textContent = data.count;
        voteBtn.classList.toggle("voted", data.voted);
        const icon = voteBtn.querySelector("i");
        if (icon) icon.style.color = data.voted ? "#A0A5B1" : "";
        gsap.fromTo(
          voteBtn,
          { scale: 1.35 },
          { scale: 1, duration: 0.4, ease: "elastic.out(1,0.5)" },
        );
      });
  });

  /* ── BOOKMARK HANDLER ── */
  document.addEventListener("click", function (e) {
    const bookmarkBtn = e.target.closest("[data-bookmark-url]");
    if (!bookmarkBtn) return;
    e.preventDefault();
    fetch(bookmarkBtn.getAttribute("data-bookmark-url"), {
      method: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((r) => r.json())
      .then((data) => {
        const icon = bookmarkBtn.querySelector("i");
        if (icon) {
          icon.className = data.bookmarked
            ? "bi bi-bookmark-fill"
            : "bi bi-bookmark";
          icon.style.color = data.bookmarked ? "#A0A5B1" : "";
        }
        gsap.fromTo(
          bookmarkBtn,
          { scale: 1.3 },
          { scale: 1, duration: 0.4, ease: "elastic.out(1,0.5)" },
        );
      });
  });

  /* ── REPLY TOGGLE ── */
  document.addEventListener("click", function (e) {
    const replyBtn = e.target.closest("[data-reply-to]");
    if (!replyBtn) return;
    const form = document.getElementById("replyForm");
    if (form) {
      form.querySelector('[name="parent_id"]').value =
        replyBtn.getAttribute("data-reply-to");
      form.scrollIntoView({ behavior: "smooth", block: "center" });
      form.querySelector("textarea")?.focus();
    }
  });

  /* ── EMOJI PICKER & VOICE RECORDER ── */
  (function () {
    const emojiSet = [
      "😀",
      "🎓",
      "💬",
      "📚",
      "✅",
      "🤔",
      "🧠",
      "✍️",
      "📌",
      "🎧",
    ];
    let currentPicker = null;
    document.addEventListener("click", function (e) {
      const emojiBtn = e.target.closest(".emoji-button");
      if (emojiBtn) {
        e.preventDefault();
        const targetId = emojiBtn.dataset.target;
        const target = document.getElementById(targetId);
        if (!target) return;
        if (currentPicker) {
          currentPicker.remove();
          currentPicker = null;
          return;
        }
        const picker = document.createElement("div");
        picker.className = "emoji-picker";
        emojiSet.forEach((emoji) => {
          const button = document.createElement("button");
          button.type = "button";
          button.textContent = emoji;
          button.addEventListener("click", () => {
            const start = target.selectionStart || 0;
            const end = target.selectionEnd || 0;
            target.value =
              target.value.slice(0, start) + emoji + target.value.slice(end);
            target.focus();
            target.setSelectionRange(
              start + emoji.length,
              start + emoji.length,
            );
            picker.remove();
            currentPicker = null;
          });
          picker.appendChild(button);
        });
        document.body.appendChild(picker);
        const rect = emojiBtn.getBoundingClientRect();
        picker.style.top = `${rect.bottom + window.scrollY + 8}px`;
        picker.style.left = `${rect.left + window.scrollX}px`;
        currentPicker = picker;
        return;
      }

      const voiceBtn = e.target.closest(".record-voice-button");
      if (voiceBtn) {
        e.preventDefault();
        const targetId = voiceBtn.dataset.target;
        const input = document.getElementById(targetId);
        if (!input) return;
        if (!navigator.mediaDevices || !window.MediaRecorder) {
          alert("Voice recording is not supported by your browser.");
          return;
        }
        if (voiceBtn.dataset.recording === "true") {
          voiceBtn.dataset.recording = "false";
          voiceBtn.textContent = "🎙 Record voice note";
          if (voiceBtn._recorder) {
            voiceBtn._recorder.stop();
          }
          return;
        }
        navigator.mediaDevices
          .getUserMedia({ audio: true })
          .then((stream) => {
            const recorder = new MediaRecorder(stream);
            const chunks = [];
            voiceBtn._recorder = recorder;
            voiceBtn.dataset.recording = "true";
            voiceBtn.textContent = "⏹ Stop recording";
            recorder.addEventListener("dataavailable", (event) => {
              if (event.data.size > 0) chunks.push(event.data);
            });
            recorder.addEventListener("stop", () => {
              stream.getTracks().forEach((track) => track.stop());
              const blob = new Blob(chunks, { type: "audio/webm" });
              const file = new File([blob], "voice-note.webm", {
                type: blob.type,
              });
              const dataTransfer = new DataTransfer();
              dataTransfer.items.add(file);
              input.files = dataTransfer.files;
              let preview =
                voiceBtn.parentElement.querySelector(".voice-preview");
              if (!preview) {
                preview = document.createElement("div");
                preview.className = "voice-preview";
                voiceBtn.parentElement.appendChild(preview);
              }
              preview.innerHTML = `<audio controls src="${URL.createObjectURL(blob)}"></audio>`;
              voiceBtn.textContent = "🎙 Record voice note";
              voiceBtn.dataset.recording = "false";
            });
            recorder.start();
          })
          .catch(() => {
            alert(
              "We could not access your microphone. Please allow audio recording.",
            );
          });
        return;
      }

      if (currentPicker && !e.target.closest(".emoji-picker")) {
        currentPicker.remove();
        currentPicker = null;
      }
    });
  })();

  /* ── CSRF ── */
  function getCookie(name) {
    for (const cookie of document.cookie.split(";")) {
      const c = cookie.trim();
      if (c.startsWith(name + "="))
        return decodeURIComponent(c.slice(name.length + 1));
    }
    return null;
  }

  /* ── TOASTS ── */
  document.querySelectorAll(".toast").forEach((toast) => {
    setTimeout(() => {
      const t = bootstrap.Toast.getInstance(toast);
      if (t) t.hide();
      else toast.style.display = "none";
    }, 4000);
  });

  /* ── SPLINE FALLBACK ── */
  const splineFallback = document.getElementById("splineFallback");
  const splineContainer = document.getElementById("splineContainer");
  if (splineContainer && splineFallback) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      splineContainer.style.display = "none";
      splineFallback.style.display = "block";
    } else {
      setTimeout(() => {
        const viewer = document.querySelector("spline-viewer");
        if (!viewer?.shadowRoot?.querySelector("canvas")) {
          splineContainer.style.display = "none";
          splineFallback.style.display = "block";
        }
      }, 6000);
    }
  }
})();
