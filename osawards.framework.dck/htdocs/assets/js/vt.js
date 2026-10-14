const URL_FRAGMENT = "&_g=()&_a=(filters:!({1}))";
const INF_YEAR = 2008;
const SUP_YEAR = 2026;
const INF_PERCENTAGE = 0;
const SUP_PERCENTAGE = 100;

const OSH_PROJECT_TYPES = [
    { value: "3D Printing", label: "3D Printing" },
    { value: "Agriculture", label: "Agriculture" },
    { value: "Arts", label: "Arts" },
    { value: "Education", label: "Education" },
    { value: "Electronics", label: "Electronics" },
    { value: "Enclosure", label: "Enclosure" },
    { value: "Environmental", label: "Environmental" },
    { value: "Home Connection", label: "Home Connection" },
    { value: "IOT", label: "IOT" },
    { value: "Manufacturing", label: "Manufacturing" },
    { value: "Other", label: "Other" },
    { value: "Robotics", label: "Robotics" },
    { value: "Science", label: "Science" },
    { value: "Sound", label: "Sound" },
    { value: "Space", label: "Space" },
    { value: "Tool", label: "Tool" },
    { value: "Wearables", label: "Wearables" }
];

const OSH_HARDWARE_LICENSES = [
    { value: "CC-BY-4.0", label: "CC-BY-4.0" },
    { value: "CC-BY-SA-4.0", label: "CC-BY-SA-4.0" },
    { value: "CC0-1.0", label: "CC0-1.0" },
    { value: "CERN", label: "CERN" },
    { value: "CERN-OHL-1.2", label: "CERN-OHL-1.2" },
    { value: "CERN-OHL-P-2.0", label: "CERN-OHL-P-2.0" },
    { value: "CERN-OHL-S-2.0", label: "CERN-OHL-S-2.0" },
    { value: "CERN-OHL-W-2.0", label: "CERN-OHL-W-2.0" },
    { value: "GPL", label: "GPL" },
    { value: "GPL-3.0-only", label: "GPL-3.0-only" },
    { value: "GPL-3.0-or-later", label: "GPL-3.0-or-later" },
    { value: "MIT", label: "MIT" },
    { value: "Other", label: "Other" },
    { value: "Solderpad", label: "Solderpad" },
    { value: "TAPR", label: "TAPR" }
]

const OSH_SOFTWARE_LICENSES = [
    { value: "Apache", label: "Apache" },
    { value: "CC-BY-4.0", label: "CC-BY-4.0" },
    { value: "CC-BY-SA-4.0", label: "CC-BY-SA-4.0" },
    { value: "CC0-1.0", label: "CC0-1.0" },
    { value: "CERN-OHL-P-2.0", label: "CERN-OHL-P-2.0" },
    { value: "CERN-OHL-S-2.0", label: "CERN-OHL-S-2.0" },
    { value: "CERN-OHL-W-2.0", label: "CERN-OHL-W-2.0" },
    { value: "GPL", label: "GPL" },
    { value: "GPL-3.0-only", label: "GPL-3.0-only" },
    { value: "GPL-3.0-or-later", label: "GPL-3.0-or-later" },
    { value: "LGPL", label: "LGPL" },
    { value: "MIT", label: "MIT" },
    { value: "Mozilla", label: "Mozilla" },
    { value: "No software", label: "No software" },
    { value: "Other", label: "Other" }
]

