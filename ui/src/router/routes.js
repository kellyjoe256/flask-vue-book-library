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
        ],
    },
    {
        path: '*',
        name: '404',
        component: NotFound,
    },
];
