function compile_latex {
  pdflatex -shell-escape -halt-on-error -interaction nonstopmode thesis.tex
}

function compile_latex_silently {
  compile_latex > /dev/null
}

function output_latex_status {
  has_compiled=$?
  has_warnings=$(analyze_texlog)
  if [ "$has_compiled" -ne 0 ]
  then
    show_error_notification
  elif [ "$has_warnings" ]
  then
    show_warning_notification
  else
    show_finished_notification
  fi
}

function show_compiling_notification {
  echo "Compiling..."
  terminal-notifier -title 'Compiling your LaTeX' -message '🤓 🚀 '
}

function show_error_notification {
  echo "Error!"
  analyze_texlog
  terminal-notifier -title '‼️  Error on LaTeX compilation!' -message 'Your document was not compiled ‼️ 🙃 '
}

function show_warning_notification {
  echo "Compiled with Warnings!"
  analyze_texlog
  terminal-notifier -title "⚠️  Warnings" -message "Compiled, but with warnings 😥"
}

function show_finished_notification {
  echo "Done!"
  analyze_texlog
  terminal-notifier -execute "open ~/thesis/writing/thesis.pdf" -title '✅ Your PDF is ready!' -message 'Click here to see it 📄 '
}

function analyze_texlog {
  ~/thesis/writing/bin/texlog_extract --config=.texlog_config thesis.log
}

function has_warnings {
  analyze_texlog > /dev/null
  return [ $? -eq 0 ]
}