const OSOR_TOPICS = {
    "Digital government": [
        "Business and competition",
        "Collaboration",
        "Demography and population",
        "Digital-ready policymaking",
        "Digital government",
        "eDelivery and eInvoicing",
        "eIdentity and eSignature",
        "eInclusion",
        "eParticipation and eVoting",
        "eProcurement",
        "European Policies",
        "Interoperable Europe policy",
        "Legal",
        "Observatories",
        "Smart cities",
        "Social",
        "Tools"
    ],
    "Economics": [
        "Banking and financial services",
        "Industry and production",
        "Taxation",
        "Trade"
    ],
    "Education": [
        "Culture and education",
        "Languages and translation",
        "Science and technology"
    ],
    "Energy and environment": [
        "Energy and environment"
    ],
    "Health": [
        "eHealth"
    ],
    "ICT": [
        "Content and knowledge management",
        "ICT",
        "Licensing",
        "Open Source Software",
        "Reusable Software Components",
        "Semantics",
        "Standardisation",
        "Statistics and information"
    ],
    "Innovation": [
        "Advanced data analytics",
        "AI Chatbot",
        "AI Machine translation",
        "AI Named entity recognition",
        "Artificial intelligence",
        "Blockchain",
        "Digital innovation",
        "Extended reality",
        "High performance computing",
        "Internet of Things",
        "Optical Character Recognition",
        "Robotic Process Automation"
    ],
    "Transport": [
        "Geospatial",
        "Land transport",
        "Maritime and inland waterway transport"
    ]
}

const container = document.getElementById('tag-input');
                            
// Create the internal input
const input = document.createElement('input');
input.id = 'taginputtext';
input.type = 'text';
input.placeholder = 'Click to open the filter...';
input.readOnly = true;
input.style.cursor = 'pointer';
container.appendChild(input);

