// @ts-nocheck
const Index = () => import('@/views/Index');
const Login = () => import('@/views/Login');
const NotFound = () => import('@/views/NotFound');

// /admin
const AdminIndex = () => import('@/views/admin/Index');
const Dashboard = () => import('@/views/admin/Dashboard');

// /admin/categories
const CategoriesIndex = () => import('@/views/admin/categories/Index');
const CategoriesListing = () => import('@/views/admin/categories/Listing');
const CategoriesAdd = () => import('@/views/admin/categories/Add');
const CategoriesEdit = () => import('@/views/admin/categories/Edit');

// /admin/authors
const AuthorsIndex = () => import('@/views/admin/authors/Index');
const AuthorsListing = () => import('@/views/admin/authors/Listing');
const AuthorsAdd = () => import('@/views/admin/authors/Add');
const AuthorsEdit = () => import('@/views/admin/authors/Edit');

export default [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/admin',
        component: AdminIndex,
        meta: {
            authRequired: true,
        },
        children: [
            {
                path: '',
                name: 'dashboard',
                component: Dashboard,
                meta: {
                    authRequired: true,
                },
            },
            {
                path: 'categories',
                component: CategoriesIndex,
                meta: {
                    authRequired: true,
                },
                children: [
                    {
                        path: '',
                        name: 'categories.index',
                        component: CategoriesListing,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: 'add',
                        name: 'categories.add',
                        component: CategoriesAdd,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: ':id/edit',
                        props: true,
                        name: 'categories.edit',
                        component: CategoriesEdit,
                        meta: {
                            authRequired: true,
                        },
                    },
                ],
            },
            {
                path: 'authors',
                component: AuthorsIndex,
                meta: {
                    authRequired: true,
                },
                children: [
                    {
                        path: '',
                        name: 'authors.index',
                        component: AuthorsListing,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: 'add',
                        name: 'authors.add',
                        component: AuthorsAdd,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: ':id/edit',
                        props: true,
                        name: 'authors.edit',
                        component: AuthorsEdit,
                        meta: {
                            authRequired: true,
                        },
                    },
                ],
            },
        ],
    },
    {
        path: '*',
        name: '404',
        component: NotFound,
    },
];
