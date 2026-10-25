source "https://rubygems.org"

# Run Jekyll with `bundle exec`, e.g. `bundle exec jekyll serve`
gem "jekyll", "~> 4.4.0"

group :jekyll_plugins do
  gem "jekyll-include-cache"
  gem "jekyll-seo-tag"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

gem "webrick"