// ****************************
// Create the combo for countries
const comboCountries = document.createElement('div');
comboCountries.style.background = '#fff';
comboCountries.style.border = '1px solid #000';
comboCountries.style.borderRadius = '4px';
comboCountries.style.padding = '8px';
comboCountries.style.position = 'absolute';
comboCountries.style.minWidth = '300px';
comboCountries.style.maxWidth = '782px';
comboCountries.style.minHeight = '100px';
comboCountries.style.marginTop = '-447px';
comboCountries.style.marginLeft = '-14px';
comboCountries.innerHTML = '<table cellpadding="0" cellspacing="0" style="width: 100%; border: 0; font-size: 13px;">' +
                     '<tr>' +
                       '<td style="width: 100%; border: 0; text-align: right; padding: 1px 4px 1px 0; font-weight: 600; font-size: 14px;" colspan="8"> ' +
                          '<a href="#" alt="Close filter" title="Close filter" style="color: #98aaf1; border: 1px solid #2943ab; border-radius: 2px; padding: 6px 14px 6px 14px; background: #1a2f80; margin-right: -6px ! important;" onmousedown="javascript:openCloseTagFilter(false);">X</a>' +
                       '</td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Austria" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Austria" style="color: #2e4ec7;" onmousedown="checkCountry(\'Austria\')">Austria</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="France" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="France" style="color: #2e4ec7;" onmousedown="checkCountry(\'France\')">France</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Malta" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Malta" style="color: #2e4ec7;" onmousedown="checkCountry(\'Malta\')">Malta</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Australia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Australia" onmousedown="checkCountry(\'Australia\')">Australia</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Belgium" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Belgium" style="color: #2e4ec7;" onmousedown="checkCountry(\'Belgium\')">Belgium</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Germany" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Germany" style="color: #2e4ec7;" onmousedown="checkCountry(\'Germany\')">Germany</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Netherlands" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Netherlands" style="color: #2e4ec7;" onmousedown="checkCountry(\'Netherlands\')">Netherlands</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Brazil" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Brazil" onmousedown="checkCountry(\'Brazil\')">Brazil</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Bulgary" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Bulgary" style="color: #2e4ec7;" onmousedown="checkCountry(\'Bulgary\')">Bulgary</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Greece" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Greece" style="color: #2e4ec7;" onmousedown="checkCountry(\'Greece\')">Greece</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Poland" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;" onmousedown="checkCountry(\'Poland\')"><label for="Poland" style="color: #2e4ec7;">Poland</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Canada" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Canada" onmousedown="checkCountry(\'Canada\')">Canada</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Croatia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Croatia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Croatia\')">Croatia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Hungary" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Hungary" style="color: #2e4ec7;" onmousedown="checkCountry(\'Hungary\')">Hungary</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Portugal" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Portugal" style="color: #2e4ec7;" onmousedown="checkCountry(\'Portugal\')">Portugal</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="China" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="China" onmousedown="checkCountry(\'China\')">China</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Cyprus" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Cyprus" style="color: #2e4ec7;" onmousedown="checkCountry(\'Cyprus\')">Cyprus</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Ireland" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Ireland" style="color: #2e4ec7;" onmousedown="checkCountry(\'Ireland\')">Ireland</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Romania" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Romania" style="color: #2e4ec7;" onmousedown="checkCountry(\'Romania\')">Romania</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Great Britain" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Great Britain" onmousedown="checkCountry(\'Great Britain\')">Great Britain</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Czechia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Czechia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Czechia\')">Czechia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Italy" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Italy" style="color: #2e4ec7;" onmousedown="checkCountry(\'Italy\')">Italy</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Slovakia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%;border-right: 1px dotted #000; border-bottom: 0;"><label for="Slovakia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Slovakia\')">Slovakia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="India" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="India" onmousedown="checkCountry(\'India\')">India</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Denmark" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Denmark" style="color: #2e4ec7;" onmousedown="checkCountry(\'Denmark\')">Denmark</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Latvia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Latvia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Latvia\')">Latvia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Slovenia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Slovenia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Slovenia\')">Slovenia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Japan" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Japan" onmousedown="checkCountry(\'Japan\')">Japan</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Estonia" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Estonia" style="color: #2e4ec7;" onmousedown="checkCountry(\'Estonia\')">Estonia</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Lithuania" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Lithuania" style="color: #2e4ec7;" onmousedown="checkCountry(\'Lithuania\')">Lithuania</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Spain" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Spain" style="color: #2e4ec7;" onmousedown="checkCountry(\'Spain\')">Spain</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="South Korea" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="South Korea" onmousedown="checkCountry(\'South Korea\')">South Korea</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Finland" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Finland" style="color: #2e4ec7;" onmousedown="checkCountry(\'Finland\')">Finland</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Luxembourg" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="Luxembourg" style="color: #2e4ec7;" onmousedown="checkCountry(\'Luxembourg\')">Luxembourg</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="Sweden" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-right: 1px dotted #000; border-bottom: 0;"><label for="Sweden" style="color: #2e4ec7;" onmousedown="checkCountry(\'Sweden\')">Sweden</label></td>' +
                       '<td style="width: 2%; border: 0; text-align: center;"><input type="checkbox" id="United States" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border: 0;"><label for="United States" onmousedown="checkCountry(\'United States\')">United States</label></td>' +
                     '</tr>' +
                     '<tr>' +
                       '<td style="width: 2%; border-bottom: 0; text-align: center;"><input type="checkbox" id="European Union" style="min-width: 10px; important;" onmousedown="checkCountry(this.id)"></td>' +
                       '<td style="width: 23%; border-bottom: 0; font-weight: 600;"><label for="European Union" style="color: #2e4ec7;" onmousedown="checkCountry(\'European Union\')">European Union</label></td>' +
                       '<td style="width: 50%; border-right: 1px dotted #000; border-bottom: 0;" colspan="4"></td>' +
                       '<td style="width: 25%; border: 0;" colspan="2"></td>' +
                     '</tr>' +
                    '</table>';
comboCountries.style.visibility = 'hidden';
container.appendChild(comboCountries);
// ****************************

// ****************************
// Create the combo for project types
if (document.getElementById('selectprojecttype') != null) {
    OSH_PROJECT_TYPES.forEach(item => {
        const option = document.createElement('option');
        option.value = item.value;
        option.textContent = item.label;
        document.getElementById('selectprojecttype').appendChild(option);
    });
}
// ****************************

// ****************************
// Create the combo for hardware licenses
if (document.getElementById('selecthardwarelicense') != null) {
    OSH_HARDWARE_LICENSES.forEach(item => {
        const option = document.createElement('option');
        option.value = item.value;
        option.textContent = item.label;
        document.getElementById('selecthardwarelicense').appendChild(option);
    });
}
// ****************************

