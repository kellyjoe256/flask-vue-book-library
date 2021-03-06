// @ts-nocheck
const Index = () => import('@/views/Index');
const Login = () => import('@/views/Login');
const NotFound = () => import('@/views/NotFound');
const BookDetails = () => import('@/views/BookDetails');

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

// /admin/books
const BooksIndex = () => import('@/views/admin/books/Index');
const BooksListing = () => import('@/views/admin/books/Listing');
const BooksAdd = () => import('@/views/admin/books/Add');
const BooksEdit = () => import('@/views/admin/books/Edit');

// /admin/users
const UsersIndex = () => import('@/views/admin/users/Index');
const UsersListing = () => import('@/views/admin/users/Listing');
const UsersAdd = () => import('@/views/admin/users/Add');
const UsersEdit = () => import('@/views/admin/users/Edit');

export default [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/:id/book_details',
        name: 'book.details',
        props: true,
        component: BookDetails,
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
            {
                path: 'books',
                component: BooksIndex,
                meta: {
                    authRequired: true,
                },
                children: [
                    {
                        path: '',
                        name: 'books.index',
                        component: BooksListing,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: 'add',
                        name: 'books.add',
                        component: BooksAdd,
                        meta: {
                            authRequired: true,
                        },
                    },
                    {
                        path: ':id/edit',
                        props: true,
                        name: 'books.edit',
                        component: BooksEdit,
                        meta: {
                            authRequired: true,
                        },
                    },
                ],
            },
            {
                path: 'users',
                component: UsersIndex,
                meta: {
                    authRequired: true,
                    adminRequired: true,
                },
                children: [
                    {
                        path: '',
                        name: 'users.index',
                        component: UsersListing,
                        meta: {
                            authRequired: true,
                            adminRequired: true,
                        },
                    },
                    {
                        path: 'add',
                        name: 'users.add',
                        component: UsersAdd,
                        meta: {
                            authRequired: true,
                            adminRequired: true,
                        },
                    },
                    {
                        path: ':id/edit',
                        props: true,
                        name: 'users.edit',
                        component: UsersEdit,
                        meta: {
                            authRequired: true,
                            adminRequired: true,
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
