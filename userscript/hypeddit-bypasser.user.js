// ==UserScript==
// @name         Hypeddit DownloadWallBypasser 2k24 (Automated Edition)
// @namespace    http://tampermonkey.net/
// @version      2024-07-24
// @description  Bypass the fangates. Soundcloud and Spotify accounts are mandatory!
// @author       fan1200 & Antigravity
// @match        https://hypeddit.com/*
// @match        https://secure.soundcloud.com/connect*
// @match        https://secure.soundcloud.com/authorize*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=hypeddit.com
// @grant        none
// ==/UserScript==

;(function () {
    "use strict"

    window.hypedditSettings = {
        email: "bernard.zhao.us@gmail.com",
        name: "Bernard",
        comment: "Nice edit!",
        auto_close: false,
        auto_close_timeout_in_ms: 5000,
    }

    // Auto-confirm SoundCloud OAuth authorization if redirected
    if (window.location.host.includes("soundcloud.com")) {
        const button = document.querySelector('button[type="submit"]')
        if (button) {
            button.click()
        } else {
            let cou = 0
            const maxTries = 15
            const retryClick = () => {
                const btn = document.querySelector('button[type="submit"]')
                if (btn) {
                    btn.click()
                } else {
                    cou++
                    if (cou < maxTries) {
                        setTimeout(retryClick, 300)
                    }
                }
            }
            setTimeout(retryClick, 300)
        }
    }

    window.handleFollowOptions = function (containerElementId, skipperId) {
        if (document.getElementById(containerElementId) !== null) {
            document
                .getElementById(containerElementId)
                .querySelectorAll("a")
                .forEach((accountItem) => {
                    accountItem.classList.remove("undone")
                    accountItem.classList.add("done")
                })
            const skipper = document.getElementById(skipperId)
            if (skipper) skipper.click()
        }
    }

    window.handleSoundCloud = function () {
        console.log("[Bypasser] Handling SoundCloud step...")
        const scSlide = document.querySelector(".sc.fangate-slider-content")
        if (scSlide) {
            scSlide.querySelectorAll(".undone").forEach(item => {
                item.classList.remove("undone")
                item.classList.add("done")
            })
            const skipChannel = document.getElementById("skipper_sc_channel")
            if (skipChannel) skipChannel.click()
            const skipNext = document.getElementById("skipper_sc_next")
            if (skipNext) skipNext.click()
        }
        const comment = window.hypedditSettings.comment
        const commentInput = document.getElementById("sc_comment_text")
        if (commentInput) {
            commentInput.value = comment
            commentInput.setAttribute("value", comment)
        }
        const stepSc = document.getElementById("step_sc")
        if (stepSc) {
            const link = stepSc.querySelector("a")
            if (link) link.click()
        }
    }

    window.handleInstagram = function () {
        console.log("[Bypasser] Handling Instagram step...")
        window.handleFollowOptions("instagram_status", "skipper_ig_next")
    }

    window.handleYoutube = function () {
        console.log("[Bypasser] Handling YouTube step...")
        window.handleFollowOptions("youtube_status", "skipper_yt_next")
    }

    window.handleSpotify = function () {
        console.log("[Bypasser] Handling Spotify step...")
        const stepSp = document.getElementById("step_sp")
        if (stepSp) {
            const link = stepSp.querySelector("a")
            if (link) link.click()
        }
    }

    window.handleDownload = function () {
        console.log("[Bypasser] Triggering Download Button...")
        const btn = document.getElementById("gateDownloadButton")
        if (btn) btn.click()
    }

    window.handleEmail = function () {
        console.log("[Bypasser] Handling Email step...")
        const email = window.hypedditSettings.email
        const name = window.hypedditSettings.name

        const nameInput = document.getElementById("email_name")
        if (nameInput) {
            nameInput.value = name
            nameInput.setAttribute("value", name)
        }

        const emailInput = document.getElementById("email_address")
        if (emailInput) {
            emailInput.value = email
            emailInput.setAttribute("value", email)
        }

        const nextBtn = document.getElementById("email_to_downloads_next")
        if (nextBtn) nextBtn.click()
    }

    window.handleTikTok = function () {
        console.log("[Bypasser] Handling TikTok step...")
        window.handleFollowOptions("tiktok_status", "skipper_tk_next")
    }

    window.handleFacebook = function () {
        console.log("[Bypasser] Handling Facebook step...")
        const fbBtn = document.getElementById("fbCarouselSocialSection")
        if (fbBtn) fbBtn.click()
    }

    window.handleMultiPortal = function () {
        const stepEmail = document.getElementById("step_email")
        if (stepEmail && stepEmail.previousElementSibling) {
            stepEmail.previousElementSibling.click()
        }
        window.handleEmail()
    }

    window.handleEmailSoundCloud = function () {
        const stepEmail = document.getElementById("step_email")
        if (stepEmail && stepEmail.previousElementSibling) {
            stepEmail.previousElementSibling.click()
        }
        window.handleEmail()
    }

    window.handleSoundCloudYoutube = function () {
        const stepYt = document.getElementById("step_yt")
        if (stepYt && stepYt.previousElementSibling) {
            stepYt.previousElementSibling.click()
        }
        window.handleYoutube()
    }

    window.handleDonate = function () {
        const stepDn = document.getElementById("step_dn")
        if (stepDn && stepDn.previousElementSibling) {
            stepDn.previousElementSibling.click()
        }
        const next = document.getElementById("donation_next")
        if (next) next.click()
    }

    window.handleMixcloud = function () {
        const skip = document.getElementById("skipper_mc")
        if (skip) skip.click()
    }

    window.handleBandCamp = function () {
        const skip = document.getElementById("skipper_bc")
        if (skip) skip.click()
    }

    function init() {
        const targetNode = document.getElementById("myCarousel")
        if (targetNode) {
            const config = { attributes: true, childList: true, subtree: true }
            let prevStepContent = null
            const callback = (mutationList, observer) => {
                for (const mutation of mutationList) {
                    if (mutation.type === "attributes") {
                        const stepContent = document.querySelector(".fangate-slider-content:not(.move-left)")
                        if (stepContent && stepContent !== prevStepContent) {
                            const stepClassList = stepContent.classList
                            if (stepClassList.contains("tk|ig")) window.handleTikTok()
                            if (stepClassList.contains("sp|ig|email")) window.handleMultiPortal()
                            if (stepClassList.contains("email|sc")) window.handleEmailSoundCloud()
                            if (stepClassList.contains("sc|yt")) window.handleSoundCloudYoutube()
                            if (stepClassList.contains("dn")) window.handleDonate()
                            if (stepClassList.contains("sc")) window.handleSoundCloud()
                            if (stepClassList.contains("ig")) window.handleInstagram()
                            if (stepClassList.contains("dw")) window.handleDownload()
                            if (stepClassList.contains("yt")) window.handleYoutube()
                            if (stepClassList.contains("sp")) window.handleSpotify()
                            if (stepClassList.contains("email")) window.handleEmail()
                            if (stepClassList.contains("tk")) window.handleTikTok()
                            if (stepClassList.contains("fb")) window.handleFacebook()
                            if (stepClassList.contains("mc")) window.handleMixcloud()
                            if (stepClassList.contains("bc")) window.handleBandCamp()
                            prevStepContent = stepContent
                        }
                    }
                }
            }
            const observer = new MutationObserver(callback)
            observer.observe(targetNode, config)
        }

        const _start = () => {
            const dlProcess = document.getElementById("downloadProcess")
            if (dlProcess) {
                console.log("[Bypasser] Starting download process...")
                dlProcess.click()
            }
        }
        window.setTimeout(_start, 1000)
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init)
    } else {
        init()
    }
})()