// ****************************
// Create the combo for software licenses
if (document.getElementById('selectsoftwarelicense') != null) {
    OSH_SOFTWARE_LICENSES.forEach(item => {
        const option = document.createElement('option');
        option.value = item.value;
        option.textContent = item.label;
        document.getElementById('selectsoftwarelicense').appendChild(option);
    });
}
// ****************************

// ****************************
// Create the combo for OSOR topics
if (document.getElementById('selecttopic') != null) {
    Object.keys(OSOR_TOPICS).forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        document.getElementById('selecttopic').appendChild(option);
    });
}
// ****************************


// Get focus when clicking
container.addEventListener('click', (event) => {
    input.focus();
    let openClose = true; 
    if (event.target.id == 'taginputtext') {
        openClose = comboCountries.style.visibility == 'hidden';
    }
    openCloseTagFilter(openClose);
});


// Function: Open/close the tag filter
function openCloseTagFilter(open) {
    comboCountries.style.visibility = open ? 'visible' : 'hidden';
}


// Function: Check a country
function checkCountry(id) {
    const tags = container.querySelectorAll('.tag');
    tagsContent = getTags();
    if (document.getElementById(id).checked) {
        if (tagsContent.length > 0) {
            tags.forEach(tag => {
                if (tag.textContent.trim() === id) {
                    tag.remove();
                }
            });
            tagsContent.splice(tagsContent.indexOf(id), 1);
        }
    } else {
        if (tagsContent.indexOf(id) == -1) {
            createTag(id);
        }
    }
}


// Function: Create tag
function createTag(text) {
    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.style.background = '#ccd7ff';
                            
    tag.innerHTML = `
        ${text}
        `;
                            
    container.insertBefore(tag, input);
}


// Function: Get all the tags
function getTags() {
    const tags = container.querySelectorAll('.tag');
    return Array.from(tags).map(tag => {
        return tag.textContent.trim();
    });
}


// Function: Remove all the tags
function removeAllTags() {
    tagsContent = getTags();
    if (tagsContent.length > 0) {
        for (let i = 0;i < tagsContent.length;i++) {
            document.getElementById(tagsContent[i]).checked = false;
        }
    }

    const tags = container.querySelectorAll('.tag');
    tags.forEach(tag => tag.remove());
}


// Function: Update the value of a range input label
function updateRangeLabelValue(id, value) {
    document.getElementById(id).textContent = value;
}


// Apply filters
function applyFilters(baseUrl, filterIndex) {
    let fragments = [];
    // Filter 1: Is one of country
    if (filterIndex == 1) {
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
        let textfrompctElement = document.getElementById("textfrompct");
        if (textfrompctElement !== null && textfrompctElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenPercentagesFilter());
        }
        let selectProjectType = document.getElementById('selectprojecttype');
        if (selectProjectType != null && selectProjectType.selectedIndex > 0) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectHardwareLicense = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicense != null && selectHardwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
        let selectSoftwareLicense = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicense != null && selectSoftwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
        let selectTopic = document.getElementById('selecttopic');
        if (selectTopic != null && selectTopic.selectedIndex > 0) {
            fragments.push(applyIsOneOfTopicFilter());
        }
        fragments.push(applyIsOneOfCountryFilter());
    }
    // Filter 2: Is between years
    if (filterIndex == 2) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfrompctElement = document.getElementById("textfrompct");
        if (textfrompctElement !== null && textfrompctElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenPercentagesFilter());
        }
        let selectTopicElement = document.getElementById('selecttopic');
        if (selectTopicElement != null && selectTopicElement.selectedIndex > 0) {
            fragments.push(applyIsOneOfTopicFilter());
        }
        fragments.push(applyIsBetweenYearsFilter());
    }
    // Filter 3: Is between percentages
    if (filterIndex == 3) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
        fragments.push(applyIsBetweenPercentagesFilter());
    }
    // Filter 4: Is one of project type
    if (filterIndex == 4) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectHardwareLicense = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicense != null && selectHardwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
        let selectSoftwareLicense = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicense != null && selectSoftwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
        fragments.push(applyIsOneOfProjectTypeFilter());
    }
    // Filter 5: Is one of hardware license
    if (filterIndex == 5) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectProjectType = document.getElementById('selectprojecttype');
        if (selectProjectType != null && selectProjectType.selectedIndex > 0) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectSoftwareLicense = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicense != null && selectSoftwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
        fragments.push(applyIsOneOfHardwareLicenseFilter());
    }
    // Filter 6: Is one of software license
    if (filterIndex == 6) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectProjectType = document.getElementById('selectprojecttype');
        if (selectProjectType != null && selectProjectType.selectedIndex > 0) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectHardwareLicense = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicense != null && selectHardwareLicense.selectedIndex > 0) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
        fragments.push(applyIsOneOfSoftwareLicenseFilter());
    }
    // Filter 7: Is one of topic
    if (filterIndex == 7) {
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
        fragments.push(applyIsOneOfTopicFilter());
    }

    // Update the iframe
    document.getElementById("iframe").src = baseUrl + URL_FRAGMENT.replaceAll("{1}", fragments.join(","));
}


