const DropdownOptionsComponent = {
    props: ['setting'],
    template: `
    <div class="dropdown-options">
        <h5>Options</h5>
        <div v-for="(opt, i) in (setting.options || [])" :key="i" class="field-row compact">
            <label class="compact-label">{{ i }}</label>
            <input v-model="opt.name" :placeholder="'Option ' + (i + 1)">
        </div>
    </div>
    `,
};
