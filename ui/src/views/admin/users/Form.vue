<template>
    <b-row class="justify-content-md-center">
        <b-col lg="8" md="auto">
            <div class="form">
                <!-- prettier-ignore -->
                <b-form @submit.prevent="onSubmit" autocomplete="off">
                    <b-form-group
                        label="Username"
                        label-for="username"
                    >
                        <b-form-input
                            id="username"
                            placeholder="Username"
                            v-model="form.username"
                            :class="{'is-invalid': hasError('username')}"
                            required trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('username')"
                            v-text="getError('username')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Password"
                        label-for="password"
                        :description="passwordDescription"
                    >
                        <b-form-input
                            id="password"
                            placeholder="Password"
                            type="password"
                            v-model="form.password"
                            :class="{'is-invalid': hasError('password')}"
                            :required="!form.id"
                            trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('password')"
                            v-text="getError('password')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group
                        label="Confirm Password"
                        label-for="confirm_password"
                    >
                        <b-form-input
                            id="confirm_password"
                            placeholder="Confirm Password"
                            type="password"
                            v-model="form.confirm_password"
                            :class="{'is-invalid': hasError('confirm_password')}"
                            :required="!form.id"
                            trim lazy
                        ></b-form-input>
                        <b-form-invalid-feedback
                            v-if="hasError('confirm_password')"
                            v-text="getError('confirm_password')"
                        ></b-form-invalid-feedback>
                    </b-form-group>
                    <b-form-group>
                        <b-form-checkbox
                            v-model="form.is_admin"
                            name="admin"
                            value="true"
                            unchecked-value="false"
                        >Admin</b-form-checkbox>
                        <b-form-invalid-feedback
                            v-if="hasError('is_admin')"
                            v-text="getError('is_admin')"
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
    name: 'AuthorForm',
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
    computed: {
        passwordDescription() {
            const { id } = this.form;
            let message = 'Please enter a strong password';
            if (id) {
                message = 'Password is not required';
            }

            return message;
        },
    },
    methods: {
        onSubmit() {
            this.$emit('save:user', this.form);
        },
    },
};
</script>