// Remove filters
function removeFilters(baseUrl, filterIndex) {
    let fragments = [];
    // Filter 1: Is one of country
    if (filterIndex == 1) {
        removeIsOneOfCountryFilter();
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
        let textfrompctElement = document.getElementById("textfrompct");
        if (textfrompctElement !== null && textfrompctElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenPercentagesFilter());
        }
        let selectProjectTypeElement = document.getElementById('selectprojecttype');
        if (selectProjectTypeElement !== null && selectProjectTypeElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectHardwareLicenseElement = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicenseElement !== null && selectHardwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
        let selectSoftwareLicenseElement = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicenseElement !== null && selectSoftwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
        let selectTopicElement = document.getElementById('selecttopic');
        if (selectTopicElement !== null && selectTopicElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfTopicFilter());
        }
    }
    // Filter 2: Is between years
    if (filterIndex == 2) {
        removeIsBetweenYearsFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfrompctElement = document.getElementById("textfrompct");
        if (textfrompctElement !== null && textfrompctElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenPercentagesFilter());
        }
        let selectTopicElement = document.getElementById('selecttopic');
        if (selectTopicElement !== null && selectTopicElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfTopicFilter());
        }
    }
    // Filter 3: Is between percentages
    if (filterIndex == 3) {
        removeIsBetweenPercentagesFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
    }
    // Filter 4: Is one of project type
    if (filterIndex == 4) {
        removeIsOneOfProjectTypeFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectHardwareLicenseElement = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicenseElement !== null && selectHardwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
        let selectSoftwareLicenseElement = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicenseElement !== null && selectSoftwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
    }
    // Filter 5: Is one of hardware license
    if (filterIndex == 5) {
        removeIsOneOfHardwareLicenseFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectProjectTypeElement = document.getElementById('selectprojecttype');
        if (selectProjectTypeElement !== null && selectProjectTypeElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectSoftwareLicenseElement = document.getElementById('selectsoftwarelicense');
        if (selectSoftwareLicenseElement !== null && selectSoftwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfSoftwareLicenseFilter());
        }
    }
    // Filter 6: Is one of software license
    if (filterIndex == 6) {
        removeIsOneOfSoftwareLicenseFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let selectProjectTypeElement = document.getElementById('selectprojecttype');
        if (selectProjectTypeElement !== null && selectProjectTypeElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfProjectTypeFilter());
        }
        let selectHardwareLicenseElement = document.getElementById('selecthardwarelicense');
        if (selectHardwareLicenseElement !== null && selectHardwareLicenseElement.classList.contains("filter-active-input")) {
            fragments.push(applyIsOneOfHardwareLicenseFilter());
        }
    }
    // Filter 7: Is one of topic
    if (filterIndex == 7) {
        removeIsOneOfTopicFilter();
        let textcountryElement = document.getElementById("textcountry");
        if (textcountryElement !== null && textcountryElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsOneOfCountryFilter());
        }
        let textfromElement = document.getElementById("textfrom");
        if (textfromElement !== null && textfromElement.classList.contains("filter-active-text")) {
            fragments.push(applyIsBetweenYearsFilter());
        }
    }

    // Update the iframe
    if (fragments.length > 0) {
        document.getElementById("iframe").src = baseUrl + URL_FRAGMENT.replaceAll("{1}", fragments.join(","));
    } else {
        document.getElementById("iframe").src = baseUrl;
    }
}


