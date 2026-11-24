nnoremap <Leader>b :w<CR>:make<CR>
nnoremap <Leader>n :cn<CR>
nnoremap <Leader>p :cp<CR>

autocmd FileType cpp setlocal makeprg=make\ %:r
autocmd FileType cpp nnoremap <Leader>r :w<CR>:!./%:r<CR>
autocmd FileType cpp nnoremap <Leader>t :w<CR>:!./%:r test<CR>
autocmd FileType cpp nnoremap <Leader>d :w<CR>:!./%:r debug<CR>

autocmd FileType python setlocal makeprg=python\ -m\ py_compile\ %
autocmd FileType python nnoremap <F5> :w<CR>:make<CR>
autocmd FileType python nnoremap <Leader>b :w<CR>:make<CR>
autocmd FileType python nnoremap <Leader>r :w<CR>:!python %<CR>
autocmd FileType python nnoremap <Leader>t :w<CR>:!python % test<CR>
autocmd FileType python nnoremap <Leader>d :w<CR>:!python % debug<CR>

autocmd FileType go setlocal makeprg=go\ build\ %
autocmd FileType go nnoremap <F5> :w<CR>:make<CR>
autocmd FileType go nnoremap <Leader>b :w<CR>:make<CR>
autocmd FileType go nnoremap <Leader>r :w<CR>:!go run %<CR>
autocmd FileType go nnoremap <Leader>t :w<CR>:!go run % test<CR>
autocmd FileType go nnoremap <Leader>d :w<CR>:!go run % debug<CR>
