function compile_latex {
  pdflatex -shell-escape -halt-on-error -interaction nonstopmode thesis.tex
}

function compile_latex_silently {
  compile_latex > /dev/null
}

function output_latex_status {
  if [ $? -eq 0 ]
  then
    show_finished_notification
  else
    show_error_notification
  fi
}

function show_compiling_notification {
  echo "Compiling..."
  terminal-notifier -title 'Compiling your LaTeX' -message '🤓 🚀 '
}

function show_finished_notification {
  echo "Done!"
  analyze_texlog
  terminal-notifier -execute "open ~/thesis/writing/thesis.pdf" -title '✅ Your PDF is ready!' -message 'Click here to see it 📄 '
}

function show_error_notification {
  echo "Error!"
  analyze_texlog
  terminal-notifier -title '‼️  Error on LaTeX compilation!' -message 'Your document was not compiled ‼️ 🙃 '
}

function analyze_texlog {
  ~/thesis/writing/bin/texlog_extract --config=.texlog_config thesis.log
}