// Apply filter: Is one of country
function applyIsOneOfCountryFilter() {
    let fragment = "";

    // Remove duplicates
    let values = [...new Set(getTags())]

    // Replace white spaces and capitalize
    for (let i = 0;i < values.length;i++) {
        splitted = values[i].split(/\s+/);
        if (splitted.length > 1) {
            for (let j = 0;j < splitted.length;j++) {
                splitted[j] = splitted[j].charAt(0).toUpperCase() + splitted[j].slice(1).toLowerCase();
            }
            values[i] = splitted.join("%20");
        } else {
            values[i] = values[i].charAt(0).toUpperCase() + values[i].slice(1).toLowerCase();
        }
    }

    // Build the new URL
    if (values.length > 0) {
        let valuesAsString = values.length > 1 ? values.join(',') : values[0];
        fragment += "(meta:(key:country,params:!('" + valuesAsString + "'),type:phrases,value:'" + valuesAsString + "'),query:(bool:(minimum_should_match:1,should:!({2}))))";
        let query = "";
        for (let i = 0;i < values.length;i++) {
            if (i > 0) {
                query += ",";
            }
            query += "(match_phrase:(country:'" + values[i] + "'))";
        }

        // Adjust styles
        document.querySelector('#textcountry').classList.add("filter-active-text");

        // Update the fragment
        fragment = fragment.replaceAll("{2}", query);
    }
    
    // Return the fragment
    return fragment;
}


// Apply filter: Is between years
function applyIsBetweenYearsFilter() {
    let fragment = "";

    // Validate the filter
    document.getElementById("from").value = (document.getElementById("from").value == '' || parseInt(document.getElementById("from").value) < INF_YEAR)
        ? INF_YEAR
        : (parseInt(document.getElementById("from").value) > SUP_YEAR)
            ? SUP_YEAR
            : document.getElementById("from").value;
    document.getElementById("to").value = (document.getElementById("to").value == '' || parseInt(document.getElementById("to").value) > SUP_YEAR)
        ? SUP_YEAR
        : (parseInt(document.getElementById("to").value) < INF_YEAR)
            ? INF_YEAR
            : document.getElementById("to").value;

    if (parseInt(document.getElementById("from").value) > parseInt(document.getElementById("to").value)) {
        let from = parseInt(document.getElementById("from").value);
        document.getElementById("from").value = parseInt(document.getElementById("to").value);
        document.getElementById("to").value = from;
    }

    // Adjust styles
    document.querySelector('#textfrom').classList.add("filter-active-text");
    document.querySelector('#textto').classList.add("filter-active-text");

    // Update the range labels
    updateRangeLabelValue('valuefrom', document.getElementById("from").value);
    updateRangeLabelValue('valueto', document.getElementById("to").value);

    // Return the fragment
    fragment += "(meta:(key:year,type:range),range:(year:(gte:" + document.getElementById("from").value + ",lte:" + document.getElementById("to").value + ")))";
    return fragment;
}


