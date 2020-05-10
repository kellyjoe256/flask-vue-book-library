<template>
    <b-row class="justify-content-md-center">
        <b-col lg="8" md="auto">
            <div class="form">
                <!-- prettier-ignore -->
                <b-form @submit.prevent="onSubmit" autocomplete="off">
                    <b-form-group
                        id="input-group-1"
                        label="Name"
                        label-for="name"
                    >
                        <b-form-input
                            id="name"
                            placeholder="Name"
                            v-model="form.name"
                            :class="{'is-invalid': hasError('name')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('name')"
                            v-text="getError('name')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-form>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import formMixin from '@/mixins/form';

export default {
    name: 'CategoryForm',
    mixins: [formMixin],
    props: {
        form: {
            type: Object,
            required: true,
        },
        errors: {
            type: Object,
            required: true,
        },
    },
    methods: {
        onSubmit() {
            this.$emit('save:category', this.form);
        },
    },
};
</script>
