/*
 *  Licensed to the Apache Software Foundation (ASF) under one
 *  or more contributor license agreements.  See the NOTICE file
 *  distributed with this work for additional information
 *  regarding copyright ownership.  The ASF licenses this file
 *  to you under the Apache License, Version 2.0 (the
 *  "License"); you may not use this file except in compliance
 *  with the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing,
 *  software distributed under the License is distributed on an
 *  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *  KIND, either express or implied.  See the License for the
 *  specific language governing permissions and limitations
 *  under the License.
 */

function initAnnounceConfirm() {
	const confirmInput = document.getElementById("confirm_announce");
	const announceForm = document.querySelector("form.atr-canary");

	if (!confirmInput || !announceForm) {
		return;
	}

	const submitButton = announceForm.querySelector('button[type="submit"]');
	if (!submitButton) {
		return;
	}

	const updateButtonState = () => {
		const isConfirmed = confirmInput.value === "CONFIRM";
		submitButton.disabled = !isConfirmed;
	};

	confirmInput.addEventListener("input", updateButtonState);

	updateButtonState();
}

function initDownloadPathValidation() {
	const pathInput = document.getElementById("download_path_suffix");
	const pathHelpText = pathInput
		? pathInput.parentElement.querySelector(".form-text")
		: null;

	if (!pathInput || !pathHelpText) {
		return;
	}

	const baseText = pathHelpText.dataset.baseText || "";
	let pathDebounce;

	const updatePathHelpText = () => {
		let suffix = pathInput.value;
		if (suffix.includes("..") || suffix.includes("//")) {
			pathHelpText.textContent =
				"Download path suffix must not contain .. or //";
			return;
		}
		if (suffix.startsWith("./")) {
			suffix = suffix.slice(1);
		} else if (suffix === ".") {
			suffix = "/";
		}
		if (!suffix.startsWith("/")) {
			suffix = `/${suffix}`;
		}
		if (!suffix.endsWith("/")) {
			suffix = `${suffix}/`;
		}
		if (suffix.includes("/.")) {
			pathHelpText.textContent = "Download path suffix must not contain /.";
			return;
		}
		pathHelpText.textContent = baseText + suffix;
	};

	pathInput.addEventListener("input", () => {
		clearTimeout(pathDebounce);
		pathDebounce = setTimeout(updatePathHelpText, 10);
	});
	updatePathHelpText();
}

document.addEventListener("DOMContentLoaded", () => {
	initAnnounceConfirm();
	initDownloadPathValidation();
});