// Apply filter: Is between percentages
function applyIsBetweenPercentagesFilter() {
    let fragment = "";

    // Validate the filter
    document.getElementById("frompct").value = (document.getElementById("frompct").value == '' || parseInt(document.getElementById("frompct").value) < INF_PERCENTAGE)
        ? INF_PERCENTAGE
        : (parseInt(document.getElementById("frompct").value) > SUP_PERCENTAGE)
            ? SUP_PERCENTAGE
            : document.getElementById("frompct").value;
    document.getElementById("topct").value = (document.getElementById("topct").value == '' || parseInt(document.getElementById("topct").value) > SUP_PERCENTAGE)
        ? SUP_PERCENTAGE
        : (parseInt(document.getElementById("topct").value) < INF_PERCENTAGE)
            ? INF_PERCENTAGE
            : document.getElementById("topct").value;
    
    if (parseInt(document.getElementById("frompct").value) > parseInt(document.getElementById("topct").value)) {
        let frompct = parseInt(document.getElementById("frompct").value);
        document.getElementById("frompct").value = parseInt(document.getElementById("topct").value);
        document.getElementById("topct").value = frompct;
    }

    // Adjust styles
    document.querySelector('#textfrompct').classList.add("filter-active-text");
    document.querySelector('#texttopct').classList.add("filter-active-text");

    // Update the range labels
    updateRangeLabelValue('valuefrompct', document.getElementById("frompct").value);
    updateRangeLabelValue('valuetopct', document.getElementById("topct").value);

    // Return the fragment
    fragment += "(meta:(key:share_pct,type:range),range:(share_pct:(gte:" + document.getElementById("frompct").value + ",lte:" + document.getElementById("topct").value + ")))";
    return fragment;
}


// Apply filter: Is one of project type
function applyIsOneOfProjectTypeFilter() {
    let fragment = "";

    if (document.getElementById('selectprojecttype').selectedIndex > 0) {
        // Adjust styles
        document.getElementById('selectprojecttype').classList.add("filter-active-input");

        // Build the fragment
        fragment += "(meta:(key:primary_type.keyword,type:phrase,value:'" + document.getElementById("selectprojecttype").value + "'),query:(bool:(minimum_should_match:1,should:!((match_phrase:(primary_type:'" + document.getElementById("selectprojecttype").value + "'))))))"
    }

    // Return the fragment
    return fragment;
}


// Apply filter: Is one of hardware license
function applyIsOneOfHardwareLicenseFilter() {
    let fragment = "";

    if (document.getElementById('selecthardwarelicense').selectedIndex > 0) {
        // Adjust styles
        document.getElementById('selecthardwarelicense').classList.add("filter-active-input");

        // Build the fragment
        fragment += "(meta:(key:hardware_license.keyword,type:phrase,value:'" + document.getElementById("selecthardwarelicense").value + "'),query:(bool:(minimum_should_match:1,should:!((match_phrase:(hardware_license:'" + document.getElementById("selecthardwarelicense").value + "'))))))"
    }

    // Return the fragment
    return fragment;
}


// Apply filter: Is one of software license
function applyIsOneOfSoftwareLicenseFilter() {
    let fragment = "";

    if (document.getElementById('selectsoftwarelicense').selectedIndex > 0) {
        // Adjust styles
        document.getElementById('selectsoftwarelicense').classList.add("filter-active-input");

        // Build the fragment
        fragment += "(meta:(key:software_license.keyword,type:phrase,value:'" + document.getElementById("selectsoftwarelicense").value + "'),query:(bool:(minimum_should_match:1,should:!((match_phrase:(software_license:'" + document.getElementById("selectsoftwarelicense").value + "'))))))"
    }

    // Return the fragment
    return fragment;
}


// Apply filter: Is one of topic
function applyIsOneOfTopicFilter() {
    let fragment = "";

    if (document.getElementById('selecttopic').selectedIndex > 0) {
        // Adjust styles
        document.getElementById('selecttopic').classList.add("filter-active-input");

        // Build the fragment
        const topicValue = document.getElementById("selecttopic").value;
        fragment += `(bool:(minimum_should_match:1,should:!((term:(primary_topic.keyword:'${topicValue}')),(term:(secondary_topic.keyword:'${topicValue}')))),meta:(value:'{"minimum_should_match":1,"should":[{"term":{"primary_topic.keyword":"${topicValue}"}},{"term":{"secondary_topic.keyword":"${topicValue}"}}]}'))`;
    }

    // Return the fragment
    return fragment;
}


