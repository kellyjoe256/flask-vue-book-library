// @ts-nocheck
const Index = () => import('@/views/Index');
const Dashboard = () => import('@/views/Dashboard');
const Login = () => import('@/views/Login');
const NotFound = () => import('@/views/NotFound');

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
        component: Dashboard,
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
        ],
    },
    {
        path: '*',
        name: '404',
        component: NotFound,
    },
];
