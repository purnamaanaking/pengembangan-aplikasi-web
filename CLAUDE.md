# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Hands-on (praktikum) work for the *Pengembangan Aplikasi Web* course. Student handouts live in `docs/modul-praktikum/*.docx`, and each folder `modul-NN-*/` is a working Laravel 13 app that reproduces one handout. Course material, test notes and commit messages are in Indonesian; keep new docs and commits consistent with that.

There is no root-level `composer.json` or `package.json`. **Every command below runs from inside a module folder.**

## Layout

- `modul-09-routing/` — routing, Vite + Bootstrap/Sass bundling. All behaviour is in `routes/web.php` (closures, `Route::view`, redirect, parameters, `where()`, named routes, prefix/group, fallback) plus a small `RouteController`.
- `modul-10-controller-view/` — `HomeController` (basic), `ProfileController` (invokable), `EmployeeController` (`Route::resource`, with Validator-based `store`) and Blade views.
- `modul-11-database-dasar/` — Modul 10's app plus MySQL `data_master`: migrations and seeders for `positions`/`employees` (FK `position_id`), and `EmployeeController` using raw SQL (`DB::select` with `left join`) and query builder for index/create/store/show/destroy. `edit`/`update` are still empty stubs (the edit feature is the handout's homework). New view `employee/show`.
- `modul-12-database-lanjut/` — Modul 11's app converted to Eloquent (`Position hasMany Employee`, `Employee belongsTo Position`) with full CRUD including `employee/edit`, and a Blade layout: `layouts/app` (`@yield('content')`), `layouts/nav` (active link via `Route::currentRouteName()`), `default`, and `employee/actions` (`@include`d per row).
- `docs/modul-praktikum/` — the `.docx` handouts. They are the source of truth for what a module's code should look like. A request to "adjust the modul" means these files.
- `docs/CATATAN-UJI-MODUL-NN.md` — test notes from walking through each handout step by step, recording where the handout and the working code diverge.

Modules are independent snapshots, not a chain: each is a separate `composer create-project` skeleton, created from `main` (Modul 10 does not build on Modul 09; Modul 11 and 12 continue the previous handout, so the previous module's end state was copied into the fresh skeleton as the starting point). Do not share code between them or hoist dependencies. Work for a new module goes in `modul-NN-slug/` on a branch `praktikum/modul-NN-slug`, merged into `main` with a merge commit; commits look like `Praktikum Modul 10: Pengenalan Controller dan View pada Laravel`.

## Commands (inside a module folder)

```sh
composer setup                 # install, copy .env, key:generate, migrate, npm install, npm run build
composer dev                   # `php artisan dev` runs serve + queue:listen + pail + `npm run dev` together
php artisan serve && npm run dev   # or run just the two you need, in separate terminals
npm run build                  # production Vite build into public/build (gitignored)
php artisan route:list         # routes are the main thing these modules teach
php artisan route:clear        # after `route:cache`, which the Modul 09 handout exercises

composer test                  # = config:clear + php artisan test
php artisan test --filter=test_the_application_returns_a_successful_response
php artisan test tests/Feature/ExampleTest.php
```

When stdout is not a TTY, `php artisan test` prints a single JSON line (from `laravel/pao`), not the usual PHPUnit report.

Tested with PHP 8.4 (`composer.json` requires `^8.3`), Node 24, Laravel 13.x, Vite 8, Bootstrap 5.3. `.npmrc` sets `ignore-scripts=true`.

## Things that are easy to get wrong

- **Views need a Vite manifest.** Every view calls `@vite(...)`, and `public/build/` is gitignored. On a fresh checkout, run `npm run build` (or keep `npm run dev` running) before opening a page *or running the tests*; otherwise you get `ViteManifestNotFoundException` and HTTP 500.
- **Modul 09's stock `ExampleTest` fails (302 instead of 200).** `routes/web.php` deliberately has `Route::redirect('/', '/routing')`, which shadows the default `/` welcome route. This is handout behaviour, not a bug; Modul 10–12 have no such redirect and their tests pass.
- **Order in Modul 09's `routes/web.php` is the lesson.** The redirect shadows `/`, `fallback` must come after the other routes, and for the same URI the last definition wins (see the Route Priority block, whose first route is commented out on purpose). Don't reorder, merge or "clean up" routes without checking the matching handout section and `docs/CATATAN-UJI-MODUL-09.md`.
- **Bootstrap via Sass, not Tailwind.** Laravel 13's default Tailwind setup was removed. The Vite entry points are `resources/sass/app.scss` (imports Bootstrap and Bootstrap Icons) and `resources/js/app.js` (`import 'bootstrap'`); `vite.config.js` silences Sass's `import` deprecation. Images go through `Vite::asset('resources/images/...')`, covered by `assets: ['resources/images/**']`.
- **Modul 11/12 need MySQL.** Their `.env.example` is set to `DB_CONNECTION=mysql`, `DB_DATABASE=data_master`, port 3306, as the handouts require (Laravel 13's default is SQLite with the `DB_*` lines commented out; only changing `DB_DATABASE` makes Laravel look for an SQLite file — see `docs/CATATAN-UJI-MODUL-11.md`). Create the database first, then `php artisan migrate --seed`; until migrated, every page 500s because sessions/cache are database-backed. Re-running `db:seed` fails on the unique email, so use `migrate:fresh --seed`. The handout code also runs on SQLite. Tests don't touch the employee tables.
- **No data layer in Modul 09/10.** The Modul 10 employee table in `employee/index.blade.php` is hard-coded rows. `EmployeeController::store` validates and returns `$request->all()` as JSON without persisting, and `show`/`edit`/`update`/`destroy` are empty stubs from `make:controller --resource`. The only model is the stock `User`. `.env.example` defaults to SQLite with database-backed session/cache/queue, so run `php artisan migrate` if you go beyond static pages; the test environment uses array drivers and in-memory SQLite.
- **No Blade layout before Modul 12.** Each Modul 10/11 view (`home`, `profile`, `employee/index`, `employee/create`) is a full HTML document with its own copy of the navbar, as in the handout. A navbar change must be made in all four (the `col-2` vs `col-6` mismatch on `profile` is a known cosmetic inconsistency). Modul 12 has a single navbar in `layouts/nav.blade.php`.
- **Don't run Pint across the module code.** `vendor/bin/pint --test` already flags handout-verbatim code (e.g. `HomeController`, `EmployeeController`), and reformatting makes the code diverge from the handout.
- **Ignore the per-module `CLAUDE.md` / `AGENTS.md`.** They are the stock Laravel Boost bootstrap stub written by `composer create-project`, asking to `composer require laravel/boost --dev`. The handouts don't use Boost and the test notes flag the stub as confusing, so don't install it unless asked.
