
# Uninstall Homebrew 

rm -rf /usr/local/Homebrew
rm -rf /usr/local/Caskroom
rm -rf /usr/local/bin/brew

# Uninstall Xcode 
rm -rf /Applications/Xcode.app
rm -rf /Library/Preferences/com.apple.dt.Xcode.plist
rm -rf ~/Library/Preferences/com.apple.dt.Xcode.plist
rm -rf ~/Library/Caches/com.apple.dt.Xcode
rm -rf ~/Library/Application Support/Xcode
rm -rf ~/Library/Developer/
rm -rf ~/Library/Developer/CoreSimulator


# Uninstall RVM 


rm -rf $HOME/.rvm $HOME/.rvmrc /etc/rvmrc /etc/profile.d/rvm.sh /usr/local/rvm /usr/local/bin/rvm

