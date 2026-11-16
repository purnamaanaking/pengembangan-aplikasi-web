# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Hands-on (praktikum) work for the *Pengembangan Aplikasi Web* course. Student handouts live in `docs/modul-praktikum/*.docx`, and each folder `modul-NN-*/` is a working Laravel 13 app that reproduces one handout. Course material, test notes and commit messages are in Indonesian; keep new docs and commits consistent with that.

There is no root-level `composer.json` or `package.json`. **Every command below runs from inside a module folder.**

## Layout

- `modul-09-routing/` — routing, Vite + Bootstrap/Sass bundling. All behaviour is in `routes/web.php` (closures, `Route::view`, redirect, parameters, `where()`, named routes, prefix/group, fallback) plus a small `RouteController`.
- `modul-10-controller-view/` — `HomeController` (basic), `ProfileController` (invokable), `EmployeeController` (`Route::resource`, with Validator-based `store`) and Blade views.
- `docs/modul-praktikum/` — the `.docx` handouts. They are the source of truth for what a module's code should look like. A request to "adjust the modul" means these files.
- `docs/CATATAN-UJI-MODUL-NN.md` — test notes from walking through each handout step by step, recording where the handout and the working code diverge.

Modules are independent snapshots, not a chain: each is a separate `composer create-project` skeleton, created from `main` (Modul 10 does not build on Modul 09). Do not share code between them or hoist dependencies. Work for a new module goes in `modul-NN-slug/` on a branch `praktikum/modul-NN-slug`, merged into `main` with a merge commit; commits look like `Praktikum Modul 10: Pengenalan Controller dan View pada Laravel`.

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
- **Modul 09's stock `ExampleTest` fails (302 instead of 200).** `routes/web.php` deliberately has `Route::redirect('/', '/routing')`, which shadows the default `/` welcome route. This is handout behaviour, not a bug; Modul 10 has no such redirect and its tests pass.
- **Order in Modul 09's `routes/web.php` is the lesson.** The redirect shadows `/`, `fallback` must come after the other routes, and for the same URI the last definition wins (see the Route Priority block, whose first route is commented out on purpose). Don't reorder, merge or "clean up" routes without checking the matching handout section and `docs/CATATAN-UJI-MODUL-09.md`.
- **Bootstrap via Sass, not Tailwind.** Laravel 13's default Tailwind setup was removed. The Vite entry points are `resources/sass/app.scss` (imports Bootstrap and Bootstrap Icons) and `resources/js/app.js` (`import 'bootstrap'`); `vite.config.js` silences Sass's `import` deprecation. Images go through `Vite::asset('resources/images/...')`, covered by `assets: ['resources/images/**']`.
- **No data layer in the lessons.** The employee table in `employee/index.blade.php` is hard-coded rows. `EmployeeController::store` validates and returns `$request->all()` as JSON without persisting, and `show`/`edit`/`update`/`destroy` are empty stubs from `make:controller --resource`. The only model is the stock `User`. `.env.example` defaults to SQLite with database-backed session/cache/queue, so run `php artisan migrate` if you go beyond static pages; the test environment uses array drivers and in-memory SQLite.
- **No Blade layout.** Each Modul 10 view (`home`, `profile`, `employee/index`, `employee/create`) is a full HTML document with its own copy of the navbar, as in the handout. A navbar change must be made in all four (the `col-2` vs `col-6` mismatch on `profile` is a known cosmetic inconsistency).
- **Don't run Pint across the module code.** `vendor/bin/pint --test` already flags handout-verbatim code (e.g. `HomeController`, `EmployeeController`), and reformatting makes the code diverge from the handout.
- **Ignore the per-module `CLAUDE.md` / `AGENTS.md`.** They are the stock Laravel Boost bootstrap stub written by `composer create-project`, asking to `composer require laravel/boost --dev`. The handouts don't use Boost and the test notes flag the stub as confusing, so don't install it unless asked.