// Remove filter: Is one of country
function removeIsOneOfCountryFilter() {
    // Remove all the tags
    removeAllTags();

    // Adjust styles
    document.querySelector('#textcountry').classList.remove("filter-active-text");
    document.getElementById('taginputtext').classList.remove("filter-active-input");
}


// Remove filter: Is between years
function removeIsBetweenYearsFilter() {
    // Reset values
    document.getElementById("from").value = INF_YEAR;
    document.getElementById("to").value = SUP_YEAR;

    // Adjust styles
    document.querySelector('#textfrom').classList.remove("filter-active-text");
    document.querySelector('#textto').classList.remove("filter-active-text");

    // Update the range labels
    updateRangeLabelValue('valuefrom', INF_YEAR);
    updateRangeLabelValue('valueto', SUP_YEAR);
}


// Remove filter: Is between percentages
function removeIsBetweenPercentagesFilter() {
    // Reset values
    document.getElementById("frompct").value = INF_PERCENTAGE;
    document.getElementById("topct").value = SUP_PERCENTAGE;

    // Adjust styles
    document.querySelector('#textfrompct').classList.remove("filter-active-text");
    document.querySelector('#texttopct').classList.remove("filter-active-text");

    // Update the range labels
    updateRangeLabelValue('valuefrompct', INF_PERCENTAGE);
    updateRangeLabelValue('valuetopct', SUP_PERCENTAGE);
}


// Remove filter: Is one of project type
function removeIsOneOfProjectTypeFilter() {
    // Reset values
    document.getElementById('selectprojecttype').selectedIndex = 0,

    // Adjust styles
    document.getElementById('selectprojecttype').classList.remove("filter-active-input");
}


// Remove filter: Is one of hardware license
function removeIsOneOfHardwareLicenseFilter() {
    // Reset values
    document.getElementById('selecthardwarelicense').selectedIndex = 0,

    // Adjust styles
    document.getElementById('selecthardwarelicense').classList.remove("filter-active-input");
}


// Remove filter: Is one of software license
function removeIsOneOfSoftwareLicenseFilter() {
    // Reset values
    document.getElementById('selectsoftwarelicense').selectedIndex = 0,

    // Adjust styles
    document.getElementById('selectsoftwarelicense').classList.remove("filter-active-input");
}


// Remove filter: Is one of topic
function removeIsOneOfTopicFilter() {
    // Reset values
    document.getElementById('selecttopic').selectedIndex = 0,

    // Adjust styles
    document.getElementById('selecttopic').classList.remove("filter-active-input");
}


// Share chart
function save(chartName, fileName) {
    // Built the chart name
    chartName = 'Chart: ' + chartName;
    
    // Build the file name
    var now = new Date();
    var year = now.getFullYear();
    var month = String(now.getMonth() + 1).padStart(2, '0');
    var day = String(now.getDate()).padStart(2, '0');
    var hour = String(now.getHours()).padStart(2, '0');
    var min = String(now.getMinutes()).padStart(2, '0');
    var formattedDate = `${year}${month}${day}${hour}${min}`;
    fileName = `${fileName}_${formattedDate}.html`;

    // Build the HTML content
    var html = '<html>' +
                    '<body style="background-color: #1a2f80;">' +
                        '<div style="margin: 24px;">' +
                            '<p style="color: #fff; font-size: 22pt;">' + chartName + '</p>' +
                            //'<p style="color: #fff; font-size: 13pt;">' + document.getElementById('descriptive-text').innerHTML + '</p>' +
                            '<iframe src="' + document.getElementById('iframe').src + '" style="width: 1024px; height: 600px;"></iframe>' +
                        '</div>' +
                    '</body>' +
                '</html>';
    var blob = new Blob([html], { type: 'text/html' });
    var url = URL.createObjectURL(blob);

    // Create the "hidden link"
    var link = document.createElement('a');
    link.href = url;
    link.download = fileName;

    // Add the "hidden link" to the document
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
