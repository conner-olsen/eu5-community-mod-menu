const { createApp, reactive, computed, ref, watch } = Vue;

const app = createApp({
    setup() {
        const state = reactive({
            mod_id: '',
            file_prefix: '',
            mod_name: '',
            mod_desc: '',
            metadata_name: '',
            metadata_id: '',
            metadata_version: '0.1',
            metadata_short_description: '',
            metadata_tags: ['Utilities'],
            metadata_game_version: '1.1.*',
            tabs: [],
        });

        const selectedTabIdx = ref(0);
        const selectedGroupIdx = ref(0);
        const rightTab = ref('preview');
        const showImport = ref(false);
        const importPath = ref('');
        const importWarnings = ref([]);

        const selectedTab = computed(() => state.tabs[selectedTabIdx.value] || null);
        const selectedGroup = computed(() => {
            const tab = selectedTab.value;
            if (!tab) return null;
            return tab.groups[selectedGroupIdx.value] || null;
        });

        watch(() => state.tabs.length, () => {
            if (selectedTabIdx.value >= state.tabs.length) {
                selectedTabIdx.value = Math.max(0, state.tabs.length - 1);
            }
        });

        watch(selectedTabIdx, () => {
            selectedGroupIdx.value = 0;
        });

        function sanitizeId(obj, key) {
            obj[key] = obj[key].replace(/[^a-z0-9_]/gi, '').toLowerCase();
        }

        function addTab() {
            state.tabs.push({
                tab_id: '',
                name: '',
                groups: [],
            });
            selectedTabIdx.value = state.tabs.length - 1;
            selectedGroupIdx.value = 0;
        }

        function removeTab(i) {
            state.tabs.splice(i, 1);
            if (selectedTabIdx.value >= state.tabs.length) {
                selectedTabIdx.value = Math.max(0, state.tabs.length - 1);
            }
        }

        function addGroup() {
            const tab = selectedTab.value;
            if (!tab) return;
            tab.groups.push({
                group_id: '',
                name: '',
                settings: [],
            });
            selectedGroupIdx.value = tab.groups.length - 1;
        }

        function removeGroup(i) {
            const tab = selectedTab.value;
            if (!tab) return;
            tab.groups.splice(i, 1);
            if (selectedGroupIdx.value >= tab.groups.length) {
                selectedGroupIdx.value = Math.max(0, tab.groups.length - 1);
            }
        }

        function addSetting() {
            const group = selectedGroup.value;
            if (!group) return;
            group.settings.push({
                setting_id: '',
                setting_type: 'bool',
                is_global: false,
                name: '',
                desc: '',
                default_value: 0,
                button_text: 'Run',
                min_value: 0,
                max_value: 100,
                step_value: 1,
                default_index: 0,
                option_count: 3,
                options: [
                    { index: 0, name: 'Option 1' },
                    { index: 1, name: 'Option 2' },
                    { index: 2, name: 'Option 3' },
                ],
                character_limit: 42,
                quote_text: 0,
                item_count: 3,
                is_ordered: 1,
                item_column_name: 'Item',
                item_names: ['Item A', 'Item B', 'Item C'],
                fields: [],
            });
        }

        function removeSetting(i) {
            const group = selectedGroup.value;
            if (group) group.settings.splice(i, 1);
        }

        function moveSetting(i, dir) {
            const group = selectedGroup.value;
            if (!group) return;
            const j = i + dir;
            if (j < 0 || j >= group.settings.length) return;
            const temp = group.settings[i];
            group.settings[i] = group.settings[j];
            group.settings[j] = temp;
        }

        function onUpdate(data) {
            Object.assign(state, data);
        }

        async function generateAndDownload() {
            try {
                const resp = await fetch('/api/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(state),
                });
                if (!resp.ok) {
                    const err = await resp.json();
                    alert('Error: ' + (err.error || 'Unknown error'));
                    return;
                }
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = (state.file_prefix || state.mod_id || 'cmm_mod') + '_cmm_integration.zip';
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert('Download failed: ' + e.message);
            }
        }

        async function importFromDir() {
            importWarnings.value = [];
            try {
                const resp = await fetch('/api/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ directory: importPath.value }),
                });
                const data = await resp.json();
                if (data.error) {
                    importWarnings.value = [data.error];
                    return;
                }
                if (data._warnings) {
                    importWarnings.value = data._warnings;
                }
                // Apply imported data
                const warnings = data._warnings;
                delete data._warnings;
                Object.assign(state, data);
                selectedTabIdx.value = 0;
                selectedGroupIdx.value = 0;
                if (!importWarnings.value.length) {
                    showImport.value = false;
                }
            } catch (e) {
                importWarnings.value = ['Import failed: ' + e.message];
            }
        }

        return {
            state, selectedTabIdx, selectedGroupIdx, rightTab,
            showImport, importPath, importWarnings,
            selectedTab, selectedGroup,
            sanitizeId, addTab, removeTab, addGroup, removeGroup,
            addSetting, removeSetting, moveSetting, onUpdate,
            generateAndDownload, importFromDir,
        };
    },
});

// Register components
app.component('mod-editor', ModEditorComponent);
app.component('setting-editor', SettingEditorComponent);
app.component('list-editor', ListEditorComponent);
app.component('dropdown-options', DropdownOptionsComponent);
app.component('preview-panel', PreviewPanelComponent);
app.component('code-panel', CodePanelComponent);
app.component('localization-panel', LocalizationPanelComponent);

app.mount('#app');
