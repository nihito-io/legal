-- PDFs have no sibling files, so relative links to the other documents ("dpa.html")
-- become absolute links to the same published version (LEGAL_LINK_BASE).
local base = os.getenv("LEGAL_LINK_BASE")

function Link(el)
  if base and not el.target:match("^%a[%w+.-]*:") and not el.target:match("^#") then
    el.target = base .. el.target
  end
  return el
end
