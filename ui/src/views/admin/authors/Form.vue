<template>
    <b-row class="justify-content-md-center">
        <b-col lg="8" md="auto">
            <div class="form">
                <!-- prettier-ignore -->
                <b-form @submit.prevent="onSubmit" autocomplete="off">
                    <b-form-group
                        id="input-group-1"
                        label="First Name"
                        label-for="first_name"
                    >
                        <b-form-input
                            id="first_name"
                            placeholder="First Name"
                            v-model="form.first_name"
                            :class="{'is-invalid': hasError('first_name')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('first_name')"
                            v-text="getError('first_name')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        id="input-group-2"
                        label="Last Name"
                        label-for="last_name"
                    >
                        <b-form-input
                            id="last_name"
                            placeholder="Last Name"
                            v-model="form.last_name"
                            :class="{'is-invalid': hasError('last_name')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('last_name')"
                            v-text="getError('last_name')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Gender"
                    >
                        <b-form-radio-group
                            id="radio-group-1"
                            v-model="form.gender"
                            :class="{'is-invalid': hasError('gender')}"
                        >
                            <b-form-radio value="M">Male</b-form-radio>
                            <b-form-radio value="F">Female</b-form-radio>
                        </b-form-radio-group>
                        <b-form-invalid-feedback
                            v-if="hasError('gender')"
                            v-text="getError('gender')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        id="input-group-3"
                        label="About"
                        label-for="about"
                    >
                        <vue-simplemde
                            id="about"
                            v-model="form.about"
                            :configs="configs"
                        ></vue-simplemde>
                    </b-form-group>
                    <p
                        class="sm-8 invalid"
                        v-if="hasError('about')"
                        v-text="getError('about')"
                    ></p>
                    <b-button type="submit" variant="primary">Save</b-button>
                </b-form>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import VueSimplemde from 'vue-simplemde';
import formMixin from '@/mixins/form';

export default {
    name: 'AuthorForm',
    mixins: [formMixin],
    components: {
        VueSimplemde,
    },
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
    data() {
        return {
            configs: {
                hideIcons: ['image', 'link'],
            },
        };
    },
    methods: {
        onSubmit() {
            this.$emit('save:author', this.form);
        },
    },
};
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';
</style>
